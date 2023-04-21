# Django admin使用

## **1. 集成SimpleUi**

django原生的admin UI风格太过于古老，因此simpleUI应运而生，让页面更具现代化。

官网链接：https://simpleui.72wo.com/docs/simpleui/#%E5%AE%98%E7%BD%91

官方[DEMO源码](https://github.com/newpanjing/simpleui_demo)

### **安装依赖**

```bash
pip install django-simpleui==2021.10.15
```

### **注册应用**
注册simpleui 放在第一个

```python
# Application definition
INSTALLED_APPS = [
    # 注册simpleui 放在第一个
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ...
]
```

### **配置urls**

```python
from django.contrib import admin


admin.site.site_title = '管理后台'
admin.site.site_header = '管理后台'

urlpatterns = [
    # 后台管理
    path('admin', admin.site.urls),
    ...
]
```

### **迁移数据库表**

```bash
python manage.py migrate --fake-initial

python manage.py migrate
```

如遇到报错：1054, "Unknown column 'name' in 'django_content_type'"

可以在django_content_type表中添加多一个字段name

再重新执行。

### **生产环境配置**

官方文档：[部署静态文件](https://docs.djangoproject.com/zh-hans/3.2/howto/static-files/deployment/)

参考博客：
- https://juejin.cn/post/6844903587470917646

- https://simpleui.72wo.com/topic/1226/

由于本身Django生产环境（DEBUG=False）不提供静态资源服务，所以我们在生产环境要使用静态文件服务器提供服务。

在settings.py中设置STATIC_ROOT

```
STATIC_ROOT = os.path.join(BASE_DIR, "static")
```

执行collectstatic命令收集静态文件

```
python manage.py collectstatic
```

配置Nignx访问静态资源

```nginx
upstream django_admin {
    ip_hash;
    server unix:/deploy/release/web_app/app.sock; # Django服务
}

# 访问管理页面配置
server {
    listen       80;
    server_name  localhost;


    location ^~ /admin/ {
        uwsgi_send_timeout 600;
        uwsgi_connect_timeout 600;
        uwsgi_read_timeout 600;
        include /etc/nginx/uwsgi_params;
        proxy_store off;
        proxy_redirect off;
        proxy_set_header X-Forwoarded_For $proxy_add_x_forwarded_for;
        proxy_set_header X-Readl-IP $remote_addr;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Remote-Host $remote_addr;
        uwsgi_pass  django_admin;
    }

    # django simpleui静态文件地址
    location /backend/static {
        alias  /deploy/release/web_app/static/;
    }
}

# 后台服务配置
server {
    listen       8000;
    server_name  localhost;

    client_max_body_size    500m;

    location / {
        include     uwsgi_params;
        # uwsgi运行的django项目 socket地址
        uwsgi_pass  unix:/deploy/release/web_app/app.sock;
    }

    # django simpleui静态文件地址
    location /backend/static {
        alias  /deploy/release/web_app/static/;
    }
}
```

重启Nignx，service nginx reload

## **2. 配置admin**

### 常用模型配置

```python
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (UserShipInline, )
    list_display = ('id', 'name', 'creator', 'groups', 'users', 'description')
    filter_horizontal = ('group', )
    list_filter = tuple()  # 下拉框过滤
    search_fields = ('id',)
    ordering = ('id',)
    list_per_page = 20

    def groups(self, obj):
        """多对多字段显示"""
        return [g.name for g in obj.group.all()]

    def users(self, obj):
        """多对多字段显示"""
        return [u.name_ch for u in obj.user.all()]
```



### 配置用户admin

参考：

[Django 中的自定义验证 - 官方](https://docs.djangoproject.com/zh-hans/3.2/topics/auth/customizing/) 

[Django 重写 UserAdmin](https://www.jianshu.com/p/1df2cda28682)

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UsernameField
from django.forms import ModelForm

from .models import User


class CUserCreationForm(ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    class Meta:
        model = User
        fields = ('name', 'email', 'phone', 'is_superuser', 'is_active', 'is_staff')
        field_classes = {'username': UsernameField}


class UserShipInline(admin.TabularInline):
    """
    当你使用 ManyToManyField`的``through 参数指定一个中间模型时，后台管理在新增、编辑模式下默认不会显示这个字段。
    解决方法：https://docs.djangoproject.com/zh-hans/3.2/ref/contrib/admin/#working-with-many-to-many-intermediary-models
    """
    model = UserShip
    extra = 1
    verbose_name_plural = "用户关联信息"


@admin.register(User)
class MyUserAdmin(UserAdmin):
    model = User

    inlines = (UserShipInline,)

    list_display = ('name', 'email', 'phone', 'is_superuser', 'is_active', 'is_staff')
    list_filter = tuple()  # 下拉框过滤
    search_fields = ('name',)
    ordering = ('name', )
    filter_horizontal = ()  # Leave it empty. You have neither `groups` or `user_permissions`
    # 更新时的字段配置
    fieldsets = (
        ('基本信息', {'fields': ('name', 'email', 'phone', 'password')}),
        ('权限', {'fields': ('is_superuser', 'is_active', 'is_staff')}),
    )
    add_form = CUserCreationForm
    # 新增时的字段配置
    add_fieldsets = (
        ('基本信息', {'fields': ('name', 'email', 'phone')}),
        ('权限', {'fields': ('is_superuser', 'is_active', 'is_staff')}),
    )
    list_per_page = 20
```

### 多对多配置（无外键）

```python
from django.contrib import admin
from django import forms
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Book, Author, BookAuthor


class BookForm(forms.ModelForm):
    authors = ModelMultipleChoiceField(
        label="关联作者",
        queryset=Author.objects.all(),
        required=False,
        widget=CheckboxSelectMultiple
    )

    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            author_ids = BookAuthor.objects.filter(book_id=self.instance.pk).values_list("author_id", flat=True)
            authors = Author.objects.filter(id__in=author_ids)
            self.initial["authors"] = authors


# 自定义作者filter
class AuthorFilter(admin.SimpleListFilter):
    title = "作者"
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        authors = Author.objects.all()
        return (
            (p.id, p.name)
            for p in authors
        )

    def queryset(self, request, queryset):
        if self.value():
            ids = BookAuthor.objects.filter(author_id=self.value()).values_list("book_id", flat=True)
            return queryset.filter(id__in=list(ids))
        return queryset


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_names')
    list_filter = (AuthorFilter, )  # 下拉框过滤
    search_fields = ('title',)
    ordering = ('id',)
    list_per_page = 20

    form = BookForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        authors = form.cleaned_data['authors']
        snp_list = [BookAuthor(book_id=obj.id, author_id=p.id) for p in authors]
        BookAuthor.objects.filter(book_id=obj.id).delete()
        BookAuthor.objects.bulk_create(snp_list)

    def author_names(self, obj):
        return ', '.join([a.name for a in obj.authors.all()])

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        BookAuthor.objects.filter(book_id=obj.id).delete()

```

