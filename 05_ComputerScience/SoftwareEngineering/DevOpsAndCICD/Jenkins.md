---
aliases: [Jenkins]
tags: ['SoftwareEngineering', 'DevOpsAndCICD', 'Jenkins']
created: 2026-05-16
updated: 2026-05-16
---

# Jenkins 指南

## 一、架构

```
┌────────────────────────────────────────────┐
│              Jenkins Master                │
│  ┌────────┐ ┌────────┐ ┌────────┐         │
│  │ Web UI │ │ REST   │ │ CLI    │         │
│  │        │ │ API    │ │        │         │
│  └────────┘ └────────┘ └────────┘         │
│  ┌──────────────────────────────────┐      │
│  │        Pipeline Engine           │      │
│  └──────────────────────────────────┘      │
│  ┌────────┐ ┌────────┐ ┌────────┐         │
│  │ Job    │ │ Job    │ │ Job    │         │
│  │ Queue  │ │ Queue  │ │ Queue  │         │
│  └────────┘ └────────┘ └────────┘         │
└───────────────────┬────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
┌───▼────┐     ┌───▼────┐     ┌───▼────┐
│ Agent 1│     │ Agent 2│     │ Agent 3│
│ (Linux)│     │(Windows)│     │(macOS) │
└────────┘     └────────┘     └────────┘
```

### 安装

```bash
# Docker 安装
docker run -d \
    --name jenkins \
    -p 8080:8080 \
    -p 50000:50000 \
    -v jenkins_home:/var/jenkins_home \
    jenkins/jenkins:lts

# 获取初始密码
docker logs jenkins
# 或
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

---

## 二、Pipeline as Code

### Declarative Pipeline

```groovy
pipeline {
    agent any

    tools {
        maven 'maven-3.9'
        jdk 'jdk-21'
    }

    environment {
        APP_NAME = 'my-app'
        REGISTRY = 'registry.example.com'
    }

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: '部署分支')
        choice(name: 'ENV', choices: ['dev', 'staging', 'prod'], description: '部署环境')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'target/*.jar'
                }
            }
        }

        stage('Test') {
            parallel {
                stage('Unit Test') {
                    steps {
                        sh 'mvn test'
                    }
                }
                stage('Lint') {
                    steps {
                        sh 'mvn checkstyle:check'
                    }
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh 'deploy.sh staging'
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
                expression { params.ENV == 'prod' }
            }
            input {
                message "确认部署到生产环境?"
                ok "确认部署"
            }
            steps {
                sh 'deploy.sh production'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            emailext subject: "构建成功: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     body: "项目 ${env.JOB_NAME} 构建成功。",
                     to: 'team@example.com'
        }
        failure {
            emailext subject: "构建失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                     body: "请检查 Jenkins 查看详情。",
                     to: 'team@example.com'
        }
    }
}
```

### Scripted Pipeline

```groovy
node('linux') {
    try {
        stage('Checkout') {
            checkout scm
        }

        stage('Build') {
            docker.image('node:18-alpine').inside {
                sh 'npm ci'
                sh 'npm run build'
            }
        }

        stage('Test') {
            parallel(
                unit: {
                    sh 'npm run test:unit'
                },
                integration: {
                    sh 'npm run test:integration'
                }
            )
        }

        stage('Archive') {
            stash includes: 'dist/**', name: 'build'
        }
    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        throw e
    } finally {
        cleanWs()
    }
}
```

---

## 三、Jenkinsfile 结构

### agent

```groovy
pipeline {
    // 在任何可用 agent 上运行
    agent any

    // 指定标签
    agent { label 'linux && docker' }

    // Docker 容器
    agent {
        docker {
            image 'node:18-alpine'
            args '-v /cache:/cache'
        }
    }

    // 不同 stage 使用不同 agent
    stages {
        stage('Build') {
            agent { label 'linux' }
            steps {
                sh 'build'
            }
        }
        stage('Test on Windows') {
            agent { label 'windows' }
            steps {
                bat 'test.bat'
            }
        }
    }
}
```

### stages / steps

```groovy
pipeline {
    stages {
        stage('Parallel') {
            parallel {
                stage('Task 1') {
                    steps {
                        echo '任务 1'
                    }
                }
                stage('Task 2') {
                    steps {
                        echo '任务 2'
                    }
                }
                stage('Task 3') {
                    steps {
                        echo '任务 3'
                    }
                }
            }
        }

        stage('Matrix') {
            matrix {
                axes {
                    axis {
                        name 'OS'
                        values 'linux', 'windows'
                    }
                    axis {
                        name 'BROWSER'
                        values 'chrome', 'firefox'
                    }
                }
                stages {
                    stage('Test') {
                        steps {
                            echo "测试 ${OS} ${BROWSER}"
                        }
                    }
                }
            }
        }
    }
}
```

### post

```groovy
pipeline {
    post {
        always {
            cleanWs()
            junit 'target/**/*.xml'
        }
        success {
            echo '构建成功！'
        }
        failure {
            echo '构建失败！'
            slackSend(
                channel: '#ci-cd',
                color: 'danger',
                message: "构建失败: ${env.BUILD_URL}"
            )
        }
        unstable {
            echo '构建不稳定'
        }
        changed {
            echo '状态相比上次构建发生变化'
        }
    }
}
```

---

## 四、凭证管理

```groovy
pipeline {
    environment {
        DOCKER_CREDS = credentials('docker-hub-creds')
    }

    stages {
        stage('Docker Login') {
            steps {
                sh """
                    echo "${DOCKER_CREDS_PSW}" | docker login \
                        -u "${DOCKER_CREDS_USR}" --password-stdin
                """
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'deploy-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    ),
                    string(
                        credentialsId: 'api-token',
                        variable: 'API_TOKEN'
                    )
                ]) {
                    sh """
                        ssh -i ${SSH_KEY} ${SSH_USER}@host 'deploy.sh'
                        curl -H "Authorization: Bearer ${API_TOKEN}" https://api.example.com/deploy
                    """
                }
            }
        }
    }
}
```

---

## 五、共享库

### 目录结构

```
jenkins-shared-library/
├── vars/
│   ├── buildDockerImage.groovy
│   ├── deployToK8s.groovy
│   └── sendNotification.groovy
├── src/
│   └── com/example/
│       └── PipelineUtils.groovy
└── resources/
    └── templates/
        └── email.html
