---
aliases: [RedisDeep, Redis深度, Redis数据结构, Redis集群]
tags: ['05_ComputerScience', 'Databases', 'Redis', 'Cache']
created: 2026-06-27
updated: 2026-06-27
---

# Redis 深度指南 (Redis Deep Dive)

## 一、概述

Redis（Remote Dictionary Server）是一个开源的内存数据结构存储，可用作数据库、缓存和消息中间件。它支持多种数据结构，提供高性能的读写能力。

### 1.1 Redis 特性

| 特性 | 描述 |
|------|------|
| **高性能** | 读 110,000 次/秒，写 81,000 次/秒 |
| **数据结构丰富** | String、Hash、List、Set、Sorted Set 等 |
| **持久化** | RDB 快照 + AOF 日志 |
| **高可用** | 主从复制、哨兵、集群 |
| **原子性** | 单线程模型保证原子操作 |
| **Lua 脚本** | 支持服务端 Lua 脚本 |

---

## 二、数据结构

### 2.1 String（字符串）

```bash
# 基础操作
SET key value
GET key
DEL key

# 设置过期时间
SETEX key 60 value  # 60秒过期
SET key value EX 60

# 不存在时设置
SETNX key value

# 批量操作
MSET key1 value1 key2 value2
MGET key1 key2

# 计数器
INCR counter
INCRBY counter 10
DECR counter

# 追加
APPEND key "suffix"

# 位操作
SETBIT key 10 1
GETBIT key 10
BITCOUNT key
```

### 2.2 Hash（哈希表）

```bash
# 基础操作
HSET user:1 name "John" age 30
HGET user:1 name
HGETALL user:1

# 批量操作
HMSET user:1 name "John" age 30 email "john@example.com"
HMGET user:1 name age

# 字段操作
HDEL user:1 age
HEXISTS user:1 name
HLEN user:1

# 计数器
HINCRBY user:1 age 1

# 所有字段和值
HKEYS user:1
HVALS user:1
```

### 2.3 List（列表）

```bash
# 基础操作
LPUSH queue task1 task2
RPUSH queue task3
LPOP queue
RPOP queue

# 范围查询
LRANGE queue 0 -1  # 所有元素
LRANGE queue 0 9   # 前10个

# 阻塞操作
BLPOP queue 30  # 阻塞30秒
BRPOP queue 30

# 长度
LLEN queue

# 索引操作
LINDEX queue 0
LSET queue 0 "new_value"

# 裁剪
LTRIM queue 0 99  # 保留前100个
```

### 2.4 Set（集合）

```bash
# 基础操作
SADD tags python javascript
SMEMBERS tags
SISMEMBER tags python

# 集合运算
SADD tags1 python java
SADD tags2 python javascript
SINTER tags1 tags2    # 交集
SUNION tags1 tags2    # 并集
SDIFF tags1 tags2     # 差集

# 随机元素
SRANDMEMBER tags 2  # 随机2个
SPOP tags           # 随机弹出

# 大小
SCARD tags
```

### 2.5 Sorted Set（有序集合）

```bash
# 基础操作
ZADD leaderboard 100 "player1"
ZADD leaderboard 200 "player2"
ZADD leaderboard 150 "player3"

# 范围查询
ZRANGE leaderboard 0 -1 WITHSCORES
ZREVRANGE leaderboard 0 9 WITHSCORES  # 前10名

# 分数操作
ZSCORE leaderboard "player1"
ZINCRBY leaderboard 50 "player1"

# 排名
ZRANK leaderboard "player1"       # 升序排名
ZREVRANK leaderboard "player1"    # 降序排名

# 范围查询
ZRANGEBYSCORE leaderboard 100 200
ZCOUNT leaderboard 100 200

# 大小
ZCARD leaderboard
```

### 2.6 HyperLogLog

```bash
# 基数统计（近似）
PFADD unique_visitors "user1" "user2" "user3"
PFCOUNT unique_visitors
PFMERGE total_visitors unique_visitors1 unique_visitors2
```

### 2.7 Bitmap

