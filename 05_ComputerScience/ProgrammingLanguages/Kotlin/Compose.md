---
aliases: [Compose]
tags: ['ProgrammingLanguages', 'Kotlin', 'Compose']
created: 2026-05-16
updated: 2026-05-16
---

# Jetpack Compose 指南

## 可组合函数

```kotlin
@Composable
fun Greeting(name: String) {
    Text(text = "Hello, $name!")
}

@Composable
fun PreviewGreeting() {
    Greeting(name = "Compose")
}

// 预览
@Preview(showBackground = true)
@Composable
fun DefaultPreview() {
    MyTheme {
        Greeting("Android")
    }
}
```

## 状态管理

```kotlin
// remember + mutableStateOf
@Composable
fun Counter() {
    val count = remember { mutableIntStateOf(0) }
    Button(onClick = { count.intValue++ }) {
        Text("Clicked ${count.intValue} times")
    }
}

// StateFlow 收集
@Composable
fun UserScreen(viewModel: UserViewModel = viewModel()) {
    val users by viewModel.users.collectAsState()
    LazyColumn {
        items(users) { user ->
            Text(user.name)
        }
    }
}

// ViewModel 配合 Compose
class MyViewModel : ViewModel() {
    private val _state = MutableStateFlow("Initial")
    val state: StateFlow<String> = _state

    fun update() { _state.value = "Updated" }
}

@Composable
fun MyScreen(viewModel: MyViewModel = viewModel()) {
    val state by viewModel.state.collectAsState()
    Text(state)
    Button(onClick = { viewModel.update() }) {
        Text("Update")
    }
}

// 状态提升
@Composable
fun Parent() {
    var text by remember { mutableStateOf("") }
    Child(text = text, onTextChange = { text = it })
}

@Composable
fun Child(text: String, onTextChange: (String) -> Unit) {
    TextField(value = text, onValueChange = onTextChange)
}
```

## 布局

```kotlin
@Composable
fun LayoutDemo() {
    // Column: 垂直排列
    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Item 1")
        Text("Item 2")
    }

    // Row: 水平排列
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceEvenly
    ) {
        Text("Left")
        Text("Center")
        Text("Right")
    }

    // Box: 层级叠加
    Box(modifier = Modifier.size(200.dp)) {
        Text("Background", modifier = Modifier.align(Alignment.Center))
        Button(onClick = {}, modifier = Modifier.align(Alignment.BottomEnd)) {
            Text("OK")
        }
    }

    // LazyColumn: 可滚动列表
    LazyColumn {
        items(100) { index ->
            ListItem(index = index)
        }
        item { Header() }           // 单个 item
        itemsIndexed(list) { i, item -> /* ... */ }
    }

    // LazyGrid
    LazyVerticalGrid(
        columns = GridCells.Fixed(3),
        contentPadding = PaddingValues(8.dp)
    ) {
        items(images) { image ->
            ImageItem(image)
        }
    }

    // ConstraintLayout
    ComposeConstraintLayout(modifier = Modifier.fillMaxSize()) {
        val (button, text) = createRefs()
        Button(onClick = {}, modifier = Modifier.constrainAs(button) {
            bottom.linkTo(parent.bottom, margin = 16.dp)
            centerHorizontallyTo(parent)
        }) {
            Text("Click")
        }
        Text("Title", modifier = Modifier.constrainAs(text) {
            top.linkTo(parent.top)
            start.linkTo(parent.start)
            end.linkTo(parent.end)
        })
    }
}
```

## 修饰符

```kotlin
@Composable
fun ModifierDemo() {
    Text(
        text = "Styled Text",
        modifier = Modifier
            .padding(16.dp)                // 内边距
            .fillMaxWidth()                 // 填充最大宽度
            .height(48.dp)                  // 高度
            .background(Color.Blue)         // 背景色
            .clip(RoundedCornerShape(8.dp)) // 剪裁为圆角
            .clickable { /* onClick */ }    // 点击
            .border(2.dp, Color.Red)        // 边框
            .offset(x = 10.dp, y = 5.dp)   // 偏移
            .alpha(0.8f)                    // 透明度
            .rotate(45f)                    // 旋转
            .scale(1.2f)                    // 缩放
    )
}
```

## 主题

