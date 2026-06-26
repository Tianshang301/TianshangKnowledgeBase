---
aliases: [CoreFrameworks, iOS核心框架, CoreAnimation, CoreLocation, MapKit]
tags: ['05_ComputerScience', 'ProgrammingLanguages', 'Swift', 'iOS']
created: 2026-06-27
updated: 2026-06-27
---

# iOS 核心框架 (iOS Core Frameworks)

## 一、概述

iOS 提供了丰富的系统框架，本文档涵盖最常用的核心框架：Core Animation、Core Graphics、Core Location、MapKit、HealthKit 和 AVFoundation。

---

## 二、Core Animation

### 2.1 基础动画

```swift
// 基础属性动画
let animation = CABasicAnimation(keyPath: "opacity")
animation.fromValue = 1.0
animation.toValue = 0.0
animation.duration = 0.5
view.layer.add(animation, forKey: "fadeAnimation")

// 位置动画
let positionAnimation = CABasicAnimation(keyPath: "position")
positionAnimation.fromValue = CGPoint(x: 0, y: 0)
positionAnimation.toValue = CGPoint(x: 200, y: 200)
positionAnimation.duration = 1.0
positionAnimation.fillMode = .forwards
positionAnimation.isRemovedOnCompletion = false
view.layer.add(positionAnimation, forKey: "moveAnimation")
```

### 2.2 关键帧动画

```swift
let keyframeAnimation = CAKeyframeAnimation(keyPath: "position")
keyframeAnimation.values = [
    CGPoint(x: 0, y: 0),
    CGPoint(x: 100, y: 0),
    CGPoint(x: 100, y: 100),
    CGPoint(x: 0, y: 100),
    CGPoint(x: 0, y: 0)
]
keyframeAnimation.keyTimes = [0, 0.25, 0.5, 0.75, 1.0]
keyframeAnimation.duration = 2.0
view.layer.add(keyframeAnimation, forKey: "pathAnimation")
```

### 2.3 弹簧动画

```swift
let springAnimation = CASpringAnimation(keyPath: "transform.scale")
springAnimation.fromValue = 0.5
springAnimation.toValue = 1.0
springAnimation.damping = 10
springAnimation.stiffness = 100
springAnimation.mass = 1
springAnimation.initialVelocity = 0
springAnimation.duration = springAnimation.settlingDuration
view.layer.add(springAnimation, forKey: "springAnimation")
```

### 2.4 转场动画

```swift
let transition = CATransition()
transition.type = .push
transition.subtype = .fromRight
transition.duration = 0.3
view.layer.add(transition, forKey: kCATransitionPush)

// 切换视图
oldView.removeFromSuperview()
.addSubview(newView)
```

### 2.5 动画组

```swift
let group = CAAnimationGroup()
group.animations = [
    CABasicAnimation(keyPath: "opacity"),
    CABasicAnimation(keyPath: "transform.scale"),
    CABasicAnimation(keyPath: "position")
]
group.duration = 1.0
group.fillMode = .forwards
group.isRemovedOnCompletion = false
view.layer.add(group, forKey: "groupAnimation")
```

---

## 三、Core Graphics

### 3.1 绘制基本图形

```swift
class CustomView: UIView {
    override func draw(_ rect: CGRect) {
        guard let context = UIGraphicsGetCurrentContext() else { return }
        
        // 绘制矩形
        let rect = CGRect(x: 50, y: 50, width: 100, height: 100)
        context.setFillColor(UIColor.red.cgColor)
        context.fill(rect)
        
        // 绘制圆形
        let circleRect = CGRect(x: 200, y: 50, width: 100, height: 100)
        context.setFillColor(UIColor.blue.cgColor)
        context.fillEllipse(in: circleRect)
        
        // 绘制线条
        context.setStrokeColor(UIColor.green.cgColor)
        context.setLineWidth(3.0)
        context.move(to: CGPoint(x: 50, y: 200))
        context.addLine(to: CGPoint(x: 300, y: 200))
        context.strokePath()
        
        // 绘制贝塞尔曲线
        context.setStrokeColor(UIColor.purple.cgColor)
        context.setLineWidth(2.0)
        context.move(to: CGPoint(x: 50, y: 300))
        context.addCurve(
            to: CGPoint(x: 300, y: 300),
            control1: CGPoint(x: 100, y: 200),
            control2: CGPoint(x: 250, y: 400)
        )
        context.strokePath()
    }
}
```

