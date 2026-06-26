---
aliases: [UIKitDeepDive, UIKit深度, UIView, UIViewController]
tags: ['05_ComputerScience', 'ProgrammingLanguages', 'Swift', 'UIKit']
created: 2026-06-27
updated: 2026-06-27
---

# UIKit 深度指南 (UIKit Deep Dive)

## 一、概述

UIKit 是 iOS 的传统 UI 框架，虽然 SwiftUI 是未来方向，但 UIKit 仍然是大量现有应用的基础，且在某些场景（复杂自定义 UI、性能敏感场景）中仍然不可替代。

### 1.1 UIKit vs SwiftUI

| 特性 | UIKit | SwiftUI |
|------|-------|---------|
| 声明式 | 否（命令式） | 是 |
| 状态管理 | 手动 | 自动 |
| 实时预览 | 不支持 | 支持 |
| 最低版本 | iOS 2 | iOS 13 |
| 成熟度 | 非常成熟 | 快速迭代中 |
| 自定义能力 | 非常灵活 | 受限于框架 |

---

## 二、UIView 生命周期

### 2.1 UIView 生命周期方法

```swift
class CustomView: UIView {
    // 1. 初始化
    override init(frame: CGRect) {
        super.init(frame: frame)
        setupView()
    }
    
    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupView()
    }
    
    private func setupView() {
        // 通用初始化代码
        backgroundColor = .systemBackground
    }
    
    // 2. 布局子视图
    override func layoutSubviews() {
        super.layoutSubviews()
        // 子视图布局（每次 bounds 改变时调用）
    }
    
    // 3. 绘制（仅在使用 draw(_:) 时）
    override func draw(_ rect: CGRect) {
        // 自定义绘制
        guard let context = UIGraphicsGetCurrentContext() else { return }
        context.setStrokeColor(UIColor.red.cgColor)
        context.setLineWidth(2.0)
        context.addRect(rect)
        context.strokePath()
    }
    
    // 4. 约束更新
    override func updateConstraints() {
        // 更新约束
        super.updateConstraints()
    }
}
```

### 2.2 UIView 生命周期顺序

```
init(frame:) / init(coder:)
    ↓
willMove(toSuperview:)
    ↓
didMoveToSuperview()
    ↓
willMove(toWindow:)
    ↓
didMoveToWindow()
    ↓
layoutSubviews()  ← 多次调用
    ↓
draw(_:)  ← 仅在需要时
```

---

## 三、UIViewController 生命周期

### 3.1 完整生命周期

```swift
class ProfileViewController: UIViewController {
    
    // MARK: - Lifecycle
    
    // 1. 加载视图（仅在 view 被访问时调用）
    override func loadView() {
        super.loadView()
        // 自定义视图创建（不使用 Storyboard 时）
    }
    
    // 2. 视图加载完成
    override func viewDidLoad() {
        super.viewDidLoad()
        // 一次性初始化：UI 设置、数据加载、绑定
        setupUI()
        setupConstraints()
        bindViewModel()
    }
    
    // 3. 视图即将显示
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        // 刷新数据、开始动画、添加观察者
        navigationController?.setNavigationBarHidden(false, animated: animated)
    }
    
    // 4. 视图布局子视图
    override func viewWillLayoutSubviews() {
        super.viewWillLayoutSubviews()
        // 布局前的准备
    }
    
    // 5. 视图完成布局
    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        // 依赖于 view bounds 的布局
    }
    
    // 6. 视图已经显示
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        // 开始追踪、动画、网络请求
    }
    
    // 7. 视图即将消失
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        // 保存状态、停止动画、移除观察者
        view.endEditing(true)
    }
    
    // 8. 视图已经消失
    override func viewDidDisappear(_ animated: Bool) {
        super.viewDidDisappear(animated)
        // 停止追踪、取消请求
    }
    
    // 9. 内存警告
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // 释放缓存、非必要资源
    }
    
    // 10. 析构
    deinit {
        // 清理：移除通知观察者、取消定时器
        NotificationCenter.default.removeObserver(self)
    }
}
```

