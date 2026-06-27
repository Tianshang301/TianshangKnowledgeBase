---
aliases: [Cybersecurity, 网络安全概述]
tags: ['05_ComputerScience', 'Cybersecurity', 'Overview']
created: 2026-05-17
updated: 2026-05-17
---

# 网络安全概述 (Cybersecurity Overview)

## 定义与核心目标

网络安全（Cybersecurity）是保护计算机系统、网络、程序和数据免受数字攻击的实践与技术领域。其核心目标由 **CIA 三元组**（CIA Triad）概括：

| 要素 | 英文 | 定义 |
|------|------|------|
| 机密性 | Confidentiality | 确保信息不被未授权访问或泄露 |
| 完整性 | Integrity | 保证数据未被篡改，来源可信 |
| 可用性 | Availability | 确保授权用户能及时访问资源 |

## 安全三要素关系

```mermaid
graph TD
    C[机密性<br/>Confidentiality] --- I[完整性<br/>Integrity]
    I --- A[可用性<br/>Availability]
    A --- C
    S((安全<br/>Security)) --> C
    S --> I
    S --> A
```

## 扩展安全模型

### Parkerian Hexad

在 CIA 基础上增加了三个要素：

| 要素 | 描述 |
|------|------|
| 持有 (Possession) | 数据的物理或逻辑控制 |
| 真实性 (Authenticity) | 数据来源的合法性验证 |
| 效用性 (Utility) | 数据的可用性与价值 |

### STRIDE 威胁分类

| 威胁类型 | 英文 | 破坏目标 |
|---------|------|---------|
| 欺骗 (Spoofing) | Spoofing | 真实性 |
| 篡改 (Tampering) | Tampering | 完整性 |
| 抵赖 (Repudiation) | Repudiation | 不可否认性 |
| 信息泄露 (Info Disclosure) | Information Disclosure | 机密性 |
| 拒绝服务 (DoS) | Denial of Service | 可用性 |
| 权限提升 (Elevation) | Elevation of Privilege | 授权 |

## 常见威胁类型 (Common Threats)

```mermaid
graph LR
    subgraph 恶意软件
        A1[病毒<br/>Virus]
        A2[蠕虫<br/>Worm]
        A3[特洛伊<br/>Trojan]
        A4[勒索软件<br/>Ransomware]
    end
    subgraph 网络攻击
        B1[钓鱼<br/>Phishing]
        B2[DDoS]
        B3[中间人<br/>MitM]
        B4[SQL 注入<br/>SQL Injection]
    end
    subgraph 社会工程
        C1[ pretexting]
        C2[Baiting]
        C3[Tailgating]
    end
```

### 威胁分类表

| 类别 | 示例 | 影响 |
|------|------|------|
| 恶意软件 (Malware) | 病毒、蠕虫、木马、勒索软件 | 数据破坏、加密勒索 |
| 网络钓鱼 (Phishing) | 鱼叉钓鱼、鲸钓 | 凭证窃取 |
| DDoS 攻击 | 应用层/网络层泛洪 | 服务不可用 |
| 中间人攻击 (MitM) | HTTPS 降级、WiFi 嗅探 | 数据窃取 |
| 内部威胁 (Insider) | 恶意/无意泄露 | 数据泄露 |
| APT 攻击 | 国家支持的高级持续威胁 | 长期潜伏窃密 |

## 防御体系 (Defense in Depth)

分层防御（Layered Defense）模型：

```mermaid
graph BT
    subgraph 第七层: 安全策略
        P[数据安全策略<br/>Data Security Policy]
    end
    subgraph 第六层: 物理安全
        PH[门禁/监控<br/>Physical Access]
    end
    subgraph 第五层: 身份与访问
        IAM[IAM/MFA/SSO<br/>Identity & Access]
    end
    subgraph 第四层: 网络安全
        N[防火墙/IDS/IPS/VPN<br/>Network Security]
    end
    subgraph 第三层: 主机安全
        H[EDR/AV/HIPS<br/>Host Security]
    end
    subgraph 第二层: 应用安全
        A[WAF/代码审计<br/>Application Security]
    end
    subgraph 第一层: 数据安全
        D[加密/DLP/备份<br/>Data Security]
    end
```

## 关键防御技术

| 技术 | 英文 | 功能 |
|------|------|------|
| 防火墙 | Firewall | 基于规则的数据包过滤 |
| 入侵检测系统 | IDS | 网络流量异常检测与告警 |
| 入侵防御系统 | IPS | 实时阻断恶意流量 |
| 虚拟专用网络 | VPN | 加密远程通信隧道 |
| 多因素认证 | MFA | 多因子身份验证 |
| 端点检测与响应 | EDR | 端点威胁实时监控 |
| 数据防泄漏 | DLP | 敏感数据流出监控 |
| 安全信息和事件管理 | SIEM | 日志聚合与分析 |

## 安全的数学基础

熵（Entropy）衡量信息的不确定性：

$$
H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)
$$

在密码学中，密钥强度通常用比特表示：$k$ 位密钥的密钥空间为 $2^k$。

## 安全成熟度模型

| 级别 | 名称 | 特征 |
|------|------|------|
| 1 | 初始级 (Initial) | 反应式、无流程 |
| 2 | 可重复级 (Repeatable) | 基本流程建立 |
| 3 | 定义级 (Defined) | 标准化流程 |
| 4 | 管理级 (Managed) | 量化度量 |
| 5 | 优化级 (Optimizing) | 持续改进 |

## 趋势与发展

- **零信任架构 (Zero Trust)**：从不信任，始终验证
- **AI 驱动的安全分析**：机器学习辅助威胁检测
- **云安全 (Cloud Security)**：CASB、CSPM、CIEM
- **量子安全密码学 (Post-Quantum Cryptography)**：抗量子攻击算法
- **安全即代码 (Security as Code)**：DevSecOps 实践

## 相关条目

- [[SecurityFrameworks]]
- [[NetworkSecurity]]
- [[Cryptography]]
- [[MalwareAnalysis]]
- [[PenetrationTesting]]
- [[WebSecurity]]

