# 声明式pipeline语法

## 1. pipeline的组成

Jenkins pipeline其实就是基于Groovy语言实现的一种DSL（领域特定语言），用于描述整条流水线是如何进行的。流水线的内容包括执行编译、打包、测试、输出测试报告等步骤。

### 1.1 pipeline最简结构

从软件版本控制库到用户手中这一过程可以分成很多阶段，每个阶段只专注处理一件事情，而这件事情又是通过多个步骤来完成的，这就是软件工程的pipeline。Jenkins对这个过程进行抽象，设计出一个基本的pipeline结构。

```groovy
pipeline {
	agent any
	stages {
		stage('build') {
			steps {
				echo "hello world"
			}
		}
	}
}
```

- pipeline：代表整条流水线，包含整条流水线的逻辑。
-  stage部分：阶段，代表流水线的阶段。每个阶段都必须有名称。本例中，build就是此阶段的名称。
- stages部分：流水线中多个stage的容器。stages部分至少包含一个stage。
- steps部分：代表阶段中的一个或多个具体步骤（step）的容器。steps部分至少包含一个步骤，本例中，echo就是一个步骤。在一个stage中有且只有一个steps。
- agent部分：指定流水线的执行位置（Jenkins agent）。流水线中的每个阶段都必须在某个地方（物理机、虚拟机或Docker容器）执行，agent部分即指定具体在哪里执行。

以上每一个部分（section）都是必需的，少一个，Jenkins都会报错。

### 1.2 步骤

pipeline基本结构决定的是pipeline整体流程，但是真正“做事”的还是pipeline中的每一个步骤。步骤是pipeline中已经不能再拆分的最小操作。前文中，我们只看到两个步骤：sh和echo。sh是指执行一条shell命令；echo是指执行echo命令。这两个步骤只是Jenkins pipeline内置的大量步骤中的两个。

更好的设计是：步骤是可插拔的，就像Jenkins的插件一样。如果现有的插件不用修改或者只需要简单修改，就能在Jenkins pipeline中当成一个步骤来使用。

Jenkins就是这样做的，只需要对现有的插件进行一些修改，就可以在pipeline中被当成一个步骤使用。这样大大降低了从现有依赖于界面的插件过渡到pipeline中步骤的成本。

已经有哪些插件适配了Jenkins pipeline呢？pipeline plugin的GitHub仓库给出了一个列表（https：//github.com/jenkinsci/pipeline-plugin/blob/master/COMPATIBILITY.md）方便大家检索，如图3-1所示（只截取了一部分）。

### 1.3 post部分

post部分包含的是在整个pipeline或阶段完成后一些附加的步骤。post部分是可选的，所以并不包含在pipeline最简结构中。但这并不代表它作用不大。

根据pipeline或阶段的完成状态，post部分分成多种条件块，包括：

- always：不论当前完成状态是什么，都执行。
- changed：只要当前完成状态与上一次完成状态不同就执行。
- fixed：上一次完成状态为失败或不稳定（unstable），当前完成状态为成功时执行。
- regression：上一次完成状态为成功，当前完成状态为失败、不稳定或中止（aborted）时执行。
- aborted：当前执行结果是中止状态时（一般为人为中止）执行。
- failure：当前完成状态为失败时执行。
- success：当前完成状态为成功时执行。
- unstable：当前完成状态为不稳定时执行。
- cleanup：清理条件块。不论当前完成状态是什么，在其他所有条件块执行完成后都执行。
- post部分可以同时包含多种条件块。以下是post部分的完整示例。

```groovy
pipeline {
	agent any
	stages {
		stage('build') {
			steps {
				echo "hello world"
			}
      		post{
                always{
                    echo "post condition: always"
                }
                success{
                    echo "post condition: success"
                }
                failure{
                    echo "post condition: failure"
                }
                aborted{
                    echo "post condition: aborted"
                }
            }
		}
	}
	post{
        always{
            echo "global post condition: always"
        }
        success{
            echo "global post condition: success"
        }
        failure{
            echo "global post condition: failure"
        }
        aborted{
            echo "global post condition: aborted"
        }
    }
}
```

## 2. pipeline指令