---

## 四、Auto Layout

### 4.1 NSLayoutConstraint

```swift
// 原生约束
let redView = UIView()
redView.translatesAutoresizingMaskIntoConstraints = false
view.addSubview(redView)

NSLayoutConstraint.activate([
    redView.centerXAnchor.constraint(equalTo: view.centerXAnchor),
    redView.centerYAnchor.constraint(equalTo: view.centerYAnchor),
    redView.widthAnchor.constraint(equalToConstant: 200),
    redView.heightAnchor.constraint(equalToConstant: 200)
])
```

### 4.2 Visual Format Language

```swift
let views = ["red": redView, "blue": blueView]

// 水平布局
let horizontal = NSLayoutConstraint.constraints(
    withVisualFormat: "H:|-20-[red(==100)]-20-[blue(==100)]",
    options: [.alignAllTop, .alignAllBottom],
    metrics: nil,
    views: views
)

// 垂直布局
let vertical = NSLayoutConstraint.constraints(
    withVisualFormat: "V:|-100-[red(50)]",
    options: [],
    metrics: nil,
    views: views
)

NSLayoutConstraint.activate(horizontal + vertical)
```

### 4.3 SnapKit (第三方库)

```swift
import SnapKit

redView.snp.makeConstraints { make in
    make.center.equalToSuperview()
    make.size.equalTo(200)
}

blueView.snp.makeConstraints { make in
    make.top.equalTo(redView.snp.bottom).offset(20)
    make.leading.trailing.equalToSuperview().inset(20)
    make.height.equalTo(100)
}
```

### 4.4 动态约束

```swift
class DynamicViewController: UIViewController {
    private var heightConstraint: NSLayoutConstraint!
    private let contentView = UIView()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        contentView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(contentView)
        
        heightConstraint = contentView.heightAnchor.constraint(equalToConstant: 100)
        
        NSLayoutConstraint.activate([
            contentView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            contentView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            contentView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            heightConstraint
        ])
    }
    
    func updateHeight(_ newHeight: CGFloat) {
        heightConstraint.constant = newHeight
        
        UIView.animate(withDuration: 0.3) {
            self.view.layoutIfNeeded()
        }
    }
}
```

---

## 五、UITableView

### 5.1 基础使用

```swift
class UserListViewController: UIViewController {
    private let tableView = UITableView()
    private var users: [User] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupTableView()
        loadData()
    }
    
    private func setupTableView() {
        tableView.dataSource = self
        tableView.delegate = self
        tableView.register(UserCell.self, forCellReuseIdentifier: "UserCell")
        
        view.addSubview(tableView)
        tableView.frame = view.bounds
        tableView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
    }
}

// MARK: - UITableViewDataSource
extension UserListViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        users.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "UserCell", for: indexPath) as! UserCell
        cell.configure(with: users[indexPath.row])
        return cell
    }
}

// MARK: - UITableViewDelegate
extension UserListViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        let user = users[indexPath.row]
        // 导航到详情
    }
    
    func tableView(_ tableView: UITableView, trailingSwipeActionsConfigurationForRowAt indexPath: IndexPath) -> UISwipeActionsConfiguration? {
        let delete = UIContextualAction(style: .destructive, title: "删除") { [weak self] _, _, completion in
            self?.users.remove(at: indexPath.row)
            tableView.deleteRows(at: [indexPath], with: .automatic)
            completion(true)
        }
        return UISwipeActionsConfiguration(actions: [delete])
    }
}
```

### 5.2 Diffable Data Source

