---
aliases: [Android]
tags: ['ProgrammingLanguages', 'Kotlin', 'Android']
---

# Android 开发基础

## Android 架构与组件

```kotlin
// Activity - 用户交互界面
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}

// Service - 后台长时间运行操作
class MyService : Service() {
    override fun onBind(intent: Intent): IBinder? = null
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // 执行后台工作
        return START_STICKY
    }
}

// BroadcastReceiver - 接收系统广播
class AirplaneModeReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val isAirplaneMode = intent.getBooleanExtra("state", false)
    }
}

// ContentProvider - 跨进程数据共享
class MyContentProvider : ContentProvider() {
    override fun query(...): Cursor? { /* ... */ }
    override fun insert(...): Uri? { /* ... */ }
    override fun update(...): Int { /* ... */ }
    override fun delete(...): Int { /* ... */ }
    override fun getType(uri: Uri): String? { /* ... */ }
    override fun onCreate(): Boolean { /* ... */ }
}
```

## 生命周期

```kotlin
// Activity 生命周期
class LifecycleActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) { /* 创建 */ }
    override fun onStart() { /* 可见 */ }
    override fun onResume() { /* 可交互 */ }
    override fun onPause() { /* 失去焦点 */ }
    override fun onStop() { /* 不可见 */ }
    override fun onDestroy() { /* 销毁 */ }
    override fun onRestart() { /* 重启 */ }
}

// Fragment 生命周期
class MyFragment : Fragment() {
    override fun onAttach(context: Context) { /* 关联 Activity */ }
    override fun onCreate(savedInstanceState: Bundle?) { /* 创建 */ }
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.fragment_my, container, false)
    }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) { /* 视图创建完毕 */ }
    override fun onStart() { /* 可见 */ }
    override fun onResume() { /* 可交互 */ }
    override fun onPause() { /* 暂停 */ }
    override fun onStop() { /* 停止 */ }
    override fun onDestroyView() { /* 销毁视图 */ }
    override fun onDestroy() { /* 销毁 */ }
    override fun onDetach() { /* 分离 */ }
}

// ViewModel - 管理 UI 数据，感知生命周期
class MyViewModel : ViewModel() {
    private val _data = MutableLiveData<String>()
    val data: LiveData<String> = _data

    fun loadData() {
        _data.value = "Hello ViewModel"
    }
}

// 在 Activity/Fragment 中使用
class MainActivity : AppCompatActivity() {
    private val viewModel: MyViewModel by viewModels()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        viewModel.data.observe(this) { value ->
            // 更新 UI
        }
    }
}
```

## 导航 (Jetpack Navigation)

```kotlin
// build.gradle (app)
dependencies {
    implementation("androidx.navigation:navigation-fragment-ktx:2.7.7")
    implementation("androidx.navigation:navigation-ui-ktx:2.7.7")
}

// NavGraph (nav_graph.xml)
// <navigation> 元素定义目标 Fragment 和动作

// 在 Activity 中设置
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val navController = findNavController(R.id.nav_host_fragment)
        NavigationUI.setupActionBarWithNavController(this, navController)
    }
}

// Fragment 中导航
class HomeFragment : Fragment() {
    fun navigateToDetail(id: Long) {
        val action = HomeFragmentDirections.actionHomeToDetail(id)
        findNavController().navigate(action)
    }
}
```

## 数据存储

```kotlin
// Room 数据库
@Entity(tableName = "users")
data class User(
    @PrimaryKey val id: Int,
    @ColumnInfo(name = "full_name") val name: String,
    val email: String
)

@Dao
interface UserDao {
    @Query("SELECT * FROM users")
    suspend fun getAll(): List<User>

    @Insert
    suspend fun insert(user: User)

    @Delete
    suspend fun delete(user: User)
}

@Database(entities = [User::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}

// 创建数据库
val db = Room.databaseBuilder(
    applicationContext,
    AppDatabase::class.java, "my-db"
).build()

// DataStore (替代 SharedPreferences)
val Context.dataStore by preferencesDataStore(name = "settings")
val COUNTER_KEY = intPreferencesKey("counter")

// 读取
val counterFlow: Flow<Int> = context.dataStore.data
    .map { preferences -> preferences[COUNTER_KEY] ?: 0 }

// 写入
suspend fun incrementCounter() {
    context.dataStore.edit { preferences ->
        val current = preferences[COUNTER_KEY] ?: 0
        preferences[COUNTER_KEY] = current + 1
    }
}

// SharedPreferences
val prefs = getSharedPreferences("my_prefs", Context.MODE_PRIVATE)
prefs.edit().putString("key", "value").apply()
val value = prefs.getString("key", "default")
```

## 网络请求

```kotlin
// Retrofit + OkHttp
interface ApiService {
    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: Int): User

    @POST("users")
    suspend fun createUser(@Body user: User): User

    @GET("posts")
    suspend fun getPosts(
        @Query("page") page: Int,
        @Query("limit") limit: Int = 20
    ): List<Post>
}

// 创建 Retrofit 实例
val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .addConverterFactory(GsonConverterFactory.create())
    .client(OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .addInterceptor { chain ->
            val request = chain.request().newBuilder()
                .addHeader("Authorization", "Bearer token")
                .build()
            chain.proceed(request)
        }
        .build())
    .build()

val api = retrofit.create(ApiService::class.java)

// 使用 Kotlin Serialization
@Serializable
data class User(val id: Int, val name: String)

// 图片加载 - Coil
// build.gradle: implementation("io.coil-kt:coil:2.6.0")
imageView.load("https://example.com/image.jpg") {
    crossfade(true)
    placeholder(R.drawable.placeholder)
    error(R.drawable.error)
}

// Glide
Glide.with(this)
    .load("https://example.com/image.jpg")
    .placeholder(R.drawable.placeholder)
    .into(imageView)
```

## 依赖注入

```kotlin
// Hilt
@HiltAndroidApp
class MyApplication : Application()

@AndroidEntryPoint
class MainActivity : AppCompatActivity() {
    @Inject lateinit var repository: UserRepository
}

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit = Retrofit.Builder()
        .baseUrl("https://api.example.com")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
}

// Koin
val appModule = module {
    single { ApiService() }
    factory { UserRepository(get()) }
    viewModel { MyViewModel(get()) }
}

class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@MyApplication)
            modules(appModule)
        }
    }
}
```

## 权限模型

```kotlin
// Android 6.0+ 运行时权限
if (ContextCompat.checkSelfPermission(
        this, Manifest.permission.CAMERA
) != PackageManager.PERMISSION_GRANTED) {
    ActivityCompat.requestPermissions(
        this,
        arrayOf(Manifest.permission.CAMERA),
        REQUEST_CAMERA
    )
}

// 处理权限结果
override fun onRequestPermissionsResult(
    requestCode: Int,
    permissions: Array<String>,
    grantResults: IntArray
) {
    when (requestCode) {
        REQUEST_CAMERA -> {
            if (grantResults.isNotEmpty() &&
                grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // 权限已授予
            }
        }
    }
}
```

## 测试

```kotlin
// JUnit + MockK
class UserRepositoryTest {
    private val api = mockk<ApiService>()
    private val repository = UserRepository(api)

    @Test
    fun `getUser returns user data`() = runBlocking {
        coEvery { api.getUser(1) } returns User(1, "Alice")
        val user = repository.getUser(1)
        assertEquals(1, user.id)
        assertEquals("Alice", user.name)
    }
}

// Espresso UI 测试
@Test
fun buttonClick_showsMessage() {
    onView(withId(R.id.button)).perform(click())
    onView(withText("Hello")).check(matches(isDisplayed()))
}
```