```kotlin
// MaterialTheme
@Composable
fun MyTheme(content: @Composable () -> Unit) {
    val colors = lightColorScheme(
        primary = Color(0xFF6200EE),
        secondary = Color(0xFF03DAC6),
        background = Color.White,
        surface = Color.White,
        onPrimary = Color.White,
        onSecondary = Color.Black,
    )
    MaterialTheme(
        colors = colors,
        typography = Typography(
            headlineLarge = TextStyle(
                fontSize = 28.sp,
                fontWeight = FontWeight.Bold
            ),
            bodyLarge = TextStyle(
                fontSize = 16.sp,
                lineHeight = 24.sp
            )
        ),
        shapes = Shapes(
            small = RoundedCornerShape(4.dp),
            medium = RoundedCornerShape(8.dp),
            large = RoundedCornerShape(16.dp)
        ),
        content = content
    )
}

// 使用主题
@Composable
fun ThemedScreen() {
    MyTheme {
        Surface(
            color = MaterialTheme.colorScheme.background
        ) {
            Text(
                text = "Themed Text",
                style = MaterialTheme.typography.headlineLarge,
                color = MaterialTheme.colorScheme.primary
            )
        }
    }
}
```

## Compose 导航

```kotlin
// build.gradle: implementation("androidx.navigation:navigation-compose:2.7.7")

@Composable
fun AppNavHost() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            HomeScreen(
                onNavigateToDetail = { id ->
                    navController.navigate("detail/$id")
                }
            )
        }
        composable(
            route = "detail/{itemId}",
            arguments = listOf(navArgument("itemId") { type = NavType.IntType })
        ) { backStackEntry ->
            val itemId = backStackEntry.arguments?.getInt("itemId") ?: 0
            DetailScreen(itemId = itemId, onBack = { navController.popBackStack() })
        }
    }
}
```

## 动画

```kotlin
@Composable
fun AnimationDemo() {
    var visible by remember { mutableStateOf(true) }

    // AnimatedVisibility
    Column {
        Button(onClick = { visible = !visible }) {
            Text("Toggle")
        }
        AnimatedVisibility(
            visible = visible,
            enter = slideInVertically() + fadeIn(),
            exit = slideOutVertically() + fadeOut()
        ) {
            Text("Animated content")
        }
    }

    // animateFloatAsState
    var enabled by remember { mutableStateOf(false) }
    val alpha by animateFloatAsState(
        targetValue = if (enabled) 1f else 0.3f,
        animationSpec = tween(durationMillis = 300)
    )
    Button(
        onClick = { enabled = !enabled },
        modifier = Modifier.alpha(alpha)
    ) {
        Text("Press me")
    }

    // animateContentSize
    var expanded by remember { mutableStateOf(false) }
    Column(
        modifier = Modifier
            .clickable { expanded = !expanded }
            .animateContentSize()
    ) {
        Text("Click to expand")
        if (expanded) {
            Text("More content here...")
        }
    }

    // 无限循环动画
    val infiniteTransition = rememberInfiniteTransition()
    val angle by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        )
    )
    Image(
        painter = painterResource(R.drawable.spinner),
        contentDescription = "Loading",
        modifier = Modifier.rotate(angle)
    )
}
```

## 副作用

```kotlin
@Composable
fun SideEffectDemo(viewModel: MyViewModel = viewModel()) {
    // LaunchedEffect: 在组合中启动协程
    LaunchedEffect(Unit) {
        viewModel.loadData()  // 只在首次组合时执行
    }

    LaunchedEffect(key1 = userId) {
        // 当 userId 变化时重新执行
        viewModel.loadUser(userId)
    }

    // rememberCoroutineScope: 在组合外启动协程
    val scope = rememberCoroutineScope()
    Button(onClick = {
        scope.launch {
            viewModel.doAction()
        }
    }) {
        Text("Action")
    }

    // DisposableEffect: 清理资源
    val context = LocalContext.current
    DisposableEffect(context) {
        val receiver = BroadcastReceiver { /* ... */ }
        context.registerReceiver(receiver, IntentFilter("ACTION"))
        onDispose {
            context.unregisterReceiver(receiver)  // 离开组合时清理
        }
    }

    // SideEffect: 每次重组时执行
    SideEffect {
        // 将 Compose 状态同步到非 Compose 代码
    }
}
```

## View 系统互操作

```kotlin
// Compose 中使用 Android View
@Composable
fun AndroidViewExample() {
    AndroidView(
        factory = { context ->
            TextView(context).apply {
                text = "来自 Android View"
                textSize = 20f
            }
        },
        modifier = Modifier.fillMaxWidth()
    )
}

// Android View 中使用 Compose
class MyActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        findViewById<ComposeView>(R.id.compose_view).setContent {
            MaterialTheme {
                Text("Hello from Compose!")
            }
        }
    }
}
```

