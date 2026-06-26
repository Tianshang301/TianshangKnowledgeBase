---
aliases: [CMake]
tags: ['ProgrammingLanguages', 'C_Cpp', 'CMake']
---

# CMake 构建系统

## CMakeLists.txt 基础

### 最小示例

```cmake
cmake_minimum_required(VERSION 3.16)

project(MyProject VERSION 1.0.0 LANGUAGES CXX)

add_executable(myapp main.cpp utils.cpp)
```

### 库与可执行文件

```cmake
# 可执行文件
add_executable(server server.cpp)

# 静态库
add_library(common STATIC common.cpp logger.cpp)

# 动态库
add_library(network SHARED tcp.cpp http.cpp)

# 对象库（不链接，仅编译）
add_library(core OBJECT parser.cpp compiler.cpp)
```

### 项目结构

```
project/
├── CMakeLists.txt          # 顶层
├── src/
│   ├── CMakeLists.txt      # 源码
│   └── main.cpp
├── libs/
│   ├── common/
│   │   ├── CMakeLists.txt
│   │   └── utils.cpp
│   └── network/
│       ├── CMakeLists.txt
│       └── socket.cpp
└── tests/
    ├── CMakeLists.txt
    └── test_main.cpp
```

```cmake
# 顶层 CMakeLists.txt
cmake_minimum_required(VERSION 3.16)
project(MyApp VERSION 1.0.0)

add_subdirectory(libs/common)
add_subdirectory(libs/network)
add_subdirectory(src)
add_subdirectory(tests)
```

## Targets 与属性

```cmake
add_library(mylib STATIC source.cpp)

# 设置目标属性
set_target_properties(mylib PROPERTIES
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    POSITION_INDEPENDENT_CODE ON
)

# 获取目标属性
get_target_property(standard mylib CXX_STANDARD)

# 接口属性
target_compile_features(mylib PUBLIC cxx_std_20)
target_include_directories(mylib PUBLIC include)
```

## 依赖管理

```cmake
# 链接库
target_link_libraries(myapp
    PRIVATE
        common
        network
    PUBLIC
        fmt
)

# 包含目录
target_include_directories(myapp
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
    PUBLIC
        $<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)

# 编译定义
target_compile_definitions(myapp
    PRIVATE
        APP_VERSION="${PROJECT_VERSION}"
    PUBLIC
        USE_SSL
)
```

### 传递性

```
target A (PUBLIC include) ──> target B (PRIVATE include A)
                                   ↓ PUBLIC
                              target C (gets A's include too)

target D (PRIVATE include) ──> target E
                                   ↓ PRIVATE
                              target F (does NOT get D's include)
```

## 变量与选项

```cmake
# 普通变量
set(PROJECT_VERSION_MAJOR 1)
set(PROJECT_VERSION_MINOR 0)
set(SOURCES main.cpp utils.cpp parser.cpp)

# 缓存变量（可由用户设置）
set(BUILD_SHARED_LIBS ON CACHE BOOL "Build shared libraries")
set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type")

# 选项
option(ENABLE_TESTS "Build tests" ON)
option(ENABLE_OPENSSL "Enable OpenSSL support" OFF)

if(ENABLE_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

if(ENABLE_OPENSSL)
    find_package(OpenSSL REQUIRED)
    target_link_libraries(myapp PRIVATE OpenSSL::SSL OpenSSL::Crypto)
endif()
```

### 生成器表达式

```cmake
# 条件编译
target_compile_definitions(myapp PRIVATE
    $<$<CONFIG:Debug>:DEBUG_BUILD>
    $<$<CONFIG:Release>:NDEBUG>
)

# 平台相关
target_sources(myapp PRIVATE
    $<$<PLATFORM_ID:Windows>:win_socket.cpp>
    $<$<PLATFORM_ID:Linux>:linux_socket.cpp>
)

# 编译器相关
target_compile_options(myapp PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
    $<$<CXX_COMPILER_ID:GNU>:-Wall -Wextra>
)
```

## 生成器（Generators）

| Generator | 平台 | 构建工具 |
|-----------|------|---------|
| Visual Studio 17 2022 | Windows | MSBuild |
| Ninja | 跨平台 | Ninja |
| MinGW Makefiles | Windows | mingw32-make |
| Unix Makefiles | Linux/macOS | make |

```bash
# Visual Studio
cmake -B build -G "Visual Studio 17 2022" -A x64

# Ninja
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release

# 构建
cmake --build build --config Release
cmake --build build --target myapp
cmake --build build -j8
```

## find_package

```cmake
# 查找包（Config 模式）
find_package(OpenCV REQUIRED)
target_link_libraries(myapp PRIVATE ${OpenCV_LIBS})

# 查找包（Module 模式）
find_package(Threads REQUIRED)
target_link_libraries(myapp PRIVATE Threads::Threads)

# 手动查找库
find_library(JPEG_LIB jpeg REQUIRED)
find_path(JPEG_INCLUDE jpeglib.h REQUIRED)

target_include_directories(myapp PRIVATE ${JPEG_INCLUDE})
target_link_libraries(myapp PRIVATE ${JPEG_LIB})
```