```

### 定义共享库

```groovy
// vars/buildDockerImage.groovy
def call(String imageName, String tag = 'latest') {
    sh """
        docker build -t ${imageName}:${tag} .
        docker tag ${imageName}:${tag} registry.example.com/${imageName}:${tag}
        docker push registry.example.com/${imageName}:${tag}
    """
}
```

```groovy
// vars/deployToK8s.groovy
def call(String namespace, String deployment, Map config = [:]) {
    withKubeConfig(caCertificate: '', serverUrl: 'https://k8s.example.com') {
        sh """
            kubectl set image deployment/${deployment} \
                ${deployment}=${config.image}:${config.tag} \
                -n ${namespace}
            kubectl rollout status deployment/${deployment} -n ${namespace}
        """
    }
}
```

### 使用共享库

```groovy
// Jenkinsfile
@Library('my-shared-library') _

pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                buildDockerImage('my-app', env.BUILD_NUMBER)
            }
        }
        stage('Deploy') {
            steps {
                deployToK8s('production', 'my-app', [
                    image: 'my-app',
                    tag: env.BUILD_NUMBER
                ])
            }
        }
    }
    post {
        success {
            sendNotification('success', '部署成功！')
        }
    }
}
```

---

## 六、JCasC (Jenkins Configuration as Code)

```yaml
# jenkins.yaml
jenkins:
  systemMessage: "Jenkins 由 JCasC 管理"

  securityRealm:
    local:
      allowsSignup: false
      users:
        - id: "admin"
          password: "${ADMIN_PASSWORD}"

  authorizationStrategy:
    globalMatrix:
      permissions:
        - "Overall/Administer:admin"
        - "Overall/Read:authenticated"

  numExecutors: 2

  clouds:
    - docker:
        dockerApi:
          dockerHost:
            uri: "unix:///var/run/docker.sock"
        templates:
          - labelString: "docker-agent"
            dockerTemplateBase:
              image: "jenkins/agent:latest"
            removeVolumes: true

jobs:
  - file: "jobs/*.xml"

credentials:
  system:
    domainCredentials:
      - credentials:
          - usernamePassword:
              scope: GLOBAL
              id: "gitlab-creds"
              username: "${GITLAB_USERNAME}"
              password: "${GITLAB_PASSWORD}"

unclassified:
  location:
    url: "https://jenkins.example.com"
```

```bash
# 应用配置
java -jar jenkins-cli.jar -s http://localhost:8080 apply-system-config < jenkins.yaml
```

## 相关条目

- [[CI-CD 与 DevOps 实践]]
- [[Pipeline]]
- [[GitHubActions]]
- [[Dockerfile]]
- [[K8s]]