### 2.1 pipeline支持的指令

显然，基本结构满足不了现实多变的需求。所以，Jenkins pipeline通过各种指令（directive）来丰富自己。指令可以被理解为对Jenkins pipeline基本结构的补充。

Jenkins pipeline支持的指令有：

- environment：用于设置环境变量，可定义在stage或pipeline部分。
- tools：可定义在pipeline或stage部分。它会自动下载并安装我们指定的工具，并将其加入PATH变量中。
- input：定义在stage部分，会暂停pipeline，提示你输入内容。
- options：用于配置Jenkins pipeline本身的选项，比如options {retry（3）}指当pipeline失败时再重试2次。options指令可定义在stage或pipeline部分。
- parallel：并行执行多个step。在pipeline插件1.2版本后，parallel开始支持对多个阶段进行并行执行。
- parameters：与input不同，parameters是执行pipeline前传入的一些参数。
- triggers：用于定义执行pipeline的触发器。
- when：当满足when定义的条件时，阶段才执行。

在使用指令时，需要注意的是每个指令都有自己的“作用域”。如果指令使用的位置不正确，Jenkins将会报错。

### 2.2 options指令

options指令用于配置整个Jenkins pipeline本身的选项。根据具体的选项不同，**可以将其放在pipeline块或stage块中**。以下例子若没有特别说明，options被放在pipeline块中。

- buildDiscarder：保存最近历史构建记录的数量。当pipeline执行完成后，会在硬盘上保存制品和构建执行日志，如果长时间不清理会占用大量空间，设置此选项后会自动清理。此选项只能在pipeline下的options中使用。示例如下：

  ```groovy
  options {
  	buildDiscarder(logRotator(numToKeepStr: '10'))
  }
  ```

- buildDiscarder：保存最近历史构建记录的数量。当pipeline执行完成后，会在硬盘上保存制品和构建执行日志，如果长时间不清理会占用大量空间，设置此选项后会自动清理。此选项只能在pipeline下的options中使用。示例如下：

  ```groovy
  options {
  	checkoutToSubdirectory('subdir')
  }
  ```

- disableConcurrentBuilds：同一个pipeline，Jenkins默认是可以同时执行多次的，如图3-2所示。此选项是为了禁止pipeline同时执行。示例如下：

  ```groovy
  options {
  	disableConcurrentBuilds()
  }
  ```

- newContainerPerStage：当agent为docker或dockerfile时，指定在同一个Jenkins节点上，每个stage都分别运行在一个新的容器中，而不是所有stage都运行在同一个容器中。

  ```groovy
  options {
  	newContainerPerStage()
  }
  ```

- retry：当发生失败时进行重试，可以指定整个pipeline的重试次数。需要注意的是，这个次数是指总次数，包括第1次失败。以下例子总共会执行4次。当使用retry选项时，options可以被放在stage块中。

  ```groovy
  pipeline {
  	agent any
  	options {
  		retry(4)
  	}
  	stages {
  		stage('build') {
  			steps {
  				echo "hello world"
  			}
  		}
  	}
  }
  ```

-  timeout：如果 pipeline 执行时间过长，超出了我们设置的 timeout 时间，Jenkins 将中止pipeline。以下例子中以小时为单位，还可以以 SECONDS（秒）、MINUTES（分钟）为单位。当使用timeout选项时，options可以被放在stage块中。

  ```groovy
  options {
  	timeout(time: 10, unit: 'HOURS')
  }
  ```

### 2.3 when指令

when指令允许pipeline根据给定的条件，决定是否执行阶段内的步骤。when指令必须至少包含一个条件。when指令除了支持branch判断条件，还支持多种判断条件。

- changelog：如果版本控制库的changelog符合正则表达式，则执行

  ```groovy
  when {
  	changelog '.*^\\[DEPENDENCY\\] .+$'
  }
  ```

- changeset：如果版本控制库的变更集合中包含一个或多个文件符合给定的Ant风格路径表达式，则执行

  ```groovy
  when {
  	changeset "**/*.js"
  }
  ```

- environment：如果环境变量的值与给定的值相同，则执行

  ```groovy
  when {
  	environment name: 'DEPLOY_TO', value: 'production'
  }
  ```

