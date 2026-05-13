# Go HTTP 编程

## net/http 客户端

```go
package main

import (
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "time"
)

// 基本 GET 请求
func basicGet() {
    resp, err := http.Get("https://api.github.com/users/golang")
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    body, _ := io.ReadAll(resp.Body)
    fmt.Println(string(body))
}

// http.Client 自定义
func customClient() {
    client := &http.Client{
        Timeout: 30 * time.Second,
        Transport: &http.Transport{
            MaxIdleConns:        100,
            IdleConnTimeout:     90 * time.Second,
            TLSHandshakeTimeout: 10 * time.Second,
        },
    }

    resp, err := client.Get("https://api.example.com/data")
    if err != nil {
        return
    }
    defer resp.Body.Close()
}

// POST 请求
func postJSON() {
    data := map[string]interface{}{
        "name":  "Alice",
        "email": "alice@example.com",
    }
    jsonData, _ := json.Marshal(data)

    resp, err := http.Post(
        "https://api.example.com/users",
        "application/json",
        bytes.NewBuffer(jsonData),
    )
    if err != nil {
        return
    }
    defer resp.Body.Close()
}

// 带 Context 的请求
func requestWithContext() {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    req, _ := http.NewRequestWithContext(ctx, "GET", "https://api.example.com", nil)
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return
    }
    defer resp.Body.Close()
}

// 处理响应状态码
func checkStatus() {
    resp, _ := http.Get("https://api.example.com")
    defer resp.Body.Close()

    switch {
    case resp.StatusCode >= 200 && resp.StatusCode < 300:
        fmt.Println("成功")
    case resp.StatusCode >= 400 && resp.StatusCode < 500:
        fmt.Println("客户端错误")
    case resp.StatusCode >= 500:
        fmt.Println("服务端错误")
    }
}
```

## net/http 服务端

```go
// 基本 Handler
func helloHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, %s!", r.URL.Path[1:])
}

func main() {
    http.HandleFunc("/hello", helloHandler)
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("Home"))
    })

    // 自定义 Server
    server := &http.Server{
        Addr:         ":8080",
        ReadTimeout:  10 * time.Second,
        WriteTimeout: 10 * time.Second,
    }
    log.Fatal(server.ListenAndServe())
}

// 自定义 Handler 类型
type apiHandler struct{}

func (h *apiHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

func main() {
    mux := http.NewServeMux()
    mux.Handle("/api/", &apiHandler{})
    mux.HandleFunc("/health", healthCheck)

    log.Fatal(http.ListenAndServe(":8080", mux))
}

// 读取请求
func requestHandler(w http.ResponseWriter, r *http.Request) {
    // 查询参数
    name := r.URL.Query().Get("name")

    // 路径参数（需要手动解析）
    // /users/123
    parts := strings.Split(r.URL.Path, "/")
    id := parts[len(parts)-1]

    // 请求头
    auth := r.Header.Get("Authorization")

    // 请求体
    body, _ := io.ReadAll(r.Body)
    defer r.Body.Close()

    // JSON 解码
    var user User
    json.NewDecoder(r.Body).Decode(&user)
}

// 设置响应
func responseHandler(w http.ResponseWriter, r *http.Request) {
    // 状态码
    w.WriteHeader(http.StatusCreated)

    // 响应头
    w.Header().Set("Content-Type", "application/json; charset=utf-8")
    w.Header().Set("X-Request-ID", "12345")

    // 写入响应体
    json.NewEncoder(w).Encode(map[string]interface{}{
        "message": "success",
        "code":    200,
    })
}

// Middleware 模式
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
    })
}

func authMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if token != "Bearer valid-token" {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }
        next.ServeHTTP(w, r)
    })
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/api/data", dataHandler)

    // 链式 middleware
    handler := loggingMiddleware(authMiddleware(mux))
    http.ListenAndServe(":8080", handler)
}

// JSON 编码/解码 Helper
func writeJSON(w http.ResponseWriter, status int, data interface{}) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(data)
}

func readJSON(r *http.Request, v interface{}) error {
    decoder := json.NewDecoder(r.Body)
    decoder.DisallowUnknownFields()  // 拒绝未知字段
    return decoder.Decode(v)
}
```

