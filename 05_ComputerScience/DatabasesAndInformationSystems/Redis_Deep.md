# Redis 缓存与数据结构服务器

## 一、概述

Redis（Remote Dictionary Server）是一个使用 ANSI C 编写的高性能 key-value 内存数据库，支持字符串、哈希、列表、集合、有序集合等丰富的数据结构。

### 特性

| 特性 | 说明 |
|------|------|
| 内存存储 | 所有数据存储在内存中，读写速度极快（~100,000+ ops/sec） |
| 持久化 | 支持 RDB 快照和 AOF 日志两种持久化方式 |
| 数据结构丰富 | String、List、Set、Sorted Set、Hash、Bitmap、HyperLogLog、Geo、Stream |
| 复制 | 主从复制，支持读写分离 |
| 高可用 | Redis Sentinel 提供自动故障转移 |
| 分布式 | Redis Cluster 提供数据分片和水平扩展 |
| Lua 脚本 | 支持在服务器端执行 Lua 脚本 |
| 事务 | MULTI/EXEC 提供基础事务支持 |

---

## 二、数据结构

### String — 字符串

最基础的数据类型，value 最大 512MB。

```redis
SET key "value"
SET name "zhangsan"
GET name                          # "zhangsan"
SET counter 100
INCR counter                      # 101
INCRBY counter 5                  # 106
DECR counter                      # 105
SETEX session:token 3600 "abc123"  # 设置带过期时间的 key
SETNX lock:1 "locked"             # 不存在才设置（分布式锁基础）
MSET k1 v1 k2 v2                  # 批量设置
MGET k1 k2                        # 批量获取
GETSET name "lisi"                # 获取旧值，设置新值
STRLEN name                       # 获取字符串长度
APPEND name " hello"              # 追加字符串
```

### List — 列表

基于双向链表实现，适合消息队列、最新消息列表。

```redis
LPUSH queue "task1"              # 左端插入
RPUSH queue "task2"              # 右端插入
LPOP queue                       # 左端弹出
RPOP queue                       # 右端弹出
LRANGE queue 0 -1               # 获取全部元素
LLEN queue                       # 列表长度
LINDEX queue 0                  # 获取指定位置元素
LTRIM queue 0 99                # 截取列表（保留前100个）
BLPOP queue 5                   # 阻塞式左弹出（超时5秒）
```

### Set — 集合

无序、去重，支持集合运算。

```redis
SADD tags "redis" "database" "nosql"  # 添加元素
SMEMBERS tags                         # 获取所有元素
SISMEMBER tags "redis"                # 判断是否存在
SCARD tags                            # 集合大小
SREM tags "nosql"                     # 删除元素
SPOP tags 2                           # 随机弹出2个元素

SINTER set1 set2                      # 交集
SUNION set1 set2                      # 并集
SDIFF set1 set2                       # 差集

# 应用：共同关注
SADD user:1:follow "A" "B" "C"
SADD user:2:follow "B" "C" "D"
SINTER user:1:follow user:2:follow    # 共同关注：B, C
```

### Sorted Set — 有序集合

每个元素关联一个 score，按 score 排序。

```redis
ZADD leaderboard 100 "player1" 200 "player2" 150 "player3"
ZRANGE leaderboard 0 -1 WITHSCORES         # 升序
ZREVRANGE leaderboard 0 -1 WITHSCORES      # 降序
ZINCRBY leaderboard 50 "player1"           # 加分
ZRANK leaderboard "player1"                # 排名（从0开始）
ZSCORE leaderboard "player1"              # 获取分数
ZREM leaderboard "player3"                # 删除元素
ZCOUNT leaderboard 100 200                # 统计分数区间内元素数
ZREVRANK leaderboard "player1"            # 降序排名

# 应用：排行榜
ZINCRBY daily:revenue "shop_1" 1500       # 每日收入排行
```

### Hash — 哈希

适合存储对象，类似 Map。

```redis
HSET user:1001 name "zhangsan" age 25 city "beijing"
HGET user:1001 name                       # "zhangsan"
HGETALL user:1001                         # 获取所有字段
HMGET user:1001 name age                  # 获取多个字段
HINCRBY user:1001 age 1                   # age 自增
HDEL user:1001 city                       # 删除字段
HEXISTS user:1001 email                   # 检查字段是否存在
HKEYS user:1001                           # 获取所有字段名
HVALS user:1001                           # 获取所有字段值
HLEN user:1001                            # 字段数量
```

### Bitmap — 位图

基于 String 的位操作，适合签到、活跃用户统计。

