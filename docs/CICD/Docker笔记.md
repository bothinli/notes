# Docker笔记

## 1. **docker命令**

### 1.1 **启动与停止**

```shell
# 启动docker
sudo service docker start

# 停止docker
sudo service docker stop

# 重启docker
sudo service docker restart

# 修改配置后重启 Docker
sudo systemctl daemon-reload
sudo systemctl restart docker

docker system df # 命令来便捷的查看镜像、容器、数据卷所占用的空间。
docker inspect 镜像名 # 获取镜像的详细信息，其中，包括创建者，各层的数字摘要等。
docker history 镜像名 # 镜像历史 查看镜像构建历史
		# 不截断输出
    --no-trunc 
```

### 1.2 **镜像命令**

列出本机Docker上已经安装的镜像:

```shell
docker images
docker image ls
```

搜索Docker hub上面的镜像

```shell
# 普通搜索,以Tomcat为例
docker search tomcat
# 搜索star大于50的镜像实例
docker search -s 50 tomcat
```

从Docker Hub上面下载镜像

```shell
# 以下载tomcat为例
docker pull tomcat[:version]
```

删除本地的某一个镜像

```shell
# 以删除tomcat为例
docker rmi tomcat[:version]
# 通过镜像ID删除
docker rmi -f 镜像ID
# 通过镜像ID删除多个
docker rmi -f 镜像名1:TAG 镜像名2:TAG 
# 删除全部
# docker images -qa : 获取所有镜像ID
docker rmi -f $(docker images -qa)
```

镜像打包与运行

```shell
#打包一个我们自己的 tomcat
docker commit -a bothin -m="package my tomcat" 要打包的镜像ID bothin/tomcat:1.0
# -a : 作者名称
# -m : 打包信息

#启动我们自己打包生成的 tomcat
docker run -it -p 7700:8080 bothin/tomcat:1.0

#这个表示docker容器在停止或服务器开机之后会自动重新启动 --restart=always
docker run -d --restart=always --name demo -p 8080:8080 my/demo 
 
```

### 1.3 **容器命令**

**启动容器**

```shell
# 新建并进入容器,最后一个为本地容器的ID  
docker run -it --name="rivercentos001" 9f38484d220f

//参数
 # 为容器启一个名称
 -name="新容器名称"
 # 后台运行容器,并返回容器ID,也就是启动守护士容器
 -d 
 # 以交互模式运行容器,通常与-t同时使用.
 -i
 # 为容器重新分配一个伪终端,通过与-i同时使用
 -t 
 # 随机端口映射 [大写P]
 -P
 # 端口映射 [小写P]
 -p
 # 数据卷 加参数 ro:容器内的目录只读,不可写
 -v /宿主机绝对路径目录:/容器内目录[:ro] 镜像名
 
 docker diff # 查看容器内部文件变化
```

**查看当前正在运行的Docker 容器**

```shell
docker ps

# 参数
    # 列出当前正在运行的以及历史上运行过的
    -a
    # 显示最近创建的容器
    -l
    # 显示最近创建的N个容器
    -n
    # 静默模式,只显示容器编号
    -q
    # 不截断输出
    --no-trunc 
```

**退出容器**

```shell
# 退出并停止
exit
# 容器不停止退出
ctrl+P+Q
```

**启动容器**

```shell
docker start 容器ID或容器name

#启动全部容器
docker start $(docker ps -qa)
```

**重启容器**

```shell
docker restart 容器ID或容器name
```

**停止**

```shell
docker stop 容器ID或容器name
```

**强制停止**

```shell
docker kill 容器ID或容器name
```

**删除容器**

```shell
# 删除已经停止的容器
docker rm 容器ID或容器name 
# 强制删除已经停止或正在运行的容器
docker rm -f  容器ID或容器name 

一次性删除所有正在运行的容器
docker rm -f $(docker ps -qa)
```

**重新进入容器**