### 3.2 UIBezierPath

```swift
// 绘制矩形
let rectPath = UIBezierPath(rect: CGRect(x: 50, y: 50, width: 100, height: 100))
UIColor.red.setFill()
rectPath.fill()

// 绘制圆形
let circlePath = UIBezierPath(ovalIn: CGRect(x: 200, y: 50, width: 100, height: 100))
UIColor.blue.setFill()
circlePath.fill()

// 绘制圆角矩形
let roundedPath = UIBezierPath(
    roundedRect: CGRect(x: 50, y: 200, width: 100, height: 100),
    cornerRadius: 10
)
UIColor.green.setFill()
roundedPath.fill()

// 绘制自定义路径
let path = UIBezierPath()
path.move(to: CGPoint(x: 50, y: 350))
path.addLine(to: CGPoint(x: 150, y: 300))
path.addLine(to: CGPoint(x: 250, y: 350))
path.addLine(to: CGPoint(x: 200, y: 450))
path.addLine(to: CGPoint(x: 100, y: 450))
path.close()
UIColor.orange.setFill()
path.fill()
```

---

## 四、Core Location

### 4.1 定位服务

```swift
import CoreLocation

class LocationManager: NSObject, CLLocationManagerDelegate {
    private let manager = CLLocationManager()
    var onLocationUpdate: ((CLLocation) -> Void)?
    
    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
    }
    
    func requestLocation() {
        manager.requestWhenInUseAuthorization()
        manager.requestLocation()
    }
    
    func startUpdatingLocation() {
        manager.startUpdatingLocation()
    }
    
    func stopUpdatingLocation() {
        manager.stopUpdatingLocation()
    }
    
    // MARK: - CLLocationManagerDelegate
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }
        onLocationUpdate?(location)
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        print("Location error: \(error)")
    }
}

// 使用
let locationManager = LocationManager()
locationManager.onLocationUpdate = { location in
    print("Latitude: \(location.coordinate.latitude)")
    print("Longitude: \(location.coordinate.longitude)")
}
locationManager.requestLocation()
```

### 4.2 地理围栏

```swift
func startMonitoring(region: CLCircularRegion) {
    if CLLocationManager.isMonitoringAvailable(for: CLCircularRegion.self) {
        manager.startMonitoring(for: region)
    }
}

func locationManager(_ manager: CLLocationManager, didEnterRegion region: CLRegion) {
    print("Entered region: \(region.identifier)")
}

func locationManager(_ manager: CLLocationManager, didExitRegion region: CLRegion) {
    print("Exited region: \(region.identifier)")
}
```

---

## 五、MapKit

### 5.1 地图显示

```swift
import MapKit

class MapViewController: UIViewController {
    @IBOutlet weak var mapView: MKMapView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // 设置初始位置
        let coordinate = CLLocationCoordinate2D(latitude: 39.9042, longitude: 116.4074)
        let region = MKCoordinateRegion(
            center: coordinate,
            span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
        )
        mapView.setRegion(region, animated: true)
        
        // 添加标注
        let annotation = MKPointAnnotation()
        annotation.coordinate = coordinate
        annotation.title = "北京"
        annotation.subtitle = "中国首都"
        mapView.addAnnotation(annotation)
    }
}
```

### 5.2 自定义标注

