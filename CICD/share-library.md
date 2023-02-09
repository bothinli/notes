# Jenkins共享库

## 1. 介绍

## 2. 使用

## 3. 语法

### 3.1 内置变量

#### Jenkins

`Jenkins`是Jenkins中的一个中心类，可以通过这个类来操作jenkins的一些资源。

> 类api [jenkins.model.Jenkins](https://javadoc.jenkins-ci.org/jenkins/model/Jenkins.html)

#### env

通过`env`变量可以访问到此次构建所包含的所有环境变量，同时也可以为此次构建添加环境变量

> 类api [org.jenkinsci.plugins.workflow.cps.EnvActionImpl](https://javadoc.jenkins.io/plugin/workflow-cps/org/jenkinsci/plugins/workflow/cps/EnvActionImpl.html)



**常用方法**

| 方法名                                                       | 返回值                                                       | 说明                                             |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------ |
| **[getProperty](https://javadoc.jenkins.io/plugin/workflow-cps/org/jenkinsci/plugins/workflow/cps/EnvActionImpl.html#getProperty(java.lang.String))**(StringpropertyName) | String                                                       | 获取环境变量，也可以通过`env.`加环境变量名获取   |
| **[setProperty](https://javadoc.jenkins.io/plugin/workflow-cps/org/jenkinsci/plugins/workflow/cps/EnvActionImpl.html#setProperty(java.lang.String,java.lang.Object))**(String propertyName, Object newValue) | void                                                         | 添加环境变量，也可以通过 `env.xxx = "xxx"`来设置 |
| **[getEnvironment](https://javadoc.jenkins.io/plugin/workflow-cps/org/jenkinsci/plugins/workflow/cps/EnvActionImpl.html#getEnvironment())**() | [EnvVars](https://javadoc.jenkins.io/hudson/EnvVars.html?is-external=true) | 获取所有环境变量                                 |

**常见内置环境变量**

| 环境变量名      | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| STAGE_NAME      | 阶段名称                                                     |
| BUILD_NUMBER    | 当前构建号                                                   |
| JOB_NAME        | 流水线全名，如果有文件夹，会包含文件夹。如：foo/bar          |
| JOB_BASE_NAME   | 流水线名称，such as "foo" for "bar/foo".                     |
| BUILD_TAG       | 构建标记 格式如 jenkins-${JOB_NAME}-${BUILD_NUMBER} 常用于保存构建中文件的文件名前缀 |
| EXECUTOR_NUMBER | 标识执行此构建的当前执行器（同一机器的执行器之间）的唯一编号 |
| JENKINS_URL     | jenkins服务地址                                              |
| NODE_NAME       | 构建机器名称                                                 |
| NODE_LABELS     | 构建机器标签                                                 |
| WORKSPACE       | 构建工作目录                                                 |



遍历所有环境变量

```groovy
def call(){
    env.getEnvironment().each { name, value ->
        println "${name}: ${value}"
    }
}
```



#### params

通过`params`可以访问此次构建定义的所有参数，这个变量只能访问不能进行修改。

> 类 java.util.Collections$UnmodifiableMap

使用示例

```groovy
if (params.BOOLEAN_PARAM_NAME) {doSomething()}

if (params.getOrDefault('BOOLEAN_PARAM_NAME', true)) {doSomething()}
```



#### currentBuild

通过这个变量可以访问当前构建的一些信息。

> 类api [org.jenkinsci.plugins.workflow.support.steps.build.RunWrapper](https://javadoc.jenkins.io/plugin/workflow-support/org/jenkinsci/plugins/workflow/support/steps/build/RunWrapper.html)

