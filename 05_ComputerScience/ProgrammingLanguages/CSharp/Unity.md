---
aliases: [Unity]
tags: ['ProgrammingLanguages', 'CSharp', 'Unity']
---

# Unity 游戏开发基础

## Unity 编辑器概览

| 窗口 | 用途 |
|------|------|
| Scene | 场景编辑器（3D/2D 视图） |
| Game | 游戏运行视图 |
| Hierarchy | 层级面板（场景中所有 GameObject） |
| Project | 项目资源面板 |
| Inspector | 检视面板（组件属性） |
| Console | 控制台（日志、错误、警告） |

## GameObject 与 Component

Unity 采用组件架构。GameObject 是容器，Component 提供功能。

```csharp
// 创建 GameObject
GameObject player = new GameObject("Player");
GameObject enemy = GameObject.CreatePrimitive(PrimitiveType.Cube);

// 添加组件
Rigidbody rb = player.AddComponent<Rigidbody>();
BoxCollider collider = player.AddComponent<BoxCollider>();

// 获取组件
Rigidbody rb = GetComponent<Rigidbody>();
Rigidbody rb = GetComponentInChildren<Rigidbody>();
Rigidbody rb = GetComponentInParent<Rigidbody>();

// 查找 GameObject
GameObject obj = GameObject.Find("Player");
GameObject obj2 = GameObject.FindWithTag("Enemy");
GameObject[] enemies = GameObject.FindGameObjectsWithTag("Enemy");
```

## MonoBehaviour 生命周期

```
Awake → OnEnable → Start → FixedUpdate → Update → LateUpdate
    → OnDisable → OnDestroy

FixedUpdate: 固定时间间隔（默认 0.02s），适合物理
Update: 每帧调用，适合逻辑更新
LateUpdate: Update 之后调用，适合相机跟随
```

```csharp
public class PlayerController : MonoBehaviour {
    private Rigidbody _rb;
    private Animator _animator;

    void Awake() {
        _rb = GetComponent<Rigidbody>();
        _animator = GetComponent<Animator>();
        // Awake 在当前场景加载时调用，适合初始化引用
    }

    void Start() {
        // Start 在第一次 Update 之前调用，适合初始化数据
        GameManager.Instance.RegisterPlayer(this);
    }

    void OnEnable() {
        // 对象激活时调用
    }

    void OnDisable() {
        // 对象禁用时调用
    }

    void FixedUpdate() {
        // 物理更新
        HandleMovement();
    }

    void Update() {
        // 每帧更新
        HandleInput();
        UpdateAnimation();
    }

    void LateUpdate() {
        // Update 之后调用
        CameraFollow();
    }

    void OnDestroy() {
        // 对象销毁时调用
        GameManager.Instance.UnregisterPlayer(this);
    }
}
```

## Transform

```csharp
public class TransformDemo : MonoBehaviour {
    void Start() {
        // 位置
        transform.position = new Vector3(0, 1, 0);
        transform.localPosition = Vector3.zero;

        // 旋转
        transform.rotation = Quaternion.identity;
        transform.eulerAngles = new Vector3(0, 45, 0);
        transform.Rotate(Vector3.up, 90 * Time.deltaTime);
        transform.RotateAround(Vector3.zero, Vector3.up, 10);

        // 缩放
        transform.localScale = new Vector3(2, 2, 2);

        // 父子关系
        transform.parent = parentTransform;
        transform.SetParent(parent, false);
        transform.DetachChildren();

        // 方向向量
        Vector3 forward = transform.forward;
        Vector3 right = transform.right;
        Vector3 up = transform.up;

        // 查找
        Transform child = transform.Find("ChildName");
        Transform child2 = transform.GetChild(0);
        int childCount = transform.childCount;

        // 坐标转换
        Vector3 worldPos = transform.TransformPoint(localPos);
        Vector3 localPos = transform.InverseTransformPoint(worldPos);
        Vector3 worldDir = transform.TransformDirection(localDir);
    }
}
```

## 物理系统

### Rigidbody

```csharp
public class PhysicsDemo : MonoBehaviour {
    private Rigidbody _rb;

    void Start() {
        _rb = GetComponent<Rigidbody>();
    }

    void FixedUpdate() {
        // 施加力
        if (Input.GetKey(KeyCode.W)) {
            _rb.AddForce(Vector3.forward * 10f, ForceMode.Force);
        }

        // 瞬时力
        if (Input.GetKeyDown(KeyCode.Space)) {
            _rb.AddForce(Vector3.up * 5f, ForceMode.Impulse);
        }

        // 扭矩
        if (Input.GetKey(KeyCode.A)) {
            _rb.AddTorque(Vector3.up * 5f);
        }
    }

    // 碰撞检测
    void OnCollisionEnter(Collision collision) {
        Debug.Log($"碰撞到: {collision.gameObject.name}");
        Debug.Log($"冲击力: {collision.impulse.magnitude}");

        // 碰撞点信息
        foreach (ContactPoint contact in collision.contacts) {
            Debug.Log($"碰撞点: {contact.point}");
            Debug.Log($"法线: {contact.normal}");
        }
    }

    void OnCollisionStay(Collision collision) { }
    void OnCollisionExit(Collision collision) { }

    // 触发器（需勾选 IsTrigger）
    void OnTriggerEnter(Collider other) {
        Debug.Log($"进入触发器: {other.gameObject.name}");
    }

    void OnTriggerStay(Collider other) { }
    void OnTriggerExit(Collider other) { }
}
```

