# PowerShell 脚本编程

## Cmdlets 与函数

```powershell
# Cmdlet 是 PowerShell 内置命令，命名格式：动词-名词
Get-Process      # 获取进程
Get-Service      # 获取服务
Set-Location     # 切换目录（等价 cd）
Get-ChildItem    # 列出子项（等价 ls/dir）
Copy-Item        # 复制（等价 cp）
Remove-Item      # 删除（等价 rm）
New-Item         # 创建（等价 mkdir/touch）

# 函数定义
function Get-Greeting {
    param($Name)
    "Hello, $Name!"
}

Get-Greeting -Name "World"

# 高级函数（带 Cmdlet 特性）
function Get-UserInfo {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$UserName,

        [Parameter()]
        [ValidateRange(1, 150)]
        [int]$Age
    )
    Begin {
        Write-Verbose "开始处理"
    }
    Process {
        [PSCustomObject]@{
            Name = $UserName
            Age  = $Age
        }
    }
    End {
        Write-Verbose "处理完成"
    }
}
```

## 管道

```powershell
# 对象管道（PowerShell 传递的是 .NET 对象，而非文本）
Get-Process | Where-Object { $_.CPU -gt 100 }
Get-Service | Where-Object Status -eq 'Running'
Get-ChildItem *.txt | Select-Object Name, Length
Get-Process | Sort-Object -Property CPU -Descending | Select-Object -First 5

# ForEach-Object
1..10 | ForEach-Object { $_ * $_ }

# 使用成员方法
Get-Process | ForEach-Object ProcessName
Get-ChildItem | ForEach-Object FullName

# 管道链式执行
Get-Process |
    Where-Object WorkingSet -gt 100MB |
    Sort-Object WorkingSet -Descending |
    Select-Object Name, @{Name='MB';Expression={$_.WorkingSet / 1MB}} |
    Format-Table -AutoSize
```

## 变量

```powershell
# 基本变量
$name = "Alice"
$count = 42
$pi = 3.14159
$isEnabled = $true

# 环境变量
$env:PATH
$env:USERNAME
$env:COMPUTERNAME

# 自动变量
$_          # 当前管道对象
$?          # 上条命令执行结果（True/False）
$args       # 函数参数数组
$true       # 布尔真
$false      # 布尔假
$null       # 空值
$Error      # 错误数组
$HOME       # 用户主目录
$PROFILE    # 当前用户配置文件路径

# 变量作用域
$script:var = "脚本级变量"
$global:var = "全局变量"
$local:var  = "局部变量"
$private:var = "私有变量"
```

## 数据类型

```powershell
# 数组
$arr = @(1, 2, 3, 4, 5)
$arr[0]            # 1
$arr[-1]           # 5（倒数第一个）
$arr[0..2]         # 1, 2, 3
$arr += 6          # 追加
$arr.Count         # 数组长度

# 空数组
$empty = @()

# 范围
$range = 1..10     # 1 到 10

# 哈希表
$user = @{
    Name = "Alice"
    Age  = 30
    City = "Beijing"
}
$user.Name          # 访问
$user['Age']        # 索引访问
$user.Keys          # 所有键
$user.Values        # 所有值
$user.Add('Phone', '1234567890')
$user.Remove('Age')

# PSCustomObject（结构化的自定义对象）
$obj = [PSCustomObject]@{
    Name = "Bob"
    Age  = 25
    Role = "Developer"
}
$obj | Format-Table
$obj | Export-Csv data.csv -NoTypeInformation
```

## 控制流

```powershell
# if/elseif/else
if ($age -ge 18) {
    "成年"
} elseif ($age -ge 60) {
    "老年"
} else {
    "未成年"
}

# 比较运算符
-eq  # 等于
-ne  # 不等于
-gt  # 大于
-ge  # 大于等于
-lt  # 小于
-le  # 小于等于
-like  # 通配符匹配
-match # 正则匹配
-contains # 集合包含
-in  # 元素在集合中

# switch
switch ($value) {
    1 { "一" }
    2 { "二" }
    {$_ -gt 10} { "大于 10" }
    default { "其他" }
}

# foreach
foreach ($file in Get-ChildItem *.txt) {
    $file.Name
}

# for
for ($i = 0; $i -lt 10; $i++) {
    $i
}

# while/do
while ($count -gt 0) {
    $count--
    $count
}

do {
    $count++
} while ($count -lt 10)
```