```swift
class ModernUserListViewController: UIViewController {
    private let tableView = UITableView()
    private var dataSource: UITableViewDiffableDataSource<Section, User>!
    
    enum Section {
        case main
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupTableView()
        setupDataSource()
        loadData()
    }
    
    private func setupDataSource() {
        dataSource = UITableViewDiffableDataSource<Section, User>(
            tableView: tableView
        ) { tableView, indexPath, user in
            let cell = tableView.dequeueReusableCell(withIdentifier: "UserCell", for: indexPath) as! UserCell
            cell.configure(with: user)
            return cell
        }
    }
    
    private func updateUI(with users: [User], animated: Bool = true) {
        var snapshot = NSDiffableDataSourceSnapshot<Section, User>()
        snapshot.appendSections([.main])
        snapshot.appendItems(users)
        dataSource.apply(snapshot, animatingDifferences: animated)
    }
}
```

### 5.3 自定义 Cell

```swift
class UserCell: UITableViewCell {
    private let avatarImageView = UIImageView()
    private let nameLabel = UILabel()
    private let emailLabel = UILabel()
    
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        setupUI()
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    private func setupUI() {
        // 头像
        avatarImageView.contentMode = .scaleAspectFill
        avatarImageView.clipsToBounds = true
        avatarImageView.layer.cornerRadius = 25
        avatarImageView.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(avatarImageView)
        
        // 姓名
        nameLabel.font = .systemFont(ofSize: 16, weight: .semibold)
        nameLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(nameLabel)
        
        // 邮箱
        emailLabel.font = .systemFont(ofSize: 14)
        emailLabel.textColor = .secondaryLabel
        emailLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(emailLabel)
        
        NSLayoutConstraint.activate([
            avatarImageView.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 16),
            avatarImageView.centerYAnchor.constraint(equalTo: contentView.centerYAnchor),
            avatarImageView.widthAnchor.constraint(equalToConstant: 50),
            avatarImageView.heightAnchor.constraint(equalToConstant: 50),
            
            nameLabel.leadingAnchor.constraint(equalTo: avatarImageView.trailingAnchor, constant: 12),
            nameLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -16),
            nameLabel.topAnchor.constraint(equalTo: contentView.topAnchor, constant: 12),
            
            emailLabel.leadingAnchor.constraint(equalTo: nameLabel.leadingAnchor),
            emailLabel.trailingAnchor.constraint(equalTo: nameLabel.trailingAnchor),
            emailLabel.topAnchor.constraint(equalTo: nameLabel.bottomAnchor, constant: 4),
            emailLabel.bottomAnchor.constraint(equalTo: contentView.bottomAnchor, constant: -12)
        ])
    }
    
    func configure(with user: User) {
        nameLabel.text = user.name
        emailLabel.text = user.email
        // 加载头像图片
    }
    
    override func prepareForReuse() {
        super.prepareForReuse()
        avatarImageView.image = nil
    }
}
```

---

## 六、UICollectionView

### 6.1 Compositional Layout

```swift
class PhotoGalleryViewController: UIViewController {
    private var collectionView: UICollectionView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupCollectionView()
    }
    
    private func setupCollectionView() {
        let layout = createLayout()
        collectionView = UICollectionView(frame: view.bounds, collectionViewLayout: layout)
        collectionView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        collectionView.register(PhotoCell.self, forCellWithReuseIdentifier: "PhotoCell")
        view.addSubview(collectionView)
    }
    
    private func createLayout() -> UICollectionViewCompositionalLayout {
        // 每行3个等宽item
        let itemSize = NSCollectionLayoutSize(
            widthDimension: .fractionalWidth(1/3),
            heightDimension: .fractionalHeight(1)
        )
        let item = NSCollectionLayoutItem(layoutSize: itemSize)
        item.contentInsets = NSDirectionalEdgeInsets(top: 2, leading: 2, bottom: 2, trailing: 2)
        
        let groupSize = NSCollectionLayoutSize(
            widthDimension: .fractionalWidth(1),
            heightDimension: .fractionalWidth(1/3)
        )
        let group = NSCollectionLayoutGroup.horizontal(layoutSize: groupSize, subitems: [item])
        
        let section = NSCollectionLayoutSection(group: group)
        
        return UICollectionViewCompositionalLayout(section: section)
    }
}
```

