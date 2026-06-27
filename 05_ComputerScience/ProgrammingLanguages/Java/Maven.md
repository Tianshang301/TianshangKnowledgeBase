---
aliases: [Maven]
tags: ['ProgrammingLanguages', 'Java', 'Maven']
created: 2026-05-16
updated: 2026-05-13
---

# Maven 构建工具

## pom.xml 结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>My Application</name>
    <description>示例项目</description>
</project>
```

### 坐标（GAV）

| 元素 | 说明 | 示例 |
|------|------|------|
| groupId | 组织标识（通常为域名倒置） | com.example |
| artifactId | 项目标识 | my-app |
| version | 版本号 | 1.0.0-SNAPSHOT |
| packaging | 打包方式 | jar, war, pom |

### 版本号约定

```
<major>.<minor>.<patch>-<qualifier>

1.0.0-SNAPSHOT    # 开发版
1.0.0-ALPHA       # 内部测试
1.0.0-BETA        # 公测
1.0.0-M1          # 里程碑
1.0.0-RELEASE     # 发布版
```

## 依赖管理

### 基本依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <version>3.2.0</version>
    </dependency>

    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>1.18.30</version>
        <scope>provided</scope>
    </dependency>

    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### Scope（作用域）

| Scope | 编译 | 测试 | 运行 | 说明 |
|-------|------|------|------|------|
| compile | ✓ | ✓ | ✓ | 默认，所有阶段可用 |
| provided | ✓ | ✓ | - | 运行时由 JDK/容器提供（如 Servlet API） |
| runtime | - | ✓ | ✓ | 运行时需要（如 JDBC 驱动） |
| test | - | ✓ | - | 仅测试阶段（如 JUnit） |
| system | ✓ | ✓ | - | 类似 provided，需指定 systemPath |

### 传递依赖

```
A ──> B（compile）──> C（compile）
A 自动依赖 C

A ──> B（compile）──> C（test）
A 不依赖 C（test 非传递）
```

### 依赖排除

```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>some-library</artifactId>
    <version>1.0</version>
    <exclusions>
        <exclusion>
            <groupId>commons-logging</groupId>
            <artifactId>commons-logging</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

### BOM（Bill of Materials）

```xml
<!-- 在父 pom 或 dependencyManagement 中导入 BOM -->

<!-- 方式一：通过 parent -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<!-- 方式二：通过 BOM import -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>2023.0.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

## 构建生命周期

### 三套生命周期

```
clean lifecycle（清理）
  pre-clean → clean → post-clean

default lifecycle（构建）
  validate → compile → test → package → verify → install → deploy

site lifecycle（站点）
  pre-site → site → post-site → site-deploy
```

### 常用命令

```bash
mvn clean                      # 清理 target 目录
mvn compile                    # 编译源码
mvn test                       # 运行测试
mvn package                    # 打包（jar/war）
mvn install                    # 安装到本地仓库
mvn deploy                     # 部署到远程仓库
mvn clean install              # 清理后构建
mvn clean install -DskipTests  # 跳过测试
mvn clean install -U           # 强制更新快照
mvn test -Dtest=MyTest         # 运行单个测试
mvn dependency:tree            # 查看依赖树
mvn dependency:analyze         # 分析未使用的依赖
```

### Phase 与 Plugin Goal 绑定

```
compile phase ──> compiler:compile
test phase    ──> surefire:test
package phase ──> jar:jar (或 war:war)
install phase ──> install:install
deploy phase  ──> deploy:deploy
```

## Profiles

```xml
<profiles>
    <profile>
        <id>dev</id>
        <activation>
            <activeByDefault>true</activeByDefault>
        </activation>
        <properties>
            <env>development</env>
            <db.url>jdbc:h2:mem:test</db.url>
        </properties>
    </profile>

    <profile>
        <id>prod</id>
        <properties>
            <env>production</env>
            <db.url>jdbc:postgresql://prod-db:5432/mydb</db.url>
        </properties>
    </profile>

    <profile>
        <id>jdk17</id>
        <activation>
            <jdk>17</jdk>
        </activation>
        <build>
            <plugins>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <configuration>
                        <release>17</release>
                    </configuration>
                </plugin>
            </plugins>
        </build>
    </profile>
