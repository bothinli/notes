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



## 2. stapler框架

### 2.1 stapler框架用法

Stapler框架是Jenkins中用于处理HTTP请求的框架。它是一个轻量级的MVC框架，提供了处理HTTP请求的标准化方法，使得开发人员可以轻松地构建RESTful风格的Web应用程序。

Stapler框架基于Java Servlet规范，使用反射机制将HTTP请求映射到Java类和方法。它提供了一些注解来处理请求，例如：

@StaplerDispatchable: 标注方法可以被处理请求；

@StaplerResponder: 标注返回响应对象的方法；

@StaplerFallback: 标注处理请求的默认方法。

另外，Stapler框架提供了一些工具类来处理请求和响应，例如：

StaplerRequest: 表示一个HTTP请求，可以获取请求参数、请求头等信息；

StaplerResponse: 表示一个HTTP响应，可以设置响应头、响应状态码等信息；

Stapler: 框架的核心类，提供了处理请求、路由请求等功能。

在Jenkins中，所有的HTTP请求都通过Stapler框架来处理。开发人员可以使用Stapler框架来编写自己的插件，为Jenkins添加新的功能或扩展现有功能。Stapler框架的使用非常广泛，在Jenkins中的几乎所有的插件都使用了Stapler框架来处理HTTP请求。

### 2.2 简单的Stapler框架的demo

```java
import org.kohsuke.stapler.StaplerRequest;
import org.kohsuke.stapler.StaplerResponse;
import org.kohsuke.stapler.Stapler;
import org.kohsuke.stapler.QueryParameter;

public class MyController {
    public void doSomething(StaplerRequest req, StaplerResponse rsp, @QueryParameter String name) {
        rsp.setContentType("text/plain");
        rsp.getWriter().println("Hello, " + name + "!");
    }
    
    public void doIndex(StaplerRequest req, StaplerResponse rsp) {
        req.getView(this, "index.jelly").forward(req, rsp);
    }
}

```
在上面的例子中，我们创建了一个名为MyController的类，它有两个方法：

doSomething: 处理/myservice/something请求，通过@QueryParameter注解获取请求参数，并返回一个文本响应；

doIndex: 处理/myservice请求，返回一个Jelly模板渲染的响应。

当请求/myservice/something?name=John时，doSomething方法会被调用，返回一个文本响应Hello, John!。当请求/myservice时，doIndex方法会被调用，返回一个Jelly模板渲染的响应。

在Stapler框架中，我们可以使用注解来声明一个方法可以处理HTTP请求，并且可以获取请求参数、请求头等信息。通过StaplerResponse类，我们可以设置响应头、响应状态码等信息，并且返回一个文本响应、Jelly模板渲染的响应等。

### 2.3 stapler常用注解

以下是Stapler框架中常用的注解：

@StaplerDispatchable: 标注方法可以被处理请求。通常用于处理HTTP GET、POST等请求。如果一个方法没有被标注为@StaplerDispatchable，则无法通过HTTP请求访问它；

@StaplerResponder: 标注返回响应对象的方法。通常用于处理HTTP PUT、DELETE等请求。如果一个方法被标注为@StaplerResponder，则它必须返回一个响应对象，否则会抛出异常；

@StaplerFallback: 标注处理请求的默认方法。如果没有找到与请求URL对应的方法，就会调用标注了@StaplerFallback的方法。如果没有标注@StaplerFallback的方法，则会返回404错误；

@RequirePOST: 标注方法必须使用HTTP POST请求。如果使用其他HTTP请求访问该方法，将返回一个405错误；

@QueryParameter: 标注方法参数来获取请求参数。例如：@QueryParameter("id") String id；

@Header: 标注方法参数来获取请求头信息。例如：@Header("Authorization") String auth；

@AncestorInPath: 标注方法参数来获取请求URL中的祖先节点。例如：@AncestorInPath String projectName；

@DataBoundConstructor: 标注构造函数来进行数据绑定。用于构造类的实例，将请求参数绑定到对象属性上；

@DataBoundSetter: 标注setter方法来进行数据绑定。用于设置对象属性，将请求参数绑定到对象属性上；

@JavaScriptMethod: 标注方法可以在Jelly脚本中被调用。用于实现AJAX功能。

以上是Stapler框架中常用的注解，通过它们可以方便地处理HTTP请求，并获取请求参数、请求头等信息。

## 3. jenkins核心注解和类

### 3.1 Jenkins 中常用的注解及其用法

@Extension: 标注扩展点的实现类。Jenkins 中有很多扩展点，如 SCM、构建后操作等，如果要实现扩展点，需要创建实现类并标注该注解；

@Symbol: 标注扩展点的唯一符号。可以让用户通过符号来引用扩展点，比如 buildDiscarder(logRotator)，其中 logRotator 就是一个扩展点符号；