```bash
# 用户签到
SETBIT sign:user1:2026-06 26 1  # 6月27日签到
GETBIT sign:user1:2026-06 26
BITCOUNT sign:user1:2026-06      # 本月签到天数
```

### 2.8 Geo

```bash
# 地理位置
GEOADD locations 116.4074 39.9042 "beijing"
GEOADD locations 121.4737 31.2304 "shanghai"

# 距离计算
GEODIST locations "beijing" "shanghai" km

# 附近位置
GEOSEARCH locations FROMLONLAT 116.4074 39.9042 BYRADIUS 100 km
```

### 2.9 Stream

```bash
# 添加消息
XADD mystream * name "John" age 30
XADD mystream * name "Jane" age 25

# 读取消息
XRANGE mystream - +
XREVRANGE mystream + -

# 消费者组
XGROUP CREATE mystream mygroup 0
XREADGROUP GROUP mygroup consumer1 COUNT 10 BLOCK 5000 STREAMS mystream >

# 确认消息
XACK mystream mygroup 1234567890
```

---

## 三、持久化

### 3.1 RDB 快照

```bash
# redis.conf 配置
save 900 1      # 900秒内至少1个key变化
save 300 10     # 300秒内至少10个key变化
save 60 10000   # 60秒内至少10000个key变化

# 手动触发
SAVE      # 同步保存（阻塞）
BGSAVE    # 后台保存（非阻塞）
```

**RDB 优缺点**：
| 优点 | 缺点 |
|------|------|
| 文件紧凑，适合备份 | 可能丢失最后一次快照后的数据 |
| 恢复速度快 | 大数据集保存时可能阻塞 |
| 对性能影响小 | fork 子进程消耗内存 |

### 3.2 AOF 日志

```bash
# redis.conf 配置
appendonly yes
appendfsync always     # 每次写入都同步
appendfsync everysec   # 每秒同步（推荐）
appendfsync no         # 由操作系统决定

# AOF 重写
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

**AOF 优缺点**：
| 优点 | 缺点 |
|------|------|
| 数据安全性高 | 文件体积大 |
| 可读性好 | 恢复速度慢 |
| 可以误操作 | 写入性能略低 |

### 3.3 混合持久化

```bash
# redis.conf 配置
aof-use-rdb-preamble yes
```

---

## 四、高可用

### 4.1 主从复制

```bash
# 从节点配置
replicaof 192.168.1.1 6379
masterauth "password"

# 查看复制信息
INFO replication
```

### 4.2 哨兵（Sentinel）

```bash
# sentinel.conf
sentinel monitor mymaster 192.168.1.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1

# 启动哨兵
redis-sentinel sentinel.conf
```

### 4.3 Redis Cluster

```bash
# 创建集群
redis-cli --cluster create 192.168.1.1:6379 192.168.1.2:6379 192.168.1.3:6379 \
    192.168.1.4:6379 192.168.1.5:6379 192.168.1.6:6379 \
    --cluster-replicas 1

# 集群信息
CLUSTER INFO
CLUSTER NODES

# 添加节点
redis-cli --cluster add-node 192.168.1.7:6379 192.168.1.1:6379

# 重新分片
redis-cli --cluster reshard 192.168.1.1:6379
```

---

## 五、Lua 脚本

### 5.1 基础使用

```bash
# 执行 Lua 脚本
EVAL "return redis.call('GET', KEYS[1])" 1 mykey

# 带参数
EVAL "return redis.call('SET', KEYS[1], ARGV[1])" 1 mykey myvalue

# 脚本缓存
SCRIPT LOAD "return redis.call('GET', KEYS[1])"
EVALSHA <sha1> 1 mykey
```

### 5.2 分布式锁

```bash
# 加锁脚本
EVAL "
    if redis.call('SET', KEYS[1], ARGV[1], 'NX', 'PX', ARGV[2]) then
        return 1
    else
        return 0
    end
" 1 lock_key unique_id 30000

# 解锁脚本
EVAL "
    if redis.call('GET', KEYS[1]) == ARGV[1] then
        return redis.call('DEL', KEYS[1])
    else
        return 0
    end
" 1 lock_key unique_id
```

### 5.3 限流器

```bash
# 滑动窗口限流
EVAL "
    local key = KEYS[1]
    local limit = tonumber(ARGV[1])
    local window = tonumber(ARGV[2])
    local now = tonumber(ARGV[3])
    
    -- 移除过期请求
    redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
    
    -- 统计当前请求数
    local count = redis.call('ZCARD', key)
    
    if count < limit then
        -- 添加当前请求
        redis.call('ZADD', key, now, now .. '-' .. math.random())
        redis.call('EXPIRE', key, window)
        return 1
    else
        return 0
    end
" 1 rate:api 100 60 1624857600
```

---

## 六、Redis 应用模式

### 6.1 缓存模式

```python
import redis
import json

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)
    
    def get(self, key):
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key, value, ttl=300):
        self.redis.setex(key, ttl, json.dumps(value))
    
    def delete(self, key):
        self.redis.delete(key)
    
    def get_or_set(self, key, factory, ttl=300):
        value = self.get(key)
        if value is None:
            value = factory()
            self.set(key, value, ttl)
        return value
```

### 6.2 分布式锁

```python
import redis
import uuid
import time

class DistributedLock:
    def __init__(self, redis_client, key, ttl=30):
        self.redis = redis_client
        self.key = f"lock:{key}"
        self.ttl = ttl
        self.token = str(uuid.uuid4())
    
    def acquire(self, timeout=10):
        start = time.time()
        while time.time() - start < timeout:
            if self.redis.set(self.key, self.token, nx=True, px=self.ttl * 1000):
                return True
            time.sleep(0.1)
        return False
    
    def release(self):
        script = """
        if redis.call('GET', KEYS[1]) == ARGV[1] then
            return redis.call('DEL', KEYS[1])
        else
            return 0
        end
        """
        self.redis.eval(script, 1, self.key, self.token)
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

# 使用
redis_client = redis.Redis()
with DistributedLock(redis_client, "my_resource"):
    # 临界区代码
    pass
```

### 6.3 限流器

```python
import redis
import time

class RedisRateLimiter:
    def __init__(self, redis_client, key, max_requests, window_seconds):
        self.redis = redis_client
        self.key = f"rate:{key}"
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    def allow(self):
        now = time.time()
        script = """
        local key = KEYS[1]
        local limit = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])
        
        redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
        local count = redis.call('ZCARD', key)
        
        if count < limit then
            redis.call('ZADD', key, now, now)
            redis.call('EXPIRE', key, window)
            return 1
        else
            return 0
        end
        """
        result = self.redis.eval(script, 1, self.key, self.max_requests, self.window_seconds, now)
        return result == 1
```

### 6.4 发布订阅

```python
import redis

class RedisPubSub:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.pubsub = self.redis.pubsub()
    
    def subscribe(self, channel, callback):
        self.pubsub.subscribe(channel)
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                callback(message['data'])
    
    def publish(self, channel, message):
        self.redis.publish(channel, message)

# 使用
redis_client = redis.Redis()
pubsub = RedisPubSub(redis_client)

# 订阅者
def handler(message):
    print(f"Received: {message}")

pubsub.subscribe("my_channel", handler)

# 发布者
pubsub.publish("my_channel", "Hello World")
```

---

## 七、Redis 性能优化

### 7.1 连接池

```python
import redis

pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=100,
    decode_responses=True
)

redis_client = redis.Redis(connection_pool=pool)
```

### 7.2 Pipeline

```python
pipe = redis_client.pipeline()

for i in range(10000):
    pipe.set(f"key:{i}", f"value:{i}")

pipe.execute()  # 批量执行
```

### 7.3 批量操作

```python
# MSET 比循环 SET 快
redis_client.mset({f"key:{i}": f"value:{i}" for i in range(1000)})

# MGET 比循环 GET 快
values = redis_client.mget([f"key:{i}" for i in range(1000)])
```

---

## 相关条目

- [[DatabasesAndInformationSystems]]
- [[MessageQueues]]
- [[HighConcurrencyDesign]]

## 参考资源

1. Redis. "Documentation." redis.io
2. Redis. "Redis University." university.redis.com
3. Carlson, J. "Redis in Action." Manning, 2013
