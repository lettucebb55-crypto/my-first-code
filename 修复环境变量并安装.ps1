# Edge WebView2 安装环境变量修复脚本
# 必须以管理员身份运行

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Edge WebView2 安装环境变量修复工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查管理员权限
$isAdmin = ([System.Security.Principal.WindowsPrincipal] [System.Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "错误: 请以管理员身份运行此脚本！" -ForegroundColor Red
    Write-Host "右键点击 PowerShell，选择'以管理员身份运行'" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✓ 管理员权限检查通过" -ForegroundColor Green
Write-Host ""

# 显示当前环境变量
Write-Host "当前环境变量设置：" -ForegroundColor Yellow
$userTemp = [System.Environment]::GetEnvironmentVariable("TEMP", "User")
$userTmp = [System.Environment]::GetEnvironmentVariable("TMP", "User")
$machineTemp = [System.Environment]::GetEnvironmentVariable("TEMP", "Machine")
$machineTmp = [System.Environment]::GetEnvironmentVariable("TMP", "Machine")

Write-Host "  用户 TEMP: $userTemp" -ForegroundColor Cyan
Write-Host "  用户 TMP:  $userTmp" -ForegroundColor Cyan
Write-Host "  系统 TEMP: $machineTemp" -ForegroundColor Cyan
Write-Host "  系统 TMP:  $machineTmp" -ForegroundColor Cyan
Write-Host ""

# 方案选择
Write-Host "请选择修复方案：" -ForegroundColor Yellow
Write-Host "1. 删除环境变量，使用系统默认临时目录（推荐）" -ForegroundColor White
Write-Host "2. 修改环境变量为系统默认路径" -ForegroundColor White
Write-Host "3. 修复 D:\Temp 权限（保留当前设置）" -ForegroundColor White
Write-Host ""
$choice = Read-Host "请输入选项 (1/2/3)"

$systemDefaultTemp = [System.IO.Path]::Combine($env:USERPROFILE, "AppData", "Local", "Temp")

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "方案1: 删除环境变量..." -ForegroundColor Yellow
        
        # 删除用户级别环境变量
        try {
            [System.Environment]::SetEnvironmentVariable("TEMP", $null, "User")
            [System.Environment]::SetEnvironmentVariable("TMP", $null, "User")
            Write-Host "  ✓ 已删除用户级别环境变量" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ 删除用户级别环境变量失败: $_" -ForegroundColor Red
        }
        
        # 删除系统级别环境变量
        try {
            [System.Environment]::SetEnvironmentVariable("TEMP", $null, "Machine")
            [System.Environment]::SetEnvironmentVariable("TMP", $null, "Machine")
            Write-Host "  ✓ 已删除系统级别环境变量" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ 删除系统级别环境变量失败: $_" -ForegroundColor Red
        }
        
        Write-Host ""
        Write-Host "✓ 环境变量已删除，系统将使用默认临时目录" -ForegroundColor Green
        Write-Host "  默认临时目录: $systemDefaultTemp" -ForegroundColor Cyan
    }
    
    "2" {
        Write-Host ""
        Write-Host "方案2: 修改环境变量为系统默认路径..." -ForegroundColor Yellow
        
        # 修改用户级别环境变量
        try {
            [System.Environment]::SetEnvironmentVariable("TEMP", $systemDefaultTemp, "User")
            [System.Environment]::SetEnvironmentVariable("TMP", $systemDefaultTemp, "User")
            Write-Host "  ✓ 已修改用户级别环境变量" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ 修改用户级别环境变量失败: $_" -ForegroundColor Red
        }
        
        # 修改系统级别环境变量
        try {
            [System.Environment]::SetEnvironmentVariable("TEMP", $systemDefaultTemp, "Machine")
            [System.Environment]::SetEnvironmentVariable("TMP", $systemDefaultTemp, "Machine")
            Write-Host "  ✓ 已修改系统级别环境变量" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ 修改系统级别环境变量失败: $_" -ForegroundColor Red
        }
        
        Write-Host ""
        Write-Host "✓ 环境变量已修改为系统默认路径" -ForegroundColor Green
    }
    
    "3" {
        Write-Host ""
        Write-Host "方案3: 修复 D:\Temp 权限..." -ForegroundColor Yellow
        
        if (-not (Test-Path "D:\Temp")) {
            try {
                New-Item -ItemType Directory -Path "D:\Temp" -Force | Out-Null
                Write-Host "  ✓ 创建 D:\Temp 目录" -ForegroundColor Green
            } catch {
                Write-Host "  ✗ 创建目录失败: $_" -ForegroundColor Red
            }
        }
        
        try {
            # 设置完全控制权限
            $acl = Get-Acl "D:\Temp"
            $permission = "Everyone", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow"
            $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
            $acl.SetAccessRule($accessRule)
            Set-Acl "D:\Temp" $acl
            Write-Host "  ✓ 权限修复完成" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ 权限修复失败: $_" -ForegroundColor Red
        }
    }
    
    default {
        Write-Host "无效选项，退出" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "重要提示" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "环境变量修改后，需要：" -ForegroundColor Yellow
Write-Host "1. 关闭所有 PowerShell 窗口" -ForegroundColor White
Write-Host "2. 重新以管理员身份打开新的 PowerShell 窗口" -ForegroundColor White
Write-Host "3. 然后运行安装程序" -ForegroundColor White
Write-Host ""

# 检查安装程序
$installerPath = "D:\MicrosoftEdgeWebView2RuntimeInstallerX64.exe"
if (Test-Path $installerPath) {
    Write-Host "找到安装程序: $installerPath" -ForegroundColor Green
    Write-Host ""
    $runNow = Read-Host "是否现在运行安装程序？(Y/N)"
    if ($runNow -eq "Y" -or $runNow -eq "y") {
        Write-Host ""
        Write-Host "正在运行安装程序..." -ForegroundColor Yellow
        Write-Host "注意: 由于环境变量已修改，建议先关闭此窗口，重新打开后再运行" -ForegroundColor Yellow
        Write-Host ""
        Start-Process -FilePath $installerPath -Wait
    }
} else {
    Write-Host "未找到安装程序，请手动运行安装程序" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "修复完成！" -ForegroundColor Green
Write-Host ""
pause