@ExtensionPoint: 标注扩展点接口。如果要创建扩展点，需要先创建扩展点接口，并标注该注解；

@DataBoundConstructor: 标注构造函数来进行数据绑定。用于构造类的实例，将请求参数绑定到对象属性上；

@DataBoundSetter: 标注 setter 方法来进行数据绑定。用于设置对象属性，将请求参数绑定到对象属性上；

@ExtensionMethod: 标注扩展方法。用于在 Jenkins 中提供新的 Groovy 方法，扩展 Jenkins 的 DSL，使得用户可以通过 Groovy 代码来调用 Jenkins API，实现更加复杂的自动化操作；

@RequirePOST: 标注方法必须使用 HTTP POST 请求。如果使用其他 HTTP 请求访问该方法，将返回一个 405 错误；

@JavaScriptMethod: 标注方法可以在 Jelly 脚本中被调用。用于实现 AJAX 功能；

@SuppressFBWarnings: 标注代码中的 FindBugs 警告。Jenkins 使用 FindBugs 工具来检测代码中可能存在的 bug，如果代码中存在 false positive 的警告，可以使用该注解来屏蔽掉这些警告。

@Initializer: 标注初始化方法。Jenkins 中有很多初始化方法，如 init()、start() 等，如果要创建初始化方法，需要在该方法上标注该注解；

@Initializer(after = InitMilestone.PLUGINS_PREPARED): 标注在插件初始化后的初始化方法。如果初始化方法依赖于插件，需要使用该注解来保证插件已经初始化完成；

@Initializer(before = InitMilestone.PLUGINS_STARTED): 标注在插件启动前的初始化方法。如果初始化方法需要在插件启动前执行，需要使用该注解来保证初始化方法在插件启动前执行；

@QueueAction: 标注队列操作。Jenkins 中有很多队列操作，如 ScheduleBuildAction、CauseAction 等，如果要创建队列操作，需要创建实现类并标注该注解；

@JavaScriptMethod: 标注方法可以在 Jelly 脚本中被调用。用于实现 AJAX 功能；

@RequirePOSTWithJenkinsSession: 标注方法必须使用 HTTP POST 请求，并且需要 Jenkins Session。如果没有 Jenkins Session，则会重定向到登录页面；

@QueryParameter: 标注查询参数。可以将查询参数绑定到方法的参数上；

@Default: 标注默认值。用于设置方法的参数默认值；

@Icon: 标注图标。可以为 Jenkins 插件添加图标；

@Localized: 标注本地化。可以为 Jenkins 插件添加本地化支持



### 3.2 Jenkins 中核心类及其用法

1. hudson.model.AbstractProject: 抽象类，表示 Jenkins 中的一个项目。通过该类可以获取项目的各种属性，如构建历史、构建环境等；

2. hudson.model.Build: 表示 Jenkins 中的一个构建。通过该类可以获取构建的各种属性，如构建编号、持续时间、状态等；

3. hudson.model.BuildListener: 表示构建监听器。当构建开始、结束、产生输出等事件时，会触发该监听器中的相应方法；

4. hudson.model.Cause: 表示 Jenkins 中的一个构建原因。Jenkins 中有很多构建原因，如用户手动触发构建、定时触发构建、SCM 变更触发构建等。通过该类可以获取构建原因的各种属性，如描述、用户、时间等；

5. hudson.model.Computer: 表示 Jenkins 中的一个计算机。通过该类可以获取计算机的各种属性，如节点名称、节点描述、在线状态等；

6. hudson.model.Executor: 表示 Jenkins 中的一个执行器。每个执行器都会运行一个构建，通过该类可以获取执行器的各种属性，如进程 ID、当前构建等；

7. hudson.model.Item: 抽象类，表示 Jenkins 中的一个项目或节点。通过该类可以获取项目或节点的各种属性，如名称、描述、权限等；

8. hudson.model.Job: 抽象类，表示 Jenkins 中的一个任务。通过该类可以获取任务的各种属性，如构建历史、构建环境等；

9. hudson.model.Label: 表示 Jenkins 中的一个标签。通过该类可以获取标签的各种属性，如名称、描述等；

10. hudson.model.LabelExpression: 表示 Jenkins 中的一个标签表达式。通过该类可以创建标签表达式，如 node('linux && x86_64')；

11. hudson.model.Node: 抽象类，表示 Jenkins 中的一个节点。通过该类可以获取节点的各种属性，如名称、描述、标签等；

12. hudson.model.ParametersAction: 表示 Jenkins 中的一个构建参数。通过该类可以获取构建参数的各种属性，如名称、值等；

13. hudson.model.Run: 抽象类，表示 Jenkins 中的一个构建或者一个部署。通过该类可以获取构建或部署的各种属性，如构建编号、持续时间、状态等；

14. hudson.model.TaskListener: 表示任务监听器。当任务开始、结束、产生输出等事件时，会触发该监听器中的相应方法；

15. hudson.model.User: 表示 Jenkins 中的一个用户。通过该类可以获取用户的各种属性，如用户名、邮箱、密码等；

16. hudson.model.View: 抽象类，表示 Jenkins 中的一个视图。通过该类可以获取视图的各种属性，如名称、描述、项目列表等；

17. hudson.scm.SCM: 抽象类，表示 Jenkins 中

18. Hudson：Jenkins 的核心类，包含了所有 Jenkins 系统的配置和状态，它是 Jenkins 服务中的单例对象。

19. Jenkins：Hudson 类的别名，是为了向后兼容而保留的。

20. Run：Jenkins 中表示一个构建或者一个构建的一次运行。它包含了构建的状态和结果、构建的日志信息等。

21. Build：Run 的子类，表示一个构建，包含了构建的一些特定信息，如构建编号、构建时间、构建状态等。

22. FreeStyleProject：Jenkins 中的一个自由风格项目，是 Jenkins 中最常用的项目类型之一。它可以执行 Shell 脚本、Windows 批处理脚本、Ant、Maven 等构建命令。

23. AbstractProject：FreeStyleProject 的父类，定义了 Jenkins 中所有项目的一些基本属性和行为，如 SCM 工具、构建触发器、构建后操作等。

24. Job：AbstractProject 的子类，表示一个抽象的项目或作业，可以是自由风格项目、Maven 项目、多分支流水线项目等。


### 3.3  Describable接口和Descriptor类 

Describable接口和Descriptor类是用于实现可描述对象的封装和提供描述信息的类。

具体来说，当您想要创建一个可描述对象时，需要让该对象实现Describable接口，并且为该对象编写Descriptor类。其中，Describable接口定义了一个名为“getDescriptor”的方法，它返回Descriptor对象，而Descriptor类则负责提供有关Describable对象的元数据信息。

#### 主要功能

1. Describable接口

Describable接口是所有可描述对象的基本接口。当您的类需要拥有描述信息时，请让该类实现Describable接口。此外，您还需要为该类提供一个Descriptor类，以便外部用户能够获取该类的元数据信息。

2. Descriptor类

Descriptor类是用于提供Describable对象的元数据信息的类。每个Describable对象都有一个对应的Descriptor对象，它包含该对象的一些信息，例如该对象支持哪些参数、如何验证这些参数、如何显示该对象等等。因此，Descriptor类常常被用于定义各种插件、构建器、触发器、发布者等Jenkins扩展点的元数据信息。

总之，Describable接口和Descriptor类是Jenkins中非常重要的两个类，它们为Jenkins扩展点提供了一种标准化的描述方式，使得Jenkins的插件和其他扩展点更加易用和可扩展。



#### 实现类的示例

1. SCM（Source Control Management）类

SCM类是Jenkins中用于管理源代码控制系统的抽象类，该类实现了Describable接口，并且提供了一个Descriptor类。 Descriptor类为用户提供了设置SCM相关参数的界面，并验证这些参数是否合法。

2. BuildWrapper类

BuildWrapper类是Jenkins中用于包装构建过程的抽象类，该类同样实现了Describable接口，并提供了相应的Descriptor类。 Descriptor类可以为用户提供一些选项来影响构建行为，例如，您可以在Descriptor类中定义一个“超时”选项，以设定构建过程最长执行时间。

3. Publisher类

Publisher类是Jenkins中用于发布构建结果的抽象类，也实现了Describable接口，同时也有相应的Descriptor类。 Descriptor类可以允许用户配置不同类型的构建后操作，例如发送电子邮件、上传构建结果等等。

4. Trigger类

Trigger类是Jenkins中用于触发构建过程的抽象类，同样实现了Describable接口并提供相应的Descriptor类。 Descriptor类可以允许用户配置何时触发构建过程，例如，基于定期或者代码仓库更新等条件。

总之，Jenkins中很多扩展点都依赖于Describable接口和Descriptor类，以提供一种标准化的描述方式和用户界面，使得插件或其他扩展点更加易用和可扩展。




## 参考

- [Learn Jenkins the hard way (1) - 从源码运行Jenkins开始](https://developer.aliyun.com/article/70440?spm=a2c6h.14164896.0.0.199a1859TSsIYV)
- [Maven常用参数说明](https://www.jianshu.com/p/25aff2bf6e56)
- [Jenkins任务调度源码简要分析](https://blog.csdn.net/qq_43509535/article/details/121030971)
- [Jenkins 一致性Hash节点调度](https://blog.csdn.net/west_609/article/details/103946448)
- [[ 源码解析 ] Jenkins 的调度过程以及相关组件的源码解读](https://nagle.top/2020/11/02/Jenkins-Queue-Arch.html)
- [stapler (github)](https://github.com/jenkinsci/stapler)
- [jenkins源码阅读：启动和请求处理](https://myzhan.github.io/post/jenkins-src-entry-point/)

