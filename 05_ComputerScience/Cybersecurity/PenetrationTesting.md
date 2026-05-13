# 渗透测试完全指南

## 概述

渗透测试（Penetration Testing）是通过模拟攻击者视角，系统性地评估目标系统安全性的实践方法。区别于自动化漏洞扫描，渗透测试强调人工分析与深度利用，遵循标准化方法论。

---

## 一、渗透测试方法论

### 1.1 标准流程

渗透测试遵循结构化流程，从信息收集到报告输出形成完整闭环。

```
PTES 标准流程:
  1. 前期交互 (Pre-engagement)
     - 范围确定、规则约定、授权书签署
  2. 情报收集 (Intelligence Gathering)
     - 被动 OSINT / 主动扫描
  3. 威胁建模 (Threat Modeling)
     - 资产识别、攻击面分析
  4. 漏洞分析 (Vulnerability Analysis)
     - 自动化扫描 + 手动验证
  5. 漏洞利用 (Exploitation)
     - 获取初始访问权限
  6. 后渗透 (Post-Exploitation)
     - 权限提升、横向移动、数据窃取
  7. 报告输出 (Reporting)
     - 发现、风险等级、修复建议
```

### 1.2 测试类型对比

| 类型 | 信息提供 | 模拟对象 | 深度 | 成本 |
|------|----------|----------|------|------|
| Black Box | 无 | 外部攻击者 | 中 | 中 |
| White Box | 完整源码/架构 | 内部开发者 | 高 | 高 |
| Gray Box | 部分凭据 | 已获权限的攻击者 | 中高 | 中高 |

---

## 二、信息收集与侦察

### 2.1 被动侦察 (OSINT)

| 信息来源 | 工具/平台 | 获取内容 |
|----------|-----------|----------|
| DNS 枚举 | dig, nslookup, dnsrecon | 子域名、MX 记录、TXT 记录 |
| 搜索引擎 | Google Dorking | 敏感文件、暴露面板 |
| 证书透明度 | crt.sh, CertSpotter | 子域名 |
| WHOIS 查询 | whois | 注册信息、IP 段 |
| 社交媒体 | LinkedIn, Twitter | 员工信息、技术栈 |
| 代码仓库 | GitHub, GitLab | 泄露的凭据、配置 |
| Shodan | shodan.io | 暴露的服务、设备指纹 |

```
Google Dorking 示例:
  site:example.com filetype:pdf          → 查找 PDF 文档
  site:example.com inurl:admin           → 查找管理后台
  site:example.com intitle:"index of"    → 目录遍历
  filetype:env "DB_PASSWORD"             → 泄露的环境变量
  inurl:wp-content/uploads               → WordPress 上传目录
```

### 2.2 主动侦察

#### Nmap 扫描

Nmap 是最核心的网络侦察工具，支持多种扫描技术。

| 扫描类型 | 命令 | 特征 | 隐蔽性 |
|----------|------|------|--------|
| TCP SYN Scan | `-sS` | 半连接扫描，不完成三次握手 | 高 |
| TCP Connect Scan | `-sT` | 完成三次握手 | 低 |
| UDP Scan | `-sU` | 发送 UDP 探测包 | 低 |
| FIN/NULL/Xmas | `-sF -sN -sX` | 发送特殊标记包 | 高（绕过非 Windows）|
| ACK Scan | `-sA` | 映射防火墙规则 | 中 |

```
NSE 脚本:
  nmap --script vuln          → 漏洞扫描
  nmap --script http-enum     → Web 目录枚举
  nmap --script smb-enum      → SMB 信息枚举
  nmap --script dns-brute     → DNS 子域名爆破

常用命令:
  nmap -sS -sV -p- -T4 -A target
  # SYN 扫描 + 版本检测 + 全端口 + 激进模式 + OS/服务检测
```

---

## 三、漏洞扫描

| 工具 | 类型 | 特点 | 适用场景 |
|------|------|------|----------|
| Nessus | 商业 | 最全面的漏洞库，GUI 友好 | 企业合规扫描 |
| OpenVAS | 开源 | Greenbone 管理界面，功能强大 | 替代 Nessus 的开源方案 |
| Nikto | Web 扫描器 | 快速检测已知 Web 漏洞 | Web 服务器初步检查 |
| Nuclei | 模板化扫描 | YAML 模板，社区丰富 | DevOps 集成 |

