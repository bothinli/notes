# Django基础学习笔记

## 1. 快速入门

**安装django**

`pip install django==3.0`

查看安装版本号 `python -m django --version`



**创建项目**

使用Django命令创建项目，它会帮你生成Django项目的一些基础代码和配置

`django-admin startproject project_name`

【注】：在Mac下，默认安装的是Python2.7，可能由于某些原因会找不到django-admin命令，可以使用以下命令代替

​             `python -m django startproject project_name`



**运行项目**

使用命令 `python manage.py runserver [addrport]` 运行Django项目，默认情况下，[`runserver`](https://docs.djangoproject.com/zh-hans/3.0/ref/django-admin/#django-admin-runserver) 命令会将服务器设置为监听本机内部 IP 的 8000 端口。

> 每次修改项目代码，不用重新启动django服务。然而，一些动作，比如添加新文件，将不会触发自动重新加载，这时你得自己手动重启服务器。



**创建应用**

> 项目 VS 应用
>
> 项目和应用有什么区别？应用是一个专门做某件事的网络应用程序——比如博客系统，或者公共记录的数据库，或者小型的投票程序。项目则是一个网站使用的配置和应用的集合。项目可以包含很多个应用。应用可以被很多个项目使用。

在manage.py目录下运行命令，也可以有路径表示manage.py。`python manage.py startapp app_name`



**创建模型**

一个模型类代表一张数据库表，一般写在app目录下的models.py文件中。

```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```



**数据库**

生成迁移文件

`python manage.py makemigrations [app_name]`

查看sql，先看看在迁移的时候实际执行的SQL语句是什么。

`python manage.py sqlmigrate polls 0001`

执行迁移

`python manage.py migrate`





## 2. 项目结构

```tex
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
    # 应用
    polls/
        __init__.py
        admin.py
        apps.py
        migrations/
            __init__.py
        models.py
        tests.py
        views.py
```

- 最外层的 `mysite/` 根目录只是你项目的容器， 根目录名称对Django没有影响，你可以将它重命名为任何你喜欢的名称。
- `manage.py`: 一个让你用各种方式管理 Django 项目的命令行工具。你可以阅读 [django-admin and manage.py](https://docs.djangoproject.com/zh-hans/3.0/ref/django-admin/) 获取所有 `manage.py` 的细节。
- 里面一层的 `mysite/` 目录包含你的项目，它是一个纯 Python 包。它的名字就是当你引用它内部任何东西时需要用到的 Python 包名。 (比如 `mysite.urls`).
- `mysite/__init__.py`：一个空文件，告诉 Python 这个目录应该被认为是一个 Python 包。如果你是 Python 初学者，阅读官方文档中的 [更多关于包的知识](https://docs.python.org/3/tutorial/modules.html#tut-packages)。
- `mysite/settings.py`：Django 项目的配置文件。如果你想知道这个文件是如何工作的，请查看 [Django 配置](https://docs.djangoproject.com/zh-hans/3.0/topics/settings/) 了解细节。
- `mysite/urls.py`：Django 项目的 URL 声明，就像你网站的“目录”。阅读 [URL调度器](https://docs.djangoproject.com/zh-hans/3.0/topics/http/urls/) 文档来获取更多关于 URL 的内容。
- `mysite/asgi.py`：作为你的项目的运行在 ASGI 兼容的Web服务器上的入口。阅读 [如何使用 WSGI 进行部署](https://docs.djangoproject.com/zh-hans/3.0/howto/deployment/wsgi/) 了解更多细节。
- `mysite/wsgi.py`：作为你的项目的运行在 WSGI 兼容的Web服务器上的入口。阅读 [如何使用 WSGI 进行部署](https://docs.djangoproject.com/zh-hans/3.0/howto/deployment/wsgi/) 了解更多细节。



## 3. 路由配置

为了给一个应用设计URL，你需要创建一个Python 模块，通常被称为**URLconf**(URL configuration)。这个模块是纯粹的Python 代码，包含URL 模式(简单的正则表达式)到Python 函数(你的视图)的简单映射。

**附：**

+ [路由配置官方文档](https://docs.djangoproject.com/zh-hans/3.0/topics/http/urls/#url-dispatcher)
+ Django 还提供根据当前语言翻译URL 的一种方法。更多信息参见 [国际化文档](https://docs.djangoproject.com/zh-hans/3.0/topics/i18n/translation/#url-internationalization)。
+ [Django 如何处理一个请求](https://docs.djangoproject.com/zh-hans/3.0/topics/http/urls/#how-django-processes-a-request)



### 3.1 简单的示例

一个路由配置模块就是一个urlpatterns列表，列表的每个元素都是一项path，每一项path都是以path()的形式存在。

path()方法可以接收4个参数，其中前2个是必须的：`route`和`view`，以及2个可选的参数：`kwargs`和`name`。

```python
from django.urls import path

from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<int:year>/', views.year_archive),
    path('articles/<int:year>/<int:month>/', views.month_archive),
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]
```

注意：

- 要从 URL 中取值，使用尖括号`<>`。
- 捕获的值可以选择性地包含转换器类型。比如，使用 `<int:name>` 来捕获整型参数。如果不包含转换器，则会匹配除了 `/` 外的任何字符。
- 这里不需要添加反斜杠，因为每个 URL 都有。比如，应该是 `articles` 而不是 `/articles` 。

一些请求的例子：

- `/articles/2005/03/` 会匹配 URL 列表中的第三项。Django 会调用函数 `views.month_archive(request, year=2005, month=3)` 。
- `/articles/2003/` 将匹配列表中的第一个模式，而不是第二个模式，因为模式是按顺序测试的，而第一个模式是第一个通过的测试。因此如果你需要特别处理一些特殊路由，可以先写在前面。在这里，Django将调用该函数`views.special_case_2003(request)`
- `/articles/2003` 不会匹配这些模式中的任何一个，因为每个模式都要求URL以斜杠结尾。
- `/articles/2003/03/building-a-django-site/` 会匹配 URL 列表中的最后一项。Django 会调用函数 `views.article_detail(request, year=2003, month=3, slug="building-a-django-site")` 。

### 3.2 路径转换器

下面的路径转换器在默认情况下是有效的：

- `str` - 匹配除了 `'/'` 之外的非空字符串。如果表达式内不包含转换器，则会默认匹配字符串。
- `int` - 匹配 0 或任何正整数。返回一个 `int` 。
- `slug` - 匹配任意由 ASCII 字母或数字以及连字符和下划线组成的短标签。比如，`building-your-1st-django-site` 。
- `uuid` - 匹配一个格式化的 UUID 。为了防止多个 URL 映射到同一个页面，必须包含破折号并且字符都为小写。比如，`075194d3-6885-417e-a8a8-6c931e272f00`。返回一个 [`UUID`](https://docs.python.org/3/library/uuid.html#uuid.UUID) 实例。
- `path` - 匹配非空字段，包括路径分隔符 `'/'` 。它允许你匹配完整的 URL 路径而不是像 `str` 那样匹配 URL 的一部分。

**附**：[注册自定义的路径转换器](https://docs.djangoproject.com/zh-hans/3.0/topics/http/urls/#registering-custom-path-converters)



### 3.3 正则表达式路由

如果路径和转化器语法不能很好的定义你的 URL 模式，你可以可以使用正则表达式。如果要这样做，请使用 [`re_path()`](https://docs.djangoproject.com/zh-hans/3.0/ref/urls/#django.urls.re_path) 而不是 [`path()`](https://docs.djangoproject.com/zh-hans/3.0/ref/urls/#django.urls.path) 。

在 Python 正则表达式中，命名正则表达式组的语法是 `(?P<name>pattern)` ，其中 `name` 是组名，`pattern` 是要匹配的模式。

这里是先前 URLconf 的一些例子，现在用正则表达式重写一下：

```python
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail),
]
```

这实现了与前面示例大致相同的功能，除了:

- `^`：意思是“模式必须从这里开始”
- 将要匹配的 URLs 将稍受限制。比如，10000 年将不在匹配，因为 year 被限制长度为4。
- 无论正则表达式进行哪种匹配，每个捕获的参数都作为字符串发送到视图。
- 为了完成这个模式，符号`$`的作用与`^`相反，表示“模式必须在这里结束”。

当从使用 [`path()`](https://docs.djangoproject.com/zh-hans/3.0/ref/urls/#django.urls.path) 切换到 [`re_path()`](https://docs.djangoproject.com/zh-hans/3.0/ref/urls/#django.urls.re_path) （反之亦然），要特别注意，视图参数类型可能发生变化，你可能需要调整你的视图。



**使用未命名的正则表达式组**

还有命名组语法，例如 `(?P<year>[0-9]{4})` ，你也可以使用更短的未命名组，例如 `([0-9]{4})` 。

不是特别推荐这个用法，因为它会更容易在匹配的预期含义和视图参数之间引发错误。

在任何情况下，推荐在给定的正则表达式里只使用一个样式。当混杂两种样式时，任何未命名的组都会被忽略，而且只有命名的组才会传递给视图函数。



### 3.4 包含app的URLconfs

任何时候，你的 `urlpatterns` 都可以 "include" 其它URLconf 模块。这实际上将一部分URL 放置于其它URL 下面。

```python
from django.urls import include, path

urlpatterns = [
    # ... snip ...
    path('community/', include('aggregator.urls')),
    path('contact/', include('contact.urls')),
    # ... snip ...
]
```

而当其中某个URL前缀被重复使用时，可以使用`include`来改进，例如：

```python
from django.urls import include, path
from . import views

urlpatterns = [
    path('<page_slug>-<page_id>/', include([
        path('history/', views.history),
        path('edit/', views.edit),
        path('discuss/', views.discuss),
        path('permissions/', views.permissions),
    ])),
]
```

被包含的URLconf 会收到来自父URLconf 捕获的任何参数，在上面的例子中，捕获的 `page_slug page_id` 变量将被如期传递给include()指向的URLconf/View。

### 3.5 额外传参

URLconfs 有钩子来允许你把其他参数作为 Python 字典来传递给视图函数。

`path()`函数可带有可选的第三参数（必须是字典），传递到视图函数里。

但是视图函数必须要有相关的参数接收，要不然就会出错。

```python
from django.urls import path
from . import views

urlpatterns = [
    path('blog/<int:year>/', views.year_archive, {'foo': 'bar'}),
    path('blog/', include('inner'), {'blog_id': 3}),
]
```

### 3.6 命名 URL 模式[¶](https://docs.djangoproject.com/zh-hans/3.0/topics/http/urls/#naming-url-patterns)



## 4. 视图

一个视图函数（或简称为视图）是一个 Python 函数/类，它接受 Web 请求并返回一个 Web 响应。这个响应可以是 Web 页面的 HTML 内容，或者重定向，或者404错误，或者 XML 文档，或一个图片...或是任何内容。视图本身包含返回响应所需的任何逻辑。这个代码可以存在任何地方，只要它在你的 Python 路径上就行。可以说，不需要其他东西，这里并没有魔法。为了将代码放置在某处，约定将视图放在名为 `views.py` 的文件里，这个文件放置在项目或应用目录里。

每个视图函数都将 [`HttpRequest`](https://docs.djangoproject.com/zh-hans/3.0/ref/request-response/#django.http.HttpRequest) 对象作为第一个参数，通常名为 `request` 。

视图返回一个包含生成的响应的 [`HttpResponse`](https://docs.djangoproject.com/zh-hans/3.0/ref/request-response/#django.http.HttpResponse) 对象。每个视图函数都要返回 [`HttpResponse`](https://docs.djangoproject.com/zh-hans/3.0/ref/request-response/#django.http.HttpResponse) 对象。





### 视图装饰器[¶](https://docs.djangoproject.com/zh-hans/3.0/topics/http/decorators/#module-django.views.decorators.http)

Django 提供很多装饰器，它们可以为视图支持多种 HTTP 特性。位于`django.views.decorators`包下。

限制http的请求方式

- `require_http_methods(request_method_list)` 要求视图只接受特定的请求方法。
- `require_GET()`装饰器可以要求视图只接受 GET 方法。
- `require_POST()`装饰器可以要求视图只接受 POST 方法。
- `require_safe()`装饰器可以要求视图只接收 GET 和 HEAD 方法。这些方法通常被认为是安全的。

用法如下：

```python
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def my_view(request):
    # I can assume now that only GET or POST requests make it this far
    # ...
    pass
```



## 4. 模型层

### 4.1 常见字段类型

下表列出了所有Django内置的字段类型，但不包括关系字段类型

| 类型                      | 说明                                                         |
| ------------------------- | ------------------------------------------------------------ |
| AutoField                 | 一个自动增加的整数类型字段。通常你不需要自己编写它，Django会自动帮你添加字段：`id = models.AutoField(primary_key=True)`，这是一个自增字段，从1开始计数。如果你非要自己设置主键，那么请务必将字段设置为`primary_key=True`。Django在一个模型中只允许有一个自增字段，并且该字段必须为主键！ |
| BigAutoField              | 64位整数类型自增字段，数字范围更大，从1到9223372036854775807 |
| BigIntegerField           | 64位整数字段（看清楚，非自增），类似IntegerField ，-9223372036854775808 到9223372036854775807。在Django的模板表单里体现为一个`NumberInput`标签。 |
| BinaryField               | 二进制数据类型。较少使用。                                   |
| **BooleanField**          | 布尔值类型。默认值是None。在HTML表单中体现为CheckboxInput标签。如果设置了参数null=True，则表现为NullBooleanSelect选择框。可以提供default参数值，设置默认值。 |
| **CharField**             | 最常用的类型，字符串类型。必须接收一个max_length参数，表示字符串长度不能超过该值。默认的表单标签是text input。 |
| **DateField**             | `class DateField(auto_now=False, auto_now_add=False, **options)` , 日期类型。一个Python中的datetime.date的实例。在HTML中表现为DateInput标签。在admin后台中，Django会帮你自动添加一个JS日历表和一个“Today”快捷方式，以及附加的日期合法性验证。两个重要参数：（参数互斥，不能共存） `auto_now`:每当对象被保存时将字段设为当前日期，常用于保存最后修改时间。`auto_now_add`：每当对象被创建时，设为当前日期，常用于保存创建日期(注意，它是不可修改的)。设置上面两个参数就相当于给field添加了`editable=False`和`blank=True`属性。如果想具有修改属性，请用default参数。例子：`pub_time = models.DateField(auto_now_add=True)`，自动添加发布时间。 |
| DateTimeField             | 日期时间类型。Python的datetime.datetime的实例。与DateField相比就是多了小时、分和秒的显示，其它功能、参数、用法、默认值等等都一样。 |
| DecimalField              | 固定精度的十进制小数。相当于Python的Decimal实例，必须提供两个指定的参数！参数`max_digits`：最大的位数，必须大于或等于小数点位数 。`decimal_places`：小数点位数，精度。 当`localize=False`时，它在HTML表现为NumberInput标签，否则是textInput类型。例子：储存最大不超过999，带有2位小数位精度的数，定义如下：`models.DecimalField(..., max_digits=5, decimal_places=2)`。 |
| DurationField             | 持续时间类型。存储一定期间的时间长度。类似Python中的timedelta。在不同的数据库实现中有不同的表示方法。常用于进行时间之间的加减运算。但是小心了，这里有坑，PostgreSQL等数据库之间有兼容性问题！ |
| **EmailField**            | 邮箱类型，默认max_length最大长度254位。使用这个字段的好处是，可以使用Django内置的EmailValidator进行邮箱格式合法性验证。 |
| **FileField**             | `class FileField(upload_to=None, max_length=100, **options)`上传文件类型，后面单独介绍。 |
| FilePathField             | 文件路径类型，后面单独介绍                                   |
| FloatField                | 浮点数类型，对应Python的float。参考整数类型字段。            |
| **ImageField**            | 图像类型，后面单独介绍。                                     |
| **IntegerField**          | 整数类型，最常用的字段之一。取值范围-2147483648到2147483647。在HTML中表现为NumberInput或者TextInput标签。 |
| **GenericIPAddressField** | `class GenericIPAddressField(protocol='both', unpack_ipv4=False, **options)`,IPV4或者IPV6地址，字符串形式，例如`192.0.2.30`或者`2a02:42fe::4`。在HTML中表现为TextInput标签。参数`protocol`默认值为‘both’，可选‘IPv4’或者‘IPv6’，表示你的IP地址类型。 |
| JSONField                 | JSON类型字段。Django3.1新增。签名为`class JSONField(encoder=None,decoder=None,**options)`。其中的encoder和decoder为可选的编码器和解码器，用于自定义编码和解码方式。如果为该字段提供default值，请务必保证该值是个不可变的对象，比如字符串对象。 |
| PositiveBigIntegerField   | 正的大整数，0到9223372036854775807                           |
| PositiveIntegerField      | 正整数，从0到2147483647                                      |
| PositiveSmallIntegerField | 较小的正整数，从0到32767                                     |
| SlugField                 | slug是一个新闻行业的术语。一个slug就是一个某种东西的简短标签，包含字母、数字、下划线或者连接线，通常用于URLs中。可以设置max_length参数，默认为50。 |
| SmallAutoField            | Django3.0新增。类似AutoField，但是只允许1到32767。           |
| SmallIntegerField         | 小整数，包含-32768到32767。                                  |
| **TextField**             | 用于储存大量的文本内容，在HTML中表现为Textarea标签，最常用的字段类型之一！如果你为它设置一个max_length参数，那么在前端页面中会受到输入字符数量限制，然而在模型和数据库层面却不受影响。只有CharField才能同时作用于两者。 |
| TimeField                 | 时间字段，Python中datetime.time的实例。接收同DateField一样的参数，只作用于小时、分和秒。 |
| **URLField**              | 一个用于保存URL地址的字符串类型，默认最大长度200。           |
| **UUIDField**             | 用于保存通用唯一识别码（Universally Unique Identifier）的字段。使用Python的UUID类。在PostgreSQL数据库中保存为uuid类型，其它数据库中为char(32)。这个字段是自增主键的最佳替代品，后面有例子展示。 |

**1.FileField**

```
class FileField(upload_to=None, max_length=100, **options)
```

上传文件字段（不能设置为主键）。默认情况下，该字段在HTML中表现为一个`ClearableFileInput`标签。在数据库内，我们实际保存的是一个字符串类型，默认最大长度100，可以通过`max_length`参数自定义。真实的文件是保存在服务器的文件系统内的。

重要参数`upload_to`用于设置上传地址的目录和文件名。如下例所示：

```python
class MyModel(models.Model):
    # 文件被传至`MEDIA_ROOT/uploads`目录，MEDIA_ROOT由你在settings文件中设置
    upload = models.FileField(upload_to='uploads/')
    # 或者
    # 被传到`MEDIA_ROOT/uploads/2015/01/30`目录，增加了一个时间划分
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
```

**Django很人性化地帮我们实现了根据日期生成目录或文件的方式！**

**`upload_to`参数也可以接收一个回调函数，该函数返回具体的路径字符串**，如下例：

```python
def user_directory_path(instance, filename):
    #文件上传到MEDIA_ROOT/user_<id>/<filename>目录中
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class MyModel(models.Model):
    upload = models.FileField(upload_to=user_directory_path)
```

例子中，`user_directory_path`这种回调函数，必须接收两个参数，然后返回一个Unix风格的路径字符串。参数`instace`代表一个定义了`FileField`的模型的实例，说白了就是当前数据记录。`filename`是原本的文件名。

从Django3.0开始，支持使用`pathlib.Path` 处理路径。

当你访问一个模型对象中的文件字段时，Django会自动给我们提供一个 FieldFile实例作为文件的代理，通过这个代理，我们可以进行一些文件操作，主要如下：

- FieldFile.name ： 获取文件名
- FieldFile.size： 获取文件大小
- FieldFile.url ：用于访问该文件的url
- FieldFile.open(mode='rb')： 以类似Python文件操作的方式，打开文件
- FieldFile.close()： 关闭文件
- FieldFile.save(name, content, save=True)： 保存文件
- FieldFile.delete(save=True)： 删除文件

这些代理的API和Python原生的文件读写API非常类似，其实本质上就是进行了一层封装，让我们可以在Django内直接对模型中文件字段进行读写，而不需要绕弯子。

**2. ImageField**

```
class ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)
```

用于保存图像文件的字段。该字段继承了FileField，其用法和特性与FileField基本一样，只不过多了两个属性height和width。默认情况下，该字段在HTML中表现为一个ClearableFileInput标签。在数据库内，我们实际保存的是一个字符串类型，默认最大长度100，可以通过max_length参数自定义。真实的图片是保存在服务器的文件系统内的。

`height_field`参数：保存有图片高度信息的模型字段名。 `width_field`参数：保存有图片宽度信息的模型字段名。

**使用Django的ImageField需要提前安装pillow模块，pip install pillow即可。**

**3. 使用FileField或者ImageField字段的步骤：**

1. 在settings文件中，配置`MEDIA_ROOT`，作为你上传文件在服务器中的基本路径（为了性能考虑，这些文件不会被储存在数据库中）。再配置个`MEDIA_URL`，作为公用URL，指向上传文件的基本路径。请确保Web服务器的用户账号对该目录具有写的权限。
2. 添加FileField或者ImageField字段到你的模型中，定义好`upload_to`参数，文件最终会放在`MEDIA_ROOT`目录的“`upload_to`”子目录中。
3. 所有真正被保存在数据库中的，只是指向你上传文件路径的字符串而已。可以通过url属性，在Django的模板中方便的访问这些文件。例如，假设你有一个ImageField字段，名叫`mug_shot`，那么在Django模板的HTML文件中，可以使用`{{ object.mug_shot.url }}`来获取该文件。其中的object用你具体的对象名称代替。
4. 可以通过`name`和`size`属性，获取文件的名称和大小信息。

安全建议：

无论你如何保存上传的文件，一定要注意他们的内容和格式，避免安全漏洞！务必对所有的上传文件进行安全检查，确保它们不出问题！如果你不加任何检查就盲目的让任何人上传文件到你的服务器文档根目录内，比如上传了一个CGI或者PHP脚本，很可能就会被访问的用户执行，这具有致命的危害。

**4. FilePathField**

```python
class FilePathField(path='', match=None, recursive=False, allow_files=True, allow_folders=False, max_length=100, **options)
```

一种用来保存文件路径信息的字段。在数据表内以字符串的形式存在，默认最大长度100，可以通过max_length参数设置。

它包含有下面的一些参数：

`path`：必须指定的参数。表示一个系统绝对路径。path通常是个字符串，也可以是个可调用对象，比如函数。

`match`:可选参数，一个正则表达式，用于过滤文件名。只匹配基本文件名，不匹配路径。例如`foo.*\.txt$`，只匹配文件名`foo23.txt`，不匹配`bar.txt`与`foo23.png`。

`recursive`:可选参数，只能是True或者False。默认为False。决定是否包含子目录，也就是是否递归的意思。

`allow_files`:可选参数，只能是True或者False。默认为True。决定是否应该将文件名包括在内。它和`allow_folders`其中，必须有一个为True。

`allow_folders`： 可选参数，只能是True或者False。默认为False。决定是否应该将目录名包括在内。

比如：

```python
FilePathField(path="/home/images", match="foo.*", recursive=True)
```

它只匹配`/home/images/foo.png`，但不匹配`/home/images/foo/bar.png`，因为默认情况，只匹配文件名，而不管路径是怎么样的。

例子：

```python
import os
from django.conf import settings
from django.db import models

def images_path():
    return os.path.join(settings.LOCAL_FILE_DIR, 'images')

class MyModel(models.Model):
    file = models.FilePathField(path=images_path)
```

**5. UUIDField**

数据库无法自己生成uuid，因此需要如下使用default参数：

```python
import uuid     # Python的内置模块
from django.db import models

class MyUUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 其它字段
```

注意不要写成`default=uuid.uuid4()`



### 4.2 字段的参数

所有的模型字段都可以接收一定数量的参数，比如CharField至少需要一个max_length参数。下面的这些参数是所有字段都可以使用的，并且是可选的。

**null**

该值为True时，Django在数据库用NULL保存空值。默认值为False。对于保存字符串类型数据的字段，请尽量避免将此参数设为True，那样会导致两种‘没有数据’的情况，一种是`NULL`，另一种是空字符串`''`。Django 的惯例是使用空字符串而不是 `NULL`。

**blank**

True时，字段可以为空。默认False。和null参数不同的是，null是纯数据库层面的，而blank是验证相关的，它与表单验证是否允许输入框内为空有关，与数据库无关。所以要小心一个null为False，blank为True的字段接收到一个空值可能会出bug或异常。

**default**

字段的默认值，可以是值或者一个可调用对象。如果是可调用对象，那么每次创建新对象时都会调用。设置的默认值不能是一个可变对象，比如列表、集合等等。lambda匿名函数也不可用于default的调用对象，因为匿名函数不能被migrations序列化。

注意：在某种原因不明的情况下将default设置为None，可能会引发`intergyerror：not null constraint failed`，即非空约束失败异常，导致`python manage.py migrate`失败，此时可将None改为False或其它的值，只要不是None就行。

**choices**

用于页面上的选择框标签，需要先提供一个二维的二元元组，第一个元素表示存在数据库内真实的值，第二个表示页面上显示的具体内容。在浏览器页面上将显示第二个元素的值。例如：

```python
gender = models.SmallIntegerField(choices=[
        (0, '女'),
        (1, '男'),
        (2, '未知')
    ])
```

反过来，要获取一个choices的第二元素的值，可以使用`get_FOO_display()`方法，其中的FOO用字段名代替，即上述使用get_gender_display()获取。

**db_column**

该参数用于定义当前字段在数据表内的列名。如果未指定，Django将使用字段名作为列名。

**db_index**

该参数接收布尔值。如果为True，数据库将为该字段创建索引。

**editable**

如果设为False，那么当前字段将不会在admin后台或者其它的ModelForm表单中显示，同时还会被模型验证功能跳过。参数默认值为True。

**error_messages**

用于自定义错误信息。参数接收字典类型的值。字典的键可以是`null`、 `blank`、 `invalid`、 `invalid_choice`、 `unique`和`unique_for_date`其中的一个。

**help_text**

额外显示在表单部件上的帮助文本。即便你的字段未用于表单，它对于生成文档也是很有用的。

该帮助文本默认情况下是可以带HTML代码的，具有风险：

```
help_text="Please use the following format: <em>YYYY-MM-DD</em>."
```

所以使用时请注意转义为纯文本，防止脚本攻击。

**primary_key**

如果你没有给模型的任何字段设置这个参数为True，Django将自动创建一个AutoField自增字段，名为‘id’，并设置为主键。也就是`id = models.AutoField(primary_key=True)`。如果你为某个字段设置了primary_key=True，则当前字段变为主键，并关闭Django自动生成id主键的功能。

**verbose_name**

为字段设置一个人类可读，更加直观的别名。

对于每一个字段类型，除了`ForeignKey`、`ManyToManyField`和`OneToOneField`这三个特殊的关系类型，其第一可选位置参数都是`verbose_name`。如果没指定这个参数，Django会利用字段的属性名自动创建它，并将下划线转换为空格。

**validators**

运行在该字段上的验证器的列表。







### 4.3 关联关系

#### 多对一（ForeignKey）

多对一的关系，通常被称为外键。外键字段类的定义如下：

`class ForeignKey(to, on_delete, **options)`

外键需要两个位置参数，一个是关联的模型，另一个是`on_delete`。在Django2.0版本后，`on_delete`属于必填参数。

自关联（递归外键），可以使用下面方法：

`models.ForeignKey('self', on_delete=models.CASCADE)`

**参数说明**：

1. **on_delete**：当一个外键关联的对象被删除时，Django将模仿`on_delete`参数定义的SQL约束执行相应操作。

```python
user = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
)
```

​	该参数可选的值都内置在`django.db.models`中（全部为大写），包括：

- CASCADE：模拟SQL语言中的`ON DELETE CASCADE`约束，将定义有外键的模型对象同时删除！
- PROTECT:阻止上面的删除操作，但是弹出`ProtectedError`异常
- SET_NULL：将外键字段设为null，只有当字段设置了`null=True`时，方可使用该值。
- SET_DEFAULT:将外键字段设为默认值。只有当字段设置了default参数时，方可使用。
- DO_NOTHING：什么也不做。
- SET()：设置为一个传递给SET()的值或者一个回调函数的返回值。注意大小写。

2. **to_field**

   默认情况下，外键都是关联到被关联对象的主键上（一般为id）。如果指定这个参数，可以关联到指定的字段上，但是该字段必须具有`unique=True`属性，也就是具有唯一属性。

3. **related_name**

   用于关联对象反向引用模型的名称。

   通常情况下，这个参数我们可以不设置，Django会默认以模型的小写加上`_set`作为反向关联名。





#### 多对多（ManyToManyField）

```
class ManyToManyField(to, **options)
```

建议为多对多字段名使用复数形式。

多对多关系需要一个位置参数：关联的对象模型，其它用法和外键多对一基本类似。

如果要创建一个关联自己的多对多字段，依然是通过`'self'`引用。

**在数据库后台，Django实际上会额外创建一张用于体现多对多关系的中间表**。默认情况下，该表的名称是“`多对多字段名+包含该字段的模型名+一个独一无二的哈希码`”，例如‘author_books_9cdf4’，当然你也可以通过`db_table`选项，自定义表名。

通常情况下，这张表在数据库内的结构是这个样子的：

```text
中间表的id列....模型对象的id列.....被关联对象的id列
# 各行数据
```

**参数说明：**

Related_name、related_query_name、limit_choices_to和外键的用法一致。参考上述用法即可。

**null参数对ManyToManyField多对多字段无效！设置null=True毫无意义**

1. **through**
   如果你想自定义多对多关系的那张额外的关联表，可以使用这个参数！参数的值为一个中间模型。

   最常见的使用场景是你需要为多对多关系添加额外的数据，比如添加两个人建立QQ好友关系的时间。

   ```python
   from django.db import models
   
   class Person(models.Model):
       name = models.CharField(max_length=50)
   
   class Group(models.Model):
       name = models.CharField(max_length=128)
       members = models.ManyToManyField(
           Person,
           through='Membership',       ## 自定义中间表
           through_fields=('group', 'person'),
       )
   
   class Membership(models.Model):  # 这就是具体的中间表模型
       group = models.ForeignKey(Group, on_delete=models.CASCADE)
       person = models.ForeignKey(Person, on_delete=models.CASCADE)
       inviter = models.ForeignKey(
           Person,
           on_delete=models.CASCADE,
           related_name="membership_invites",
       )
       invite_reason = models.CharField(max_length=64)
   ```

   上面的代码中，通过`class Membership(models.Model)`定义了一个新的模型，用来保存Person和Group模型的多对多关系，并且同时增加了‘邀请人’和‘邀请原因’的字段。

2. **through_fields**

   `through_fields`参数指定从中间表模型Membership中选择哪两个字段，作为关系连接字段。

   `through_fields`参数接收一个二元元组('field1', 'field2')，field1是指向定义有多对多关系的模型的外键字段的名称，这里是Membership中的‘group’字段（注意大小写），另外一个则是指向目标模型的外键字段的名称，这里是Membership中的‘person’



3. **db_table**

   设置中间表的名称。不指定的话，则使用默认值。



#### 一对一（OneToOneField）

一对一关系类型的定义如下：

```python
class OneToOneField(to, on_delete, parent_link=False, **options)
```

从概念上讲，一对一关系非常类似具有`unique=True`属性的外键关系，但是反向关联对象只有一个。这种关系类型多数用于当一个模型需要从别的模型扩展而来的情况。

如果你没有给一对一关系设置`related_name`参数，Django将使用当前模型的小写名作为默认值。

也可以连接第三方导入的模型。



### 4.4 元数据类Meta

模型的元数据，指的是“除了字段外的所有内容”，例如排序方式、数据库表名、人类可读的单数或者复数名等等。

想在模型中增加元数据，方法很简单，在模型类中添加一个内部类，名字是固定的`Meta`，然后在这个Meta类下面增加各种元数据选项或者说设置项。参考下面的例子：

```python
from django.db import models

class Ox(models.Model):
    horn_length = models.IntegerField()

    class Meta:         # 注意，是模型的内部类，要缩进！
        ordering = ["horn_length"]
        verbose_name_plural = "oxen"
```

**配置属性：**

**abstract**

如果`abstract=True`，那么模型会被认为是一个抽象模型。抽象模型本身不实际生成数据库表，而是作为其它模型的父类，被继承使用。具体内容可以参考Django模型的继承。

**app_label**

如果定义了模型的app没有在`INSTALLED_APPS`中注册，则必须通过此元选项声明它属于哪个app，例如：

```
app_label = 'myapp'
```

**db_table**

指定在数据库中，当前模型生成的数据表的表名。不要使用SQL语言或者Python的保留字，注意冲突。

如果你没有指定这个选项，那么Django会自动使用app名和模型名，通过下划线连接生成数据表名，比如`app_book`。

友情建议：使用MySQL和MariaDB数据库时，`db_table`用小写英文。

**db_tablespace**

自定义数据库表空间的名字。默认值是项目的`DEFAULT_TABLESPACE`配置项指定的值。

**base_manager_name**

模型的`_base_manager`管理器的名字，默认是`'objects'`。

**default_manager_name**

模型的`_default_manager`管理器的名字。

**default_related_name**

默认情况下，从一个模型反向关联设置有关系字段的源模型，我们使用`<model_name>_set`，也就是源模型的名字+下划线+`set`。

这个元数据选项可以让你自定义反向关系名，同时也影响反向查询关系名！看下面的例子：

```
from django.db import models

class Foo(models.Model):
    pass

class Bar(models.Model):
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'bars'   # 关键在这里
```

具体的使用差别如下：

```
>>> bar = Bar.objects.get(pk=1)
>>> # 不能再使用"bar"作为反向查询的关键字了。
>>> Foo.objects.get(bar=bar)
>>> # 而要使用你自己定义的"bars"了。
>>> Foo.objects.get(bars=bar)
```

**get_latest_by**

Django管理器给我们提供有latest()和earliest()方法，分别表示获取最近一个和最前一个数据对象。但是，如何来判断最近一个和最前面一个呢？也就是根据什么来排序呢？

`get_latest_by`元数据选项帮你解决这个问题，它可以指定一个类似 `DateField`、`DateTimeField`或者`IntegerField`这种可以排序的字段，作为latest()和earliest()方法的排序依据，从而得出最近一个或最前面一个对象。例如：

```
get_latest_by = "order_date"   # 根据order_date升序排列

get_latest_by = ['-priority', 'order_date']  # 根据priority降序排列，如果发生同序，则接着使用order_date升序排列
```

**managed**

该元数据默认值为True，表示Django将按照既定的规则，管理数据库表的生命周期。

如果设置为False，将不会针对当前模型创建和删除数据库表，也就是说Django暂时不管这个模型了。

在某些场景下，这可能有用，但更多时候，你可以忘记该选项。

**order_with_respect_to**

这个选项不好理解。其用途是根据指定的字段进行排序，通常用于关系字段。看下面的例子：

```
from django.db import models

class Question(models.Model):
    text = models.TextField()
    # ...

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ...

    class Meta:
        order_with_respect_to = 'question'
```

上面在Answer模型中设置了`order_with_respect_to = 'question'`，这样的话，Django会自动提供两个API，`get_RELATED_order()`和`set_RELATED_order()`，其中的`RELATED`用小写的模型名代替。假设现在有一个Question对象，它关联着多个Answer对象，下面的操作返回包含关联的Anser对象的主键的列表[1,2,3]：

```
>>> question = Question.objects.get(id=1)
>>> question.get_answer_order()
[1, 2, 3]
```

我们可以通过`set_RELATED_order()`方法，指定上面这个列表的顺序：

```
>>> question.set_answer_order([3, 1, 2])
```

同样的，关联的对象也获得了两个方法`get_next_in_order()`和`get_previous_in_order()`，用于通过特定的顺序访问对象，如下所示：

```
>>> answer = Answer.objects.get(id=2)
>>> answer.get_next_in_order()
<Answer: 3>
>>> answer.get_previous_in_order()
<Answer: 1>
```

这个元数据的作用......还没用过，囧。

**ordering**

最常用的元数据之一了！

用于指定该模型生成的所有对象的排序方式，接收一个字段名组成的元组或列表。默认按升序排列，如果在字段名前加上字符“-”则表示按降序排列，如果使用字符问号“？”表示随机排列。请看下面的例子：

这个顺序是你通过查询语句，获得Queryset后的列表内元素的顺序，切不可和前面的`get_latest_by`等混淆。

```
ordering = ['pub_date']             # 表示按'pub_date'字段进行升序排列
ordering = ['-pub_date']            # 表示按'pub_date'字段进行降序排列
ordering = ['-pub_date', 'author']  # 表示先按'pub_date'字段进行降序排列，再按`author`字段进行升序排列。
```

**permissions**

该元数据用于当创建对象时增加额外的权限。它接收一个所有元素都是二元元组的列表或元组，每个元素都是`(权限代码, 直观的权限名称)`的格式。比如下面的例子：

这个Meta选项非常重要，和auth框架的权限系统紧密相关。

```
permissions = (("can_deliver_pizzas", "可以送披萨"),)
```

**default_permissions**

Django默认会在建立数据表的时候就自动给所有的模型设置('add', 'change', 'delete')的权限，也就是增删改。你可以自定义这个选项，比如设置为一个空列表，表示你不需要默认的权限，但是这一操作必须在执行migrate命令之前。也是配合auth框架使用。

**proxy**

如果设置了`proxy = True`，表示使用代理模式的模型继承方式。具体内容与abstract选项一样，参考模型继承章节。

**required_db_features**

声明模型依赖的数据库功能。比如['gis_enabled']，表示模型的建立依赖GIS功能。

**required_db_vendor**

声明模型支持的数据库。Django默认支持`sqlite, postgresql, mysql, oracle`。

**select_on_save**

决定是否使用1.6版本之前的`django.db.models.Model.save()`算法保存对象。默认值为False。这个选项我们通常不用关心。

**indexes**

接收一个应用在当前模型上的索引列表，如下例所示：

```
from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['first_name'], name='first_name_idx'),
        ]
```

**unique_together**

这个元数据是非常重要的一个！它等同于数据库的联合约束！

举个例子，假设有一张用户表，保存有用户的姓名、出生日期、性别和籍贯等等信息。要求是所有的用户唯一不重复，可现在有好几个叫“张伟”的，如何区别它们呢？（不要和我说主键唯一，这里讨论的不是这个问题）

我们可以设置不能有两个用户在同一个地方同一时刻出生并且都叫“张伟”，使用这种联合约束，保证数据库能不能重复添加用户（也不要和我谈小概率问题）。在Django的模型中，如何实现这种约束呢？

使用`unique_together`，也就是联合唯一！

比如：

```
unique_together = [['name', 'birth_day', 'address'],......]
```

这样，哪怕有两个在同一天出生的张伟，但他们的籍贯不同，也就是两个不同的用户。一旦三者都相同，则会被Django拒绝创建。这个元数据选项经常被用在admin后台，并且强制应用于数据库层面。

unique_together接收一个二维的列表，每个元素都是一维列表，表示一组联合唯一约束，可以同时设置多组约束。为了方便，对于只有一组约束的情况下，可以简单地使用一维元素，例如：

```
unique_together = ['name', 'birth_day', 'address']
```

联合唯一无法作用于普通的多对多字段。

**index_together**

联合索引，用法和特性类似unique_together。

> 使用 [`indexes`](https://docs.djangoproject.com/zh-hans/3.2/ref/models/options/#django.db.models.Options.indexes) 选项代替。
>
> 新的 [`indexes`](https://docs.djangoproject.com/zh-hans/3.2/ref/models/options/#django.db.models.Options.indexes) 选项比 `index_together` 提供了更多的功能。`index_together` 今后可能会被废弃。

**constraints**

为模型添加约束条件。通常是列表的形式，每个列表元素就是一个约束。

```
from django.db import models

class Customer(models.Model):
    age = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=18), name='age_gte_18'),
        ]
```

上例中，会检查age年龄的大小，不得低于18。

**verbose_name**

最常用的元数据之一！用于设置模型对象的直观、人类可读的名称，用于在各种打印、页面展示等场景。可以用中文。例如：

```
verbose_name = "story"
verbose_name = "披萨"
```

如果你不指定它，那么Django会使用小写的模型名作为默认值。

**verbose_name_plural**

英语有单数和复数形式。这个就是模型对象的复数名，比如“apples”。因为我们中文通常不区分单复数，所以保持和`verbose_name`一致也可以。

```
verbose_name_plural = "stories"
verbose_name_plural = "披萨"
verbose_name_plural = verbose_name
```

如果不指定该选项，那么默认的复数名字是`verbose_name`加上‘s’

**label**

前面介绍的元数据都是可修改和设置的，但还有两个只读的元数据，label就是其中之一。

label等同于`app_label.object_name`。例如`polls.Question`，polls是应用名，Question是模型名。

**label_lower**

同上，不过是小写的模型名。



### 4.5 事务

[原博文](https://www.jianshu.com/p/36af33d4eb42)

### 4.6 配置多数据库[¶](https://docs.djangoproject.com/zh-hans/3.0/topics/db/multi-db/#multiple-databases)

[官方文档](https://docs.djangoproject.com/zh-hans/3.0/topics/db/multi-db/)

### 4.7 查询

**复杂查询**

```python
# 店铺商品
def mygoods(request, shop_id):
    if request.method == "GET":
        try:
        	# 卖家数量范围区间
            seller_volume_from = request.GET.get('seller_volume_from')
            seller_volume_to = request.GET.get('seller_volume_to')
            # 评论数量范围区间
            comment_volume_from = request.GET.get('comment_volume_from')
            comment_volume_to = request.GET.get('comment_volume_to')
            # 上传时间范围区间
            upload_date_from = request.GET.get('upload_date_from')
            upload_date_to = request.GET.get('upload_date_to')
            # 关键词模糊查询
            search_amazon = request.GET.get('search_amazon')
			
			# ***********************************************************************
			
            # 定义一个总的Q对象，把下边的q1，q2对象添加进去
            con = Q()
            q1 = Q()
            q1.connector = 'AND' # q1对象表示‘AND’关系，也就是说q1下的条件都要满足‘AND’
            # 判断前台传过来的值是否存在，存在的话追加到去Q对象中，不存在的话可以赋一个空值
            if comment_volume_from:
                q1.children.append(('comment_volume__gte', int(comment_volume_from)))
            else:
                comment_volume_from = ""

            if comment_volume_to:
                q1.children.append(('comment_volume__lte', int(comment_volume_to)))
            else:
                comment_volume_to = ""

			
			# 对时间类型的查询进行一个转换格式的处理（str转date）
            if upload_date_from:
                upload_date_from = datetime.strptime(upload_date_from, "%Y-%m-%d")
                upload_date_from = datetime.date(upload_date_from)
                q1.children.append(('upload_date__gte', upload_date_from))
            else:
                upload_date_from = ""
			
			# ***********************************************************************
			
            q2 = Q()
            q2.connector = 'OR' # q2对象表示‘OR’关系，也就是说q2下的条件都要满足‘OR’
            if search_amazon:
                search_amazon = search_amazon.strip() # 去除字符串左右空格
            
                # 加上‘__contains’表示包含，可以达成模糊查询的目的，目前模糊查询只对这两个
                # 字段进行匹配，如果有多个的话就往下边继续添加,如果不是模糊查询去掉‘__contains’即可
                q2.children.append(('product_name__contains', search_amazon))
                q2.children.append(('ASIN__contains', search_amazon))
            else:
                search_amazon = ""
                
            # 把q1和q2对象添加到总的Q对象
            con.add(q1, 'AND')
            con.add(q2, 'AND')

			# ***********************************************************************

            # 查询数据（把con这个总的Q对象添加到filter过滤条件中，还可以在con后边继续添加过滤条件）
            goods = MapMyShopGoods.objects.filter(con, shop=shop_id)
            
            # 调用分页
            goods_list = mygoods_page_goods(request, goods)['goods_list']
            page_list = mygoods_page_goods(request, goods)['page_list']
            goods_count = goods.count()

            return render(request, 'amazonshop/mygoods.html', locals())
        except Exception as e:
            print('店铺商品---', e, str(e.__traceback__.tb_lineno))
            return render(request, 'amazonshop/mygoods.html', locals())

```



## Django缓存

### 配置缓存

在settings.py中配置一个名为`CACHES`的字典，字典中可以配置多个缓存。

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'caches'),
    },
  	'缓存配置名': {
      	'缓存配置项': '配置值'
    }
}
```

### 缓存配置类型

#### **数据库缓存**

需要注意的是，在创建完数据库缓存后还需要手动执行一条命令来创建数据库表：
`python manage.py createcachetable`

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
        'TIMEOUT': '300',  # 缓存保存时间 单位秒，默认为300
        'OPTIONS': {
            'MAX_ENTRIES': 300,  # 缓存最大数据条数
            'CULL_FREQUENCY': 2,  # 缓存条数达到最大值时，删除1/x的缓存数据
        }
    }
}
```

#### **文件缓存**

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'caches'),
    }
}
```

#### **基于本地内存的缓存**

如果你的本地主机内存够大够快，也可以直接使用它作为缓存，并且这也是Django默认使用的缓存后端。配置如下：

```
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

`LOCATION` 被用于标识各个内存存储位置。如果只有一个 `locmem` 缓存，你可以忽略 `LOCATION` 。但是如果你有多个本地内存缓存，那么你至少要为其中一个起个名字，以便将它们区分开。

这种缓存使用最近最少使用（LRU）的淘汰策略。

#### **Memcached**

如果你是新手，那么要清楚：

- Memcached不是Django自带的软件，而是一个独立的软件，需要你自己安装、配置和启动服务；
- Memcached安装好了后，还要安装Python操作Memcached的依赖库，最常用的是python-memcached和pylibmc；
- 上面两个条件都满足了后，还要在Django中进行配置。

**配置方法：**

- 根据你安装的Python依赖库不同，将CACHES的BACKEND设置为django.core.cache.backends.memcached.MemcachedCache或者django.core.cache.backends.memcached.PyLibMCCache
- 设置LOCATION为你的Memecached守护进程所在的主机IP和进程端口，格式为ip:port的字符串。或者unix:path的形式，在Unix操作系统中。

下面是一个参考例子，Memcached运行在`localhost (127.0.0.1) port 11211`，使用了`python-memcached`库：

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
```

下面的Memcached运行在本地的Unix socket上：`/tmp/memcached.sock`，依赖`python-memcached`：

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/tmp/memcached.sock',
    }
}
```

下面的Memcached运行在`/tmp/memcached.sock`，不带`unix:/`前缀，依赖pylibmc库：

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '/tmp/memcached.sock',
    }
}
```

Memcached支持分布式服务，可能同时在几台机器上运行，将它们的IP地址都加入到LOCATION中，如下所示：

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            '172.19.26.240:11211',
            '172.19.26.242:21423',
            '172.19.26.244:11213',
        ]
        # 我们也可以给缓存机器加权重，权重高的承担更多的请求，如下
        'LOCATION': [
            ('172.19.26.240:11211',5),
            ('172.19.26.242:11211',1),
        ]
    }
}
```

基于内存的缓存系统有个明显的缺点就是断电数据丢失，尤其是Memcached这种不支持序列化的缓存

#### **基于redis缓存**

基于redis缓存需求安装redis依赖，`pip install django-redis`

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 'redis://127.0.0.1:6379/1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "MAX_ENTRIES": 500,
            # "PASSWORD": env.REDIS_PASSWORD,
        },
        "KEY_FUNCTION": "make_key.func"
    }
}
```

### 缓存配置参数

每个缓存后端可以通过额外的参数来控制缓存行为。这些参数在 [`CACHES`](https://docs.djangoproject.com/zh-hans/3.2/ref/settings/#std:setting-CACHES) 配置中作为附加键提供。有效参数如下：

- [`TIMEOUT`](https://docs.djangoproject.com/zh-hans/3.2/ref/settings/#std:setting-CACHES-TIMEOUT) ：缓存的默认超时时间，以秒为单位。这个参数默认为 `300` 秒（5 分钟）。你可以将 `TIMEOUT` 设置为 `None`，这样，默认情况下，缓存键永远不会过期。值为 `0` 会导致键立即过期（实际上是 “不缓存”）。

- [`OPTIONS`](https://docs.djangoproject.com/zh-hans/3.2/ref/settings/#std:setting-CACHES-OPTIONS) ：任何应该传递给缓存后端的选项。有效的选项列表会随着每个后端而变化，由第三方库支持的缓存后端会直接将其选项传递给底层缓存库。

  实施自有缓存策略的缓存后端（即 `locmem`、`filesystem` 和 `database` 后端）将尊重以下选项：

  - `MAX_ENTRIES` ：删除旧值之前允许缓存的最大条目。默认是 `300` 。

  - `CULL_FREQUENCY` ：当达到 `MAX_ENTRIES` 时，被删除的条目的比例。实际比例是 `1 / CULL_FREQUENCY`，所以将 `CULL_FREQUENCY` 设置为 `2`，即当达到 `MAX_ENTRIES` 时将删除一半的条目。这个参数应该是一个整数，默认为 `3`。

    `CULL_FREQUENCY` 的值为 `0` 意味着当达到 `MAX_ENTRIES` 时，整个缓存将被转储。在某些后端（特别是 `database` ），这使得缓存速度 *更* 快，但代价是缓存未命中更多。

  Memcached 后端将 [`OPTIONS`](https://docs.djangoproject.com/zh-hans/3.2/ref/settings/#std:setting-CACHES-OPTIONS) 的内容作为关键字参数传递给客户端构造函数，允许对客户端行为进行更高级的控制。具体用法请看下文[¶](https://docs.djangoproject.com/zh-hans/3.2/topics/cache/#cache-arguments)。

- [`KEY_PREFIX`](https://docs.djangoproject.com/zh-hans/3.2/ref/settings/#std:setting-CACHES-KEY_PREFIX)。一个自动包含在 Django 服务器使用的所有缓存键中的字符串（默认为前缀）。

  查看 [缓存文档](https://docs.djangoproject.com/zh-hans/3.2/topics/cache/#cache-key-prefixing) 获取更多信息。

- [`VERSION`](https://docs.djangoproject.com/zh-hans/3.2/ref/settings/#std:setting-CACHES-VERSION) ：Django 服务器生成的缓存键的默认版本号。

  查看 [缓存文档](https://docs.djangoproject.com/zh-hans/3.2/topics/cache/#cache-versioning) 获取更多信息。

- [`KEY_FUNCTION`](https://docs.djangoproject.com/zh-hans/3.2/ref/settings/#std:setting-CACHES-KEY_FUNCTION) 一个字符串，包含一个函数的点分隔路径，该函数定义了如何将前缀、版本和键组成一个最终的缓存键。

  查看 [缓存文档](https://docs.djangoproject.com/zh-hans/3.2/topics/cache/#cache-key-transformation) 获取更多信息

自定义KEY_FUNCTION

```python
def make_key(key, key_prefix, version):
    return ':'.join(["key_start", key_prefix, str(version), key])
```

### 缓存粒度

#### **单页缓存**

```python
from django.views.decorators.cache import cache_page

@cache_page(5)  # 缓存5s钟
def test_cache(request):
    """配置缓存之后，当你五秒钟之内进行访问，时间将会一成不变。"""
    import time
    ctime=time.time()
    return render(request,'index.html',context={'ctime':ctime})
```

`cache_page`有一个必填参数，缓存时限，单位为秒，为了便于理解，可以写成表达式形式，如上`60 * 15`即900秒。其他选填参数有cache：指定其他的缓存类型；key_prefix：指定键前缀。

在URL配置中使用缓存：

```python
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('foo/<int:code>/', cache_page(60 * 15)(my_view)),
]
```

类视图不能直接使用`cache_page`装饰器，因为装饰器本质是个函数，接收函数并返回函数，所以只要把类视图转为函数就行。

```python
# 在views.py中使用
class MyView(View):
    ...

my_view = cache_page(60 * 15)(MyView.as_view())



# 在urls.py中使用
urlpatterns = [
    path('foo/<int:code>/', cache_page(60 * 15)(MyView.as_view())),
]
```

#### **局部缓存**

在一个模板中，使用`tag`进行局部缓存：

```html
<p>未进行缓存：{{ ctime }}</p>
<hr>

<!--导入tage-->
{% load cache %}
<!--5表示5s钟，name是唯一key值-->

{% cache 5 'name' %}
	{{ ctime }}
{% endcache %}

```

#### **缓存全站**

```python
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',  # 这个放在最上面
    # ...  其他中间件
    'django.middleware.cache.FetchFromCacheMiddleware',  # 这个放在最下面
]
```

注意： `update`中间件必须放在列表的开始位置，而`fectch`中间件，必须放在最后。 这是Django使用中间件的规则，它们是有顺序关系的。

#### **高级技巧**

**使用cache_control**

通常用户将会面对两种缓存： 他或她自己的浏览器缓存（私有缓存）以及他或她的提供者缓存（公共缓存）。 公共缓存由多个用户使用，而受其它人的控制。 这就产生了你不想遇到的敏感数据的问题，比如说你的银行账号被存储在公众缓存中。 因此，Web 应用程序需要以某种方式告诉缓存那些数据是私有的，哪些是公共的。

解决方案是标示出某个页面缓存应当是私有的。 要在 Django 中完成此项工作，可使用 cache_control 视图修饰器：

```python
from django.views.decorators.cache import cache_control
 
 
@cache_control(private=True)
def my_view(request):
# ...

# 在下例中， cache_control 告诉缓存对每次访问都重新验证缓存并在最长 3600 秒内保存所缓存版本。
@cache_control(must_revalidate=True, max_age=3600)
def my_view(request):
# ...
```

**使用vary_on_headers**

缺省情况下，Django 的缓存系统使用所请求的路径(如blog/article/1)来创建其缓存键。这意味着不同用户请求同样路径都会得到同样的缓存版本，不考虑客户端user-agent, cookie和语言配置的不同, 除非你使用Vary头部通知缓存机制需要考虑请求头里的cookie和语言的不同。

```python
from django.views.decorators.vary import vary_on_headers
 
 
@vary_on_headers('User-Agent', 'Cookie')
def my_view(request):
    ...
```

**使用never_cache禁用缓存**
如果你想用头部完全禁掉缓存, 你可以使用django.views.decorators.cache.never_cache装饰器。如果你不在视图中使用缓存，服务器端是肯定不会缓存的，然而用户的客户端如浏览器还是会缓存一些数据，这时你可以使用never_cache禁用掉客户端的缓存。

```python
from django.views.decorators.cache import never_cache
 
@never_cache
def myview(request):
# ...
```



### 缓存API

Django还提供了一个简单的API，可以保存任意粒度的数据。你可以使用一个类似字典的对象，`django.core.cache.caches`，来访问缓存，这允许使用不同缓存方式：

```python
from django.core.cache import caches
cache1 = caches['default']
cache2 = caches['others']
```

如果只有一个缓存默认的设置，使用`from django.core.cache import cache`获取默认缓存，这等于`caches['default']`。

| 方法                                                         | 描述                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| cache.set(key,value,timeout=DEFAULT_TIMEOUT,version=None)    | 设置缓存，当不存在时则创建。                                 |
| cache.get(key,default=None,version=None)                     | 根据key获取缓存，若不存在则返回默认值None                    |
| cache.add(key,value,timeout=DEFAULT_TIMEOUT,version=None)    | 使用与set相同，当缓存已存在时，将不会更新，而set则会更新     |
| cache.get_or_set(key,default,timeout=DEFALUT_TIMEOUT,version=None) | 获取缓存，当获取不到时设置缓存，并拿到设置的值               |
| cache.get_many(key,version=None)                             | 传入一个可迭代对象，它将会返回一个字典，将可迭代对象中所有key对应的value取出 |
| cache.set_many(dict,timeout)                                 | 传入一个dict，它将会迭代该dict并且为每一组k，v存放到缓存中   |
| cache.delete(key,version=None)                               | 清除特定对象                                                 |
| delete_many({ list })                                        | 清除多个对象                                                 |
| cache.clear()                                                | 清楚缓存。`clear()` 将删除缓存里的 *任何* 键                 |
| cache.touch(key,timeout=DEFAULT_TIMEOUT,version=None)        | 当缓存马上到期时，重新设置它的过期时间                       |
| cache.incr(key,*delta*=1,version=None)                       | 对缓存中的数据做递增操作，如k对应的v原本是1，使用该方法后变为2 |
| cache.decr(key,*delta*=1,version=None)                       | 对缓存中的数据做递减操作，如k对应的v原本是2，使用该方法后变为1 |
| cache.close()                                                | 关闭缓存链接                                                 |

基本的用法很简单：

```shell
>>> cache.set('my_key', 'hello, world!', 30)
>>> cache.get('my_key')
'hello, world!'
>>> # 等待 30 秒，'my_key'将过期...
>>> cache.get('my_key')
None
>>> # add()方法只添加不存在或失效的key，如果key仍有效则不会更新
>>> cache.set('add_key', 'Initial value')
>>> cache.add('add_key', 'New value') # 使用add()方法来新增一个原来没有的键值。 它接受的参数和set()一样，但是并不去尝试更新已经存在的键值。
>>> cache.get('add_key')
'Initial value'
>>> # 同时设置获取多对值
>>> cache.set('a', 1)
>>> cache.set('b', 2)
>>> cache.set('c', 3)
>>> cache.get_many(['a', 'b', 'c'])
{'a': 1, 'b': 2, 'c': 3}
>>> cache.set_many({'a': 1, 'b': 2, 'c': 3})
>>> cache.get_many(['a', 'b', 'c'])
{'a': 1, 'b': 2, 'c': 3}
>>> # 删除缓存
>>> cache.delete('a')
>>> cache.delete_many(['a', 'b', 'c'])
>>> cache.clear()
>>> # 关闭连接
>>> cache.close()
```

























## 附录

##### django中引入常见的包

```python
# urls.py
# django路由
from django.urls import include, path

# 引入django配置
from django.conf import settings

# views.py
# http响应
from django.http import HttpResponse

# 内置校验器
from django.core import validators

# 缓存
from django.core.cache import caches
from django.core.cache import cache
```

##### DRF中引入常见的包

```python
from rest_framework import serializers

# 转成JSON
from rest_framework.renderers import JSONRenderer

# 解析JSON
from rest_framework.parsers import JSONParser

import rest_framework.status
import rest_framework.Request
import rest_framework.Response

import rest_framework.mixins

# 通用视图
import rest_framework.generics

```



sudo ln -s /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.8/lib/python3.8/config-3.8-darwin  /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.8/lib/python3.8/config-3.8/libpython3.8.a

