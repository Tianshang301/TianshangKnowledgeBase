---
aliases: [HistoryOfComputing]
tags: ['HistoryOfComputing', 'HistoryOfComputing']
---

# 计算历史完全指南

## 概述

计算的历史是一部人类不断追求更高效信息处理能力的演进史。从算盘到量子计算机，每一次突破都深刻改变了社会结构、经济模式和生活方式的方方面面。

---

## 一、前电子时代

### 1.1 早期计算工具

| 工具 | 年代 | 发明者/地区 | 功能 |
|------|------|-------------|------|
| 算盘 | ~2700 BCE | 美索不达米亚/中国 | 四则运算 |
| 安提基特拉机械 | ~100 BCE | 古希腊 | 天文计算 |
| 纳皮尔骨牌 | 1617 | John Napier | 乘除运算 |
| 计算尺 | 1620 | William Oughtred | 对数计算 |

### 1.2 机械计算时代

**Pascaline (1642)** — Blaise Pascal 发明的齿轮式加法器，是第一个成功的机械计算器。

**差分机 (Difference Engine, 1822)** — Charles Babbage 设计的多项式计算机械，但从未完全建成。

**分析机 (Analytical Engine, 1837)** — Babbage 提出的通用计算机设计，包含了现代计算机的所有核心概念：

```
分析机架构:
  ┌──────────┐    ┌──────────┐
  │  The Mill │◀──▶│ The Store│
  │  (ALU)   │    │ (Memory) │
  └────┬─────┘    └──────────┘
       │
  ┌────▼─────┐
  │ Operation│  ←  punched cards (来自 Jacquard 织布机)
  │ Cards    │
  └──────────┘
```

**Ada Lovelace (1815-1852)** — 为分析机编写了第一个算法（计算伯努利数），被公认为世界上第一位程序员。

---

## 二、第一代计算机：真空管 (1940-1956)

### 2.1 关键机器

| 计算机 | 年份 | 地点 | 特点 |
|--------|------|------|------|
| ENIAC | 1945 | 宾夕法尼亚大学 | 第一台通用电子计算机，18000 个真空管 |
| EDVAC | 1949 | 宾夕法尼亚大学 | 首次实现存储程序概念 |
| UNIVAC I | 1951 | Remington Rand | 第一台商用计算机 |
| IBM 701 | 1952 | IBM | IBM 第一台科学计算机 |

### 2.2 冯·诺伊曼架构

John von Neumann 在 EDVAC 设计中提出的存储程序概念成为现代计算机的基石：

```
冯·诺伊曼架构:
  ┌──────────┐     ┌──────────────┐
  │   CPU    │     │              │
  │ ┌──────┐ │◀───▶│   内存       │
  │ │ 运算器│ │     │ (数据和程序) │
  │ │ 控制器│ │     │              │
  │ └──────┘ │     └──────────────┘
  └────┬─────┘
       │
  ┌────▼─────┐     ┌──────────────┐
  │  输入    │     │   输出       │
  └──────────┘     └──────────────┘
```

---

## 三、第二代：晶体管 (1956-1963)

### 3.1 晶体管革命

1947 年，贝尔实验室的 Shockley、Bardeen 和 Brattain 发明了晶体管。相比真空管：

| 特性 | 真空管 | 晶体管 |
|------|--------|--------|
| 尺寸 | 大（如灯泡） | 小（毫米级） |
| 功耗 | 高（发热严重） | 低 |
| 寿命 | 数千小时 | 数百万小时 |
| 速度 | 慢 | 快（开关速度提升百倍） |
| 可靠性 | 低（常坏） | 高 |

### 3.2 代表机型

- **IBM 1401** (1959) — 最成功的小型商用计算机
- **IBM 7090** (1959) — 大型科学计算
- **DEC PDP-1** (1961) — 小型机先驱，影响了个人计算机发展

---

## 四、第三代：集成电路 (1964-1971)

### 4.1 IBM System/360

IBM System/360 (1964) 是计算机史上最重要的产品之一：

- 首个兼容的计算机系列（同一软件可跨不同型号运行）
- 首次区分体系结构和实现
- 奠定了 IBM 在大型机市场的主导地位

### 4.2 Moore 定律

1965 年，Gordon Moore 提出：

> 集成电路上可容纳的晶体管数量约每两年翻一番，同时成本减半。

这一定律在接下来的 50 多年中基本成立，驱动了信息技术产业的指数级增长。

```
晶体管数量增长趋势:
  1971: Intel 4004 — 2,300 个晶体管
  1985: Intel 80386 — 275,000 个晶体管
  2000: Pentium 4 — 42,000,000 个晶体管
  2020: Apple M1 — 16,000,000,000 个晶体管
  2023: NVIDIA H100 — 80,000,000,000 个晶体管
```

---

## 五、微处理器时代 (1971-1980)

### 5.1 关键处理器

| 处理器 | 年份 | 位数 | 频率 | 晶体管 | 意义 |
|--------|------|------|------|--------|------|
| Intel 4004 | 1971 | 4-bit | 740 KHz | 2,300 | 第一个商用微处理器 |
| Intel 8080 | 1974 | 8-bit | 2 MHz | 4,500 | Altair 8800 使用 |
| Intel 8086 | 1978 | 16-bit | 5-10 MHz | 29,000 | x86 架构起点 |
| Motorola 68000 | 1979 | 16/32-bit | 8 MHz | 68,000 | Macintosh 使用 |
| Intel 80386 | 1985 | 32-bit | 16-33 MHz | 275,000 | 首个 32 位 x86 |