## 函数（高级）

```powershell
# 高级函数模板
<#
.SYNOPSIS
    函数简要说明
.DESCRIPTION
    详细描述
.PARAMETER Path
    参数说明
.EXAMPLE
    Get-MyData -Path "C:\data"
#>
function Get-MyData {
    [CmdletBinding(SupportsShouldProcess=$true, ConfirmImpact='Medium')]
    param(
        [Parameter(Mandatory=$true, Position=0, ValueFromPipeline=$true)]
        [ValidateNotNullOrEmpty()]
        [ValidateScript({Test-Path $_})]
        [string]$Path,

        [Parameter()]
        [ValidateSet('File', 'Directory')]
        [string]$Type,

        [Parameter()]
        [switch]$Recurse
    )

    begin {
        Write-Verbose "开始处理"
    }

    process {
        if ($PSCmdlet.ShouldProcess($Path, "处理路径")) {
            try {
                Get-ChildItem -Path $Path -Recurse:$Recurse
            } catch {
                Write-Error $_
            }
        }
    }

    end {
        Write-Verbose "处理完成"
    }
}
```

## 模块

```powershell
# 导入模块
Import-Module ActiveDirectory
Import-Module .\MyModule.psm1 -Force

# 查看可用模块
Get-Module -ListAvailable

# 创建模块（MyModule.psm1）
function Get-Hello {
    param($Name)
    "Hello, $Name!"
}

Export-ModuleMember -Function Get-Hello

# 模块清单（MyModule.psd1）
@{
    RootModule = 'MyModule.psm1'
    ModuleVersion = '1.0.0'
    Author = 'Author Name'
    FunctionsToExport = @('Get-Hello', 'Set-Greeting')
    CmdletsToExport = @()
    VariablesToExport = '*'
    AliasesToExport = @()
}
```

## 错误处理

```powershell
# try/catch/finally
try {
    $result = 1 / 0
} catch [System.DivideByZeroException] {
    Write-Error "除零错误"
} catch {
    Write-Error "未知错误: $_"
} finally {
    Write-Host "总是执行"
}

# $ErrorActionPreference
$ErrorActionPreference = 'Stop'      # 出错停止
$ErrorActionPreference = 'Continue'  # 出错继续（默认）
$ErrorActionPreference = 'SilentlyContinue'  # 静默

# 错误处理参数
Get-Item "nonexistent.txt" -ErrorAction Stop
Get-Item "nonexistent.txt" -ErrorAction SilentlyContinue

# trap
trap {
    Write-Warning "捕获到错误: $_"
    continue  # 继续执行
}
```

## 远程管理

```powershell
# 单台计算机
Invoke-Command -ComputerName "Server01" -ScriptBlock {
    Get-Service -Name "W3SVC"
}

# 多台计算机
$computers = @("Server01", "Server02", "Server03")
Invoke-Command -ComputerName $computers -ScriptBlock {
    Get-Process | Where-Object CPU -gt 100
} -Credential (Get-Credential)

# 持久连接（PSSession）
$session = New-PSSession -ComputerName "Server01"
Invoke-Command -Session $session -ScriptBlock { $PSVersionTable }
Remove-PSSession $session

# 隐式远程
Import-PSSession -Session $session -Module ActiveDirectory
```

## PowerShell vs Bash 对比

| 功能 | PowerShell | Bash |
|------|-----------|------|
| 数据类型 | 强类型，基于 .NET | 弱类型，字符串为主 |
| 管道传递 | 对象 | 文本 |
| 路径分隔符 | \（但支持 /） | / |
| 变量语法 | $variable | $variable 或 ${variable} |
| 字符串拼接 | "$a$b" 或 -join | "$a$b" 或拼接 |
| 布尔值 | $true/$false | true/false |
| 注释 | #（单行） | #（单行） |
| 行继续 | 反引号 ` | 反斜杠 \ |
| 函数定义 | function | function 或 name() |
| Help 系统 | Get-Help 或 -? | man 或 --help |
| 远程管理 | Invoke-Command | ssh |
| 模块系统 | 强模块系统 | source |
| 错误处理 | try/catch/finally | trap 或 set -e |
| 对象创建 | [PSCustomObject]@{...} | 无原生支持 |

## 相关条目

- [[Bash]]
- [[Scripting]]
- [[Environment]]
- [[Basics]]
- [[Advanced]]