```shell
# 第一种方式
docker attach 容器ID或容器名称
# 第二种方式{隔山打牛式,在宿主机向容器发送命令并获取结果}
docker exec -t 容器ID或容器名称 ls# 列出文件列表
# 交互
docker exec -it rivertomcat  /bin/bash
```

**从容器内拷贝文件到宿主机**

```shell
docker cp 容器ID或容器名称:/文件路径与文件名 宿主机地址
 #例：拷贝容器tomcat的aaa文件夹下的a.txt到宿主机的当前位置 
 docker cp tomcat:/aaa/a.txt .
```

### 1.4 **日志命令**

```shell
docker logs -f -t --tail 10 容器ID或容器名称
# 加入的时间戳
-t
# 跟随最新的日志打印
-f
# 输出最后几行的日志
--tail 行数



# 启动一个centos,并且每两秒在Console输出一个Hello bothin
docker run -d --name tomcat centos /bin/sh -c "while true;do echo hello bothin;sleep 2;done"
# 查看最后10行的日志
docker logs -f -t --tail 10 river

#查看容器内的进程
docker top 容器ID或容器名称
```







### 1.99 **DockerFile**

- FROM		 基础镜像,当前新镜像是基于哪个镜像的。

- MAINTAINER 	 镜像维护者的姓名和邮箱地址。

- RUN 		 容器构建时需要运行的命令。

- EXPOSE		 当前容器对外暴露出的端口。

- WORKDIR		 指定在创建容器后,终端默认登陆的进来工作目录,也不是运行并登录进来的当前目录位置。

- ENV 		 用来构建镜像过程中设置环境变量。

- ADD 		 将宿主机目录下的文件拷贝进镜像且ADD命令会自动处理URL和解压tar压缩包。

- COPY 	 类似ADD,但只是复制,不带解压压缩包的功能。

- VOLUME 	 容器数据卷,用于数据保存和持久化工作。

- CMD			 指定一个容器启动时要运行的命令,DockerFile中可以有多个CMD指令,但只有最后一个会生效执行。

- ENTRYPOINT  指定一个容器启动时要运行的命令

  ENTRYPOINT的作用和CMD一样,都是在指定容器启动程序及参数

  相当于CMD的升级版本,CMD只能执行一条命令,运行时如果加一些参数是不行的.但如果把CMD替换成ENTRYPOINT就可以在Run镜像的时候在尾部追回指令.

  简单的说如果Run镜像的时候追回了命令,CMD会用追回的覆盖掉旧的,ENTRYPOINT会追回执行。

- ONBUILD 	 当构建一个被继承的DockerFile时运行命令,父镜像在被子继承后父镜像的onbuild被触发。

```dockerfile
# 构建自己的centos
FROM centos
MAINTAINER zzyy<zzyy167@126.com>
ENV MYPATH /usr/local
WORKDIR $MYPATH
RUN yum -y install vim
RUN yum -y install net-tools
EXPOSE 80
CMD echo $MYPATH
CMD echo "success--------------ok"
CMD /bin/bash


# 制作CMD版可以查询IP信息的容器
FROM centos
RUN yum install -y curl
CMD [ "curl", "-s", "http://ip.cn" ]


# 构建自己的tomcat
FROM         centos
MAINTAINER    zzyy<zzyybs@126.com>
#把宿主机当前上下文的c.txt拷贝到容器/usr/local/路径下
COPY c.txt /usr/local/cincontainer.txt
#把java与tomcat添加到容器中
ADD jdk-8u171-linux-x64.tar.gz /usr/local/
ADD apache-tomcat-9.0.8.tar.gz /usr/local/
#安装vim编辑器
RUN yum -y install vim
#设置工作访问时候的WORKDIR路径，登录落脚点
ENV MYPATH /usr/local
WORKDIR $MYPATH
#配置java与tomcat环境变量
ENV JAVA_HOME /usr/local/jdk1.8.0_171
ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
ENV CATALINA_HOME /usr/local/apache-tomcat-9.0.8
ENV CATALINA_BASE /usr/local/apache-tomcat-9.0.8
ENV PATH $PATH:$JAVA_HOME/bin:$CATALINA_HOME/lib:$CATALINA_HOME/bin
#容器运行时监听的端口
EXPOSE  8080
#启动时运行tomcat
# ENTRYPOINT ["/usr/local/apache-tomcat-9.0.8/bin/startup.sh" ]
# CMD ["/usr/local/apache-tomcat-9.0.8/bin/catalina.sh","run"]
CMD /usr/local/apache-tomcat-9.0.8/bin/startup.sh && tail -F /usr/local/apache-tomcat-9.0.8/bin/logs/catalina.out
```

