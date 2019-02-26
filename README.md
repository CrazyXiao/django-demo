# django-demo(python3)

### 安装Django

如果Django还没有安装，可以在命令行，尝试使用pip安装:

```
pip install django
```

启动计算机中的Python，尝试载入Django模块。如果可以成功载入，那么说明Django已经安装好：

```
import django
```

 

### 启动

使用下面的命令创建项目：

```
django-admin.py startproject mysite
```

在当前目录下，将生成mysite文件夹。其文件树结构如下:

```
mysite
├── manage.py
└── mysite
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

这里我们将mysite中的所有文件放入django-demo，进入django-demo，启动服务器：

```
python manage.py runserver 8000
```

上面的8000为端口号，如果不说明，那么端口号默认为8000。

打开浏览器，访问http://127.0.0.1:8000，可以看到服务器已经在运行。



### 第一个网页

在http协议中可以看到，网络服务器是“请求-回应”的工作模式。客户向URL发送请求，服务器根据请求，开动后厨，并最终为客人上菜。Django采用的MVC结构，即点单、厨房、储藏室分离。

修改urls.py将URL分配给某个对象处理。

将urls.py修改为:

```
from django.contrib import admin
from django.urls import path
from mysite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.first_page),
]
```

我们添加了最后一行。它将根目录的URL分配给一个对象进行处理，这个对象是views.first_page。

用以处理HTTP请求的这一对象还不存在，我们在mysite下创建views.py，并在其中定义first_page函数:

```
...
from django.http import HttpResponse
def first_page(request):
    return HttpResponse("<p>hello, django.</p>")
```

first_page函数的功能，是返回http回复。first_page有一个参数request，该参数包含有请求的具体信息，比如请求的类型等，这里并没有用到。



### 增加app

一个网站可能有多个功能。我们可以在Django下，以app为单位，模块化的管理，而不是将所有的东西都丢到一个文件夹中。在django-demo下，运行manange.py，创建新的app：

```
python manage.py startapp west
```

我们的根目录下，出现了一个新的叫做west的文件夹。

我们还需要修改项目设置，说明我们要使用west。在mysite/setting.py中，在INSTALLED_APPS中，增加"west"：

```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'west',
)
```

可以看到，除了新增加的west，Django已经默认加载了一些功能性的app，比如用户验证、会话管理、显示静态文件等。

### 增加APP页面

我们下面为APP增加首页。我们之前是在mysite/urls.py中设置的URL访问对象。依然采用类似的方式设置。

另一方面，为了去耦合，实现模块化，我们应该在west/urls.py中设置URL访问对象。具体如下：

首先，修改mysite/urls.py：

```
from django.contrib import admin
from django.urls import path, include
from mysite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.first_page),
    path('west/', include('west.urls')),
]
```

注意新增加的最后一行。这里，我们提醒指挥员，对于west/的访问，要参考west/urls.py。

随后，我们创建west/urls.py，添加内容：

```
from django.urls import path
from west import views

urlpatterns = [
    path('', views.first_page),
]
```

将URL对应west下，views.py中的first_page函数。

最后，在west下，修改views.py为:

```
...
from django.http import HttpResponse
def first_page(request):
    return HttpResponse("<p>hello, west.</p>")
```

访问http://127.0.0.1:8000/west，查看效果。





