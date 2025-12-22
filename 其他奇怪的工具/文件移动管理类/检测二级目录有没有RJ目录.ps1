# 等待用户输入根目录
$rootPath = Read-Host "请输入根目录路径"

# 检查路径是否存在
if (-not (Test-Path -Path $rootPath -PathType Container)) {
    Write-Host "错误：指定的路径不存在或不是一个目录。" -ForegroundColor Red
    exit
}

# 获取根目录下所有一级子目录
$firstLevelDirs = Get-ChildItem -Path $rootPath -Directory

if ($null -eq $firstLevelDirs -or $firstLevelDirs.Count -eq 0) {
    Write-Host "根目录下没有一级子目录。"
    exit
}

# 存储没有 RJ 开头二级目录的一级目录名称
$missingRJDirs = @()

foreach ($dir in $firstLevelDirs) {
    # 获取当前一级目录下的所有二级子目录
    $secondLevelDirs = Get-ChildItem -Path $dir.FullName -Directory -ErrorAction SilentlyContinue

    # 检查是否有以 "RJ" 开头的目录（不区分大小写）
    $hasRJ = $false
    foreach ($subDir in $secondLevelDirs) {
        if ($subDir.Name -like "RJ*") {
            $hasRJ = $true
            break
        }
    }

    if (-not $hasRJ) {
        $missingRJDirs += $dir.Name
    }
}

# 输出结果
if ($missingRJDirs.Count -eq 0) {
    Write-Host "全都有"
} else {
    Write-Host "以下一级子目录中没有 RJ 开头的二级目录："
    $missingRJDirs | ForEach-Object { Write-Host $_ }
}

Read-Host "按 Enter 键退出"