### 编写 Find 模块

```cmake
# cmake/FindMyLib.cmake
find_path(MYLIB_INCLUDE_DIR mylib.h
    PATHS /usr/local/include /opt/local/include
)

find_library(MYLIB_LIBRARY mylib
    PATHS /usr/local/lib /opt/local/lib
)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(MyLib
    REQUIRED_VARS MYLIB_LIBRARY MYLIB_INCLUDE_DIR
)

if(MyLib_FOUND AND NOT TARGET MyLib::MyLib)
    add_library(MyLib::MyLib UNKNOWN IMPORTED)
    set_target_properties(MyLib::MyLib PROPERTIES
        IMPORTED_LOCATION ${MYLIB_LIBRARY}
        INTERFACE_INCLUDE_DIRECTORIES ${MYLIB_INCLUDE_DIR}
    )
endif()

mark_as_advanced(MYLIB_INCLUDE_DIR MYLIB_LIBRARY)
```

## FetchContent

```cmake
include(FetchContent)

# 从 Git 获取依赖
FetchContent_Declare(
    fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG 10.1.0
)

FetchContent_Declare(
    nlohmann_json
    URL https://github.com/nlohmann/json/releases/download/v3.11.2/json.hpp
)

FetchContent_MakeAvailable(fmt nlohmann_json)

target_link_libraries(myapp PRIVATE fmt::fmt nlohmann_json::nlohmann_json)
```

## 多配置支持

```cmake
# 设置编译类型
set(CMAKE_CONFIGURATION_TYPES "Debug;Release;RelWithDebInfo" CACHE STRING "")

# 不同配置的不同编译选项
target_compile_options(myapp PRIVATE
    $<$<CONFIG:Debug>:/Od /Zi>
    $<$<CONFIG:Release>:/O2 /GL>
)

target_link_options(myapp PRIVATE
    $<$<CONFIG:Debug>:/DEBUG>
    $<$<CONFIG:Release>:/LTCG>
)
```

## 安装规则

```cmake
# 安装可执行文件
install(TARGETS myapp
    RUNTIME DESTINATION bin
)

# 安装库
install(TARGETS common network
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# 安装头文件
install(DIRECTORY include/
    DESTINATION include
    FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp"
)

# 安装配置文件（供其他项目 find_package 使用）
install(EXPORT MyAppTargets
    FILE MyAppTargets.cmake
    NAMESPACE MyApp::
    DESTINATION lib/cmake/MyApp
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/MyAppConfig.cmake
    DESTINATION lib/cmake/MyApp
)
```

## CPack

```cmake
# 打包配置
set(CPACK_PACKAGE_NAME "MyApp")
set(CPACK_PACKAGE_VERSION "${PROJECT_VERSION}")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "My Application")
set(CPACK_PACKAGE_VENDOR "Example Corp")

# Windows 安装器
set(CPACK_GENERATOR "NSIS")
set(CPACK_NSIS_DISPLAY_NAME "MyApp")
set(CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES")

# Linux 包
set(CPACK_GENERATOR "DEB;RPM")
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "dev@example.com")
set(CPACK_DEBIAN_PACKAGE_SECTION "devel")

include(CPack)
```

```bash
# 生成包
cpack
cpack -G NSIS
cpack -G DEB
```

## 完整示例

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.16)
project(WebServer VERSION 1.0.0 LANGUAGES CXX)

# C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 选项
option(BUILD_TESTS "Build tests" ON)
option(ENABLE_SSL "Enable SSL support" OFF)

# 查找依赖
find_package(Threads REQUIRED)

if(ENABLE_SSL)
    find_package(OpenSSL REQUIRED)
endif()

# 源码
set(SOURCES
    src/main.cpp
    src/server.cpp
    src/http_parser.cpp
    src/route_handler.cpp
)

# 头文件
set(PUBLIC_HEADERS
    include/server.h
    include/http_parser.h
)

# 创建库
add_library(webserver STATIC ${SOURCES} ${PUBLIC_HEADERS})
target_include_directories(webserver
    PUBLIC include
    PRIVATE src
)
target_link_libraries(webserver PUBLIC Threads::Threads)

if(ENABLE_SSL)
    target_compile_definitions(webserver PRIVATE ENABLE_SSL)
    target_link_libraries(webserver PUBLIC OpenSSL::SSL OpenSSL::Crypto)
endif()

# 可执行文件
add_executable(webserver_app src/main.cpp)
target_link_libraries(webserver_app PRIVATE webserver)

# 测试
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# 安装
install(TARGETS webserver webserver_app
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)
install(FILES ${PUBLIC_HEADERS} DESTINATION include/webserver)
```