- equals：如果期望值与给定的值相同，则执行

  ```groovy
  when {
  	equals expected: 2, actual: currentBuild.number
  }
  ```

- expression：如果Groovy表达式返回的是true，则执行

  当表达式返回的是字符串时，它必须转换成布尔类型或null；否则，所有的字符串都被当作true处理。

  ```groovy
  when {
  	expression {
  		return env.BRANCH_NAME != 'master'
  	}
  }
  ```

-  buildingTag：如果pipeline所执行的代码被打了tag（代码仓库打tag），则执行

  ```groovy
  when {
  	buildingTag()
  }
  ```

- tag：如果pipeline所执行的代码被打了tag，且tag名称符合规则，则执行

  如果tag的参数为空，即tag（），则表示不论tag名称是什么都执行，与buildingTag的效果相同。tag条件支持comparator参数，支持的值如下。

  - EQUALS：简单的文本比较。

    ```groovy
    when {
    	tag pattern: "release-3.1", comparator: "EQUALS"
    }
    ```

  - GLOB （默认值）：Ant风格路径表达式。由于是默认值，所以使用时一般省略。完整写法如下：

    ```groovy
    when {
    	tag pattern: "release-*", comparator: "GLOB"
    }
    ```

  - REGEXP：正则表达式。使用方法如下：

    ```groovy
    when {
    	tag pattern: "release-\\d+", comparator: "REGEXP"
    }
    ```

- allOf：所有条件都必须符合。下例表示当分支为master且环境变量DEPLOY_TO的值为production时，才符合条件。

  ```groovy
  when {
  	allOf {
  		branch 'master'
  		environment name: 'DEPLOY_TO', value: 'production'
  	}
  }
  ```

- anyOf：其中一个条件为true，就符合。下例表示master分支或staging分支都符合条件。

  ```groovy
  when {
  	anyOf {
  		branch 'master'
  		branch 'staging'
  	}
  }
  ```

### 2.4 parameters指令

在Jenkins pipeline中定义参数使用的是parameters指令，其只允许被放在pipeline块下。代码如下：

```groovy
pipeline {
	agent any

	parameters {
		booleanParam(defaultValue: true, description: '', name: 'userFlag')
	}

	stages {
		stage("foo") {
			steps {
				echo "flag: ${params.userFlag}"
			}
		}
	}
}
```

在定义了pipeline的参数后，如何使用呢？被传入的参数会放到一个名为params的对象中，在pipeline中可直接使用。params.userFlag就是引用parameters指令中定义的userFlag参数。

值得注意的是，在Jenkins新增此pipeline后，至少要手动执行一次，它才会被Jenkins加载生效。生效后，在执行项目时，就可以设置参数值了

- booleanParam方法用于定义一个布尔类型的参数。

  booleanParam方法接收三个参数。

  - defaultValue：默认值。
  - description：参数的描述信息。
  - name：参数名。

- string，字符串类型。

- text，多行文本类型，换行使用\n。

- choice，选择参数类型，使用\n来分隔多个选项。

- password，密码类型。

### 2.5 environment指令

environment指令可以在pipeline中定义，代表变量作用域为整个pipeline；也可以在stage中定义，代表变量只在该阶段有效。

但是这些变量都不是跨pipeline的，比如pipeline a访问不到pipeline b的变量。在pipeline之间共享变量可以通过参数化pipeline来实现。我们将在第8章中进行讨论。

在实际工作中，还会遇到一个环境变量引用另一个环境变量的情况。在environment中可以这样定义：

```groovy
environment {
	server_name = 'mail-server'
  version = "${BUILD_NUMBER}"
	artifact_name = "${server_name}-${verison}.jar"
}
```

值得注意的是，如果在environment中定义的变量与env中的变量重名，那么被重名的变量的值会被覆盖掉

- Jenkins内置环境变量

  pipeline内置环境变量可以通过`http://<JENKINS_URL>/job/<job_name>/pipeline-syntax/globalsenv`页面查看

  在调试pipeline时，可以在pipeline的开始阶段加一句：`sh 'printenv'`，将env变量的属性值打印出来。这样可以帮助我们避免不少问题。

