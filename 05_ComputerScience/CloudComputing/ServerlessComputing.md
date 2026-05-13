# 无服务器计算

> 无服务器计算（Serverless）是一种云执行模型，云提供商动态管理资源分配，开发者只需关注代码。

## 核心概念

- **函数即服务（FaaS）**：事件驱动的函数执行
- **后端即服务（BaaS）**：使用第三方后端服务（数据库、认证）
- **按需付费**：仅在代码执行时计费
- **自动扩缩**：从零到无限，无需手动配置

## 平台对比

| 平台 | 运行时支持 | 触发方式 |
|------|-----------|---------|
| AWS Lambda | Node.js, Python, Java, Go, .NET | API Gateway, S3, SQS, DynamoDB Streams |
| Azure Functions | C#, Java, JavaScript, Python | HTTP, Timer, Blob, Queue |
| Google Cloud Functions | Node.js, Python, Go | HTTP, Cloud Pub/Sub, Cloud Storage |
| 阿里云函数计算 | Node.js, Python, Java, PHP | HTTP, OSS, Log, Timer |

## 使用场景

- **Web API**：结合 API Gateway 构建 REST API
- **数据处理**：图片/视频转码、ETL 管道
- **定时任务**：定时备份、报表生成
- **事件响应**：文件上传触发处理流程
- **聊天机器人**：消息驱动的无状态处理

## 优缺点

| 优势 | 挑战 |
|------|------|
| 无需管理服务器 | 冷启动延迟 |
| 自动扩缩容 | 执行时间限制 |
| 按使用量付费 | 调试和监控复杂 |
| 提高开发效率 | 供应商锁定风险 |
