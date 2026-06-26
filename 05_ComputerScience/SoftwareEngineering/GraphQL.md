---
aliases: [GraphQL, GraphQL查询, Apollo]
tags: ['05_ComputerScience', 'SoftwareEngineering', 'GraphQL', 'API']
created: 2026-06-27
updated: 2026-06-27
---

# GraphQL

## 一、概述

GraphQL 是一种用于 API 的查询语言，允许客户端精确指定需要的数据。相比 REST，GraphQL 避免了过度获取和不足获取的问题。

### 1.1 GraphQL vs REST

| 特性 | REST | GraphQL |
|------|------|---------|
| 端点 | 多个端点 | 单一端点 |
| 数据获取 | 固定结构 | 按需获取 |
| 版本控制 | URL 版本 | Schema 演进 |
| 过度获取 | 常见 | 避免 |
| 不足获取 | 常见 | 避免 |

---

## 二、Schema 定义

### 2.1 类型系统

```graphql
# 自定义类型
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
  tags: [String!]!
}

type Comment {
  id: ID!
  content: String!
  author: User!
  createdAt: DateTime!
}

# 查询类型
type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  post(id: ID!): Post
  posts(tag: String): [Post!]!
}

# 变更类型
type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
  
  createPost(input: CreatePostInput!): Post!
  updatePost(id: ID!, input: UpdatePostInput!): Post!
  deletePost(id: ID!): Boolean!
}

# 订阅类型
type Subscription {
  postCreated: Post!
  commentAdded(postId: ID!): Comment!
}

# 输入类型
input CreateUserInput {
  name: String!
  email: String!
}

input UpdateUserInput {
  name: String
  email: String
}

input CreatePostInput {
  title: String!
  content: String!
  tags: [String!]
}
```

### 2.2 枚举类型

```graphql
enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

enum SortOrder {
  ASC
  DESC
}

type Query {
  postsByStatus(status: PostStatus!, order: SortOrder): [Post!]!
}
```

### 2.3 接口和联合类型

```graphql
# 接口
interface Node {
  id: ID!
}

type User implements Node {
  id: ID!
  name: String!
}

type Post implements Node {
  id: ID!
  title: String!
}

# 联合类型
union SearchResult = User | Post | Comment

type Query {
  search(query: String!): [SearchResult!]!
}
```

---

## 三、Resolver 实现

### 3.1 Python Resolver (Strawberry)

```python
import strawberry
from typing import List, Optional
from datetime import datetime

@strawberry.type
class User:
    id: str
    name: str
    email: str
    created_at: datetime
    
    @strawberry.field
    async def posts(self) -> List["Post"]:
        return await PostRepository.get_by_author(self.id)

@strawberry.type
class Post:
    id: str
    title: str
    content: str
    author: User
    
    @strawberry.field
    async def comments(self) -> List["Comment"]:
        return await CommentRepository.get_by_post(self.id)

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: str) -> Optional[User]:
        return await UserRepository.get_by_id(id)
    
    @strawberry.field
    async def users(self, limit: int = 10, offset: int = 0) -> List[User]:
        return await UserRepository.get_all(limit, offset)
    
    @strawberry.field
    async def posts(self, tag: Optional[str] = None) -> List[Post]:
        if tag:
            return await PostRepository.get_by_tag(tag)
        return await PostRepository.get_all()

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, name: str, email: str) -> User:
        return await UserRepository.create(name=name, email=email)
    
    @strawberry.mutation
    async def create_post(self, title: str, content: str, tags: List[str] = []) -> Post:
        return await PostRepository.create(title=title, content=content, tags=tags)

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

### 3.2 JavaScript Resolver (Apollo Server)

```javascript
const resolvers = {
  Query: {
    user: async (_, { id }, context) => {
      return await context.dataSources.userAPI.getById(id);
    },
    users: async (_, { limit, offset }, context) => {
      return await context.dataSources.userAPI.getAll(limit, offset);
    },
    posts: async (_, { tag }, context) => {
      if (tag) {
        return await context.dataSources.postAPI.getByTag(tag);
      }
      return await context.dataSources.postAPI.getAll();
    }
  },
  
  Mutation: {
    createUser: async (_, { input }, context) => {
      return await context.dataSources.userAPI.create(input);
    },
    createPost: async (_, { input }, context) => {
      return await context.dataSources.postAPI.create(input);
    }
  },
  
  User: {
    posts: async (parent, _, context) => {
      return await context.dataSources.postAPI.getByAuthor(parent.id);
    }
  },
  
  Post: {
    author: async (parent, _, context) => {
      return await context.dataSources.userAPI.getById(parent.authorId);
    },
    comments: async (parent, _, context) => {
      return await context.dataSources.commentAPI.getByPost(parent.id);
    }
  }
};
```

---

## 四、查询示例

### 4.1 基础查询

```graphql
# 精确获取需要的字段
query GetUser {
  user(id: "1") {
    name
    email
  }
}