x86 架构从 1978 年延续至今，保持了向后兼容性，是计算机史上最成功的指令集架构之一。

---

## 六、个人计算机革命 (1975-1990)

| 机器 | 年份 | 公司 | 意义 |
|------|------|------|------|
| Altair 8800 | 1975 | MITS | 第一台个人计算机，启发了 Microsoft |
| Apple II | 1977 | Apple | 首个成功的大众市场 PC |
| IBM PC | 1981 | IBM | 确立 PC 标准，采用 Intel CPU + MS-DOS |
| Macintosh | 1984 | Apple | 首个成功的 GUI 个人计算机 |

IBM PC 的开放架构催生了兼容机市场，也使得 Intel 和 Microsoft 成为行业霸主（Wintel 联盟）。

---

## 七、图形用户界面 (GUI)

### 7.1 关键里程碑

| 系统/概念 | 年份 | 机构 | 创新 |
|-----------|------|------|------|
| Sketchpad | 1963 | MIT | Ivan Sutherland 的交互式图形系统 |
| Xerox Alto | 1973 | Xerox PARC | 第一个 GUI 计算机（窗口、图标、鼠标）|
| Macintosh | 1984 | Apple | 首个成功的 GUI 个人计算机 |
| Windows 3.0 | 1990 | Microsoft | 首个广泛成功的 Windows 版本 |
| Windows 95 | 1995 | Microsoft | 开始菜单、任务栏、即插即用 |

---

## 八、互联网历史

### 8.1 时间线

```
1969: ARPANET 建立 (4 个节点: UCLA, SRI, UCSB, Utah)
1971: 第一封电子邮件 (Ray Tomlinson, @符号)
1974: TCP/IP 协议提出 (Cerf & Kahn)
1983: ARPANET 正式采用 TCP/IP
1989: World Wide Web 发明 (Tim Berners-Lee, CERN)
1993: Mosaic 浏览器 (NCSA) — 第一个图形化浏览器
1994: Netscape Navigator 发布
1995: Internet Explorer 发布，浏览器战争开始
1998: Google 成立
2004: Web 2.0 概念普及
2005: YouTube, Facebook (大学版)
2007: iPhone — 移动互联网开端
```

### 8.2 浏览器战争

| 时期 | 主要竞争者 | 结果 |
|------|-----------|------|
| 第一次 (1995-1999) | Netscape vs IE | IE 获胜（捆绑 Windows）|
| 第二次 (2004-2010) | IE vs Firefox vs Chrome | Chrome 胜出 |
| 第三次 (2010-至今) | Chrome vs Safari vs Firefox vs Edge | Chrome 主导 |

---

## 九、移动计算

| 产品 | 年份 | 意义 |
|------|------|------|
| Palm Pilot | 1996 | 第一个成功的 PDA |
| BlackBerry 850 | 1999 | 移动邮件设备 |
| iPhone | 2007 | 触摸屏智能手机革命 |
| Android (G1) | 2008 | 开源移动平台 |
| iPad | 2010 | 平板电脑普及 |

---

## 十、AI 里程碑

| 事件 | 年份 | 意义 |
|------|------|------|
| Deep Blue 击败 Kasparov | 1997 | 计算机首次在国际象棋中击败世界冠军 |
| IBM Watson 赢得 Jeopardy! | 2011 | 自然语言问答能力 |
| AlphaGo 击败李世石 | 2016 | 深度强化学习在围棋上的突破 |
| GPT-3 | 2020 | 大规模语言模型展示通用能力 |
| AlphaFold2 | 2021 | AI 解决蛋白质折叠问题 |

---

## 十一、计算技术发展时间线

| 时代 | 年份范围 | 关键技术 | 代表机器 |
|------|----------|----------|----------|
| 机械时代 | ~2700 BCE - 1940 | 齿轮、打孔卡 | 分析机 |
| 第一代 (真空管) | 1940-1956 | 真空管、磁鼓 | ENIAC, UNIVAC |
| 第二代 (晶体管) | 1956-1963 | 晶体管、磁芯 | IBM 1401 |
| 第三代 (IC) | 1964-1971 | 小规模集成电路 | IBM System/360 |
| 第四代 (VLSI) | 1971-至今 | 微处理器、大规模集成 | PC, 智能手机 |
| 第五代 (?) | 未来 | 量子计算、AI 加速 | 待定 |

---

## 相关条目

- [[05_ComputerScience/ProgrammingLanguages/INDEX|ProgrammingLanguages]]
- ComputerOrganization
- AIHistory
- InternetHistory

## 参考资源

- 《计算机组成与设计》— Patterson & Hennessy
- 《Code: The Hidden Language of Computer Hardware and Software》— Charles Petzold
- 《The Innovators》— Walter Isaacson
- 《UNIX: A History and a Memoir》— Brian Kernighan
- 计算机历史博物馆: https://www.computerhistory.org
- Intel 微处理器历史: https://www.intel.com/content/www/us/en/history