```redis
SETBIT user:sign:202401 0 1               # 1号签到
SETBIT user:sign:202401 1 1               # 2号签到
GETBIT user:sign:202401 0                 # 获取1号签到状态
BITCOUNT user:sign:202401                 # 统计签到天数
BITOP AND result bitmap1 bitmap2          # 位运算

# 应用：日活跃用户（以 user_id 为偏移位）
SETBIT dau:2024-06-01 100 1               # user_id 100 在 6月1日 活跃
SETBIT dau:2024-06-01 200 1               # user_id 200 在 6月1日 活跃
BITCOUNT dau:2024-06-01                   # 统计 6月1日 活跃用户数
```

### HyperLogLog — 基数统计

用于大数据量的去重计数，误差约 0.81%，每个 key 仅占用 12KB。

```redis
PFADD unique:visitors:today "ip1" "ip2" "ip3" "ip1"
PFCOUNT unique:visitors:today              # 结果：3（去重后）
PFMERGE result visitors:day1 visitors:day2
```

### Geo — 地理位置

```redis
GEOADD cities 116.40 39.90 "beijing"
GEOADD cities 121.47 31.23 "shanghai"
GEOADD cities 113.27 23.13 "guangzhou"

GEODIST cities beijing shanghai km         # 两地距离
GEORADIUS cities 116.40 39.90 1000 km      # 北京周围1000km内的城市
GEORADIUSBYMEMBER cities beijing 1500 km WITHCOORD WITHDIST
```

### Stream — 消息流

Redis 5.0 引入，支持消息持久化和消费组。

```redis
# 生产者
XADD mystream * sensor-id 1234 temperature 19.8
XADD mystream MAXLEN ~ 10000 * sensor-id 5678 temperature 21.0

# 消费者
XRANGE mystream - +
XREAD COUNT 10 STREAMS mystream 0

# 消费组
XGROUP CREATE mystream mygroup $
XREADGROUP GROUP mygroup consumer1 COUNT 1 STREAMS mystream >
XACK mystream mygroup message-id
XPENDING mystream mygroup
```

---

## 三、持久化

### RDB（默认）

```redis
# redis.conf
save 900 1          # 900秒内有1次变更则快照
save 300 10         # 300秒内有10次变更则快照
save 60 10000       # 60秒内有10000次变更则快照
dbfilename dump.rdb
dir /var/lib/redis
```

| 优点 | 缺点 |
|------|------|
| 文件紧凑，适合备份 | 可能丢失最后一次快照后的数据 |
| 恢复速度快 | 数据量大时 fork 可能阻塞 |
| 适合灾难恢复 | |

### AOF

```redis
# redis.conf
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec    # 可选：always / everysec / no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

| 优点 | 缺点 |
|------|------|
| 数据更安全（最多丢1秒） | AOF 文件通常比 RDB 大 |
| AOF 重写可压缩 | 恢复速度比 RDB 慢 |
| 日志格式可读 | |

### RDB + AOF 混合（Redis 4.0+）

```redis
aof-use-rdb-preamble yes
```

同时开启时，AOF 重写使用 RDB 格式作为前缀，兼具 RDB 的恢复速度和 AOF 的数据安全性。

---

## 四、复制

### 主从复制

```redis
# 从库配置
replicaof master_ip 6379
replica-read-only yes

# 或运行时
SLAVEOF master_ip 6379   # 6.2+ 推荐 REPLICAOF
```

**复制过程**：
1. 从库发送 SYNC/PSYNC 命令
2. 主库执行 BGSAVE 生成 RDB 快照
3. 主库将 RDB 发送给从库
4. 从库加载 RDB
5. 主库将持续推送增量命令给从库

### Redis Sentinel

```redis
# sentinel.conf
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 15000
```

```bash
redis-sentinel /path/to/sentinel.conf
```

### 读写分离

```
应用层 → Sentinel → 获取主库/从库地址
                  → 写请求发往 Master
                  → 读请求发往 Replica
```

---

## 五、集群

### Redis Cluster

```redis
# redis.conf
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
```

```bash
# 创建集群（6个节点，3主3从）
redis-cli --cluster create \
    127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
    127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 \
    --cluster-replicas 1

# 集群命令
redis-cli -c -p 7000              # -c 表示集群模式
CLUSTER INFO                       # 集群状态
CLUSTER NODES                      # 节点信息
CLUSTER KEYSLOT keyname            # 查看 key 的哈希槽
```

### 哈希槽

Redis Cluster 将 key 空间分为 **16384 个哈希槽**：

```text
HASH_SLOT = CRC16(key) % 16384
```

**分区方式**：

```redis
# 使用 hash tag 确保相关 key 在同一节点
user:{1001}:profile
user:{1001}:orders
```

---

## 六、常见使用场景

### 缓存

```redis
# 缓存数据库查询结果
SETEX user:info:1001 3600 '{"name":"zhangsan","age":25}'

# 缓存穿透防护（缓存空值）
SETEX empty:product:9999 60 "null"