### 6.2 Diffable Data Source (Collection View)

```swift
// 使用 Diffable Data Source
private func setupDataSource() {
    dataSource = UICollectionViewDiffableDataSource<Section, Photo>(
        collectionView: collectionView
    ) { collectionView, indexPath, photo in
        let cell = collectionView.dequeueReusableCell(
            withReuseIdentifier: "PhotoCell",
            for: indexPath
        ) as! PhotoCell
        cell.configure(with: photo)
        return cell
    }
}
```

---

## 七、UIKit 与 SwiftUI 互操作

### 7.1 在 UIKit 中使用 SwiftUI

```swift
import SwiftUI

// SwiftUI View
struct SwiftUIView: View {
    let title: String
    
    var body: some View {
        Text(title)
            .font(.largeTitle)
            .padding()
    }
}

// 在 UIKit 中嵌入
class UIKitViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let swiftUIView = SwiftUIView(title: "Hello")
        let hostingController = UIHostingController(rootView: swiftUIView)
        
        addChild(hostingController)
        view.addSubview(hostingController.view)
        hostingController.view.frame = view.bounds
        hostingController.view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        hostingController.didMove(toParent: self)
    }
}
```

### 7.2 在 SwiftUI 中使用 UIKit

```swift
// UIViewRepresentable
struct ActivityIndicator: UIViewRepresentable {
    var isAnimating: Bool
    
    func makeUIView(context: Context) -> UIActivityIndicatorView {
        let indicator = UIActivityIndicatorView(style: .large)
        return indicator
    }
    
    func updateUIView(_ uiView: UIActivityIndicatorView, context: Context) {
        if isAnimating {
            uiView.startAnimating()
        } else {
            uiView.stopAnimating()
        }
    }
}

// UIViewControllerRepresentable
struct ImagePicker: UIViewControllerRepresentable {
    @Binding var image: UIImage?
    @Environment(\.dismiss) var dismiss
    
    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.delegate = context.coordinator
        return picker
    }
    
    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        let parent: ImagePicker
        
        init(_ parent: ImagePicker) {
            self.parent = parent
        }
        
        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey: Any]) {
            if let image = info[.originalImage] as? UIImage {
                parent.image = image
            }
            parent.dismiss()
        }
    }
}
```

---

## 八、手势识别

### 8.1 UIGestureRecognizer

```swift
class GestureViewController: UIViewController {
    private let draggableview = UIView()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupGestures()
    }
    
    private func setupGestures() {
        // 点击手势
        let tap = UITapGestureRecognizer(target: self, action: #selector(handleTap(_:)))
        tap.numberOfTapsRequired = 1
        view.addGestureRecognizer(tap)
        
        // 拖拽手势
        let pan = UIPanGestureRecognizer(target: self, action: #selector(handlePan(_:)))
        draggableview.addGestureRecognizer(pan)
        
        // 长按手势
        let longPress = UILongPressGestureRecognizer(
            target: self,
            action: #selector(handleLongPress(_:))
        )
        longPress.minimumPressDuration = 1.0
        view.addGestureRecognizer(longPress)
        
        // 缩放手势
        let pinch = UIPinchGestureRecognizer(target: self, action: #selector(handlePinch(_:)))
        view.addGestureRecognizer(pinch)
        
        // 旋转手势
        let rotation = UIRotationGestureRecognizer(target: self, action: #selector(handleRotation(_:)))
        view.addGestureRecognizer(rotation)
        
        // 滑动手势
        let swipe = UISwipeGestureRecognizer(target: self, action: #selector(handleSwipe(_:)))
        swipe.direction = .left
        view.addGestureRecognizer(swipe)
    }
    
    @objc private func handleTap(_ gesture: UITapGestureRecognizer) {
        let point = gesture.location(in: view)
        print("Tapped at: \(point)")
    }
    
    @objc private func handlePan(_ gesture: UIPanGestureRecognizer) {
        let translation = gesture.translation(in: view)
        
        switch gesture.state {
        case .changed:
            draggableview.center = CGPoint(
                x: draggableview.center.x + translation.x,
                y: draggableview.center.y + translation.y
            )
            gesture.setTranslation(.zero, in: view)
        default:
            break
        }
    }
}
```

