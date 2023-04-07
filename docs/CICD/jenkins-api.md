
关于 Jenkins REST api部分，主要参考[官方文档](https://www.jenkins.io/doc/book/using/remote-access-api/)和部分实践

## API类型
Jenkins 提供了三种风格的 API类型。
1. XML
    - 即接口返回内容为 xml, eg：`http://<JENKINS_HOST>/config.xml`
2. JSON 以及 JSONP 支持
    - 接口返回内容格式还可以为 JSON, eg: `http://<JENKINS_HOST>/api`
    - JSONP 的例子没有给，查了下似乎需要装个[secure-requester-whitelist](https://github.com/jenkinsci/secure-requester-whitelist-plugin)插件使生效
3. Python
    - 通过 `ast.literal_eval(urllib.urlopen("JENKINS_URL").read())` 将远程输出解析成一个 Python对象

感觉第三种效率不是很高，目前看到的封装库也都是对前两种 API的封装

## 接口列表
官方文档没有给出所有接口的一个列表，需要开发者自己分页面去寻找……  
这里以 JSON接口为主，xml接口为辅总结所有接口。  
接口前缀默认为 `http://<JENKINS_HOST>`
### 首页
通过 `http://<JENKINS_HOST>/api`页面查看

#### 获取首页目录信息
`GET /api/json`

### 任务
通过 `http://<JENKINS_HOST>/job/JobName/api`页面查看

#### 创建任务
`POST /createItem?name=<JOBNAME>`
- header: `Content-Type: application/xml` 
- body: `config.xml`

#### 复制任务
`POST /createItem?name=<NEWJOBNAME>&mode=copy&from=<FROMJOBNAME>`

#### 获取/更新任务配置
`POST /job/<JOBNAME>/config.xml`  
`POST /job/<JOBNAME>/config.xml`, 参数为 `更新后的cofig.xml`

#### 获取多分支任务列表
`GET /job/<JOBNAME>/api/json`

#### 删除任务
`POST /job/<JOBNAME>/doDelete`

#### 获取当前任务|分支任务所有构建
默认包含最近 50次构建
`POST /job/<JOBNAME>/job/<BranchName>/api/json`

#### 更新任务描述
`POST /job/<JOBNAME>/job/<BranchName>/description`
参数类型为`form-data`, description=xxx

#### 构建任务
无参数构建
`POST /job/<JOBNAME>/job/<BranchName>/build`  
带参数构建为：
`POST /job/<JOBNAME>/job/<BranchName>/buildWithParameters`, 参数形式为 `form data`

### 节点
通过 `http://local.jenkins.com/computer/api`及 `http://local.jenkins.com/computer/<DisplayName>/api` 页面查看
#### 获取所有节点信息
`GET /computer/api/json`

#### 获取特定节点信息
`GET /computer/<DisplayName>/api/json`

#### 获取/更新节点配置信息
- `GET /computer/<DisplayName>/config.xml`
- `POST /computer/<DisplayName>/config.xml`, 参数为 `更新后的config.xml`

### 队列
通过 `http://<JENKINS_HOST>/queue/api/`页面查看
#### 获取所有排队任务
`GET /queue/api/json`  
- 可以通过 tree参数进行数组过滤，eg：
    - `GET /queue/api/json?tree=items[actions[causes[shortDescription]]]`  
- 可以对数组结果进行数量筛选 eg: `tree=arrs[attr1, attr2]{0,10}`
    - `{M,N}`: From the M-th element (inclusive) to the N-th element (exclusive).
    - `{M,}`: From the M-th element (inclusive) to the end.
    - `{,N}`: From the first element (inclusive) to the N-th element (exclusive). The same as {0,N}.
    - `{N}`: Just retrieve the N-th element. The same as {N,N+1}.

### Pipeline 
[Pipeline REST api](https://github.com/jenkinsci/pipeline-stage-view-plugin/tree/master/rest-api#get-jobjob-namewfapiruns)

## 参考
- [python-jenkins](https://opendev.org/jjb/python-jenkins/src/branch/master/jenkins/__init__.py)