# 嵌套查询
query GetUserWithPosts {
  user(id: "1") {
    name
    posts {
      title
      comments {
        content
        author {
          name
        }
      }
    }
  }
}
```

### 4.2 参数和变量

```graphql
# 使用变量
query GetPosts($tag: String, $limit: Int) {
  posts(tag: $tag, limit: $limit) {
    title
    content
  }
}

# 变量
{
  "tag": "graphql",
  "limit": 10
}
```

### 4.3 片段

```graphql
# 定义片段
fragment UserFields on User {
  id
  name
  email
}

fragment PostFields on Post {
  id
  title
  content
  author {
    ...UserFields
  }
}

# 使用片段
query GetPosts {
  posts {
    ...PostFields
  }
}
```

### 4.4 指令

```graphql
# 条件字段
query GetUser($includePosts: Boolean!) {
  user(id: "1") {
    name
    email
    posts @include(if: $includePosts) {
      title
    }
  }
}

# 跳过字段
query GetUser($skipEmail: Boolean!) {
  user(id: "1") {
    name
    email @skip(if: $skipEmail)
  }
}
```

---

## 五、变更操作

### 5.1 创建

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
  }
}

# 变量
{
  "input": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### 5.2 更新

```graphql
mutation UpdateUser($id: ID!, $input: UpdateUserInput!) {
  updateUser(id: $id, input: $input) {
    id
    name
    email
  }
}
```

### 5.3 删除

```graphql
mutation DeleteUser($id: ID!) {
  deleteUser(id: $id)
}
```

---

## 六、订阅

### 6.1 WebSocket 订阅

```graphql
subscription OnPostCreated {
  postCreated {
    id
    title
    content
    author {
      name
    }
  }
}

subscription OnCommentAdded($postId: ID!) {
  commentAdded(postId: $postId) {
    id
    content
    author {
      name
    }
  }
}
```

### 6.2 服务端实现

```python
import asyncio
from typing import AsyncGenerator

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def post_created(self) -> AsyncGenerator[Post, None]:
        async for post in PostEvent.subscribe():
            yield post
    
    @strawberry.subscription
    async def comment_added(self, post_id: str) -> AsyncGenerator[Comment, None]:
        async for comment in CommentEvent.subscribe(post_id):
            yield comment
```

---

## 七、错误处理

### 7.1 错误类型

```graphql
type UserError {
  field: String
  message: String!
}

type CreateUserResult {
  user: User
  errors: [UserError!]!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserResult!
}
```

### 7.2 错误处理实现

```python
@strawberry.type
class UserError:
    field: Optional[str]
    message: str

@strawberry.type
class CreateUserResult:
    user: Optional[User]
    errors: List[UserError]

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, input: CreateUserInput) -> CreateUserResult:
        errors = []
        
        if not input.name:
            errors.append(UserError(field="name", message="Name is required"))
        
        if not input.email:
            errors.append(UserError(field="email", message="Email is required"))
        elif await UserRepository.email_exists(input.email):
            errors.append(UserError(field="email", message="Email already exists"))
        
        if errors:
            return CreateUserResult(user=None, errors=errors)
        
        user = await UserRepository.create(input.name, input.email)
        return CreateUserResult(user=user, errors=[])
```

---

## 八、性能优化

### 8.1 DataLoader

```python
from strawberry.dataloader import DataLoader

async def load_users(user_ids: List[str]) -> List[User]:
    users = await UserRepository.get_by_ids(user_ids)
    user_map = {user.id: user for user in users}
    return [user_map.get(uid) for uid in user_ids]

user_loader = DataLoader(load_fn=load_users)

@strawberry.type
class Post:
    @strawberry.field
    async def author(self) -> User:
        return await user_loader.load(self.author_id)
```

### 8.2 查询复杂度分析

```python
from strawberry.extensions import QueryComplexityLimiter

schema = strawberry.Schema(
    query=Query,
    extensions=[
        QueryComplexityLimiter(max_complexity=1000)
    ]
)
```

### 8.3 响应缓存

```python
from strawberry.extensions import ResponseCache

schema = strawberry.Schema(
    query=Query,
    extensions=[
        ResponseCache(
            default_ttl=60,
            should_cache=lambda ctx, data: not ctx.get("errors")
        )
    ]
)
```

---

## 九、安全

### 9.1 认证

```python
from strawberry.permission import Permission
from strawberry.types import Info

class IsAuthenticated(Permission):
    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        return info.context.get("user") is not None

@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def me(self, info: Info) -> User:
        return info.context["user"]
```

### 9.2 限流

```python
from strawberry.extensions import RateLimiter

schema = strawberry.Schema(
    query=Query,
    extensions=[
        RateLimiter(
            default_limit=100,
            default_window=60
        )
    ]
)
```

---

## 相关条目

- [[Microservices]]
- [[HTTPAPI]]
- [[NetworkSecurity]]

## 参考资源

1. GraphQL. "Official Specification." graphql.org
2. Apollo. "Apollo Server Documentation." apollographql.com
3. Strawberry. "Strawberry GraphQL." strawberry-graphql.github.io