---

## 九、动画

### 9.1 UIView 动画

```swift
// 基础动画
UIView.animate(withDuration: 0.3) {
    self.view.alpha = 0.5
    self.view.transform = CGAffineTransform(scaleX: 1.2, y: 1.2)
}

// 带完成回调
UIView.animate(withDuration: 0.3, delay: 0, options: [.curveEaseInOut]) {
    self.view.frame.origin.y += 100
} completion: { finished in
    print("动画完成")
}

// 弹簧动画
UIView.animate(
    withDuration: 0.5,
    delay: 0,
    usingSpringWithDamping: 0.5,
    initialSpringVelocity: 0.5,
    options: []
) {
    self.view.transform = .identity
}

// 关键帧动画
UIView.animateKeyframes(withDuration: 2, delay: 0) {
    UIView.addKeyframe(withRelativeStartTime: 0, relativeDuration: 0.5) {
        self.view.center.x += 100
    }
    UIView.addKeyframe(withRelativeStartTime: 0.5, relativeDuration: 0.5) {
        self.view.center.y += 100
    }
}
```

### 9.2 UIViewPropertyAnimator

```swift
// 交互式动画
let animator = UIViewPropertyAnimator(
    duration: 1,
    timingParameters: UISpringTimingParameters(
        dampingRatio: 0.5,
        initialVelocity: CGVector(dx: 0, dy: 0)
    )
)

animator.addAnimations {
    self.view.transform = CGAffineTransform(scaleX: 1.5, y: 1.5)
}

animator.addCompletion { position in
    switch position {
    case .end: print("动画完成")
    case .start: print("动画取消")
    case .current: print("动画中断")
    @unknown default: break
    }
}

// 开始
animator.startAnimation()

// 暂停
animator.pauseAnimation()

// 继续
animator.continueAnimation(withTimingParameters: nil, durationFactor: 0)

// 反转
animator.isReversed = true
```

---

## 十、最佳实践

### 10.1 代码组织

```swift
// MARK: - 使用 MARK 注释组织代码
class ViewController: UIViewController {
    
    // MARK: - Properties
    
    private let tableView = UITableView()
    private var dataSource: [Item] = []
    
    // MARK: - Lifecycle
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }
    
    // MARK: - Setup
    
    private func setupUI() {
        // UI 设置
    }
    
    // MARK: - Data
    
    private func loadData() {
        // 数据加载
    }
    
    // MARK: - Actions
    
    @objc private func buttonTapped() {
        // 按钮点击处理
    }
    
    // MARK: - Helpers
    
    private func formatData(_ data: Any) -> String {
        // 辅助方法
    }
}

// MARK: - Extensions
extension ViewController: UITableViewDataSource {
    // 数据源方法
}

extension ViewController: UITableViewDelegate {
    // 代理方法
}
```

### 10.2 内存管理

```swift
// 使用 weak self 避免循环引用
class ViewModel {
    var onUpdate: (() -> Void)?
    
    func fetchData() {
        APIService.shared.request { [weak self] result in
            guard let self = self else { return }
            // 使用 self
        }
    }
}

// 使用 unowned（确定不会为 nil 时）
class ViewController {
    func process() {
        APIService.shared.request { [unowned self] result in
            // self 不会为 nil
        }
    }
}
```

---

## 相关条目

- [[Swift]]
- [[SwiftUI与iOS开发]]
- [[AppArchitecture]]

## 参考资源

1. Apple. "UIKit Documentation." developer.apple.com
2. Apple. "Auto Layout Guide." developer.apple.com
3. raywenderlich.com. "UIKit tutorials." raywenderlich.com
4. Hudson, P. "Hacking with Swift: UIKit." hackingwithswift.com