```
Nessus 策略配置:
  - 扫描范围: 指定 IP/域名
  - 扫描模板: 基本网络扫描 / Web 应用测试 / PCI DSS 合规
  - 凭据扫描: 提供 SSH/Windows 凭据进行深度检测

OpenVAS / Greenbone:
  gvm-cli --gmp-username admin --gmp-password pass \
    socket --socketpath /var/run/gvmd.sock \
    --xml "<create_target><name>target</name><hosts>10.0.0.1</hosts></create_target>"
```

---

## 四、漏洞利用

### 4.1 Metasploit Framework

Metasploit 是最主流的渗透测试框架，提供完整的漏洞利用生命周期。

```
msfconsole 基本工作流:
  1. search <漏洞名称>        → 查找模块
  2. use exploit/<路径>       → 选择利用模块
  3. show options             → 查看配置项
  4. set RHOSTS <目标>        → 设置目标
  5. run / exploit            → 执行利用

  选择 Payload:
    反向 Shell:  set PAYLOAD linux/x64/shell_reverse_tcp
    Meterpreter: set PAYLOAD linux/x64/meterpreter_reverse_tcp
    Bind Shell:  set PAYLOAD linux/x64/shell_bind_tcp
```

| 组件 | 说明 | 示例 |
|------|------|------|
| Exploit | 漏洞利用代码 | `exploit/multi/http/struts2_rest_xstream` |
| Payload | 利用成功后执行的操作 | `meterpreter`, `shell`, `migrate` |
| Auxiliary | 辅助模块（扫描、枚举、DoS） | `auxiliary/scanner/portscan/tcp` |
| Post | 后渗透模块 | `post/linux/gather/hashdump` |
| Encoder | Payload 编码（免杀） | `cmd/powershell_base64` |

### 4.2 Web 应用测试工具

#### Burp Suite

Burp Suite 是 Web 应用渗透测试的行业标准工具。

| 模块 | 功能 | 快捷键 |
|------|------|--------|
| Proxy | 拦截/修改 HTTP 请求 | Ctrl+R 发送到 Repeater |
| Repeater | 手动重放和修改请求 | Ctrl+U 发送到 Intruder |
| Intruder | 自动化参数爆破 | 多个位置、字典载荷 |
| Scanner | 自动化漏洞扫描 | 爬虫 + 主动扫描 |
| Decoder | 编解码工具 | Base64/URL/Hex/ASCII |
| Extender | BApp 商店扩展 | JSON Web Tokens, Turbo Intruder |

#### SQLMap

```bash
# SQLMap 自动化 SQL 注入
sqlmap -u "http://target.com/page?id=1" --dbs
sqlmap -u "http://target.com/page?id=1" -D dbname --tables
sqlmap -u "http://target.com/page?id=1" -D dbname -T users --dump

# 进阶选项
sqlmap -r request.txt --level 3 --risk 2
sqlmap -u "http://target.com/page?id=1" --os-shell
sqlmap --batch --random-agent --threads 10
```

---

## 五、权限提升

### 5.1 Linux 提权

| 向量 | 描述 | 检查命令 |
|------|------|----------|
| SUID 提权 | 利用设置了 SUID 位的二进制 | `find / -perm -4000 2>/dev/null` |
| 内核漏洞 | 利用内核 CVE | `uname -a` → searchsploit |
| Sudo 配置 | `/etc/sudoers` 中的危险配置 | `sudo -l` |
| Cron 任务 | 可写的计划任务脚本 | `cat /etc/crontab` |
| 不安全的路径 | PATH 劫持 | `echo $PATH` |
| Docker 逃逸 | 挂载宿主机目录 | `docker -v` |

```bash
# SUID 提权示例
./vuln_program  # 如果具有 SUID root，可利用它执行系统命令

# 内核提权
linux-exploit-suggester.sh  # 检测可利用的内核漏洞

# Docker 逃逸
docker run -v /:/mnt -it alpine chroot /mnt
```

### 5.2 Windows 提权

