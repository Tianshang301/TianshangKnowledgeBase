# 智能合约完全指南

## 概述

智能合约（Smart Contract）是运行在区块链上的可编程代码，能够自动执行预设的逻辑。以太坊通过图灵完备的以太坊虚拟机（EVM）使智能合约得以普及，开启了去中心化应用（DApp）时代。

---

## 一、智能合约基础

### 1.1 核心概念

| 概念 | 说明 |
|------|------|
| 图灵完备 | EVM 可执行任意计算（Gas 限制避免无限循环）|
| Gas | 执行每步操作消耗的计算单位，防止资源滥用 |
| 账户模型 | EOA（外部账户）vs 合约账户 |
| 状态 | 区块链上的持久化键值存储 |
| 交易 | 由 EOA 发起的签名消息，可触发合约执行 |

### 1.2 账户类型

```
EOA (Externally Owned Account):
  - 由私钥控制
  - 余额 = ETH
  - nonce = 交易计数
  - 可发起交易
  - 地址: 0x + 40 位十六进制

合约账户 (Contract Account):
  - 由合约代码控制
  - 存储合约状态
  - 由交易触发
  - 地址由创建者地址 + nonce 哈希生成

EOA → 发起交易 → 合约账户 → 执行代码 → 状态变更
```

---

## 二、Solidity 基础

### 2.1 数据类型

| 类别 | 类型 | 说明 |
|------|------|------|
| 值类型 | `bool`, `int`, `uint`, `address`, `bytes1~32` | 按值传递，复制 |
| 引用类型 | `string`, `bytes`, `array`, `struct`, `mapping` | 引用传递，需指定数据位置 |
| 特殊类型 | `address payable` | 可接收 ETH 的地址 |

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataTypes {
    // 状态变量 (持久化到存储)
    uint256 public count;           // 默认 0
    address public owner;           // 默认 address(0)
    bool public active;             // 默认 false

    // 枚举
    enum Status { Pending, Active, Closed }
    Status public status;

    // 结构体
    struct User {
        string name;
        uint256 age;
    }

    // 映射
    mapping(address => User) public users;

    // 数组
    uint256[] public numbers;

    function addUser(string calldata _name, uint256 _age) external {
        users[msg.sender] = User(_name, _age);
    }
}
```

### 2.2 数据位置

| 关键字 | 存储位置 | 持久性 | Gas 成本 |
|--------|----------|--------|----------|
| `storage` | 区块链状态 | 持久 | 高（修改需 SSTORE） |
| `memory` | 内存 | 临时（函数内）| 中 |
| `calldata` | 交易输入数据 | 只读 | 低（不可修改）|

```solidity
function processArray(uint256[] calldata _input) external pure returns (uint256) {
    // calldata: 只读，低 Gas
    // memory:   可读写，中等 Gas
    uint256[] memory temp = new uint256[](_input.length);
    temp[0] = _input[0];
    return temp[0];
}
```

### 2.3 函数与修饰器

```solidity
contract FunctionExamples {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // 函数可见性
    function externalFunc() external {}    // 仅外部可调用
    function publicFunc() public {}       // 内外皆可
    function internalFunc() internal {}   // 合约内部及子合约
    function privateFunc() private {}     // 仅当前合约

    // view / pure: 不消耗 Gas (外部调用时)
    function viewFunc() external view returns (uint256) {}
    function pureFunc() external pure returns (uint256) {}

    // modifier
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function adminAction() external onlyOwner {
        // 只有 owner 可调用
    }

    // 事件 (Event)
    event Transfer(address indexed from, address indexed to, uint256 value);

    function transfer(address _to, uint256 _amount) external {
        emit Transfer(msg.sender, _to, _amount);
    }
}
```

---

## 三、常见设计模式

### 3.1 Ownable

```solidity
abstract contract Ownable {
    address private _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() {
        _owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == _owner, "Ownable: caller is not the owner");
        _;
    }

    function owner() public view returns (address) { return _owner; }

    function renounceOwnership() external onlyOwner {
        _owner = address(0);
    }

    function transferOwnership(address newOwner) external onlyOwner {
        _owner = newOwner;
    }
}
```

### 3.2 Pausable

```solidity
abstract contract Pausable is Ownable {
    bool private _paused;

    modifier whenNotPaused() {
        require(!_paused, "Paused");
        _;
    }

    function pause() external onlyOwner { _paused = true; }
    function unpause() external onlyOwner { _paused = false; }
}
```

### 3.3 代币标准

| 标准 | 类型 | 特性 | 用途 |
|------|------|------|------|
| ERC-20 | 同质化代币 | `transfer`, `approve`, `transferFrom`, `balanceOf` | USDT, UNI, LINK |
| ERC-721 | NFT | `ownerOf`, `tokenURI`, `safeTransferFrom` | CryptoPunks, BAYC |
| ERC-1155 | 多代币 | 批量铸造，同质化+非同质化混合 | 游戏物品 |

```solidity
// ERC-20 核心接口
interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}
```

### 3.4 代理模式与可升级合约

```
代理模式结构:
  用户 → 代理合约 (Proxy) → 逻辑合约 (Implementation)
            ↓
       存储: 代理合约的存储（通过 delegatecall）

工作流程:
  1. Proxy 使用 delegatecall 调用 Implementation
  2. 逻辑代码在 Implementation 中
  3. 状态存储在 Proxy 中（不被抹除）
  4. 升级时部署新的 Implementation，更新 Proxy 指向

常见实现:
  - Transparent Proxy (OpenZeppelin)
  - UUPS (Universal Upgradeable Proxy Standard)