# 缓存雪崩防护（过期时间加随机值）
SETEX cache:key 3600+RANDOM(0,300) "value"
```

### 限流

```redis
# 简单限流：每分钟最多100次
INCR rate:limit:user:1001
EXPIRE rate:limit:user:1001 60

# 滑动窗口限流（使用 ZSET）
ZREM range:limit:user:1001 BYSCORE 0 (NOW - 60
ZADD range:limit:user:1001 NOW NOW
ZCOUNT range:limit:user:1001 -inf +inf
# 超过阈值则拒绝
```

### 分布式锁

```redis
# Redlock 简易实现
SET lock:resource1 "instance1" NX EX 10    # 获取锁，10秒自动释放

# 释放锁（使用 Lua 保证原子性）
EVAL "
    if redis.call('get', KEYS[1]) == ARGV[1] then
        return redis.call('del', KEYS[1])
    else
        return 0
    end
" 1 lock:resource1 instance1
```

### 消息队列

```redis
# List 实现简单队列
RPUSH task:queue "task_data"
BLPOP task:queue 0

# Stream 实现可靠消息队列
XGROUP CREATE task:stream consumer-group $
XREADGROUP GROUP consumer-group consumer-1 COUNT 1 task:stream >
XACK task:stream consumer-group message-id
```

### 排行榜

```redis
# 游戏排行榜
ZADD game:scores 1500 "player_1001"
ZADD game:scores 2000 "player_1002"
ZADD game:scores 1800 "player_1003"
ZREVRANGE game:scores 0 9 WITHSCORES     # Top 10
```

### Session 存储

```redis
# 分布式 Session
SETEX session:token:abc123 86400 '{"user_id":1001,"role":"admin"}'
GET session:token:abc123
```

---

## 七、过期与淘汰策略

### 过期策略

| 策略 | 说明 |
|------|------|
| 定期删除 | 每100ms随机抽取20个key，删除其中过期的 |
| 惰性删除 | 访问 key 时才检查是否过期 |
| 定时删除 | 为每个过期 key 创建定时器（不常用） |

### 淘汰策略

```redis
# redis.conf
maxmemory 4gb
maxmemory-policy allkeys-lru
```

| 策略 | 说明 |
|------|------|
| noeviction | 不淘汰，写入返回错误 |
| allkeys-lru | 对所有 key 使用 LRU |
| allkeys-lfu | 对所有 key 使用 LFU |
| volatile-lru | 对过期集合中的 key 使用 LRU |
| volatile-lfu | 对过期集合中的 key 使用 LFU |
| volatile-ttl | 淘汰即将过期的 key |
| volatile-random | 随机淘汰过期集合中的 key |
| allkeys-random | 随机淘汰任意 key |

---

## 八、Lua 脚本

```lua
-- 扣减库存脚本
local key = KEYS[1]
local qty = tonumber(ARGV[1])

local stock = redis.call('GET', key)
if not stock then
    return -1  -- 不存在
end

if tonumber(stock) < qty then
    return 0   -- 库存不足
end

redis.call('DECRBY', key, qty)
return 1       -- 成功
```

```redis
EVAL "script" 1 stock:product:1001 2
EVALSHA <sha1> 1 stock:product:1001 2  -- 缓存脚本后使用 SHA 调用
SCRIPT LOAD "script"                    -- 加载脚本，返回 SHA
SCRIPT EXISTS <sha1>
SCRIPT FLUSH
```

## 九、性能优化

```ini
# redis.conf 性能优化参数

# 网络
tcp-backlog 511
timeout 300
tcp-keepalive 300

# 内存
maxmemory 4gb
maxmemory-policy allkeys-lru
activedefrag yes                       # 主动碎片整理

# 持久化
save ""                                # 从库关闭持久化
stop-writes-on-bgsave-error no

# 慢查询
slowlog-log-slower-than 10000          # 微秒
slowlog-max-len 128

# 连接
maxclients 10000
```

### 监控命令

```redis
INFO                     # 全面信息
INFO memory              # 内存使用
INFO stats               # 统计信息
INFO commandstats        # 命令执行统计
SLOWLOG GET 10           # 最近10条慢查询
CLIENT LIST              # 客户端列表
MONITOR                  # 实时监控（生产慎用）
```

### 性能建议

| 建议 | 说明 |
|------|------|
| pipeline | 批量操作减少 RTT |
| 连接池 | 复用连接，避免频繁创建 |
| 大 key 拆分 | 单个 string 不超过 10KB，Hash 不超过 1000 字段 |
| 合理过期时间 | 避免大量 key 同时过期 |
| 从库持久化 | 主库关闭持久化提高性能，从库开启 |
| 禁用危险命令 | `rename-command FLUSHALL ""` |

## 相关条目

- [[NoSQL]]
- [[Optimization]]
- [[MongoDB_Deep]]
- [[分布式数据库与NewSQL]]
- [[Transaction]]
