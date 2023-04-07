
Jenkins 环境搭建

## Master
### 前置依赖
- 安装 Java
  - java 8 或 java 11
- 准备外网权限或代理

### 安装 Jenkins Server
参考官网, 有[多种安装方式](https://www.jenkins.io/doc/book/installing/)  
这里使用的是 [war-files](https://www.jenkins.io/doc/book/installing/war-file/#war-files)的安装方式，原因是方便迁移及升级可控

具体操作，以`centos7` 为例说明如下
1. 设置工作目录的环境变量 `JENKINS_HOME`
  ```sh
  export JENKINS_HOME=/data/home/jenkins/.jenkins
  ```
2. 下载[稳定版本](https://get.jenkins.io/war-stable/) `jenkins.war`包, 放在 `$JENKINS_HOME` 目录下
3. 写入配置文件到 `/etc/sysconfig/jenkins` 如下：
  ```ini
  #jenkins system configuration
  JENKINS_HOME=/data/jenkins_home/.jenkins   # 工作目录，可自定义
  JENKINS_USER=root                          # 启动用户
  JENKINS_LOG=/data/jenkins_home/jenkins.log # 日志文件，可自定义
  JENKINS_JAVA=/usr/bin/java                 # 安装的 java路径
  JENKINS_JAVAOPTS="-Dorg.apache.commons.jelly.tags.fmt.timeZone=Asia/Shanghai -Duser.timezone=Asia/Shanghai -Dfile.encoding=UTF-8 -Djava.awt.headless=true -Dhudson.model.DirectoryBrowserSupport.CSP= "
  JENKINS_IP=0.0.0.0                         # socket ip
  JENKINS_PORT=8000                          # socket port
  ```
4. 编写启动脚本 `start-jenkins.sh`, 放到 `$JENKINS_HOME` 目录下
```sh
#!/bin/bash

# import sysconfig settings and set defaults
[ -f /etc/sysconfig/jenkins ] && . /etc/sysconfig/jenkins

JENKINS_WAR=${JENKINS_HOME}/jenkins.war

$JENKINS_JAVA $JENKINS_JAVAOPTS -jar $JENKINS_WAR --httpListenAddress=$JENKINS_IP --httpPort=$JENKINS_PORT $> $JENKINS_LOG 2>&1 &
```
5. 编写停止脚本 `stop-jenkins.sh`
  ```sh
  #!/bin/bash
  kill `ps -ef | grep [j]enkins.war | awk '{ print $2 }'`
  ```
6. 配置 jenkins服务
  -  编写 `jenkins.service`如下
  ```ini
  [Unit]
  Description=start jenkins server on satrtup
  After=network.target
  
  [Service]
  User=root
  EnvironmentFile=/etc/sysconfig/jenkins
  ExecStart=/bin/bash ${JENKINS_HOME}/start-jenkins.sh
  Restart=on-abort
  
  [Install]
  WantedBy=multi-user.target
  ```
7. 服务操作
  ```sh
  #启动服务
  sudo systemctl start jenkins
  #查看服务
  sudo systemctl status jenkins
  #停止服务
  sudo systemctl stop jenkins
  #设置开机自启
  sudo systemctl enable jenkins
  #取消开机自启
  sudo systemctl disable jenkins
  ```

### 配置 Jenkins Server
如果是首次使用，安装必要的插件手动配置

#### 从备份安装
有两种方式，推荐第一种
1. 将已有机器的 `$JENKINS_HOME`目录，打包拷贝过去启动即可
2. 拷贝 thinBackup的备份，安装 thinBackup插件，恢复备份
