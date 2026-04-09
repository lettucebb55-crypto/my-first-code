# Microsoft Edge WebView2 安装问题解决方案

## 问题描述
安装 Microsoft Edge WebView2 时出现错误："无法创建临时目录"

## 解决方案

### 方案1：以管理员权限运行安装程序（推荐）

1. **关闭当前的 PowerShell 窗口**

2. **右键点击 PowerShell 图标**，选择"以管理员身份运行"

3. **在新的管理员 PowerShell 窗口中**，执行以下命令：
```powershell
# 检查当前临时目录
$env:TEMP
$env:TMP

# 如果需要，可以临时设置为系统默认目录
$env:TEMP = [System.IO.Path]::GetTempPath()
$env:TMP = [System.IO.Path]::GetTempPath()

# 然后运行安装程序
.\MicrosoftEdgeWebView2.exe
```

### 方案2：直接下载并安装（最简单）

1. **访问 Microsoft 官方下载页面**：
   - 打开浏览器，访问：https://developer.microsoft.com/zh-cn/microsoft-edge/webview2/
   - 或者直接下载：https://go.microsoft.com/fwlink/p/?LinkId=2124703

2. **下载安装程序**：
   - 下载 "Evergreen Runtime"（常青版运行时）
   - 这是一个 `.exe` 文件

3. **右键点击下载的安装程序**，选择"以管理员身份运行"

4. **按照安装向导完成安装**

### 方案3：清理临时目录并重试

1. **清理 D:\Temp 目录**：
```powershell
# 以管理员身份运行 PowerShell
Remove-Item "D:\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
```

2. **确保目录存在且有正确权限**：
```powershell
# 创建目录（如果不存在）
New-Item -ItemType Directory -Path "D:\Temp" -Force

# 设置权限
icacls "D:\Temp" /grant Everyone:F /T
```

3. **重新运行安装程序**

### 方案4：使用系统默认临时目录

1. **恢复系统默认临时目录设置**：
```powershell
# 在管理员 PowerShell 中执行
Remove-Item Env:\TEMP
Remove-Item Env:\TMP
```

2. **重新打开 PowerShell**（让系统使用默认的 `%USERPROFILE%\AppData\Local\Temp`）

3. **运行安装程序**

### 方案5：检查磁盘空间

1. **检查 D 盘空间**：
```powershell
Get-PSDrive D | Select-Object Used,Free,@{Name="FreeGB";Expression={[math]::Round($_.Free/1GB,2)}}
```

2. **如果空间不足**，清理磁盘空间或使用其他盘符

## 为什么会出现这个问题？

1. **权限不足**：安装程序需要管理员权限来创建临时文件和安装系统组件
2. **临时目录权限问题**：自定义的临时目录可能没有足够的权限
3. **磁盘空间不足**：临时目录所在磁盘空间不够
4. **防病毒软件拦截**：某些安全软件可能阻止创建临时文件

## 推荐操作步骤

**最简单的方法**：
1. 访问 Microsoft 官网下载 Edge WebView2 安装程序
2. 右键点击下载的 `.exe` 文件
3. 选择"以管理员身份运行"
4. 按照提示完成安装

这样通常可以解决所有权限和临时目录相关的问题。

## 验证安装是否成功

安装完成后，可以通过以下方式验证：

```powershell
# 检查注册表（如果安装成功会有相关项）
Get-ItemProperty "HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}" -ErrorAction SilentlyContinue
```

或者直接尝试运行需要使用 WebView2 的应用程序。