</profiles>
```

```bash
# 激活 profile
mvn clean install -Pprod
mvn clean install -Pdev,test

# 查看当前生效的 profile
mvn help:active-profiles
```

## 多模块项目

### 父 POM

```xml
<!-- parent/pom.xml -->
<groupId>com.example</groupId>
<artifactId>parent</artifactId>
<version>1.0.0</version>
<packaging>pom</packaging>

<modules>
    <module>common</module>
    <module>api</module>
    <module>service</module>
    <module>web</module>
</modules>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>3.2.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### 子模块

```xml
<!-- service/pom.xml -->
<parent>
    <groupId>com.example</groupId>
    <artifactId>parent</artifactId>
    <version>1.0.0</version>
</parent>

<artifactId>service</artifactId>

<dependencies>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>common</artifactId>
        <version>${project.version}</version>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter</artifactId>
    </dependency>
</dependencies>
```

### 模块间依赖

```
common（工具类、DTO）
  └── api（接口定义）
        └── service（业务逻辑）
              └── web（REST 控制器）
```

## 常用插件

### maven-compiler-plugin

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.11.0</version>
    <configuration>
        <source>17</source>
        <target>17</target>
        <encoding>UTF-8</encoding>
        <parameters>true</parameters>
        <annotationProcessorPaths>
            <path>
                <groupId>org.projectlombok</groupId>
                <artifactId>lombok</artifactId>
                <version>1.18.30</version>
            </path>
        </annotationProcessorPaths>
    </configuration>
</plugin>
```

### maven-surefire-plugin（测试）

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>3.1.2</version>
    <configuration>
        <includes>
            <include>**/*Test.java</include>
            <include>**/*Tests.java</include>
        </includes>
        <excludes>
            <exclude>**/*IntegrationTest.java</exclude>
        </excludes>
        <forkCount>4</forkCount>
        <reuseForks>true</reuseForks>
    </configuration>
</plugin>
```

### maven-shade-plugin（Fat JAR）

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>3.5.0</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>shade</goal>
            </goals>
            <configuration>
                <transformers>
                    <transformer implementation=
                        "org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                        <mainClass>com.example.Main</mainClass>
                    </transformer>
                </transformers>
                <filters>
                    <filter>
                        <artifact>*:*</artifact>
                        <excludes>
                            <exclude>META-INF/*.SF</exclude>
                            <exclude>META-INF/*.DSA</exclude>
                            <exclude>META-INF/*.RSA</exclude>
                        </excludes>
                    </filter>
                </filters>
            </configuration>
        </execution>
    </executions>
</plugin>
```

### maven-assembly-plugin（自定义打包）

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-assembly-plugin</artifactId>
    <version>3.6.0</version>
    <configuration>
        <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
        </descriptorRefs>
        <archive>
            <manifest>
                <mainClass>com.example.Main</mainClass>
            </manifest>
        </archive>
    </configuration>
    <executions>
        <execution>
            <id>make-assembly</id>
            <phase>package</phase>
            <goals>
                <goal>single</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

### spring-boot-maven-plugin

```xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <configuration>
        <excludes>
            <exclude>
                <groupId>org.projectlombok</groupId>
                <artifactId>lombok</artifactId>
            </exclude>
        </excludes>
    </configuration>
</plugin>
```

## settings.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0
          http://maven.apache.org/xsd/settings-1.0.0.xsd">

    <localRepository>D:/.m2/repository</localRepository>

    <mirrors>
        <mirror>
            <id>aliyun</id>
            <mirrorOf>central</mirrorOf>
            <name>阿里云 Maven 镜像</name>
            <url>https://maven.aliyun.com/repository/central</url>
        </mirror>
    </mirrors>

    <profiles>
        <profile>
            <id>jdk-17</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <properties>
                <maven.compiler.source>17</maven.compiler.source>
                <maven.compiler.target>17</maven.compiler.target>
            </properties>
        </profile>
    </profiles>
</settings>
```