| 向量 | 描述 | 工具 |
|------|------|------|
| Token Abuse | SeImpersonate 窃取系统 Token | JuicyPotato, RoguePotato |
| 未引号服务路径 | 空格导致路径劫持 | `wmic service get name,pathname` |
| 内核漏洞 | Windows 内核 CVE | Windows-Exploit-Suggester |
| AlwaysInstallElevated | MSI 以 SYSTEM 权限安装 | 检查注册表 |
| UAC 绕过 | 绕过用户账户控制 | UACME 项目 |

---

## 六、横向移动

| 技术 | 原理 | 工具 |
|------|------|------|
| Pass-the-Hash | 使用 NTLM 哈希直接认证 | Mimikatz, Impacket |
| Pass-the-Ticket | Kerberos 票据窃取与重放 | Mimikatz, Rubeus |
| SSH 密钥窃取 | 收集 `~/.ssh/id_rsa` | 手动 / 脚本 |
| WMI 远程执行 | Windows Management Instrumentation | wmic, Impacket |
| WinRM | Windows 远程管理 | evil-winrm |
| PsExec | Sysinternals 远程执行 | Impacket-psexec |

```
Mimikatz 常用命令:
  sekurlsa::logonpasswords      → 提取明文密码
  sekurlsa::tickets             → 提取 Kerberos 票据
  lsadump::sam                  → 提取 SAM 哈希
  token::elevate                → 提升 Token
  lsadump::dcsync /user:krbtgt → DCSync 攻击
```

---

## 七、密码攻击

| 工具 | 类型 | 特点 | 性能 (H/s) |
|------|------|------|------------|
| Hashcat | GPU 加速 | 支持 200+ 哈希类型 | 最高（依赖 GPU）|
| John the Ripper | CPU | 自动识别哈希类型 | 中等 |
| Hydra | 在线爆破 | 支持多种协议 | 受限于网络 |
| Medusa | 在线爆破 | 并行连接 | 类似 Hydra |

```
Hashcat 工作流:
  hashcat -m 1000 -a 0 hash.txt wordlist.txt  # MD5 字典攻击
  hashcat -m 1000 -a 3 hash.txt ?a?a?a?a?a?a  # 掩码攻击 (6位全部字符)
  hashcat -m 1000 -a 1 hash.txt word1.txt word2.txt  # 组合攻击

  -m: 哈希类型 (1000=NTLM, 0=MD5, 1400=SHA256)
  -a: 攻击模式 (0=字典, 1=组合, 3=掩码, 6=混合)

常用字典:
  rockyou.txt         → 最经典的密码字典 (1400万+)
  SecLists            → 全面的安全测试字典
  CrackStation        → 彩虹表
  Have I Been Pwned   → 真实泄露密码 (6亿+)
```

---

## 八、报告与修复

### 8.1 报告结构

```
渗透测试报告标准结构:
  1. 执行摘要 (Executive Summary)
     - 面向管理层、非技术视角
     - 整体风险评分、关键发现
  2. 技术报告 (Technical Report)
     - 每个漏洞的详细信息
  3. 漏洞详情
     - 漏洞名称 / CVE 编号 / CVSS 评分
     - 复现步骤 (PoC)
     - 影响分析
     - 修复建议
  4. 严重性分级

CVSS 3.1 评分标准:
  严重 (Critical):   9.0-10.0
  高危 (High):       7.0-8.9
  中危 (Medium):     4.0-6.9
  低危 (Low):        0.1-3.9
  信息 (Info):       0.0
```

### 8.2 修复优先级矩阵

| 影响/可能性 | 高可能性 | 中可能性 | 低可能性 |
|-------------|----------|----------|----------|
| 高影响 | 立即修复 | 24-48h 内 | 下周前 |
| 中影响 | 48h 内 | 本周内 | 本月内 |
| 低影响 | 本周内 | 本月内 | 下季度 |

---

## 相关条目

- [[WebSecurity]]
- [[NetworkSecurity]]
- [[Cybersecurity]]
- EthicalHacking

## 参考资源

- PTES 标准: http://www.pentest-standard.org
- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide
- Metasploit Unleashed: https://www.offensive-security.com/metasploit-unleashed
- Hack The Box / TryHackMe 练习平台
- 《The Hacker Playbook 3》— Peter Kim
- 《Penetration Testing: A Hands-On Introduction to Hacking》— Georgia Weidman
- MITRE ATT&CK: https://attack.mitre.org
- PayloadsAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings
