# Jenkins源码学习

## 1. 运行源码

**下载源码**

```shell
git clone https://github.com/jenkinsci/jenkins.git

# 可以切换到某个稳定分支 
git checkout stable-2.235
```

Jenkins2.0以上的版本依赖JDK1.7以上，以及Maven3.0.4以上（如果需要本地调试Jenkins还需要安装Node.js）

**安装依赖**

Jenkins是一个比较大的项目，里面有非常多的依赖,因此最好使用一个国内的Maven加速源进行加速,可以在.m2的settings.xml中配置mirror

```
 <mirrors>
    <mirror>
      <id>alimaven</id>
      <name>aliyun maven</name>
      <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
      <mirrorOf>central</mirrorOf>        
    </mirror>
  </mirrors>
```

安装前端依赖

```shell
yarn install
```

**编译启动**

参考文件`CONTRIBUTING.md`

1. 安装maven多模块依赖 `mvn -am -pl war,bom -DskipTests -Dspotbugs.skip clean install`
2. 启动服务 `mvn -pl war jetty:run`
3. 访问服务 [http://localhost:8080/jenkins](http://localhost:8080/jenkins)





## 参考

- [Learn Jenkins the hard way (1) - 从源码运行Jenkins开始](https://developer.aliyun.com/article/70440?spm=a2c6h.14164896.0.0.199a1859TSsIYV)
- [Maven常用参数说明](https://www.jianshu.com/p/25aff2bf6e56)

