---
aliases: [Compression]
tags: ['Basics', 'Compression']
created: 2026-05-16
updated: 2026-05-16
---

# 压缩与解压缩完全指南

## 常见格式对比

| 格式 | 算法 | 压缩率 | 速度 | 支持分卷 | 支持加密 | 跨平台 | 典型用途 |
|------|------|--------|------|---------|---------|--------|---------|
| ZIP | Deflate | 中等 | 快 | 是 | 是（AES-256） | 优秀 | 通用压缩，Windows 原生支持 |
| tar | 无（仅打包） | 无 | 极快 | 是 | 否 | 优秀 | Unix 归档（通常配合 gz/bz2/xz） |
| tar.gz | gzip | 中等 | 快 | 是 | 否 | 优秀 | Linux 软件包、源码分发 |
| tar.bz2 | bzip2 | 较高 | 较慢 | 是 | 否 | 优秀 | 大文件压缩 |
| tar.xz | LZMA2 | 很高 | 慢 | 是 | 否 | 优秀 | 高压缩比需求 |
| 7z | LZMA/LZMA2 | 很高 | 较慢 | 是 | 是（AES-256） | 好 | 极致压缩比 |
| RAR | 私有 | 高 | 中等 | 是 | 是（AES-256） | 好 | 商业场景、分卷压缩 |

> **压缩率对比**（以 1GB 文本文件为例，越大约 100MB）：
> - tar.gz: ~200MB
> - tar.bz2: ~180MB
> - tar.xz: ~150MB
> - 7z: ~140MB
> - ZIP: ~220MB
> - RAR: ~190MB

## Windows 自带 zip 功能

### 图形界面

1. 选中文件/文件夹 → 右键 → **发送到** → **压缩(zipped)文件夹**
2. 双击 .zip 文件即可查看内容
3. 解压：右键 → **全部提取**

### PowerShell 操作

```powershell
# 创建 zip
Compress-Archive -Path C:\Data\* -DestinationPath C:\Archive\backup.zip

# 解压 zip
Expand-Archive -Path C:\Archive\backup.zip -DestinationPath C:\Restored\

# 带压缩级别
Compress-Archive -Path C:\Data\* -DestinationPath C:\Archive\backup.zip -CompressionLevel Optimal
```

## 7-Zip 使用

### 安装

官网下载：https://www.7-zip.org/，安装后支持上下文菜单集成。

### 命令行操作（7z.exe）

```powershell
# 创建 7z 压缩包
7z a archive.7z C:\Folder\*

# 创建 zip（兼容性更好）
7z a -tzip archive.zip C:\Folder\*

# 解压
7z x archive.7z -oC:\Destination\

# 查看压缩包内容
7z l archive.7z

# 测试压缩包完整性
7z t archive.7z

# 加密压缩
7z a -pmyPassword -mhe=on secret.7z confidential.txt

# 分卷压缩（每卷 100MB）
7z a -v100m large.7z C:\LargeFolder\*

# 指定压缩级别（0=不压缩, 9=最大压缩）
7z a -mx=9 archive.7z C:\Folder\*
```

### 常用参数

| 参数 | 含义 |
|------|------|
| `a` | 添加到压缩包（add） |
| `x` | 解压（extract with full paths） |
| `e` | 解压（extract without paths） |
| `l` | 列出内容（list） |
| `t` | 测试（test） |
| `-t{type}` | 指定格式：`-tzip`, `-t7z` |
| `-o{dir}` | 输出目录（output） |
| `-p{pass}` | 密码（password） |
| `-mhe=on` | 加密文件头（加密文件名） |
| `-v{size}` | 分卷大小：`-v100m`, `-v1g` |
| `-mx={0-9}` | 压缩级别：0=存储, 9=最大 |
| `-r` | 递归处理子目录 |

## tar 命令详解

### 基本语法

```bash
tar [选项] [归档文件] [源文件...]
```

### 常用操作

```bash
# 创建 tar 包
tar -cf archive.tar file1.txt file2.txt folder/

# 创建 tar.gz（最常用）
tar -czf archive.tar.gz folder/

# 创建 tar.bz2
tar -cjf archive.tar.bz2 folder/

# 创建 tar.xz
tar -cJf archive.tar.xz folder/

# 解压 tar.gz
tar -xzf archive.tar.gz

# 解压到指定目录
tar -xzf archive.tar.gz -C /target/directory/

# 列出内容
tar -tzf archive.tar.gz

# 追加文件到 tar
tar -rf archive.tar newfile.txt
```