- 自定义全局环境变量

  env中的变量都是Jenkins内置的，或者是与具体pipeline相关的。有时候，我们需要定义一些全局的跨pipeline的自定义变量。进入Manage Jenkins→Configure System→Global properties页，勾选“Environment variables”复选框，单击“Add”按钮，在输入框中输入变量名和变量值即可

### 2.6 tools指令



### 2.7 triggers指令



## 3. pipeline内置基础步骤

pipeline内置步骤可以通过`http://<JENKINS_URL>/job/<job_name>/pipeline-syntax/html`页面查看

### 3.1 文件目录相关步骤

#### deleteDir：删除当前目录

deleteDir是一个无参步骤，删除的是当前工作目录。通常它与dir步骤一起使用，用于删除指定目录下的内容。

#### dir：切换到目录

默认pipeline工作在工作空间目录下，dir步骤可以让我们切换到其他目录。使用方法如下：

```groovy
dir('/var/logs') {
	deleteDir()
}
```

#### fileExists：判断文件是否存在

fileExists（'/tmp/a.jar'）判断/tmp/a.jar文件是否存在。如果参数是相对路径，则判断在相对当前工作目录下，该文件是否存在。结果返回布尔类型。

#### isUnix：判断是否为类UNIX系统

如果当前pipeline运行在一个类UNIX系统上，则返回true。

#### pwd：确认当前目录

pwd与Linux的pwd命令一样，返回当前所在目录。

它有一个布尔类型的可选参数：tmp，如果参数值为true，则返回与当前工作空间关联的临时目录。

#### writeFile：将内容写入指定文件中

writeFile支持的参数有：

- file：文件路径，可以是绝对路径，也可以是相对路径。
- text：要写入的文件内容。
- encoding（可选）：目标文件的编码。如果留空，则使用操作系统默认的编码。如果写的是Base64的数据，则可以使用Base64编码。

#### readFile：读取文件内容

读取指定文件的内容，以文本返回。

readFile支持的参数有：

- file：路径，可以是绝对路径，也可以是相对路径。
- encoding（可选）：读取文件时使用的编码。示例如下：

```groovy
script {
	writeFile(file: "base.txt", text: "amVua21ucyBib29r", encoding: "Base64")
	def content = readFile(file: 'base.txt', encoding: 'UTF-8')
	echo "${content}"
	// 打印结果：jenkins book
}
```

### 3.2 制品相关步骤

#### stash：保存临时文件

stash步骤可以将一些文件保存起来，以便被同一次构建的其他步骤或阶段使用。如果整个pipeline的所有阶段在同一台机器上执行，则stash步骤是多余的。所以，通常需要stash的文件都是要跨Jenkins node使用的。

stash步骤会将文件存储在tar文件中，对于大文件的stash操作将会消耗Jenkins master的计算资源。Jenkins官方文档推荐，当文件大小为5∼100MB时，应该考虑使用其他替代方案。

stash步骤的参数列表如下：

- name：字符串类型，保存文件的集合的唯一标识。
- allowEmpty：布尔类型，允许stash内容为空。
- excludes：字符串类型，将哪些文件排除。如果排除多个文件，则使用逗号分隔。留空代表不排除任何文件。
- includes：字符串类型，stash哪些文件，留空代表当前文件夹下的所有文件。
- useDefaultExcludes：布尔类型，如果为true，则代表使用Ant风格路径默认排除文件列表。

除了name参数，其他参数都是可选的。excludes和includes使用的是Ant风格路径表达式。在3.7.5节中将简单介绍该表达式写法。

#### unstash：取出之前stash的文件

unstash步骤只有一个name参数，即stash时的唯一标识。通常stash与unstash步骤同时使用。以下是完整示例。

```groovy
pipeline {
	agent none

	stages {
		stage('stash') {
			agent { label "master" }
			steps {
				writeFile file: "a.txt",text: "$BUILD_NUMBER"
				stash(name: "abc", includes: "a.txt")
			}
		}
		stage('unstash') {
			agent { label "node2" }
			steps {
				unstash("abc")
				def content = readFile("a.txt")
				echo "${content}"
			}
		}
	}
}
```

