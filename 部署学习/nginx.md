# Nginx学习

> 大部分内容来源于：[万字总结，体系化带你全面认识 Nginx ！](https://juejin.cn/post/6942607113118023710)

## 1. 安装

```bash
$ sudo yum -y install nginx   # 安装 nginx
$ sudo yum remove nginx  # 卸载 nginx
```

使用 yum 进行 Nginx 安装时，Nginx 配置文件在 `/etc/nginx` 目录下。也通过 `rpm -ql nginx` 命令查看 `Nginx` 的安装信息。

```text
# Nginx配置文件
/etc/nginx/nginx.conf # nginx 主配置文件
/etc/nginx/nginx.conf.default

# 可执行程序文件
/usr/bin/nginx-upgrade
/usr/sbin/nginx

# nginx库文件
/usr/lib/systemd/system/nginx.service # 用于配置系统守护进程
/usr/lib64/nginx/modules # Nginx模块目录

# 帮助文档
/usr/share/doc/nginx-1.16.1
/usr/share/doc/nginx-1.16.1/CHANGES
/usr/share/doc/nginx-1.16.1/README
/usr/share/doc/nginx-1.16.1/README.dynamic
/usr/share/doc/nginx-1.16.1/UPGRADE-NOTES-1.6-to-1.10

# 静态资源目录
/usr/share/nginx/html/404.html
/usr/share/nginx/html/50x.html
/usr/share/nginx/html/index.html

# 存放Nginx日志文件
/var/log/nginx
```

主要关注的文件夹有两个：

1. `/etc/nginx/conf.d/` 是子配置项存放处， `/etc/nginx/nginx.conf` 主配置文件会默认把这个文件夹中所有子配置项都引入；
2. `/usr/share/nginx/html/` 静态文件都放在这个文件夹，也可以根据你自己的习惯放在其他地方

## 2. Nginx 常用命令

`systemctl` 系统命令：

```bash
# 开机配置
systemctl enable nginx # 开机自动启动
systemctl disable nginx # 关闭开机自动启动

# 启动Nginx
systemctl start nginx # 启动Nginx成功后，可以直接访问主机IP，此时会展示Nginx默认页面

# 停止Nginx
systemctl stop nginx

# 重启Nginx
systemctl restart nginx

# 重新加载Nginx
systemctl reload nginx

# 查看 Nginx 运行状态
systemctl status nginx

# 查看Nginx进程
ps -ef | grep nginx

# 杀死Nginx进程
kill -9 pid # 根据上面查看到的Nginx进程号，杀死Nginx进程，-9 表示强制结束进程
```

`Nginx` 应用程序命令

```text
nginx -s reload  # 向主进程发送信号，重新加载配置文件，热重启
nginx -s reopen	 # 重启 Nginx
nginx -s stop    # 快速关闭
nginx -s quit    # 等待工作进程处理完成后关闭
nginx -T         # 查看当前 Nginx 最终的配置
nginx -t         # 检查配置是否有问题
```

## 3. Nginx 配置文件详解

### 3.1 主要结构

```bash
# main段配置信息
user  nginx;                        # 运行用户，默认即是nginx，可以不进行设置
worker_processes  auto;             # Nginx 进程数，一般设置为和 CPU 核数一样
error_log  /var/log/nginx/error.log warn;   # Nginx 的错误日志存放目录
pid        /var/run/nginx.pid;      # Nginx 服务启动时的 pid 存放位置

# events段配置信息
events {
    use epoll;     # 使用epoll的I/O模型(如果你不知道Nginx该使用哪种轮询方法，会自动选择一个最适合你操作系统的)
    worker_connections 1024;   # 每个进程允许最大并发数
}

# http段配置信息
# 配置使用最频繁的部分，代理、缓存、日志定义等绝大多数功能和第三方模块的配置都在这里设置
http { 
    # 设置日志模式
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;   # Nginx访问日志存放位置

    sendfile            on;   # 开启高效传输模式
    tcp_nopush          on;   # 减少网络报文段的数量
    tcp_nodelay         on;
    keepalive_timeout   65;   # 保持连接的时间，也叫超时时间，单位秒
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;      # 文件扩展名与类型映射表
    default_type        application/octet-stream;   # 默认文件类型

    include /etc/nginx/conf.d/*.conf;   # 加载子配置项
    
    # server段配置信息
    server {
    	listen       80;       # 配置监听的端口
    	server_name  localhost;    # 配置的域名
      
    	# location段配置信息
    	location / {
    		root   /usr/share/nginx/html;  # 网站根目录
    		index  index.html index.htm;   # 默认首页文件
    		deny 172.168.22.11;   # 禁止访问的ip地址，可以为all
    		allow 172.168.33.44；# 允许访问的ip地址，可以为all
    	}
    	
    	error_page 500 502 503 504 /50x.html;  # 默认50x对应的访问页面
    	error_page 400 404 error.html;   # 同上
    }
}
```

`main` 全局配置，对全局生效；

`events` 配置影响 `Nginx` 服务器与用户的网络连接；

`http` 配置代理，缓存，日志定义等绝大多数功能和第三方模块的配置；

`server` 配置虚拟主机的相关参数，一个 `http` 块中可以有多个 `server` 块；

`location` 用于配置匹配的 `uri` ；

`upstream` 配置后端服务器具体地址，负载均衡配置不可或缺的部分；

下图能清晰的展示它的层级结构：

![未命名文件 (4).png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/87fffe0360aa4f34adb6258a955aad38~tplv-k3u1fbpfcp-zoom-in-crop-mark:4536:0:0:0.image)

### 3.2 main 段核心参数

#### user

指定运行 `Nginx` 的 `woker` 子进程的属主和属组，其中组可以不指定。

```bash
user USERNAME [GROUP]

user nginx lion; # 用户是nginx;组是lion
复制代码
```

#### pid

指定运行 `Nginx` `master` 主进程的 `pid` 文件存放路径。

```bash
pid /opt/nginx/logs/nginx.pid # master主进程的的pid存放在nginx.pid的文件
复制代码
```

#### worker_rlimit_nofile_number

指定 `worker` 子进程可以打开的最大文件句柄数。

```bash
worker_rlimit_nofile 20480; # 可以理解成每个worker子进程的最大连接数量。
复制代码
```

#### worker_rlimit_core

指定 `worker` 子进程异常终止后的 `core` 文件，用于记录分析问题。

```bash
worker_rlimit_core 50M; # 存放大小限制
working_directory /opt/nginx/tmp; # 存放目录
复制代码
```

#### worker_processes_number

指定 `Nginx` 启动的 `worker` 子进程数量。

```bash
worker_processes 4; # 指定具体子进程数量
worker_processes auto; # 与当前cpu物理核心数一致
复制代码
```

#### worker_cpu_affinity

将每个 `worker` 子进程与我们的 `cpu` 物理核心绑定。

```bash
worker_cpu_affinity 0001 0010 0100 1000; # 4个物理核心，4个worker子进程
复制代码
```


![未命名文件 (1).png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e3c23de61deb4c6391fe70e561f18aa3~tplv-k3u1fbpfcp-zoom-in-crop-mark:4536:0:0:0.image)
 
将每个 `worker` 子进程与特定 `CPU` 物理核心绑定，优势在于，避免同一个 `worker` 子进程在不同的 `CPU` 核心上切换，缓存失效，降低性能。但其并不能真正的避免进程切换。

#### worker_priority

指定 `worker` 子进程的 `nice` 值，以调整运行 `Nginx` 的优先级，通常设定为负值，以优先调用 `Nginx` 。

```bash
worker_priority -10; # 120-10=110，110就是最终的优先级
复制代码
```

`Linux` 默认进程的优先级值是120，值越小越优先； `nice` 定范围为 `-20` 到 `+19` 。
 
[备注] 应用的默认优先级值是120加上 `nice` 值等于它最终的值，这个值越小，优先级越高。

#### worker_shutdown_timeout

指定 `worker` 子进程优雅退出时的超时时间。

```bash
worker_shutdown_timeout 5s;
复制代码
```

#### timer_resolution

`worker` 子进程内部使用的计时器精度，调整时间间隔越大，系统调用越少，有利于性能提升；反之，系统调用越多，性能下降。

```bash
timer_resolution 100ms;
复制代码
```

在 `Linux` 系统中，用户需要获取计时器时需要向操作系统内核发送请求，有请求就必然会有开销，因此这个间隔越大开销就越小。

#### daemon

指定 `Nginx` 的运行方式，前台还是后台，前台用于调试，后台用于生产。

```bash
daemon off; # 默认是on，后台运行模式
```

### 3.3 events 段核心参数

#### use

`Nginx` 使用何种事件驱动模型。

```bash
use method; # 不推荐配置它，让nginx自己选择

method 可选值为：select、poll、kqueue、epoll、/dev/poll、eventport
复制代码
```

#### worker_connections

`worker` 子进程能够处理的最大并发连接数。

```bash
worker_connections 1024 # 每个子进程的最大连接数为1024
复制代码
```

#### accept_mutex

是否打开负载均衡互斥锁。

```bash
accept_mutex on # 默认是off关闭的，这里推荐打开
```

### 3.4 server段核心参数

#### server_name 指令

指定虚拟主机域名。

```bash
server_name name1 name2 name3

# 示例：
server_name www.nginx.com;
复制代码
```

域名匹配的四种写法：

- 精确匹配： `server_name www.nginx.com` ;
- 左侧通配： `server_name *.nginx.com` ;
- 右侧统配： `server_name  www.nginx.*` ;
- 正则匹配： `server_name ~^www\.nginx\.*$` ;

匹配优先级：**精确匹配 > 左侧通配符匹配 > 右侧通配符匹配 > 正则表达式匹配**

`server_name` 配置实例：
 
1、配置本地  `DNS` 解析 `vim /etc/hosts` （ `macOS` 系统）

```bash
# 添加如下内容，其中 121.42.11.34 是阿里云服务器IP地址
121.42.11.34 www.nginx-test.com
121.42.11.34 mail.nginx-test.com
121.42.11.34 www.nginx-test.org
121.42.11.34 doc.nginx-test.com
121.42.11.34 www.nginx-test.cn
121.42.11.34 fe.nginx-test.club
复制代码
```

[注意] 这里使用的是虚拟域名进行测试，因此需要配置本地 `DNS` 解析，如果使用阿里云上购买的域名，则需要在阿里云上设置好域名解析。
 
2、配置阿里云 `Nginx` ，`vim /etc/nginx/nginx.conf` 

```bash
# 这里只列举了http端中的sever端配置

# 左匹配
server {
	listen	80;
	server_name	*.nginx-test.com;
	root	/usr/share/nginx/html/nginx-test/left-match/;
	location / {
		index index.html;
	}
}

# 正则匹配
server {
	listen	80;
	server_name	~^.*\.nginx-test\..*$;
	root	/usr/share/nginx/html/nginx-test/reg-match/;
	location / {
		index index.html;
	}
}

# 右匹配
server {
	listen	80;
	server_name	www.nginx-test.*;
	root	/usr/share/nginx/html/nginx-test/right-match/;
	location / {
		index index.html;
	}
}

# 完全匹配
server {
	listen	80;
	server_name	www.nginx-test.com;
	root	/usr/share/nginx/html/nginx-test/all-match/;
	location / {
		index index.html;
	}
}
复制代码
```

3、访问分析

- 当访问 `www.nginx-test.com` 时，都可以被匹配上，因此选择优先级最高的“完全匹配”；
- 当访问 `mail.nginx-test.com` 时，会进行“左匹配”；
- 当访问 `www.nginx-test.org` 时，会进行“右匹配”；
- 当访问 `doc.nginx-test.com` 时，会进行“左匹配”；
- 当访问 `www.nginx-test.cn` 时，会进行“右匹配”；
- 当访问 `fe.nginx-test.club` 时，会进行“正则匹配”；

#### root

指定静态资源目录位置，它可以写在 `http` 、 `server` 、 `location` 等配置中。

```bash
root path

例如：
location /image {
	root /opt/nginx/static;
}

当用户访问 www.test.com/image/1.png 时，实际在服务器找的路径是 /opt/nginx/static/image/1.png
复制代码
```

[注意] `root` 会将定义路径与 `URI` 叠加， `alias` 则只取定义路径。

#### alias

它也是指定静态资源目录位置，它只能写在 `location` 中。

```bash
location /image {
	alias /opt/nginx/static/image/;
}

当用户访问 www.test.com/image/1.png 时，实际在服务器找的路径是 /opt/nginx/static/image/1.png
复制代码
```

[注意] 使用 alias 末尾一定要添加 `/` ，并且它只能位于 `location` 中。

#### location

配置路径。

```bash
location [ = | ~ | ~* | ^~ ] uri {
	...
}
复制代码
```

匹配规则：

- `=` 精确匹配；
- `~` 正则匹配，区分大小写；
- `~*` 正则匹配，不区分大小写；
- `^~` 匹配到即停止搜索；


匹配优先级： `=` > `^~` >  `~` > `~*` > 不带任何字符。
 
实例：

```bash
server {
  listen	80;
  server_name	www.nginx-test.com;
  
  # 只有当访问 www.nginx-test.com/match_all/ 时才会匹配到/usr/share/nginx/html/match_all/index.html
  location = /match_all/ {
      root	/usr/share/nginx/html
      index index.html
  }
  
  # 当访问 www.nginx-test.com/1.jpg 等路径时会去 /usr/share/nginx/images/1.jpg 找对应的资源
  location ~ \.(jpeg|jpg|png|svg)$ {
  	root /usr/share/nginx/images;
  }
  
  # 当访问 www.nginx-test.com/bbs/ 时会匹配上 /usr/share/nginx/html/bbs/index.html
  location ^~ /bbs/ {
  	root /usr/share/nginx/html;
    index index.html index.htm;
  }
}
复制代码
```

**location 中的反斜线**

```bash
location /test {
	...
}

location /test/ {
	...
}
复制代码
```

- 不带 `/` 当访问 `www.nginx-test.com/test` 时， `Nginx` 先找是否有 `test` 目录，如果有则找 `test` 目录下的 `index.html` ；如果没有 `test` 目录， `nginx` 则会找是否有 `test` 文件。
- 带 `/` 当访问 `www.nginx-test.com/test` 时， `Nginx` 先找是否有 `test` 目录，如果有则找 `test` 目录下的 `index.html` ，如果没有它也不会去找是否存在 `test` 文件。

#### return

停止处理请求，直接返回响应码或重定向到其他 `URL` ；执行 `return` 指令后， `location` 中后续指令将不会被执行。

```bash
return code [text];
return code URL;
return URL;

例如：
location / {
	return 404; # 直接返回状态码
}

location / {
	return 404 "pages not found"; # 返回状态码 + 一段文本
}

location / {
	return 302 /bbs ; # 返回状态码 + 重定向地址
}

location / {
	return https://www.baidu.com ; # 返回重定向地址
}
复制代码
```

#### rewrite

根据指定正则表达式匹配规则，重写 `URL` 。

```bash
语法：rewrite 正则表达式 要替换的内容 [flag];

上下文：server、location、if

示例：rewirte /images/(.*\.jpg)$ /pic/$1; # $1是前面括号(.*\.jpg)的反向引用
复制代码
```


`flag` 可选值的含义：

- `last` 重写后的 `URL` 发起新请求，再次进入 `server` 段，重试 `location` 的中的匹配；
- `break` 直接使用重写后的 `URL` ，不再匹配其它 `location` 中语句；
- `redirect` 返回302临时重定向；
- `permanent` 返回301永久重定向；

```bash
server{
  listen 80;
  server_name fe.lion.club; # 要在本地hosts文件进行配置
  root html;
  location /search {
  	rewrite ^/(.*) https://www.baidu.com redirect;
  }
  
  location /images {
  	rewrite /images/(.*) /pics/$1;
  }
  
  location /pics {
  	rewrite /pics/(.*) /photos/$1;
  }
  
  location /photos {
  
  }
}
复制代码
```

按照这个配置我们来分析：

- 当访问 `fe.lion.club/search` 时，会自动帮我们重定向到 `https://www.baidu.com`。
- 当访问 `fe.lion.club/images/1.jpg` 时，第一步重写 `URL` 为 `fe.lion.club/pics/1.jpg` ，找到 `pics` 的 `location` ，继续重写 `URL` 为 `fe.lion.club/photos/1.jpg` ，找到 `/photos` 的 `location` 后，去 `html/photos` 目录下寻找 `1.jpg` 静态资源。

#### if 指令

```bash
语法：if (condition) {...}

上下文：server、location

示例：
if($http_user_agent ~ Chrome){
  rewrite /(.*)/browser/$1 break;
}
复制代码
```


`condition` 判断条件：

- `$variable` 仅为变量时，值为空或以0开头字符串都会被当做 `false` 处理；
- `=` 或 `!=` 相等或不等；
- `~` 正则匹配；
- `! ~` 非正则匹配；
- `~*` 正则匹配，不区分大小写；
- `-f` 或 `! -f` 检测文件存在或不存在；
- `-d` 或 `! -d` 检测目录存在或不存在；
- `-e` 或 `! -e` 检测文件、目录、符号链接等存在或不存在；
- `-x` 或 `! -x` 检测文件可以执行或不可执行；


实例：

```bash
server {
  listen 8080;
  server_name localhost;
  root html;
  
  location / {
  	if ( $uri = "/images/" ){
    	rewrite (.*) /pics/ break;
    }
  }
}
复制代码
```

当访问 `localhost:8080/images/` 时，会进入 `if` 判断里面执行 `rewrite` 命令。

#### autoindex

用户请求以 `/` 结尾时，列出目录结构，可以用于快速搭建静态资源下载网站。

`autoindex.conf` 配置信息：

```bash
server {
  listen 80;
  server_name fe.lion-test.club;
  
  location /download/ {
    root /opt/source;
    
    autoindex on; # 打开 autoindex，，可选参数有 on | off
    autoindex_exact_size on; # 修改为off，以KB、MB、GB显示文件大小，默认为on，以bytes显示出⽂件的确切⼤⼩
    autoindex_format html; # 以html的方式进行格式化，可选参数有 html | json | xml
    autoindex_localtime off; # 显示的⽂件时间为⽂件的服务器时间。默认为off，显示的⽂件时间为GMT时间
  }
}
复制代码
```

当访问 `fe.lion.com/download/` 时，会把服务器 `/opt/source/download/` 路径下的文件展示出来，如下图所示：

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/38aa834307654ae08ebf5aa72507daf7~tplv-k3u1fbpfcp-zoom-in-crop-mark:4536:0:0:0.image)

