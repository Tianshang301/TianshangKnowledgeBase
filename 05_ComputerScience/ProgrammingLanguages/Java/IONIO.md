---
aliases: [IONIO]
tags: ['ProgrammingLanguages', 'Java', 'IONIO']
created: 2026-05-16
updated: 2026-05-16
---

# Java I/O 与 NIO

## I/O 流体系

### 字节流（InputStream / OutputStream）

```
InputStream
  ├── FileInputStream
  ├── BufferedInputStream
  ├── DataInputStream
  ├── ObjectInputStream
  └── ByteArrayInputStream

OutputStream
  ├── FileOutputStream
  ├── BufferedOutputStream
  ├── DataOutputStream
  ├── ObjectOutputStream
  └── ByteArrayOutputStream
```

### 字符流（Reader / Writer）

```
Reader
  ├── FileReader
  ├── BufferedReader
  ├── InputStreamReader
  └── StringReader

Writer
  ├── FileWriter
  ├── BufferedWriter
  ├── OutputStreamWriter
  └── StringWriter
```

## 文件读写

### 字节流读写

```java
// 写入文件
try (FileOutputStream fos = new FileOutputStream("output.dat")) {
    byte[] data = "Hello World".getBytes(StandardCharsets.UTF_8);
    fos.write(data);
}

// 读取文件
try (FileInputStream fis = new FileInputStream("output.dat")) {
    byte[] buffer = new byte[1024];
    int bytesRead;
    while ((bytesRead = fis.read(buffer)) != -1) {
        System.out.write(buffer, 0, bytesRead);
    }
}
```

### 字符流读写

```java
// 写入文件
try (FileWriter fw = new FileWriter("output.txt", StandardCharsets.UTF_8)) {
    fw.write("Hello 世界");
}

// 读取文件
try (FileReader fr = new FileReader("output.txt", StandardCharsets.UTF_8)) {
    int ch;
    while ((ch = fr.read()) != -1) {
        System.out.print((char) ch);
    }
}
```

### 带缓冲的读写

```java
// 高效读取文本文件
try (BufferedReader br = new BufferedReader(new FileReader("large.txt"))) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
}

// 高效写入文本文件
try (BufferedWriter bw = new BufferedWriter(new FileWriter("output.txt"))) {
    bw.write("第一行");
    bw.newLine();
    bw.write("第二行");
    bw.newLine();
}
```

### InputStreamReader / OutputStreamWriter（字节与字符桥接）

```java
// 指定编码读写
try (BufferedReader br = new BufferedReader(
        new InputStreamReader(new FileInputStream("input.txt"), "UTF-8"))) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
}

try (BufferedWriter bw = new BufferedWriter(
        new OutputStreamWriter(new FileOutputStream("output.txt"), "UTF-8"))) {
    bw.write("中文内容");
}
```

## 序列化

### Serializable

```java
public class User implements Serializable {
    private static final long serialVersionUID = 1L;

    private Long id;
    private String name;
    private transient String password;  // transient 字段不被序列化
    private static String staticField;   // 静态字段不被序列化

    // getters and setters
}
```

```java
// 序列化
try (ObjectOutputStream oos = new ObjectOutputStream(
        new FileOutputStream("user.ser"))) {
    User user = new User(1L, "Alice", "secret123");
    oos.writeObject(user);
}

// 反序列化
try (ObjectInputStream ois = new ObjectInputStream(
        new FileInputStream("user.ser"))) {
    User user = (User) ois.readObject();
    System.out.println(user.getName());  // Alice
    System.out.println(user.getPassword());  // null（transient）
}
```

### Externalizable

自定义序列化逻辑，比 Serializable 更高效。

```java
public class User implements Externalizable {
    private Long id;
    private String name;

    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        out.writeLong(id);
        out.writeUTF(name);
    }

    @Override
    public void readExternal(ObjectInput in) throws IOException, ClassNotFoundException {
        this.id = in.readLong();
        this.name = in.readUTF();
    }
}
```

### serialVersionUID

```java
// 显式声明 UID
private static final long serialVersionUID = 1L;

// 不声明则 JVM 根据类结构自动生成
// 类结构变更后 UID 会变化，导致反序列化失败
```

## NIO（New I/O）

### Buffer（缓冲区）

```
Buffer 常用类型：
  ByteBuffer
  CharBuffer
  IntBuffer
  LongBuffer
  FloatBuffer
  DoubleBuffer
  ShortBuffer
```

```java
// 创建 Buffer
ByteBuffer buffer = ByteBuffer.allocate(1024);
ByteBuffer directBuffer = ByteBuffer.allocateDirect(1024);  // 直接内存

// 写数据
buffer.put((byte) 'H');
buffer.put("ello".getBytes());

// 翻转（从写模式切换到读模式）
buffer.flip();

// 读数据
while (buffer.hasRemaining()) {
    System.out.print((char) buffer.get());
}

// 重置
buffer.rewind();    // 重新读取
buffer.clear();     // 清空缓冲区
buffer.compact();   // 压缩（保留未读数据）

// Buffer 属性
buffer.position();   // 当前位置
buffer.limit();      // 界限
buffer.capacity();   // 容量
```

### Channel（通道）

```java
// FileChannel
try (FileChannel fileChannel = FileChannel.open(
        Path.of("input.txt"), StandardOpenOption.READ)) {
    ByteBuffer buf = ByteBuffer.allocate(1024);
    while (fileChannel.read(buf) != -1) {
        buf.flip();
        while (buf.hasRemaining()) {
            System.out.print((char) buf.get());
        }
        buf.clear();
    }
}

// 文件复制
try (FileChannel in = FileChannel.open(Path.of("source.txt"), StandardOpenOption.READ);
     FileChannel out = FileChannel.open(Path.of("dest.txt"),
         StandardOpenOption.WRITE, StandardOpenOption.CREATE)) {
    in.transferTo(0, in.size(), out);  // 零拷贝
}
```