```swift
class CustomAnnotation: NSObject, MKAnnotation {
    let coordinate: CLLocationCoordinate2D
    let title: String?
    let subtitle: String?
    let image: UIImage?
    
    init(coordinate: CLLocationCoordinate2D, title: String?, subtitle: String?, image: UIImage?) {
        self.coordinate = coordinate
        self.title = title
        self.subtitle = subtitle
        self.image = image
    }
}

extension MapViewController: MKMapViewDelegate {
    func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
        guard let customAnnotation = annotation as? CustomAnnotation else { return nil }
        
        let identifier = "CustomPin"
        var annotationView = mapView.dequeueReusableAnnotationView(withIdentifier: identifier) as? MKMarkerAnnotationView
        
        if annotationView == nil {
            annotationView = MKMarkerAnnotationView(annotation: annotation, reuseIdentifier: identifier)
            annotationView?.canShowCallout = true
        }
        
        annotationView?.markerTintColor = .systemBlue
        annotationView?.glyphImage = customAnnotation.image
        
        return annotationView
    }
}
```

### 5.3 路径规划

```swift
func calculateRoute(from source: CLLocationCoordinate2D, to destination: CLLocationCoordinate2D) {
    let request = MKDirections.Request()
    request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
    request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
    request.transportType = .automobile
    
    let directions = MKDirections(request: request)
    directions.calculate { response, error in
        guard let route = response?.routes.first else { return }
        
        // 显示路径
        self.mapView.addOverlay(route.polyline)
        
        // 显示信息
        print("Distance: \(route.distance) meters")
        print("Expected travel time: \(route.expectedTravelTime) seconds")
    }
}

extension MapViewController: MKMapViewDelegate {
    func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
        if let polyline = overlay as? MKPolyline {
            let renderer = MKPolylineRenderer(polyline: polyline)
            renderer.strokeColor = .systemBlue
            renderer.lineWidth = 5
            return renderer
        }
        return MKOverlayRenderer(overlay: overlay)
    }
}
```

---

## 六、HealthKit

### 6.1 健康数据访问

```swift
import HealthKit

class HealthManager {
    let store = HKHealthStore()
    
    func requestAuthorization() {
        let typesToRead: Set<HKObjectType> = [
            HKObjectType.quantityType(forIdentifier: .heartRate)!,
            HKObjectType.quantityType(forIdentifier: .stepCount)!,
            HKObjectType.quantityType(forIdentifier: .activeEnergyBurned)!
        ]
        
        store.requestAuthorization(toShare: nil, read: typesToRead) { success, error in
            if success {
                print("HealthKit authorized")
            }
        }
    }
    
    func fetchHeartRate(completion: @escaping ([HKQuantitySample]) -> Void) {
        let heartRateType = HKQuantityType.quantityType(forIdentifier: .heartRate)!
        
        let sortDescriptor = NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: false)
        
        let query = HKSampleQuery(
            sampleType: heartRateType,
            predicate: nil,
            limit: 10,
            sortDescriptors: [sortDescriptor]
        ) { _, samples, error in
            guard let samples = samples as? [HKQuantitySample] else { return }
            completion(samples)
        }
        
        store.execute(query)
    }
}
```

---

## 七、AVFoundation

### 7.1 音频录制

```swift
import AVFoundation

class AudioRecorder: NSObject, AVAudioRecorderDelegate {
    var recorder: AVAudioRecorder?
    
    func startRecording() {
        let audioFilename = getDocumentsDirectory().appendingPathComponent("recording.m4a")
        
        let settings = [
            AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
            AVSampleRateKey: 12000,
            AVNumberOfChannelsKey: 1,
            AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
        ]
        
        do {
            recorder = try AVAudioRecorder(url: audioFilename, settings: settings)
            recorder?.delegate = self
            recorder?.record()
        } catch {
            print("Recording failed: \(error)")
        }
    }
    
    func stopRecording() {
        recorder?.stop()
        recorder = nil
    }
    
    func getDocumentsDirectory() -> URL {
        FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    }
}
```

### 7.2 视频播放

```swift
import AVKit

class VideoPlayerViewController: UIViewController {
    var player: AVPlayer?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        guard let url = URL(string: "https://example.com/video.mp4") else { return }
        
        player = AVPlayer(url: url)
        
        let playerLayer = AVPlayerLayer(player: player)
        playerLayer.frame = view.bounds
        view.layer.addSublayer(playerLayer)
        
        player?.play()
    }
}
```