stash步骤在master节点上执行，而unstash步骤在node2节点上执行。

### 3.3 命令相关步骤

与命令相关的步骤其实是Pipeline：Nodes and Processes插件提供的步骤。由于它是Pipeline插件的一个组件，所以基本不需要单独安装。

#### sh：执行shell命令

sh步骤支持的参数有：

- script：将要执行的shell脚本，通常在类UNIX系统上可以是多行脚本。
- encoding：脚本执行后输出日志的编码，默认值为脚本运行所在系统的编码。
- returnStatus：布尔类型，默认脚本返回的是状态码，如果是一个非零的状态码，则会引发pipeline执行失败。如果returnStatus参数为true，则不论状态码是什么，pipeline的执行都不会受影响。
- returnStdout：布尔类型，如果为true，则任务的标准输出将作为步骤的返回值，而不是打印到构建日志中（如果有错误，则依然会打印到日志中）。除了script参数，其他参数都是可选的。

returnStatus与returnStdout参数一般不会同时使用，因为返回值只能有一个。如果同时使用，则只有returnStatus参数生效。

#### bat、powershell步骤

bat步骤执行的是Windows的批处理命令。powershell步骤执行的是PowerShell脚本，支持3+版本。这两个步骤支持的参数与sh步骤的一样

### 3.4 其他命令步骤

#### build步骤触发下一流水线

既然存在参数化的pipeline，那么就表示可以在一个pipeline中“调用”另一个pipeline。在Jenkinspipeline中可以使用build步骤实现此功能。build步骤是pipeline插件的一个组件，所以不需要另外安装插件，可以直接使用。

build步骤其实也是一种触发pipeline执行的方式，它与triggers指令中的upstream方式有两个区别：

（1） build步骤是由上游pipeline使用的，而upstream方式是由下游pipeline使用的。

（2） build步骤是可以带参数的，而upstream方式只是被动触发，并且没有带参数。

如下我们可以在steps部分定义：

```groovy
steps {
	build(
		job: 'next-job-name',
		parameters: [
			booleanParam(name: 'userFlag', value:)
		]
	)
}
```

build步骤的基本参数。

- job（必填）：目标Jenkins任务的名称。

- parameters（可选）：数组类型，传入目标pipeline的参数列表。传参方法与定参方法类似。

  ```groovy
  parameters: [
  	booleanParam(name: 'DEBUG_BUILD', value: true),
  	password(name: 'PASSWORD', value: 'prodSECRET'),
  	string(name: 'DEPLOY_ENV', value: 'prod'),
  	text(name: 'DEPLOY_TEXT', value: 'a\nb\nc\n'),
  	string(name: 'CHOICES', value: 'dev')
  ]
  ```

  我们注意到choice类型的参数没有对应的传参方法，而是使用string传参方法代替的。

- propagate（可选）：布尔类型，如果值为true，则只有当下游pipeline的最终构建状态为SUCCESS时，上游pipeline才算成功；如果值为false，则不论下游pipeline的最终构建状态是什么，上游pipeline都忽略。默认值为true。

- quietPeriod（可选）：整型，触发下游pipeline后，下游pipeline等待多久执行。如果不设置此参数，则等待时长由下游pipeline确定。单位为秒。

- wait（可选）：布尔类型，是否等待下游pipeline执行完成。默认值为true。

#### Workspace Cleanup插件清理空间

通常，当pipeline执行完成后，并不会自动清理空间。如果需要（通常需要）清理工作空间，则可以通过Workspace Cleanup插件实现。

（1）安装Workspace Cleanup插件（地址为https：//plugins.jenkins.io/ws-cleanup）。

（2）在pipeline的post部分加入插件步骤。

```groovy
post {
	always {
		cleanWs()
	}
}
```

### 3.5 Ant风格路径表达式

Ant是比Maven更老的Java构建工具。Ant发明了一种描述文件路径的表达式，大家都习惯称其为Ant风格路径表达式。Jenkins pipeline的很多步骤的参数也会使用此表达式。

Ant路径表达式包括3种通配符。

- `？`：匹配任何单字符。
- `*`：匹配0个或者任意数量的字符。
- `**`：匹配0个或者更多的目录。