## 4. 变量

`Nginx` 提供给使用者的变量非常多，但是终究是一个完整的请求过程所产生数据， `Nginx` 将这些数据以变量的形式提供给使用者。
 
下面列举些项目中常用的变量：

| 变量名               | 含义                                                         |
| -------------------- | ------------------------------------------------------------ |
| `remote_addr`        | 客户端 `IP` 地址                                             |
| `remote_port`        | 客户端端口                                                   |
| `server_addr`        | 服务端 `IP` 地址                                             |
| `server_port`        | 服务端端口                                                   |
| `server_protocol`    | 服务端协议                                                   |
| `binary_remote_addr` | 二进制格式的客户端 `IP` 地址                                 |
| `connection`         | `TCP` 连接的序号，递增                                       |
| `connection_request` | `TCP` 连接当前的请求数量                                     |
| `uri`                | 请求的URL，不包含参数                                        |
| `request_uri`        | 请求的URL，包含参数                                          |
| `scheme`             | 协议名， `http` 或 `https`                                   |
| `request_method`     | 请求方法                                                     |
| `request_length`     | 全部请求的长度，包含请求行、请求头、请求体                   |
| `args`               | 全部参数字符串                                               |
| `arg_参数名`         | 获取特定参数值                                               |
| `is_args`            | `URL` 中是否有参数，有的话返回 `?` ，否则返回空              |
| `query_string`       | 与 `args` 相同                                               |
| `host`               | 请求信息中的 `Host` ，如果请求中没有 `Host` 行，则在请求头中找，最后使用 `nginx` 中设置的 `server_name` 。 |
| `http_user_agent`    | 用户浏览器                                                   |
| `http_referer`       | 从哪些链接过来的请求                                         |
| `http_via`           | 每经过一层代理服务器，都会添加相应的信息                     |
| `http_cookie`        | 获取用户 `cookie`                                            |
| `request_time`       | 处理请求已消耗的时间                                         |
| `https`              | 是否开启了 `https` ，是则返回 `on` ，否则返回空              |
| `request_filename`   | 磁盘文件系统待访问文件的完整路径                             |
| `document_root`      | 由 `URI` 和 `root/alias` 规则生成的文件夹路径                |
| `limit_rate`         | 返回响应时的速度上限值                                       |















## 参考

- [万字总结，体系化带你全面认识 Nginx ！](https://juejin.cn/post/6942607113118023710)

- [Nginx中文文档](https://blog.redis.com.cn/doc/)
- [全面掌握Nginx](https://mp.weixin.qq.com/s/zMKkFHlApy8B28n_ARnGSg)









