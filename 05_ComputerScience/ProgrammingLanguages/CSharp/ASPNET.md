---
aliases: [ASPNET]
tags: ['ProgrammingLanguages', 'CSharp', 'ASPNET']
created: 2026-05-16
updated: 2026-05-16
---

# ASP.NET Core 指南

## Program.cs 与 Startup 配置

### 最小 API 风格（.NET 6+）

```csharp
var builder = WebApplication.CreateBuilder(args);

// 注册服务
builder.Services.AddControllers();
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options => {
        options.TokenValidationParameters = new TokenValidationParameters {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!))
        };
    });

var app = builder.Build();

// 中间件管道
if (app.Environment.IsDevelopment()) {
    app.UseDeveloperExceptionPage();
}

app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

### 传统方式（Startup 类）

```csharp
public class Program {
    public static void Main(string[] args) {
        CreateHostBuilder(args).Build().Run();
    }

    public static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .ConfigureWebHostDefaults(webBuilder => {
                webBuilder.UseStartup<Startup>();
            });
}

public class Startup {
    public IConfiguration Configuration { get; }

    public Startup(IConfiguration configuration) {
        Configuration = configuration;
    }

    public void ConfigureServices(IServiceCollection services) {
        services.AddControllers();
        services.AddSwaggerGen();
    }

    public void Configure(IApplicationBuilder app, IWebHostEnvironment env) {
        if (env.IsDevelopment()) {
            app.UseDeveloperExceptionPage();
            app.UseSwagger();
            app.UseSwaggerUI();
        }

        app.UseHttpsRedirection();
        app.UseRouting();
        app.UseAuthorization();

        app.UseEndpoints(endpoints => {
            endpoints.MapControllers();
        });
    }
}
```

## 中间件管道

```
请求进入
    │
    ▼
UseExceptionHandler / UseDeveloperExceptionPage
    │
    ▼
UseHttpsRedirection
    │
    ▼
UseStaticFiles
    │
    ▼
UseRouting
    │
    ▼
UseAuthentication
    │
    ▼
UseAuthorization
    │
    ▼
UseEndpoints → Controller Action
    │
    ▼
响应返回
```

### 自定义中间件

```csharp
// 方式一：显式中间件类
public class RequestLoggingMiddleware {
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(RequestDelegate next, ILogger<RequestLoggingMiddleware> logger) {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context) {
        var sw = Stopwatch.StartNew();

        _logger.LogInformation("请求开始: {Method} {Path}",
            context.Request.Method, context.Request.Path);

        await _next(context);

        sw.Stop();
        _logger.LogInformation("请求结束: {StatusCode} {Elapsed}ms",
            context.Response.StatusCode, sw.ElapsedMilliseconds);
    }
}

// 注册
app.UseMiddleware<RequestLoggingMiddleware>();

// 方式二：内联中间件
app.Use(async (context, next) => {
    Console.WriteLine($"请求: {context.Request.Path}");
    await next();
    Console.WriteLine($"响应: {context.Response.StatusCode}");
});
```

## 路由

```csharp
// 传统路由
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

// 属性路由
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase {
    [HttpGet]
    public IActionResult GetAll() { }

    [HttpGet("{id:int}")]
    public IActionResult GetById(int id) { }

    [HttpPost]
    public IActionResult Create([FromBody] Product product) { }

    [HttpPut("{id}")]
    public IActionResult Update(int id, [FromBody] Product product) { }

    [HttpDelete("{id}")]
    public IActionResult Delete(int id) { }
}
```

## 依赖注入

### 服务生命周期

| 生命周期 | 实例 | 适用场景 |
|---------|------|---------|
| AddSingleton | 全局唯一 | 配置、日志、缓存 |
| AddScoped | 每个请求/连接 | DbContext、请求上下文 |
| AddTransient | 每次注入时创建 | 轻量无状态服务 |

```csharp
// 注册
builder.Services.AddSingleton<ICacheService, MemoryCacheService>();
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddTransient<IEmailService, EmailService>();

// 工厂模式注册
builder.Services.AddScoped<IService>(sp => {
    var config = sp.GetRequiredService<IConfiguration>();
    return new Service(config["ServiceUrl"]);
});

// 装饰器
builder.Services.Decorate<IUserService, CachedUserService>();
```

## Entity Framework Core

```csharp
public class AppDbContext : DbContext {
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();

    protected override void OnModelCreating(ModelBuilder modelBuilder) {
        // 配置
        modelBuilder.Entity<Product>(entity => {
            entity.ToTable("Products");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).HasMaxLength(200).IsRequired();
            entity.Property(e => e.Price).HasColumnType("decimal(18,2)");
            entity.HasOne(e => e.Category)
                  .WithMany(c => c.Products)
                  .HasForeignKey(e => e.CategoryId);
        });
    }
}

