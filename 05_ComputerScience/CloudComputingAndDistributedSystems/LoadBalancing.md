---
aliases: [LoadBalancing, 负载均衡, L4负载均衡, L7负载均衡]
tags: ['05_ComputerScience', 'CloudComputing', 'LoadBalancing', 'DistributedSystems']
created: 2026-06-27
updated: 2026-06-27
---

# 负载均衡 (Load Balancing)

## 一、概述

负载均衡是将网络流量分发到多个服务器的技术，目的是提高系统可用性、可靠性和性能。它是高并发系统架构的核心组件。

### 1.1 负载均衡的作用

| 作用 | 描述 |
|------|------|
| **高可用** | 单点故障自动切换 |
| **水平扩展** | 增加服务器提升处理能力 |
| **会话保持** | 同一用户请求路由到同一服务器 |
| **健康检查** | 自动剔除故障节点 |

### 1.2 负载均衡层次

| 层次 | 协议 | 代表产品 | 特点 |
|------|------|---------|------|
| **L4（传输层）** | TCP/UDP | LVS, F5, NLB | 性能高，不解析应用层 |
| **L7（应用层）** | HTTP/HTTPS | Nginx, HAProxy, ALB | 功能丰富，可解析应用层 |

---

## 二、负载均衡算法

### 2.1 轮询 (Round Robin)

```python
class RoundRobinBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current = 0
    
    def get_server(self):
        server = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        return server

# 使用
balancer = RoundRobinBalancer(["server1", "server2", "server3"])
for _ in range(6):
    print(balancer.get_server())
# server1, server2, server3, server1, server2, server3
```

### 2.2 加权轮询 (Weighted Round Robin)

```python
class WeightedRoundRobinBalancer:
    def __init__(self, servers_weights):
        self.servers = []
        for server, weight in servers_weights:
            self.servers.extend([server] * weight)
        self.current = 0
    
    def get_server(self):
        server = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        return server

# 使用：server1权重3，server2权重1
balancer = WeightedRoundRobinBalancer([
    ("server1", 3),
    ("server2", 1)
])
```

### 2.3 最少连接 (Least Connections)

```python
class LeastConnectionsBalancer:
    def __init__(self, servers):
        self.connections = {server: 0 for server in servers}
    
    def get_server(self):
        return min(self.connections, key=self.connections.get)
    
    def add_connection(self, server):
        self.connections[server] += 1
    
    def remove_connection(self, server):
        self.connections[server] -= 1
```

### 2.4 加权最少连接 (Weighted Least Connections)

```python
class WeightedLeastConnectionsBalancer:
    def __init__(self, servers_weights):
        self.weights = {s: w for s, w in servers_weights}
        self.connections = {s: 0 for s, _ in servers_weights}
    
    def get_server(self):
        return min(
            self.connections,
            key=lambda s: self.connections[s] / self.weights[s]
        )
```

### 2.5 IP Hash

```python
import hashlib

class IPHashBalancer:
    def __init__(self, servers):
        self.servers = servers
    
    def get_server(self, client_ip):
        hash_value = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        return self.servers[hash_value % len(self.servers)]
```

### 2.6 一致性哈希 (Consistent Hashing)

```python
import hashlib
from bisect import bisect_right

class ConsistentHashBalancer:
    def __init__(self, servers, virtual_nodes=150):
        self.ring = {}
        self.sorted_keys = []
        
        for server in servers:
            for i in range(virtual_nodes):
                key = self._hash(f"{server}:{i}")
                self.ring[key] = server
                self.sorted_keys.append(key)
        
        self.sorted_keys.sort()
    
    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def get_server(self, client_key):
        if not self.ring:
            return None
        
        hash_value = self._hash(client_key)
        index = bisect_right(self.sorted_keys, hash_value)
        
        if index == len(self.sorted_keys):
            index = 0
        
        return self.ring[self.sorted_keys[index]]
    
    def add_server(self, server, virtual_nodes=150):
        for i in range(virtual_nodes):
            key = self._hash(f"{server}:{i}")
            self.ring[key] = server
            self.sorted_keys.append(key)
        self.sorted_keys.sort()
    
    def remove_server(self, server, virtual_nodes=150):
        for i in range(virtual_nodes):
            key = self._hash(f"{server}:{i}")
            del self.ring[key]
            self.sorted_keys.remove(key)
```

### 2.7 算法对比

| 算法 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **轮询** | 简单、公平 | 不考虑服务器性能 | 服务器性能相近 |
| **加权轮询** | 考虑服务器性能 | 权重静态配置 | 服务器性能不同 |
| **最少连接** | 动态负载均衡 | 需要维护连接数 | 长连接场景 |
| **IP Hash** | 会话保持 | 负载可能不均 | 需要会话保持 |
| **一致性哈希** | 节点增删影响小 | 实现复杂 | 分布式缓存 |

---

## 三、Nginx 负载均衡

### 3.1 基础配置

```nginx
# 定义后端服务器组
upstream backend {
    server 192.168.1.1:8080 weight=3;
    server 192.168.1.2:8080 weight=2;
    server 192.168.1.3:8080 weight=1;
    
    # 健康检查
    # server 192.168.1.4:8080 backup;  # 备用服务器
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 3.2 负载均衡算法配置

```nginx
# 轮询（默认）
upstream backend {
    server 192.168.1.1:8080;
    server 192.168.1.2:8080;
}

# 加权轮询
upstream backend {
    server 192.168.1.1:8080 weight=3;
    server 192.168.1.2:8080 weight=2;
}

# IP Hash
upstream backend {
    ip_hash;
    server 192.168.1.1:8080;
    server 192.168.1.2:8080;
}

# 最少连接
upstream backend {
    least_conn;
    server 192.168.1.1:8080;
    server 192.168.1.2:8080;
}

# 响应时间（Fair，需第三方模块）
upstream backend {
    fair;
    server 192.168.1.1:8080;
    server 192.168.1.2:8080;
}
```

### 3.3 健康检查

```nginx
upstream backend {
    server 192.168.1.1:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.2:8080 max_fails=3 fail_timeout=30s;
    
    # 连接超时
    keepalive 32;
}

server {
    location / {
        proxy_pass http://backend;
        proxy_connect_timeout 5s;
        proxy_read_timeout 60s;
        proxy_send_timeout 60s;
        
        # 重试机制
        proxy_next_upstream error timeout http_500 http_502 http_503;
        proxy_next_upstream_tries 3;
    }
}
```

### 3.4 会话保持

```nginx
# 基于 Cookie 的会话保持
upstream backend {
    ip_hash;
    server 192.168.1.1:8080;
    server 192.168.1.2:8080;
}

# 基于 Cookie 的粘性会话（Nginx Plus）
upstream backend {
    sticky cookie srv_id expires=1h domain=.example.com path=/;
    server 192.168.1.1:8080;
    server 192.168.1.2:8080;
}
```

---

## 四、HAProxy 负载均衡

### 4.1 基础配置

```haproxy
global
    maxconn 50000
    log /dev/log local0

defaults
    mode http
    timeout connect 5s
    timeout client 30s
    timeout server 30s
    option httplog
    option dontlognull

frontend http_front
    bind *:80
    default_backend http_back

backend http_back
    balance roundrobin
    server server1 192.168.1.1:8080 check weight 3
    server server2 192.168.1.2:8080 check weight 2
    server server3 192.168.1.3:8080 check weight 1 backup
```

### 4.2 健康检查

```haproxy
backend http_back
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    
    server server1 192.168.1.1:8080 check inter 5s fall 3 rise 2
    server server2 192.168.1.2:8080 check inter 5s fall 3 rise 2
```

### 4.3 ACL 规则

```haproxy
frontend http_front
    bind *:80
    
    # 基于路径的路由
    acl is_api path_beg /api
    use_backend api_back if is_api
    
    # 基于域名的路由
    acl is_blog hdr(host) -i blog.example.com
    use_backend blog_back if is_blog
    
    default_backend web_back

backend api_back
    balance leastconn
    server api1 192.168.2.1:8080 check
    server api2 192.168.2.2:8080 check

backend web_back
    balance roundrobin
    server web1 192.168.3.1:80 check
    server web2 192.168.3.2:80 check
```

---

## 五、DNS 负载均衡

### 5.1 DNS 轮询

```bash
# DNS 配置示例
example.com.    IN    A    192.168.1.1
example.com.    IN    A    192.168.1.2
example.com.    IN    A    192.168.1.3
```

### 5.2 GeoDNS

```python
# 基于地理位置的 DNS 解析
def geo_dns_resolve(client_ip, domain):
    # 获取客户端地理位置
    location = get_geo_location(client_ip)
    
    # 根据位置返回最近的服务器
    if location.region == "asia":
        return "asia.example.com"
    elif location.region == "europe":
        return "eu.example.com"
    else:
        return "us.example.com"
```

### 5.3 DNS 优缺点

| 优点 | 缺点 |
|------|------|
| 简单易实现 | TTL 缓存导致切换慢 |
| 无需额外设备 | 健康检查困难 |
| 成本低 | 客户端缓存问题 |

---

## 六、服务网格负载均衡

### 6.1 Istio 负载均衡配置

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: my-service
spec:
  host: my-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: DEFAULT
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
    loadBalancer:
      simple: LEAST_CONN  # ROUND_ROBIN, LEAST_CONN, RANDOM
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

### 6.2 Envoy 代理配置

```yaml
static_resources:
  clusters:
  - name: backend_cluster
    type: EDS
    lb_policy: LEAST_REQUEST
    health_checks:
    - timeout: 1s
      interval: 5s
      unhealthy_threshold: 3
      healthy_threshold: 2
      http_health_check:
        path: "/health"
    circuit_breakers:
      thresholds:
      - max_connections: 100
        max_pending_requests: 100
        max_requests: 1000
```

---

## 七、负载均衡最佳实践

### 7.1 会话保持策略

| 策略 | 实现方式 | 适用场景 |
|------|---------|---------|
| **IP Hash** | 负载均衡器 | 简单场景 |
| **Cookie** | 应用层 | Web 应用 |
| **Token** | 应用层 | API 服务 |
| **Session Store** | Redis/Memcached | 分布式系统 |

### 7.2 健康检查策略

| 检查类型 | 方法 | 频率 |
|---------|------|------|
| **TCP 检查** | 建立连接 | 5-10秒 |
| **HTTP 检查** | GET /health | 5-10秒 |
| **应用检查** | 自定义端点 | 10-30秒 |

### 7.3 故障转移策略

```python
class FailoverBalancer:
    def __init__(self, primary, backup):
        self.primary = primary
        self.backup = backup
        self.primary_failed = False
    
    def get_server(self):
        if self.primary_failed:
            return self.backup
        return self.primary
    
    def mark_primary_failed(self):
        self.primary_failed = True
    
    def mark_primary_healthy(self):
        self.primary_failed = False
```

---

## 相关条目

- [[CloudComputingAndDistributedSystems]]
- [[Nginx]]
- [[05_ComputerScience/SoftwareEngineering/DevOpsAndCICD/K8s|K8s]]
- [[05_ComputerScience/Cybersecurity/NetworkSecurity|NetworkSecurity]]

## 参考资源

1. Nginx. "Load Balancing Documentation." nginx.org
2. HAProxy. "Configuration Manual." haproxy.org
3. Istio. "Traffic Management." istio.io
4. AWS. "Elastic Load Balancing." aws.amazon.com