### Selector（选择器）

```java
Selector selector = Selector.open();
ServerSocketChannel serverChannel = ServerSocketChannel.open();
serverChannel.configureBlocking(false);
serverChannel.bind(new InetSocketAddress(8080));
serverChannel.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    int readyChannels = selector.select();  // 阻塞直到有事件
    if (readyChannels == 0) continue;

    Set<SelectionKey> selectedKeys = selector.selectedKeys();
    Iterator<SelectionKey> it = selectedKeys.iterator();

    while (it.hasNext()) {
        SelectionKey key = it.next();
        it.remove();

        if (key.isAcceptable()) {
            handleAccept(key);
        } else if (key.isReadable()) {
            handleRead(key);
        } else if (key.isWritable()) {
            handleWrite(key);
        }
    }
}
```

### Path / Files API（NIO.2）

```java
// Path 操作
Path path = Path.of("dir", "subdir", "file.txt");
Path absolute = path.toAbsolutePath();
Path normalized = path.normalize();
Path parent = path.getParent();
Path filename = path.getFileName();

// Files 工具类
Path source = Path.of("source.txt");
Path target = Path.of("target.txt");

// 读写
String content = Files.readString(source, StandardCharsets.UTF_8);
Files.writeString(target, content, StandardCharsets.UTF_8);

byte[] bytes = Files.readAllBytes(source);
List<String> lines = Files.readAllLines(source);
Files.write(target, lines);

// 文件操作
Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
Files.move(source, target, StandardCopyOption.REPLACE_EXISTING);
Files.delete(target);
Files.createDirectories(Path.of("a/b/c"));

// 文件属性
Files.exists(path);
Files.isDirectory(path);
Files.isRegularFile(path);
Files.size(path);
Files.getLastModifiedTime(path);

// 目录遍历
try (Stream<Path> stream = Files.walk(Path.of("dir"))) {
    stream.filter(Files::isRegularFile)
          .forEach(System.out::println);
}

// 目录监听（WatchService）
try (WatchService watcher = FileSystems.getDefault().newWatchService()) {
    Path dir = Path.of(".");
    dir.register(watcher, StandardWatchEventKinds.ENTRY_CREATE,
                         StandardWatchEventKinds.ENTRY_MODIFY);

    WatchKey key = watcher.take();
    for (WatchEvent<?> event : key.pollEvents()) {
        System.out.println(event.context() + " was " + event.kind());
    }
}
```

### 异步 I/O（AsynchronousFileChannel）

```java
// Future 方式
try (AsynchronousFileChannel channel = AsynchronousFileChannel.open(
        Path.of("input.txt"), StandardOpenOption.READ)) {
    ByteBuffer buffer = ByteBuffer.allocate(1024);
    Future<Integer> result = channel.read(buffer, 0);
    int bytesRead = result.get();  // 阻塞等待
    buffer.flip();
}

// CompletionHandler 方式
try (AsynchronousFileChannel channel = AsynchronousFileChannel.open(
        Path.of("input.txt"), StandardOpenOption.READ)) {
    ByteBuffer buffer = ByteBuffer.allocate(1024);
    channel.read(buffer, 0, buffer, new CompletionHandler<Integer, ByteBuffer>() {
        @Override
        public void completed(Integer result, ByteBuffer attachment) {
            attachment.flip();
            System.out.println(StandardCharsets.UTF_8.decode(attachment));
        }

        @Override
        public void failed(Throwable exc, ByteBuffer attachment) {
            exc.printStackTrace();
        }
    });
    Thread.sleep(1000);  // 等待异步完成
}
```

## NIO vs IO 对比

| 特性 | IO（BIO） | NIO |
|------|-----------|-----|
| 模型 | 阻塞 I/O | 非阻塞 I/O |
| 方向 | 单向（InputStream/OutputStream） | 双向（Buffer 可读可写） |
| 核心 | Stream（流） | Buffer（缓冲区）+ Channel（通道） |
| 多路复用 | 无（每连接一线程） | Selector（单线程处理多连接） |
| 数据操作 | 面向字节/字符 | 面向缓冲区（块） |
| 适用场景 | 连接少、文件小 | 连接多、高性能场景 |
| 文件操作 | FileInputStream/FileReader | FileChannel + Files API |

```java
// BIO: 每个连接一个线程
public class BioServer {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(8080);
        while (true) {
            Socket client = serverSocket.accept();  // 阻塞
            new Thread(() -> handle(client)).start();
        }
    }
}

// NIO: 单线程处理多个连接
public class NioServer {
    public static void main(String[] args) throws IOException {
        Selector selector = Selector.open();
        ServerSocketChannel ssc = ServerSocketChannel.open();
        ssc.configureBlocking(false);
        ssc.bind(new InetSocketAddress(8080));
        ssc.register(selector, SelectionKey.OP_ACCEPT);

        while (true) {
            selector.select();  // 阻塞直到有事件
            // 处理所有就绪事件
        }
    }
}
```

### 零拷贝

```java
// 传统 IO：需要 4 次上下文切换 + 4 次拷贝
// File -> Kernel Read Buffer -> User Buffer -> Kernel Socket Buffer -> NIC

// 零拷贝（transferTo/transferFrom）：2 次上下文切换 + 2 次拷贝
FileChannel in = FileChannel.open(Path.of("input.txt"), StandardOpenOption.READ);
FileChannel out = FileChannel.open(Path.of("output.txt"),
    StandardOpenOption.WRITE, StandardOpenOption.CREATE);
in.transferTo(0, in.size(), out);
```
