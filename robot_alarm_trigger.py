import socket
import requests
import urllib3
import uuid
import time
import threading
import signal
import sys
from queue import Queue, Empty

# 屏蔽 HTTPS 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ==================== 配置封装 ====================
class Config:
    """所有可配置参数集中管理"""
    # 机器人服务
    robot_server = "https://192.168.50.204:41443"
    api_key = "0c7f68b58c2e46fa95d84164f489fd81"
    robot_id = "26WV530004"

    # 导航目标（19号仓库）
    target_x = "-333"
    target_y = "-3478"
    target_angle = "90"
    point_name = "19号仓库"

    # TTS 播报
    tts_text = "十九号库发生烟雾报警我将立即联动库内摄像机进行核验并去现场查看"
    tts_playback_duration = 12  # 播报预估时长（秒）

    # 导航
    nav_walk_time = 10  # 行驶预留时间（秒）

    # 网络监听
    udp_port = 5000
    short_cooldown = 10  # 两次报警最小间隔（秒）

    # 外部海康球机
    ptz_ip = "192.168.50.203"
    ptz_port = 8000
    ptz_run_duration = 50
    ptz_run_packet = bytes.fromhex("3050202603180001080102971800")
    ptz_stop_packet = bytes.fromhex("3050202603180001080102971801")


# 全局状态
speak_queue = Queue(maxsize=5)
last_trigger = 0.0
exit_flag = False
mission_running = False
mission_lock = threading.Lock()
is_speaking = False

# ===============================================

def robot_post(url_path, data):
    """通用API请求函数"""
    url = f"{Config.robot_server}{url_path}"
    headers = {"Content-Type": "application/json", "key": Config.api_key}
    try:
        resp = requests.post(url, json=data, headers=headers, verify=False, timeout=12)
        res_json = resp.json()
        print(f"[API响应] {url_path}: {res_json}")
        return res_json
    except Exception as e:
        print(f"API请求失败: {e}")
        return None

def send_ptz_packet(packet):
    """发送外部球机UDP指令"""
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        udp_sock.sendto(packet, (Config.ptz_ip, Config.ptz_port))
    finally:
        udp_sock.close()

def ptz_thread_worker():
    """外部监控异步线程"""
    send_ptz_packet(Config.ptz_run_packet)
    time.sleep(Config.ptz_run_duration)
    send_ptz_packet(Config.ptz_stop_packet)

def speak_worker():
    """语音播报后台线程"""
    global is_speaking
    while not exit_flag:
        try:
            _ = speak_queue.get(timeout=1)
            is_speaking = True
            try:
                print(f"[TTS] 开始播报: {Config.tts_text[:30]}...")
                result = robot_post("/robot/third/pengan/tts", {
                    "requestId": str(uuid.uuid4()),
                    "message": Config.tts_text,
                    "robot_id": Config.robot_id
                })
                if result is None:
                    print(f"[TTS] 接口返回异常，请检查网络或API")
                else:
                    print(f"[TTS] 播报请求已发送")
            except Exception as e:
                print(f"[TTS] 语音接口异常: {e}")
            finally:
                is_speaking = False
                speak_queue.task_done()
        except Empty:
            continue

def execute_mission():
    """核心联动流程 - 先播报完成再导航，避免移动/云台打断语音"""
    global mission_running
    try:
        with mission_lock:
            mission_running = True

        print(f"报警任务启动...")

        # 1. 启动外部球机监控 (异步)
        threading.Thread(target=ptz_thread_worker, daemon=True).start()

        # 2. 先触发语音播报，等播完再导航
        print(f"[播报] 先播报，播完后再导航...")
        try:
            speak_queue.put_nowait(1)
            print(f"播报任务已加入队列")
        except Exception as e:
            print(f"播报队列已满: {e}")

        # 3. 等待播报播放完成
        print(f"等待播报播放约 {Config.tts_playback_duration} 秒...")
        time.sleep(Config.tts_playback_duration)

        # 4. 发起导航
        print(f"[导航] 正在前往 {Config.point_name}...")
        robot_post("/apiRequest", {
            "version": "1.0.0", "key": Config.api_key, "module": "walk", "function": "singlePointNav",
            "requestId": str(uuid.uuid4()),
            "param": {
                "robotId": Config.robot_id, "control": 1,
                "positionX": Config.target_x, "positionY": Config.target_y, "positionAngle": Config.target_angle
            }
        })

        # 5. 行走等待
        print(f"[行驶中] {Config.nav_walk_time} 秒行走时间...")
        time.sleep(Config.nav_walk_time)

        # 6. 云台动作
        print("[动作] 执行观察...")
        robot_post("/robot/remote/panTilt", {"robotId": Config.robot_id, "action": "5"})

    except Exception as e:
        print(f"流程执行出错: {e}")
    finally:
        time.sleep(0)
        with mission_lock:
            mission_running = False
        print("[系统重置] 任务结束，机器人原地待命，恢复监听状态")


def udp_listen():
    """UDP监听主循环"""
    global last_trigger
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", Config.udp_port))
    sock.settimeout(1)
    print(f"系统就绪。监听端口: {Config.udp_port} | 目标: {Config.point_name}")

    while not exit_flag:
        try:
            data, addr = sock.recvfrom(1024)
            if len(data) >= 22:
                is_alarm = (data[18] == 0x81 and data[19] == 0x01) or \
                           (data[20] == 0x82 and data[21] == 0x01)

                if is_alarm:
                    now = time.time()
                    if not mission_running and (now - last_trigger >= Config.short_cooldown):
                        last_trigger = now
                        threading.Thread(target=execute_mission, daemon=True).start()
        except socket.timeout:
            continue
    sock.close()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    threading.Thread(target=speak_worker, daemon=True).start()
    udp_listen()