## 2. **DockerFile**

### 2.1 build 命令

使用了 `docker build` 命令进行镜像构建。其格式为：

```shell
# 上下文路径可以是本地路径、远程仓库地址、给定的 tar 压缩包
docker build [选项] <上下文路径/URL/->
```

### 2.2 镜像构建上下文

首先我们要理解 `docker build` 的工作原理。Docker 在运行时分为 Docker 引擎（也就是服务端守护进程）和客户端工具。Docker 的引擎提供了一组 REST API，被称为 [Docker Remote API](https://docs.docker.com/develop/sdk/)，而如 `docker` 命令这样的客户端工具，则是通过这组 API 与 Docker 引擎交互，从而完成各种功能。因此，虽然表面上我们好像是在本机执行各种 `docker` 功能，但实际上，一切都是使用的远程调用形式在服务端（Docker 引擎）完成。也因为这种 C/S 设计，让我们操作远程服务器的 Docker 引擎变得轻而易举。

当我们进行镜像构建的时候，并非所有定制都会通过 `RUN` 指令完成，经常会需要将一些本地文件复制进镜像，比如通过 `COPY` 指令、`ADD` 指令等。

而 `docker build` 命令构建镜像，其实并非在本地构建，而是在服务端，也就是 Docker 引擎中构建的。那么在这种客户端/服务端的架构中，如何才能让服务端获得本地文件呢？

这就引入了上下文的概念。当构建的时候，用户会指定构建镜像上下文的路径，`docker build` 命令得知这个路径后，会将路径下的所有内容打包，然后上传给 Docker 引擎。这样 Docker 引擎收到这个上下文包后，展开就会获得构建镜像所需的一切文件。

如果在 `Dockerfile` 中这么写：

```shell
COPY ./package.json /app/
```

这并不是要复制执行 `docker build` 命令所在的目录下的 `package.json`，也不是复制 `Dockerfile` 所在目录下的 `package.json`，而是复制 **上下文（context）** 目录下的 `package.json`。

因此，`COPY` 这类指令中的源文件的路径都是*相对路径*。这也是初学者经常会问的为什么 `COPY ../package.json /app` 或者 `COPY /opt/xxxx /app` 无法工作的原因，因为这些路径已经超出了上下文的范围，Docker 引擎无法获得这些位置的文件。如果真的需要那些文件，应该将它们复制到上下文目录中去。

现在就可以理解刚才的命令 `docker build -t nginx:v3 .` 中的这个 `.`，实际上是在指定上下文的目录，`docker build` 命令会将该目录下的内容打包交给 Docker 引擎以帮助构建镜像。



### 2.3 Docker指令

#### 2.3.1 COPY 复制文件

格式：

- `COPY [--chown=<user>:<group>] <源路径>... <目标路径>`
- `COPY [--chown=<user>:<group>] ["<源路径1>",... "<目标路径>"]`

`COPY` 指令将从构建上下文目录中 `<源路径>` 的文件/目录复制到新的一层的镜像内的 `<目标路径>` 位置。

`<源路径>` 可以是多个，甚至可以是通配符，其通配符规则要满足 Go 的 [`filepath.Match`](https://golang.org/pkg/path/filepath/#Match) 规则，如：

```shell
COPY hom* /mydir/
COPY hom?.txt /mydir/
```

`<目标路径>` 可以是容器内的绝对路径，也可以是相对于工作目录的相对路径（工作目录可以用 `WORKDIR` 指令来指定）。目标路径不需要事先创建，如果目录不存在会在复制文件前先行创建缺失目录。

此外，还需要注意一点，使用 `COPY` 指令，源文件的各种元数据都会保留。比如读、写、执行权限、文件变更时间等。在使用该指令的时候还可以加上 `--chown=<user>:<group>` 选项来改变文件的所属用户及所属组。

**【注】：**如果源路径为文件夹，复制的时候不是直接复制该文件夹，而是将文件夹中的内容复制到目标路径。

#### 2.3.2 ADD 更高级的复制文件

`ADD` 指令和 `COPY` 的格式和性质基本一致。但是在 `COPY` 基础上增加了一些功能。

如果 `<源路径>` 为一个 `tar` 压缩文件的话，压缩格式为 `gzip`, `bzip2` 以及 `xz` 的情况下，`ADD` 指令将会自动解压缩这个压缩文件到 `<目标路径>` 去。

在 `COPY` 和 `ADD` 指令中选择的时候，可以遵循这样的原则，所有的文件复制均使用 `COPY` 指令，仅在需要自动解压缩的场合使用 `ADD`。

在使用该指令的时候还可以加上 `--chown=<user>:<group>` 选项来改变文件的所属用户及所属组。

#### 2.3.3 RUN 执行命令

`RUN` 指令是用来执行命令行命令的。由于命令行的强大能力，`RUN` 指令在定制镜像时是最常用的指令之一。其格式有两种：

- *shell* 格式：`RUN <命令>`，就像直接在命令行中输入的命令一样。刚才写的 Dockerfile 中的 `RUN` 指令就是这种格式。
- *exec* 格式：`RUN ["可执行文件", "参数1", "参数2"]`，这更像是函数调用中的格式。



多条命令尽量放到一起执行，Dockerfile 支持 Shell 类的行尾添加 `\` 的命令换行方式，以及行首 `#` 进行注释的格式。

正确的写法应该是这样：

```shell
FROM debian:stretch


RUN set -x; buildDeps='gcc libc6-dev make wget' \
    && apt-get update \
    && apt-get install -y $buildDeps \
    && wget -O redis.tar.gz "http://download.redis.io/releases/redis-5.0.3.tar.gz" \
    && mkdir -p /usr/src/redis \
    && tar -xzf redis.tar.gz -C /usr/src/redis --strip-components=1 \
    && make -C /usr/src/redis \
    && make -C /usr/src/redis install \
    && rm -rf /var/lib/apt/lists/* \
    && rm redis.tar.gz \
    && rm -r /usr/src/redis \
    && apt-get purge -y --auto-remove $buildDeps
```

#### 2.3.4 CMD 容器启动命令

`CMD` 指令的格式和 `RUN` 相似，也是两种格式：

- `shell` 格式：`CMD <命令>`
- `exec` 格式：`CMD ["可执行文件", "参数1", "参数2"...]`
- 参数列表格式：`CMD ["参数1", "参数2"...]`。在指定了 `ENTRYPOINT` 指令后，用 `CMD` 指定具体的参数。
- **`CMD`, `ENTRYPOINT` , `HEALTHCHECK` 只可以出现一次，如果写了多个，只有最后一个生效**。

Docker 不是虚拟机，容器就是进程。既然是进程，那么在启动容器的时候，需要指定所运行的程序及参数。`CMD` 指令就是用于指定默认的容器主进程的启动命令的，在运行时可以指定新的命令来替代镜像设置中的这个默认命令。

在指令格式上，**一般推荐使用 `exec` 格式**，这类格式在解析时会被解析为 JSON 数组，因此一定要使用双引号 `"`，而不要使用单引号。

如果使用 `shell` 格式的话，实际的命令会被包装为 `sh -c` 的参数的形式进行执行。比如：

```
CMD echo $HOME
```

在实际执行中，会将其变更为：

```
CMD [ "sh", "-c", "echo $HOME" ]
```

#### 2.3.5 ENTRYPOINT 入口点

`ENTRYPOINT` 的格式和 `RUN` 指令格式一样，分为 `exec` 格式和 `shell` 格式。

`ENTRYPOINT` 的目的和 `CMD` 一样，都是在指定容器启动程序及参数。`ENTRYPOINT` 在运行时也可以替代，不过比 `CMD` 要略显繁琐，需要通过 `docker run` 的参数 `--entrypoint` 来指定。

当指定了 `ENTRYPOINT` 后，`CMD` 的含义就发生了改变，不再是直接的运行其命令，而是将 `CMD` 的内容作为参数传给 `ENTRYPOINT` 指令，换句话说实际执行时，将变为：

```
<ENTRYPOINT> "<CMD>"
```

Exec格式时,ENTRYPOINT可以通过CMD提供额外参数,CMD的额外参数可以在容器启动时动态替换。在shell格式时ENTRYPOINT会忽略任何CMD或docker run提供的参数。

```dockerfile
[root@server1 docker]# vim Dockerfile 
文件编辑内容如下：
FROM busybox
ENTRYPOINT ["/bin/echo", "hello"]
CMD ["world"] # 可以动态替换这部分
```



#### 2.3.6 ENV 设置环境变量

格式有两种：

- `ENV <key> <value>`
- `ENV <key1>=<value1> <key2>=<value2>...`

这个指令很简单，就是设置环境变量而已，无论是后面的其它指令，如 `RUN`，还是运行时的应用，都可以直接使用这里定义的环境变量。

```shell
# 设置多个环境变量
ENV VERSION=1.0 DEBUG=on \
    NAME="Happy Feet"
```

#### 2.3.7 ARG 构建参数

格式：`ARG <参数名>[=<默认值>]`

构建参数和 `ENV` 的效果一样，都是设置环境变量。所不同的是，`ARG` 所设置的构建环境的环境变量，在将来容器运行时是不会存在这些环境变量的。但是不要因此就使用 `ARG` 保存密码之类的信息，因为 `docker history` 还是可以看到所有值的。

`Dockerfile` 中的 `ARG` 指令是定义参数名称，以及定义其默认值。该默认值可以在构建命令 `docker build` 中用 `--build-arg <参数名>=<值>` 来覆盖。

**灵活的使用 `ARG` 指令，能够在不修改 Dockerfile 的情况下，构建出不同的镜像**。

ARG 指令有生效范围，如果在 `FROM` 指令之前指定，那么只能用于 `FROM` 指令中。

```shell
# 只在 FROM 中生效
ARG DOCKER_USERNAME=library

FROM ${DOCKER_USERNAME}/alpine

# 要想在 FROM 之后使用，必须再次指定
ARG DOCKER_USERNAME=library

RUN set -x ; echo ${DOCKER_USERNAME}
```

#### 2.3.8 VOLUME 定义匿名卷

格式为：

- `VOLUME ["<路径1>", "<路径2>"...]`
- `VOLUME <路径>`

容器运行时应该尽量保持容器存储层不发生写操作，对于数据库类需要保存动态数据的应用，其数据库文件应该保存于卷(volume)中。为了防止运行时用户忘记将动态文件所保存目录挂载为卷，在 `Dockerfile` 中，我们可以事先指定某些目录挂载为匿名卷，这样在运行时如果用户不指定挂载，其应用也可以正常运行，不会向容器存储层写入大量数据。

```sh
VOLUME /data
```

这里的 `/data` 目录就会在容器运行时自动挂载为匿名卷，任何向 `/data` 中写入的信息都不会记录进容器存储层，从而保证了容器存储层的无状态化。

当然，运行容器时可以覆盖这个挂载设置。比如：

```sh
$ docker run -d -v mydata:/data xxxx
```

在这行命令中，就使用了 `mydata` 这个命名卷挂载到了 `/data` 这个位置，替代了 `Dockerfile` 中定义的匿名卷的挂载配置。

#### 3.3.9 EXPOSE 暴露端口

格式为 `EXPOSE <端口1> [<端口2>...]`。

`EXPOSE` 指令是声明容器运行时提供服务的端口，这只是一个声明，在容器运行时并不会因为这个声明应用就会开启这个端口的服务。在 Dockerfile 中写入这样的声明有两个好处，一个是帮助镜像使用者理解这个镜像服务的守护端口，以方便配置映射；另一个用处则是在运行时使用随机端口映射时，也就是 `docker run -P` 时，会自动随机映射 `EXPOSE` 的端口。

要将 `EXPOSE` 和在运行时使用 `-p <宿主端口>:<容器端口>` 区分开来。`-p`，是映射宿主端口和容器端口，换句话说，就是将容器的对应端口服务公开给外界访问，而 `EXPOSE` 仅仅是声明容器打算使用什么端口而已，并不会自动在宿主进行端口映射。

#### 3.3.10 WORKDIR 指定工作目录

格式为 `WORKDIR <工作目录路径>`。

使用 `WORKDIR` 指令可以来指定工作目录（或者称为当前目录），以后各层的当前目录就被改为指定的目录，如该目录不存在，`WORKDIR` 会帮你建立目录。

在`Dockerfile`每一层镜像构建时都会重置回这个工作目录，

如果你的 `WORKDIR` 指令使用的相对路径，那么所切换的路径与之前的 `WORKDIR` 有关：

```dockerfile
WORKDIR /a
WORKDIR b
WORKDIR c

RUN pwd
```

`RUN pwd` 的工作目录为 `/a/b/c`。

#### 3.3.11 USER 指定当前用户

格式：`USER <用户名>[:<用户组>]`

`USER` 指令和 `WORKDIR` 相似，都是改变环境状态并影响以后的层。`WORKDIR` 是改变工作目录，`USER` 则是改变之后层的执行 `RUN`, `CMD` 以及 `ENTRYPOINT` 这类命令的身份。

注意，`USER` 只是帮助你切换到指定用户而已，这个用户必须是事先建立好的，否则无法切换。

```dockerfile
RUN groupadd -r redis && useradd -r -g redis redis
USER redis
RUN [ "redis-server" ]
```

如果以 `root` 执行的脚本，在执行期间希望改变身份，比如希望以某个已经建立好的用户来运行某个服务进程，不要使用 `su` 或者 `sudo`，这些都需要比较麻烦的配置，而且在 TTY 缺失的环境下经常出错。建议使用 [`gosu`](https://github.com/tianon/gosu)。

```dockerfile
# 建立 redis 用户，并使用 gosu 换另一个用户执行命令
RUN groupadd -r redis && useradd -r -g redis redis
# 下载 gosu
RUN wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.12/gosu-amd64" \
    && chmod +x /usr/local/bin/gosu \
    && gosu nobody true
# 设置 CMD，并以另外的用户执行
CMD [ "exec", "gosu", "redis", "redis-server" ]
```

#### 3.3.12 ONBUILD 为他人作嫁衣裳

格式：`ONBUILD <其它指令>`。

`ONBUILD` 是一个特殊的指令，它后面跟的是其它指令，比如 `RUN`, `COPY` 等，而这些指令，在当前镜像构建时并不会被执行。只有当以当前镜像为基础镜像，去构建下一级镜像的时候才会被执行。

`Dockerfile` 中的其它指令都是为了定制当前镜像而准备的，唯有 `ONBUILD` 是为了帮助别人定制自己而准备的。

#### 3.3.13 LABEL 为镜像添加元数据

`LABEL` 指令用来给镜像以键值对的形式添加一些元数据（metadata）。

```dockerfile
LABEL <key>=<value> <key>=<value> <key>=<value> ...
```

我们还可以用一些标签来申明镜像的作者、文档地址等：

```dockerfile
LABEL org.opencontainers.image.authors="yeasy"

LABEL org.opencontainers.image.documentation="https://yeasy.gitbooks.io"
```



## 3. 数据卷

`数据卷` 是一个可供一个或多个容器使用的特殊目录，它绕过 UFS，可以提供很多有用的特性：

- `数据卷` 可以在容器之间共享和重用
- 对 `数据卷` 的修改会立马生效
- 对 `数据卷` 的更新，不会影响镜像
- `数据卷` 默认会一直存在，即使容器被删除

### 3.1 常用命令

docker 专门提供了 volume 子命令来操作数据卷：

- **create**    创建数据卷
- **inspect**   显示数据卷的详细信息
- **ls**        列出所有的数据卷
- **prune**    删除所有**未使用的 volumes**，并且有 -f 选项
- **rm**       删除一个或多个未使用的 volumes，并且有 -f 选项

```sh
# 创建数据卷
docker volume create my-vol
# 查看所有的 数据卷
$ docker volume ls
# 查看指定 数据卷 的信息
$ docker volume inspect my-vol
```

### 3.2 **使用数据卷的最佳场景**

- 在多个容器之间共享数据，多个容器可以同时以只读或者读写的方式挂载同一个数据卷，从而共享数据卷中的数据。
- 当宿主机不能保证一定存在某个目录或一些固定路径的文件时，使用数据卷可以规避这种限制带来的问题。
- 当你想把容器中的数据存储在宿主机之外的地方时，比如远程主机上或云存储上。
- 当你需要把容器数据在不同的宿主机之间备份、恢复或迁移时，数据卷是很好的选择。

### 3.3 **使用 mount 语法挂载数据卷**

之前我们使用 --volume(-v) 选项来挂载数据卷，现在 docker 提供了更强大的 --mount 选项来管理数据卷。mount 选项可以通过逗号分隔的多个键值对一次提供多个配置项，因此 mount 选项可以提供比 volume 选项更详细的配置。使用 mount 选项的常用配置如下：

- **type** 指定挂载方式，我们这里用到的是 volume，其实还可以有 bind 和 tmpfs。
- **volume-driver** 指定挂载数据卷的驱动程序，默认值是 local。
- **source** 指定挂载的源，对于一个命名的数据卷，这里应该指定这个数据卷的名称。在使用时可以写 source，也可以简写为 src。
- **destination** 指定挂载的数据在容器中的路径。在使用时可以写 destination，也可以简写为 dst 或 target。
- **readonly** 指定挂载的数据为只读。
- **volume-opt** 可以指定多次，用来提高更多的 mount 相关的配置。

```
$ docker volume create hello
$ docker run -id --mount type=volume,source=hello,target=/world ubuntu /bin/bash
```

**使用 volume driver 把数据存储到其它地方**

除了默认的把数据卷中的数据存储在宿主机，docker 还允许我们通过指定 volume driver 的方式把数据卷中的数据存储在其它的地方，比如 Azrue Storge 或 AWS 的 S3。
简单起见，我们接下来的 demo 演示如何通过 vieux/sshfs 驱动把数据卷的存储在其它的主机上。
docker 默认是不安装 vieux/sshfs 插件的，我们可以通过下面的命令进行安装：

```
$ docker plugin install --grant-all-permissions vieux/sshfs
```

然后通过 vieux/sshfs 驱动创建数据卷，并指定远程主机的登录用户名、密码和数据存放目录：

```
docker volume create --driver vieux/sshfs \
    -o sshcmd=nick@10.32.2.134:/home/nick/sshvolume \
    -o password=yourpassword \
    mysshvolume
```

注意，请确保你指定的远程主机上的挂载点目录是存在的(demo 中是 /home/nick/sshvolume 目录)，否则在启动容器时会报错。
最后在启动容器时指定挂载这个数据卷：

```
docker run -id \
    --name testcon \
    --mount type=volume,volume-driver=vieux/sshfs,source=mysshvolume,target=/world \
    ubuntu /bin/bash
```

### 3.4 **数据的覆盖问题**

- 如果挂载一个空的数据卷到容器中的一个非空目录中，那么这个目录下的文件会被复制到数据卷中。
- 如果挂载一个非空的数据卷到容器中的一个目录中，那么容器中的目录中会显示数据卷中的数据。如果原来容器中的目录中有数据，那么这些原始数据会被隐藏掉。

这两个规则都非常重要，灵活利用第一个规则可以帮助我们初始化数据卷中的内容。掌握第二个规则可以保证挂载数据卷后的数据总是你期望的结果。

### 3.5 在 Dockerfile 中添加数据卷

在 Dockerfile 中我们可以使用 VOLUME 指令向容器添加数据卷：

```
VOLUME /data
```

在使用 docker build 命令生成镜像并且以该镜像启动容器时会挂载一个数据卷到 /data 目录。根据我们已知的数据覆盖规则，如果镜像中存在 /data 目录，这个目录中的内容将全部被复制到宿主机中对应的目录中，并且根据容器中的文件设置合适的权限和所有者。
注意，**VOLUME 指令不能挂载主机中指定的目录。这是为了保证 Dockerfile 的可一致性，因为不能保证所有的宿主机都有对应的目录**。
在实际的使用中，这里还有一个陷阱需要大家注意：**在 Dockerfile 中使用 VOLUME 指令之后的代码，如果尝试对这个数据卷进行修改，这些修改都不会生效！**下面是一个这样的例子：

```
FROM ubuntu
RUN useradd nick
VOLUME /data
RUN touch /data/test.txt
RUN chown -R nick:nick /data
```

通过这个 Dockerfile 创建镜像并启动容器后，该容器中存在用户 nick，并且能够看到 /data 目录挂载的数据卷。但是 /data 目录内并没有文件 test.txt，更别说 test.txt 文件的所有者属性了。要解释这个现象需要我们了解通过 Dockerfile 创建镜像的过程：
Dockerfile 中除了 FROM 指令的每一行都是基于上一行生成的临时镜像运行一个容器，执行一条指令并执行类似 docker commit 的命令得到一个新的镜像。这条类似 docker commit 的命令不会对挂载的数据卷进行保存。
所以上面的 Dockerfile 最后两行执行时，都会在一个临时的容器上挂载 /data，并对这个临时的数据卷进行操作，但是这一行指令执行并提交后，这个临时的数据卷并没有被保存。因而我们最终通过镜像创建的容器所挂载的数据卷是没有被最后两条指令操作过的。我们姑且叫它 "Dockerfile 中数据卷的初始化问题"。

下面的写法可以解决 Dockerfile 中数据卷的初始化问题：

```
FROM ubuntu
RUN useradd nick
RUN mkdir /data && touch /data/test.txt
RUN chown -R nick:nick /data
VOLUME /data
```

通过这个 Dockerfile 创建镜像并启动容器后，数据卷的初始化是符合预期的。这是由于在挂载数据卷时，/data 已经存在，/data 中的文件以及它们的权限和所有者设置会被复制到数据卷中。
还有另外一种方法可以解决 Dockerfile 中数据卷的初始化问题。就是利用 CMD 指令和 ENTRYPOINT 指令的执行特点：与 RUN 指令在镜像构建过程中执行不同，CMD 指令和 ENTRYPOINT 指令是在容器启动时执行。因此使用下面的 Dockerfile 也可以达到对数据卷的初始化目的：

```
FROM ubuntu
RUN useradd nick
VOLUME /data
CMD touch /data/test.txt && chown -R nick:nick /data && /bin/bash
```











## 附录

- [Docker —— 从入门到实践](https://yeasy.gitbook.io/docker_practice/)

- [ Dockerfile 最佳实践文档](https://yeasy.gitbook.io/docker_practice/appendix/best_practices#jiang-duo-hang-can-shu-pai-xu)

- `Dockerfie` 官方文档：https://docs.docker.com/engine/reference/builder/

- `Dockerfile` 最佳实践文档：https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

- `Docker` 官方镜像 `Dockerfile`：https://github.com/docker-library/docs

  

  