### 7.3 相机捕获

```swift
import AVFoundation

class CameraManager: NSObject {
    var captureSession: AVCaptureSession?
    var previewLayer: AVCaptureVideoPreviewLayer?
    
    func setupCamera(in view: UIView) {
        captureSession = AVCaptureSession()
        
        guard let camera = AVCaptureDevice.default(for: .video) else { return }
        
        do {
            let input = try AVCaptureDeviceInput(device: camera)
            captureSession?.addInput(input)
            
            previewLayer = AVCaptureVideoPreviewLayer(session: captureSession!)
            previewLayer?.videoGravity = .resizeAspectFill
            previewLayer?.frame = view.bounds
            view.layer.addSublayer(previewLayer!)
            
            captureSession?.startRunning()
        } catch {
            print("Camera setup failed: \(error)")
        }
    }
}
```

---

## 八、Core Data

### 8.1 数据模型

```swift
import CoreData

// NSManagedObject 子类
@objc(User)
public class User: NSManagedObject {
    @NSManaged public var id: UUID
    @NSManaged public var name: String
    @NSManaged public var email: String
    @NSManaged public var createdAt: Date
}

// 扩展
extension User {
    @nonobjc public class func fetchRequest() -> NSFetchRequest<User> {
        return NSFetchRequest<User>(entityName: "User")
    }
}
```

### 8.2 CRUD 操作

```swift
class CoreDataManager {
    static let shared = CoreDataManager()
    
    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "MyApp")
        container.loadPersistentStores { _, error in
            if let error = error {
                fatalError("Core Data error: \(error)")
            }
        }
        return container
    }()
    
    var context: NSManagedObjectContext {
        persistentContainer.viewContext
    }
    
    // 创建
    func createUser(name: String, email: String) -> User {
        let user = User(context: context)
        user.id = UUID()
        user.name = name
        user.email = email
        user.createdAt = Date()
        saveContext()
        return user
    }
    
    // 读取
    func fetchUsers() -> [User] {
        let request = User.fetchRequest()
        return (try? context.fetch(request)) ?? []
    }
    
    // 更新
    func updateUser(_ user: User, name: String) {
        user.name = name
        saveContext()
    }
    
    // 删除
    func deleteUser(_ user: User) {
        context.delete(user)
        saveContext()
    }
    
    // 保存
    func saveContext() {
        if context.hasChanges {
            try? context.save()
        }
    }
}
```

---

## 九、SwiftData

### 9.1 SwiftData 模型

```swift
import SwiftData

@Model
class User {
    var id: UUID
    var name: String
    var email: String
    var createdAt: Date
    
    @Relationship(deleteRule: .cascade)
    var posts: [Post]
    
    init(name: String, email: String) {
        self.id = UUID()
        self.name = name
        self.email = email
        self.createdAt = Date()
        self.posts = []
    }
}

@Model
class Post {
    var title: String
    var content: String
    var createdAt: Date
    
    var author: User?
    
    init(title: String, content: String) {
        self.title = title
        self.content = content
        self.createdAt = Date()
    }
}
```

### 9.2 SwiftData CRUD

```swift
import SwiftUI
import SwiftData

struct UserListView: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var users: [User]
    
    var body: some View {
        List(users) { user in
            Text(user.name)
        }
        .toolbar {
            Button("Add") {
                let user = User(name: "John", email: "john@example.com")
                modelContext.insert(user)
            }
        }
    }
    
    func deleteUser(_ user: User) {
        modelContext.delete(user)
    }
}
```

---

## 相关条目

- [[Swift]]
- [[SwiftUI与iOS开发]]
- [[AppArchitecture]]

## 参考资源

1. Apple. "Core Animation Documentation." developer.apple.com
2. Apple. "Core Location Documentation." developer.apple.com
3. Apple. "MapKit Documentation." developer.apple.com
4. Apple. "HealthKit Documentation." developer.apple.com
5. Apple. "AVFoundation Documentation." developer.apple.com
6. Apple. "SwiftData Documentation." developer.apple.com