优点: 可修复 bug、可迭代
缺点: 存储布局冲突风险、函数选择器冲突
```

---

## 四、安全漏洞

### 4.1 重入攻击 (Reentrancy)

```
攻击流程:
  1. 合约 A 调用 合约 B（withdraw）
  2. 合约 B 的 fallback 再次调用 合约 A 的 withdraw
  3. 合约 A 的余额还未更新 → 重复提取

防护:
  1. 检查-生效-交互模式 (Checks-Effects-Interactions)
  2. ReentrancyGuard (OpenZeppelin)
  3. 避免在状态更新前进行外部调用
```

```solidity
contract Vulnerable {
    mapping(address => uint256) public balances;

    function withdraw() external {
        uint256 bal = balances[msg.sender];
        require(bal > 0);
        (bool ok, ) = msg.sender.call{value: bal}("");  // 先转账
        balances[msg.sender] = 0;                         // 后更新 ❌
    }
}

contract Secure {
    mapping(address => uint256) public balances;

    function withdraw() external {
        uint256 bal = balances[msg.sender];
        require(bal > 0);
        balances[msg.sender] = 0;                         // 先更新 ✅
        (bool ok, ) = msg.sender.call{value: bal}("");    // 后转账
        require(ok);
    }
}
```

### 4.2 其他常见漏洞

| 漏洞 | 描述 | 防护 |
|------|------|------|
| 整数溢出 | 算术运算超出类型范围 | Solidity ^0.8 内置检查 / SafeMath |
| tx.origin vs msg.sender | `tx.origin` 可能被钓鱼 | 使用 `msg.sender` |
| 访问控制缺陷 | `public` 函数可被任意调用 | 正确使用 modifier |
| 预言机操纵 | 价格预言机被操纵 | 使用 TWAP 或去中心化预言机 |
| 闪电贷攻击 | 借贷大量资金操纵价格 | 防止价格依赖单笔交易 |
| 时间戳依赖 | `block.timestamp` 可被矿工操纵 | 避免作为随机数源 |

```solidity
// tx.origin 钓鱼攻击
contract Phishable {
    address public owner;

    constructor() { owner = msg.sender; }

    function withdraw() external {
        require(tx.origin == owner);  // ❌ 易受钓鱼攻击
        payable(owner).transfer(address(this).balance);
    }
}

// 正确: 使用 msg.sender
contract SafeContract {
    function withdraw() external {
        require(msg.sender == owner);  // ✅ msg.sender 是直接调用者
    }
}
```

---

## 五、开发工具链

| 工具 | 类型 | 特点 | 适用阶段 |
|------|------|------|----------|
| Hardhat | 开发框架 | 本地网络、调试、插件生态 | 开发主力 |
| Foundry | 开发框架 | 极致速度（Rust）、Solidity 测试 | 测试/部署 |
| Truffle | 开发框架 | 成熟、Suite 生态 | 兼容场景 |
| Remix | 在线 IDE | 浏览器直接编写、快速原型 | 学习/原型 |
| OpenZeppelin | 合约库 | 经过审计的标准合约 | 基础组件 |

```bash
# Hardhat 工作流
npx hardhat init
npx hardhat compile
npx hardhat test
npx hardhat run scripts/deploy.js --network sepolia

# Foundry 工作流
forge init
forge build
forge test
forge script script/Deploy.s.sol --rpc-url $RPC --broadcast
```

### 5.1 测试与验证

| 测试类型 | 目的 | 工具 |
|----------|------|------|
| 单元测试 | 测试单个函数逻辑 | Hardhat (JS/TS), Foundry (Solidity) |
| 集成测试 | 多合约交互流程 | Hardhat, Foundry |
| 分叉测试 | 在主网状态下测试 | Hardhat fork, Anvil fork |
| 形式化验证 | 数学证明合约正确性 | Certora, Scribble |
| 模糊测试 | 随机输入寻找边界情况 | Foundry fuzz, Echidna |

### 5.2 Gas 优化

```
Gas 优化技巧:
  1. 使用 uint256 而非 smaller types（EVM 按 256 位寻址）
  2. 将变量打包到同一个 storage slot
  3. 使用 calldata 而非 memory（只读参数）
  4. 短路操作 (require 条件顺序优化)
  5. 批量写入 (循环 vs 多笔交易)
  6. 使用 mapping 而非 Array 存储（查找更便宜）
  7. 事件存储数据而非链上存储

Storage Slot 打包:
  struct Data {
      uint128 a;  // slot 0 (16 bytes)
      uint128 b;  // slot 0 (16 bytes) → 打包到一个 slot
      uint256 c;  // slot 1 (独立 slot)
  }
```

---

## 六、合约部署与治理

```
合约部署流程:
  1. 编写合约 + 单元测试
  2. 审计 (内部 + 第三方)
  3. 测试网部署验证
  4. 主网部署
     - 使用多重签名 (Gnosis Safe)
     - 时间锁 (Timelock) 延迟管理操作
  5. 开源验证 (Etherscan)
  6. 监控与紧急暂停机制

合约治理:
  - 链上治理: 用户投票 → 合约自动执行
  - 链下治理: Snapshot 投票 → 多签手动执行
  - 时间锁: 任何管理操作有延迟窗口
```

---

## 相关条目

- [[Blockchain]]
- [[ConsensusMechanisms]]
- [[DeFi]]
- Cryptography

## 参考资源

- Solidity 官方文档: https://docs.soliditylang.org
- OpenZeppelin Contracts: https://www.openzeppelin.com/contracts
- Ethereum Yellow Paper: Gavin Wood
- 《Mastering Ethereum》— Antonopoulos & Wood
- Smart Contract Security: https://swcregistry.io
- Ethers.js / Web3.js 文档
- Hardhat 文档: https://hardhat.org
- Foundry Book: https://book.getfoundry.sh
