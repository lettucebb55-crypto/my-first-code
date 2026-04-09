# Edge WebView2 安装详细步骤

## ✅ 已找到安装程序文件

你的系统中找到了以下安装程序：
1. `D:\MicrosoftEdgeWebView2RuntimeInstallerX64.exe`
2. `C:\Users\Administrator\Downloads\MicrosoftEdgeWebView2RuntimeInstallerX64.exe`

## 📋 安装步骤（按顺序执行）

### 步骤1：以管理员身份打开 PowerShell

1. 按 `Win + X` 键
2. 选择"Windows PowerShell (管理员)" 或 "终端 (管理员)"
3. 或者在开始菜单搜索 "PowerShell"，右键选择"以管理员身份运行"

### 步骤2：设置正确的临时目录

在 PowerShell 中执行以下命令：

```powershell
# 设置临时目录为系统默认路径
$env:TEMP = [System.IO.Path]::Combine($env:USERPROFILE, "AppData", "Local", "Temp")
$env:TMP = $env:TEMP

# 验证设置
Write-Host "临时目录已设置为: $env:TEMP" -ForegroundColor Green
```

### 步骤3：切换到安装程序所在目录并运行

**方法A：使用 D 盘根目录的安装程序**

```powershell
# 切换到 D 盘根目录
cd D:\

# 运行安装程序
.\MicrosoftEdgeWebView2RuntimeInstallerX64.exe
```

**方法B：使用下载文件夹的安装程序**

```powershell
# 切换到下载文件夹
cd $env:USERPROFILE\Downloads

# 运行安装程序
.\MicrosoftEdgeWebView2RuntimeInstallerX64.exe
```

**方法C：使用完整路径（推荐，最简单）**

```powershell
# 直接使用完整路径运行，不需要切换目录
& "D:\MicrosoftEdgeWebView2RuntimeInstallerX64.exe"
```

### 步骤4：如果还是报错，尝试静默安装

如果图形界面安装还是失败，可以尝试静默安装：

```powershell
# 设置临时目录
$env:TEMP = [System.IO.Path]::Combine($env:USERPROFILE, "AppData", "Local", "Temp")
$env:TMP = $env:TEMP

# 静默安装
& "D:\MicrosoftEdgeWebView2RuntimeInstallerX64.exe" /silent /install
```

## 🔍 完整的一键安装命令（复制粘贴即可）

在**管理员 PowerShell** 中，直接复制粘贴以下全部内容：

```powershell
# 设置临时目录
$env:TEMP = [System.IO.Path]::Combine($env:USERPROFILE, "AppData", "Local", "Temp")
$env:TMP = $env:TEMP

# 运行安装程序
& "D:\MicrosoftEdgeWebView2RuntimeInstallerX64.exe"
```

## ⚠️ 如果仍然失败

### 备选方案1：使用另一个安装程序

```powershell
# 设置临时目录
$env:TEMP = [System.IO.Path]::Combine($env:USERPROFILE, "AppData", "Local", "Temp")
$env:TMP = $env:TEMP

# 使用下载文件夹中的安装程序
& "$env:USERPROFILE\Downloads\MicrosoftEdgeWebView2RuntimeInstallerX64.exe"
```

### 备选方案2：重新下载最新版本

1. 访问：https://developer.microsoft.com/zh-cn/microsoft-edge/webview2/
2. 下载 "Evergreen Standalone Installer (x64)"
3. 下载后右键以管理员身份运行

### 备选方案3：检查是否已安装

```powershell
# 检查是否已经安装
Get-ItemProperty "HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}" -ErrorAction SilentlyContinue
```

如果返回信息，说明已经安装成功。

## 📝 常见问题

**Q: 为什么找不到文件？**  
A: 文件名是 `MicrosoftEdgeWebView2RuntimeInstallerX64.exe`，不是 `MicrosoftEdgeWebView2.exe`

**Q: 为什么需要设置临时目录？**  
A: 安装程序需要创建临时文件，使用系统默认路径更稳定

**Q: 静默安装和普通安装有什么区别？**  
A: 静默安装不显示图形界面，直接在后台安装，适合自动化场景

## ✅ 验证安装成功

安装完成后，可以通过以下方式验证：

```powershell
# 方法1：检查注册表
Get-ItemProperty "HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}" -ErrorAction SilentlyContinue

# 方法2：检查文件是否存在
Test-Path "C:\Program Files (x86)\Microsoft\EdgeWebView\Application"
```