## 流行框架

```go
// Gin
func main() {
    r := gin.Default()

    r.GET("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "pong",
        })
    })

    r.GET("/users/:id", func(c *gin.Context) {
        id := c.Param("id")
        name := c.Query("name")
        c.JSON(200, gin.H{"id": id, "name": name})
    })

    r.POST("/users", func(c *gin.Context) {
        var user User
        if err := c.ShouldBindJSON(&user); err != nil {
            c.JSON(400, gin.H{"error": err.Error()})
            return
        }
        c.JSON(201, user)
    })

    // 路由组
    api := r.Group("/api")
    {
        api.GET("/products", getProducts)
        api.POST("/products", createProduct)
    }

    r.Run(":8080")
}

// Echo
func main() {
    e := echo.New()
    e.Use(middleware.Logger())
    e.Use(middleware.Recover())

    e.GET("/", func(c echo.Context) error {
        return c.String(http.StatusOK, "Hello, Echo!")
    })

    e.GET("/users/:id", getUser)
    e.POST("/users", createUser)

    // 分组
    g := e.Group("/admin")
    g.Use(middleware.BasicAuth(func(username, password string, c echo.Context) (bool, error) {
        return username == "admin" && password == "secret", nil
    }))

    e.Start(":8080")
}

// Fiber
func main() {
    app := fiber.New()

    app.Get("/", func(c *fiber.Ctx) error {
        return c.SendString("Hello, Fiber!")
    })

    app.Get("/users/:id", func(c *fiber.Ctx) error {
        id := c.Params("id")
        return c.JSON(fiber.Map{"id": id})
    })

    app.Post("/users", func(c *fiber.Ctx) error {
        user := new(User)
        if err := c.BodyParser(user); err != nil {
            return c.Status(400).JSON(fiber.Map{"error": err.Error()})
        }
        return c.Status(201).JSON(user)
    })

    app.Listen(":8080")
}
```

## REST API 设计

```go
// 资源命名
// GET    /users          - 获取用户列表
// POST   /users          - 创建用户
// GET    /users/:id      - 获取单个用户
// PUT    /users/:id      - 更新用户（全量）
// PATCH  /users/:id      - 更新用户（部分）
// DELETE /users/:id      - 删除用户
// GET    /users/:id/posts - 获取用户帖子

type UserResponse struct {
    ID        uint      `json:"id"`
    Name      string    `json:"name"`
    Email     string    `json:"email"`
    CreatedAt time.Time `json:"created_at"`
}

type CreateUserRequest struct {
    Name     string `json:"name" binding:"required"`
    Email    string `json:"email" binding:"required,email"`
    Password string `json:"password" binding:"required,min=8"`
}
```

## 测试 HTTP Handler

```go
func TestHelloHandler(t *testing.T) {
    // 创建请求
    req := httptest.NewRequest("GET", "/hello", nil)
    w := httptest.NewRecorder()

    // 调用 handler
    helloHandler(w, req)

    // 验证响应
    resp := w.Result()
    body, _ := io.ReadAll(resp.Body)

    if resp.StatusCode != http.StatusOK {
        t.Errorf("预期状态 200，得到 %d", resp.StatusCode)
    }
    if string(body) != "expected body" {
        t.Errorf("预期 'expected body'，得到 '%s'", string(body))
    }
}

// 表格驱动测试
func TestHandlers(t *testing.T) {
    tests := []struct {
        name       string
        method     string
        path       string
        body       io.Reader
        wantStatus int
    }{
        {"GET /users", "GET", "/users", nil, 200},
        {"POST /users", "POST", "/users", bytes.NewBuffer([]byte(`{"name":"test"}`)), 201},
        {"GET /users/invalid", "GET", "/users/invalid", nil, 400},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest(tt.method, tt.path, tt.body)
            w := httptest.NewRecorder()
            // router.ServeHTTP(w, req)
            if w.Code != tt.wantStatus {
                t.Errorf("状态: 得到 %d, 预期 %d", w.Code, tt.wantStatus)
            }
        })
    }
}
```