// 迁移命令
// dotnet ef migrations add InitialCreate
// dotnet ef database update

// 高级查询
public async Task<List<Product>> SearchProductsAsync(
    string? name,
    decimal? minPrice,
    decimal? maxPrice,
    int? categoryId,
    int page = 1,
    int pageSize = 20) {
    var query = _context.Products.AsQueryable();

    if (!string.IsNullOrEmpty(name))
        query = query.Where(p => p.Name.Contains(name));

    if (minPrice.HasValue)
        query = query.Where(p => p.Price >= minPrice);

    if (maxPrice.HasValue)
        query = query.Where(p => p.Price <= maxPrice);

    if (categoryId.HasValue)
        query = query.Where(p => p.CategoryId == categoryId);

    return await query
        .OrderBy(p => p.Name)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync();
}

// 事务
using var transaction = await _context.Database.BeginTransactionAsync();
try {
    _context.Orders.Add(order);
    _context.SaveChanges();

    await transaction.CommitAsync();
} catch {
    await transaction.RollbackAsync();
    throw;
}
```

## 认证与授权

### JWT 认证

```csharp
// 登录端点
[AllowAnonymous]
[HttpPost("login")]
public async Task<IActionResult> Login([FromBody] LoginRequest request) {
    var user = await _userService.AuthenticateAsync(request.Username, request.Password);
    if (user == null)
        return Unauthorized();

    var token = GenerateJwtToken(user);
    return Ok(new { token });
}

private string GenerateJwtToken(User user) {
    var claims = new[] {
        new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
        new Claim(ClaimTypes.Name, user.Username),
        new Claim(ClaimTypes.Role, user.Role)
    };

    var key = new SymmetricSecurityKey(
        Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]!));

    var token = new JwtSecurityToken(
        issuer: _configuration["Jwt:Issuer"],
        audience: _configuration["Jwt:Audience"],
        claims: claims,
        expires: DateTime.UtcNow.AddHours(2),
        signingCredentials: new SigningCredentials(key, SecurityAlgorithms.HmacSha256)
    );

    return new JwtSecurityTokenHandler().WriteToken(token);
}

// 授权策略
builder.Services.AddAuthorization(options => {
    options.AddPolicy("RequireAdmin", policy =>
        policy.RequireRole("Admin"));

    options.AddPolicy("Over18", policy =>
        policy.RequireAssertion(context =>
            context.User.HasClaim(c =>
                c.Type == "Age" && int.Parse(c.Value) >= 18)));
});

[Authorize(Policy = "Over18")]
[HttpPost("purchase")]
public IActionResult Purchase() { }
```

## Minimal APIs（.NET 6+）

```csharp
var app = builder.Build();

// 简化路由
app.MapGet("/api/products", async (AppDbContext db) =>
    await db.Products.ToListAsync());

app.MapGet("/api/products/{id:int}", async (int id, AppDbContext db) =>
    await db.Products.FindAsync(id) is Product product
        ? Results.Ok(product)
        : Results.NotFound());

app.MapPost("/api/products", async (Product product, AppDbContext db) => {
    db.Products.Add(product);
    await db.SaveChangesAsync();
    return Results.Created($"/api/products/{product.Id}", product);
});

// 依赖注入
app.MapGet("/api/orders", async (
    IOrderService orderService,
    [FromQuery] int page = 1,
    [FromQuery] int size = 20) => {
    return await orderService.GetOrdersAsync(page, size);
});

// 分组路由
var api = app.MapGroup("/api/v1");
api.MapGet("/items", GetAllItems);
api.MapPost("/items", CreateItem);
```

## Blazor 基础

### 组件

```razor
@* Components/Counter.razor *@
@page "/counter"

<PageTitle>计数器</PageTitle>

<h1>计数: @currentCount</h1>

<button @onclick="IncrementCount">+1</button>

@code {
    private int currentCount = 0;

    [Parameter]
    public int IncrementAmount { get; set; } = 1;

    private void IncrementCount() {
        currentCount += IncrementAmount;
    }
}
```

### 数据绑定

```razor
<input @bind="name" />
<p>Hello, @name!</p>

@code {
    private string name = "";
}
```

## 测试

```csharp
// 单元测试
[Fact]
public async Task GetProduct_ReturnsProduct_WhenExists() {
    // Arrange
    var product = new Product { Id = 1, Name = "Test" };
    var mockRepo = new Mock<IProductRepository>();
    mockRepo.Setup(r => r.GetByIdAsync(1)).ReturnsAsync(product);

    var controller = new ProductsController(mockRepo.Object);

    // Act
    var result = await controller.GetProduct(1);

    // Assert
    var okResult = Assert.IsType<OkObjectResult>(result);
    var returnValue = Assert.IsType<Product>(okResult.Value);
    Assert.Equal("Test", returnValue.Name);
}
```