### Raycast

```csharp
public class RaycastDemo : MonoBehaviour {
    void Update() {
        // 鼠标点击射线检测
        if (Input.GetMouseButtonDown(0)) {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit hit;

            if (Physics.Raycast(ray, out hit, 100f)) {
                Debug.Log($"击中: {hit.collider.gameObject.name}");
                Debug.Log($"点: {hit.point}");
                Debug.Log($"法线: {hit.normal}");
                Debug.Log($"距离: {hit.distance}");

                // 击中的物体
                hit.collider.GetComponent<Renderer>().material.color = Color.red;
            }
        }

        // 球形射线检测
        Collider[] colliders = Physics.OverlapSphere(transform.position, 5f);
        foreach (var collider in colliders) {
            if (collider.CompareTag("Enemy")) {
                // 检测到敌人
            }
        }

        // 可视化调试
        Debug.DrawRay(transform.position, transform.forward * 10, Color.red);
    }

    void OnDrawGizmosSelected() {
        // 在 Scene 视图中显示检测范围
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, 5f);
    }
}
```

## 输入系统

### 传统输入

```csharp
public class InputDemo : MonoBehaviour {
    void Update() {
        // 键盘输入
        if (Input.GetKey(KeyCode.W)) Move(Vector3.forward);
        if (Input.GetKeyDown(KeyCode.Space)) Jump();
        if (Input.GetKeyUp(KeyCode.LeftShift)) StopSprint();

        // 轴输入
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        Vector3 movement = new Vector3(horizontal, 0, vertical) * speed * Time.deltaTime;
        transform.Translate(movement);

        // 鼠标输入
        float mouseX = Input.GetAxis("Mouse X");
        float mouseY = Input.GetAxis("Mouse Y");

        // 鼠标按钮
        if (Input.GetMouseButton(0)) Shoot();        // 左键按住
        if (Input.GetMouseButtonDown(1)) Aim();       // 右键按下

        // 触屏/移动端
        if (Input.touchCount > 0) {
            Touch touch = Input.GetTouch(0);
            if (touch.phase == TouchPhase.Began) { }
            if (touch.phase == TouchPhase.Moved) { }
        }
    }
}
```

### 新输入系统（Input System Package）

```csharp
using UnityEngine.InputSystem;

public class NewInputDemo : MonoBehaviour {
    private PlayerInputActions _inputActions;

    void Awake() {
        _inputActions = new PlayerInputActions();
    }

    void OnEnable() {
        _inputActions.Enable();
        _inputActions.Player.Jump.performed += OnJump;
        _inputActions.Player.Shoot.started += OnShootStarted;
        _inputActions.Player.Shoot.canceled += OnShootCanceled;
    }

    void OnDisable() {
        _inputActions.Disable();
        _inputActions.Player.Jump.performed -= OnJump;
        _inputActions.Player.Shoot.started -= OnShootStarted;
        _inputActions.Player.Shoot.canceled -= OnShootCanceled;
    }

    void Update() {
        Vector2 move = _inputActions.Player.Move.ReadValue<Vector2>();
        // 处理移动
    }

    void OnJump(InputAction.CallbackContext context) {
        // 跳跃
    }

    void OnShootStarted(InputAction.CallbackContext context) { }
    void OnShootCanceled(InputAction.CallbackContext context) { }
}
```

## 场景管理

```csharp
using UnityEngine.SceneManagement;

public class SceneManagerExample : MonoBehaviour {
    // 加载场景
    public void LoadScene(string sceneName) {
        SceneManager.LoadScene(sceneName);
    }

    public void LoadSceneAsync(string sceneName) {
        StartCoroutine(LoadSceneAsyncCoroutine(sceneName));
    }

    IEnumerator LoadSceneAsyncCoroutine(string sceneName) {
        AsyncOperation operation = SceneManager.LoadSceneAsync(sceneName);
        operation.allowSceneActivation = false;

        while (!operation.isDone) {
            float progress = Mathf.Clamp01(operation.progress / 0.9f);
            Debug.Log($"加载进度: {progress * 100}%");

            if (operation.progress >= 0.9f) {
                // 加载完成，等待用户确认
                operation.allowSceneActivation = true;
            }

            yield return null;
        }
    }

    // 场景事件
    void OnSceneLoaded(Scene scene, LoadSceneMode mode) {
        Debug.Log($"场景 {scene.name} 已加载");
    }
}
```