### tar 参数速查

| 参数 | 长参数 | 含义 |
|------|--------|------|
| `-c` | `--create` | 创建归档 |
| `-x` | `--extract` | 解压 |
| `-t` | `--list` | 列出内容 |
| `-f` | `--file` | 指定归档文件名 |
| `-z` | `--gzip` | 通过 gzip 压缩/解压 |
| `-j` | `--bzip2` | 通过 bzip2 压缩/解压 |
| `-J` | `--xz` | 通过 xz 压缩/解压 |
| `-v` | `--verbose` | 显示处理过程 |
| `-C` | `--directory` | 解压到指定目录 |
| `-r` | `--append` | 追加文件到归档 |
| `-u` | `--update` | 仅追加比归档中新的文件 |

## 相关条目

- [[05_ComputerScience/ComputerOrganizationAndArchitecture/DigitalLogic/DigitalLogic|DigitalLogic]]
- ComputerOrganization
- InformationTheory
- Cryptography

## 压缩率对比

以下对 1.2GB 虚拟机磁盘镜像的测试数据：

| 格式 | 压缩后大小 | 压缩时间 | 解压时间 | 压缩率 |
|------|-----------|---------|---------|--------|
| 无压缩 | 1.2 GB | — | — | 0% |
| ZIP (默认) | 892 MB | 45s | 12s | 26% |
| tar.gz | 834 MB | 52s | 15s | 30% |
| tar.bz2 | 712 MB | 2m30s | 1m10s | 41% |
| tar.xz | 645 MB | 8m20s | 2m05s | 46% |
| 7z (默认) | 621 MB | 5m10s | 1m30s | 48% |
| 7z (极限) | 598 MB | 12m45s | 1m35s | 50% |
| RAR (默认) | 668 MB | 3m20s | 55s | 44% |

> 注：实际压缩率因文件类型而异。（文本文件压缩率高，已压缩格式如 jpg/mp4 效果差）

## 分卷压缩

### 7-Zip 分卷

```bash
# 每卷 100MB
7z a -v100m large_archive.7z big_folder/

# 生成的文件：large_archive.7z.001, large_archive.7z.002, ...

# 解压分卷（只需指定第一个文件）
7z x large_archive.7z.001
```

### tar 分卷

```bash
# 创建分卷（每卷 100MB）
tar -czf - large_folder/ | split -b 100m - archive_part.tar.gz.

# 合并并解压
cat archive_part.tar.gz.* | tar -xzf -

# 生成的文件：archive_part.tar.gz.aa, archive_part.tar.gz.ab, ...
```

### WinRAR 分卷

```bash
# 命令行分卷（每卷 50MB）
rar a -v50m archive.rar large_folder/

# 解压（只需第一个文件）
rar x archive.part01.rar
```

## 加密压缩

### 7-Zip 加密

```bash
# AES-256 加密 + 加密文件头（推荐）
7z a -pMyStr0ngPass -mhe=on secret.7z confidential.docx

# 不解密查看文件列表会被阻止
```

### ZIP 加密

```bash
# 传统 ZipCrypto（兼容性较好）
7z a -pMyPass -tzip secret.zip confidential.docx

# AES-256（更安全，部分旧版解压工具不支持）
7z a -pMyPass -tzip -mem=AES256 secret.zip confidential.docx
```

### GPG 加密（跨平台）

```bash
# 先压缩再加密（推荐）
tar -czf data.tar.gz data/
gpg -c data.tar.gz  # 对称加密，提示输入密码
# 生成 data.tar.gz.gpg

# 解密
gpg -d data.tar.gz.gpg | tar -xzf -
```

### 安全建议

| 建议 | 说明 |
|------|------|
| 使用强密码 | 至少 12 位，包含大小写字母、数字、特殊字符 |
| 优先 AES-256 | ZipCrypto 已被证明可破解 |
| 加密文件头 | 7z 的 `-mhe=on` 可保护文件名不被泄露 |
| 先压缩后加密 | 用 GPG 等工具加密比压缩软件自带加密更灵活 |
| 勿通过不安全的渠道传输密码 | 密码与压缩包分开传输 |


