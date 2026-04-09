# Edge WebView2 安装 - 立即修复脚本
# 必须以管理员身份运行

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Edge WebView2 安装修复工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查管理员权限
$isAdmin = ([System.Security.Principal.WindowsPrincipal] [System.Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "错误: 请以管理员身份运行此脚本！" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "✓ 管理员权限检查通过" -ForegroundColor Green
Write-Host ""

# 获取系统默认临时目录
$systemDefaultTemp = [System.IO.Path]::Combine($env:USERPROFILE, "AppData", "Local", "Temp")
Write-Host "系统默认临时目录: $systemDefaultTemp" -ForegroundColor Cyan
Write-Host ""

# 方案：修改环境变量（不删除，避免文件夹占用问题）
Write-Host "正在修改环境变量..." -ForegroundColor Yellow

try {
    # 修改用户级别环境变量
    [System.Environment]::SetEnvironmentVariable("TEMP", $systemDefaultTemp, "User")
    [System.Environment]::SetEnvironmentVariable("TMP", $systemDefaultTemp, "User")
    Write-Host "  ✓ 已修改用户级别环境变量" -ForegroundColor Green
} catch {
    Write-Host "  ✗ 修改用户级别环境变量失败: $_" -ForegroundColor Red
}

try {
    # 修改系统级别环境变量
    [System.Environment]::SetEnvironmentVariable("TEMP", $systemDefaultTemp, "Machine")
    [System.Environment]::SetEnvironmentVariable("TMP", $systemDefaultTemp, "Machine")
    Write-Host "  ✓ 已修改系统级别环境变量" -ForegroundColor Green
} catch {
    Write-Host "  ✗ 修改系统级别环境变量失败: $_" -ForegroundColor Red
}

Write-Host ""

# 在当前会话中立即设置环境变量
$env:TEMP = $systemDefaultTemp
$env:TMP = $systemDefaultTemp

Write-Host "✓ 当前会话环境变量已更新" -ForegroundColor Green
Write-Host "  TEMP = $env:TEMP" -ForegroundColor Cyan
Write-Host "  TMP  = $env:TMP" -ForegroundColor Cyan
Write-Host ""

# 检查安装程序
$installerPath = "D:\MicrosoftEdgeWebView2RuntimeInstallerX64.exe"
if (Test-Path $installerPath) {
    Write-Host "找到安装程序: $installerPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "准备安装..." -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "注意: 环境变量已修改，但为了确保生效，" -ForegroundColor Yellow
    Write-Host "建议关闭所有 PowerShell 窗口后重新打开，然后再运行安装程序。" -ForegroundColor Yellow
    Write-Host ""
    
    $runNow = Read-Host "是否现在立即运行安装程序？(Y/N)"
    if ($runNow -eq "Y" -or $runNow -eq "y") {
        Write-Host ""
        Write-Host "正在启动安装程序..." -ForegroundColor Yellow
        Write-Host ""
        Start-Process -FilePath $installerPath -Wait
        Write-Host ""
        Write-Host "安装程序已运行完成" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "请稍后手动运行安装程序：" -ForegroundColor Yellow
        Write-Host "  & `"$installerPath`"" -ForegroundColor Cyan
    }
} else {
    Write-Host "未找到安装程序: $installerPath" -ForegroundColor Yellow
    Write-Host "请手动运行安装程序" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "修复完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "重要提示：" -ForegroundColor Yellow
Write-Host "1. 环境变量已修改为系统默认路径" -ForegroundColor White
Write-Host "2. 当前会话的环境变量已更新" -ForegroundColor White
Write-Host "3. 如果安装失败，请关闭所有窗口，重新以管理员身份打开 PowerShell 后再试" -ForegroundColor White
Write-Host ""
pause