## 预制体系统

```csharp
public class PrefabManager : MonoBehaviour {
    [SerializeField] private GameObject _enemyPrefab;
    [SerializeField] private Transform _spawnPoint;

    void Start() {
        // 实例化预制体
        GameObject enemy = Instantiate(_enemyPrefab, _spawnPoint.position, Quaternion.identity);

        // 指定父对象
        GameObject enemy2 = Instantiate(_enemyPrefab, _spawnPoint.position, Quaternion.identity, parentTransform);

        // 带参数
        EnemyController controller = Instantiate(_enemyPrefab, pos, rot).GetComponent<EnemyController>();
        controller.Initialize(difficulty);
    }

    // 对象池
    public class ObjectPool {
        private Queue<GameObject> _pool = new Queue<GameObject>();
        private GameObject _prefab;

        public ObjectPool(GameObject prefab, int initialSize) {
            _prefab = prefab;
            for (int i = 0; i < initialSize; i++) {
                GameObject obj = CreateNew();
                obj.SetActive(false);
                _pool.Enqueue(obj);
            }
        }

        public GameObject Get() {
            if (_pool.Count == 0) {
                return CreateNew();
            }
            GameObject obj = _pool.Dequeue();
            obj.SetActive(true);
            return obj;
        }

        public void Return(GameObject obj) {
            obj.SetActive(false);
            _pool.Enqueue(obj);
        }

        private GameObject CreateNew() {
            return Instantiate(_prefab);
        }
    }
}
```

## 协程

```csharp
public class CoroutineDemo : MonoBehaviour {
    void Start() {
        StartCoroutine(MyCoroutine());
        StartCoroutine("NamedCoroutine");
    }

    IEnumerator MyCoroutine() {
        Debug.Log("开始");
        yield return new WaitForSeconds(2f);  // 等待 2 秒
        Debug.Log("2 秒后");

        yield return new WaitForFixedUpdate();  // 等待下一个 FixedUpdate
        yield return new WaitForEndOfFrame();   // 等待帧结束
        yield return null;                      // 等待一帧
        yield return new WaitUntil(() => score > 100);  // 等待条件满足
        yield return new WaitWhile(() => isLoading);    // 等待条件不满足

        // 嵌套协程
        yield return StartCoroutine(AnotherCoroutine());
    }

    IEnumerator AttackSequence() {
        while (true) {
            // 攻击动画
            yield return new WaitForSeconds(0.5f);

            // 伤害判定
            DealDamage();

            // 攻击间隔
            yield return new WaitForSeconds(1.5f);
        }
    }
}
```

## UI 系统

```csharp
using UnityEngine.UI;
using TMPro;

public class UIDemo : MonoBehaviour {
    [SerializeField] private TextMeshProUGUI _scoreText;
    [SerializeField] private Slider _healthBar;
    [SerializeField] private Button _startButton;
    [SerializeField] private Image _crosshair;
    [SerializeField] private GameObject _gameOverPanel;

    void Start() {
        // 按钮事件
        _startButton.onClick.AddListener(StartGame);
        _startButton.onClick.AddListener(() => Debug.Log("游戏开始"));

        // 更新 UI
        _scoreText.text = $"分数: {score}";
        _healthBar.value = currentHealth / maxHealth;
    }

    public void UpdateScore(int score) {
        _scoreText.text = $"分数: {score}";
        // 渐变动画
        StartCoroutine(ScoreAnimation());
    }

    IEnumerator ScoreAnimation() {
        _scoreText.transform.localScale = Vector3.one * 1.5f;
        float duration = 0.2f;
        float elapsed = 0;

        while (elapsed < duration) {
            float t = elapsed / duration;
            _scoreText.transform.localScale = Vector3.Lerp(
                Vector3.one * 1.5f, Vector3.one, t);
            elapsed += Time.deltaTime;
            yield return null;
        }

        _scoreText.transform.localScale = Vector3.one;
    }
}
```

## 构建管线

```csharp
// 自定义构建脚本
using UnityEditor;
using UnityEditor.Build.Reporting;

public class BuildScript {
    [MenuItem("Build/Build Windows")]
    public static void BuildWindows() {
        BuildPlayerOptions buildOptions = new BuildPlayerOptions {
            scenes = new[] {
                "Assets/Scenes/MainMenu.unity",
                "Assets/Scenes/Game.unity"
            },
            locationPathName = "Builds/Windows/MyGame.exe",
            target = BuildTarget.StandaloneWindows64,
            options = BuildOptions.None
        };

        BuildReport report = BuildPipeline.BuildPlayer(buildOptions);
        BuildSummary summary = report.summary;

        if (summary.result == BuildResult.Succeeded) {
            Debug.Log($"构建成功: {summary.totalSize / 1048576} MB");
        } else {
            Debug.LogError($"构建失败: {summary.result}");
        }
    }
}
```
