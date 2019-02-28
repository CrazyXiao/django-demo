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

打开浏览器，访问`http://127.0.0.1:8000`，可以看到服务器已经在运行。



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

访问`http://127.0.0.1:8000/west`，查看效果。

### MYSQL

#### 安装mysql

```
apt-get install mysql-server
apt-get isntall mysql-client
apt-get install libmysqlclient-dev # python操作mysql需要
```

安装过程中会提示设置密码什么的，注意设置了不要忘了。

#### 启动mysql

```
service mysql start
```

通过下面命令检查之后，如果看到有mysql 的socket处于 listen 状态则表示安装成功。

```
netstat -tap | grep mysql
```

#### 登陆mysql

```
mysql -u root -p
```

#### 允许远程连接

修改 /etc/mysql/mysql.conf.d/mysqld.cnf

找到bind-address = 127.0.0.1这一行
改为bind-address = 0.0.0.0

重启mysql

```
service mysql restart
```

连接到mysql服务器，然后执行：

```
grant all privileges on *.* to 'root'@'%' identified by '123456' with grant option;
flush privileges;
```

### 连接MYSQL

在MySQL中创立Django项目的数据库：

```
mysql> CREATE DATABASE villa DEFAULT CHARSET=utf8;
```

这里使用utf8作为默认字符集，以便支持中文。

在settings.py中，将DATABASES对象更改为:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'villa',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'your host ip',
        'PORT': '3306',
    }
}
```

后台类型为mysql。上面包含数据库名称和用户的信息，它们与MySQL中对应数据库和用户的设置相同。Django根据这一设置，与MySQL中相应的数据库和用户连接起来。此后，Django就可以在数据库中读写了。

### 创立模型

MySQL是关系型数据库。但在Django的帮助下，我们不用直接编写SQL语句。Django将关系型的表(table)转换成为一个类(class)。而每个记录(record)是该类下的一个对象(object)。我们可以使用基于对象的方法，来操纵关系型的MySQL数据库。

在models.py中，我们创建一个只有一列的表，即只有一个属性的类：

```
from django.db import models

# Create your models here.
class Character(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
```

类Character定义了数据模型，它需要继承自models.Model。在MySQL中，这个类实际上是一个表。表只有一列，为name。可以看到，name属性是字符类型，最大长度为200。

类Character有一个 `__str__() ` 方法，用来说明对象的字符表达方式。

Django命令同步数据库

```
python3 manage.py makemigrations
python3 manage.py migrate
```

查看数据：

```
mysql> use villa;
...
mysql> show tables;
...
mysql> show columns from west_character;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int(11)      | NO   | PRI | NULL    | auto_increment |
| name  | varchar(200) | NO   |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+
2 rows in set (0.00 sec)

```

### 显示数据

数据模型虽然建立了，但还没有数据输入。为了简便，我们手动添加记录。打开MySQL命令行,并切换到相应数据库。添加记录：

```
INSERT INTO west_character (name) Values ('Vamei');
INSERT INTO west_character (name) Values ('Django');
INSERT INTO west_character (name) Values ('John');
```

查看记录：

```
 SELECT * FROM west_character;
```

可以看到，三个名字已经录入数据库。

下面我们从数据库中取出数据，并返回给http请求。

编辑west/views.py

```
from west.models import Character
...
def staff(request):
    staff_list = Character.objects.all()
    staff_str  = map(str, staff_list)
    return HttpResponse("<p>" + ' '.join(staff_str) + "</p>")
```

可以看到，我们从west.models中引入了Character类。通过操作该类，我们可以读取表格中的记录。

 为了让http请求能找到上面的程序，在west/urls.py增加url导航：

```
...
urlpatterns = [
    ...
    path('staff/', views.staff),
]
```

访问` http://127.0.0.1:8000/west/staff` 查看效果。

### 模板

在之前的程序中，我们直接生成一个字符串，作为http回复，返回给客户端。这一过程中使用了django.http.HttpResponse()。

在这样的一种回复生成过程中，我们实际上将数据和视图的格式混合了到上面的字符串中。看似方便，却为我们的管理带来困难。

Django中自带的模板系统，可以将视图格式分离出来，作为模板使用。这样，不但视图可以容易修改，程序也会显得美观大方。

默认templates文件夹放置我们的模板，所以我们west中新建该文件夹。

然后新建base.html

```
<html>
  <head>
    <title>templay</title>
  </head>

  <body>
    <h1>come from base.html</h1>
    {% block mainbody %}
       <p>original</p>
    {% endblock %}
  </body>
</html>
```

该页面中，名为mainbody的block标签是可以被继承者们替换掉的部分。

我们在下面的templay.html中继承base.html，并替换特定block：

```
{% extends "base.html" %}

{% block mainbody %}

{% for item in staffs %}
<p>{{ item.id }},{{ item.name }}</p>
{% endfor %}

{% endblock %}
```

第一句说明templay.html继承自base.html。可以看到，这里相同名字的block标签用以替换base.html的相应block。

上面我们从数据库中提取出了数据。如果利用模板语言，我们可以直接传送数据容器本身到模板。

修改views.py中staff()为:

```
def staff(request):
    staff_list = Character.objects.all()
    return render(request, 'templay.html', {'staffs': staff_list})
```

从数据库中查询到的三个对象都在staff_list中。我们直接将staff_list传送给模板。

访问` http://127.0.0.1:8000/west/staff` 查看效果。

#### 流程

west/views.py中的staff()在返回时，将字典数据传递给模板templay.html。Django根据字典中的键值，将相应数据放入到模板中的对应位置，生成最终的http回复。

### 提交表格

我们下面使用POST方法，并用一个URL和处理函数，同时显示视图和处理请求，并让客户提交的数据存入数据库

先创建模板investigate.html

```
<form action="/west/investigate/" method="post">
  {% csrf_token %}
  <input type="text" name="staff">
  <input type="submit" value="Submit">
</form>

{% for person in staff %}
<p>{{ person }}</p>
{% endfor %}
```

我们修改提交表格的方法为post。

表格后面还有一个{% csrf_token %}的标签。csrf全称是Cross Site Request Forgery。这是Django提供的防止伪装提交请求的功能。POST方法提交的表格，必须有此标签。

编辑west/views.py，用investigate()来处理表格：

```
...
def investigate(request):
    if request.POST:
        submitted  = request.POST['staff']
        new_record = Character(name = submitted)
        new_record.save()
    ctx ={}
    all_records = Character.objects.all()
    ctx['staff'] = all_records
    return render(request, "investigate.html", ctx)
```

在POST的处理部分，我们调用Character类创建新的对象，并让该对象的属性name等于用户提交的字符串。通过save()方法，我们让该记录入库。随后，我们从数据库中读出所有的对象，并传递给模板。

在west/urls.py增加url导航：

```
...
urlpatterns = [
    ...
    path('investigate/', views.investigate),
]
```

访问`http://127.0.0.1:8000/west/investigate/`，查看效果。

### 表格对象

客户提交数据后，服务器往往需要对数据做一些处理。比如检验数据，看是否符合预期的长度和数据类型。在必要的时候，还需要对数据进行转换，比如从字符串转换成整数。这些过程通常都相当的繁琐。

Django提供的数据对象可以大大简化这一过程。该对象用于说明表格所预期的数据类型和其它的一些要求。这样Django在获得数据后，可以自动根据该表格对象的要求，对数据进行处理。

修改west/views.py：

```
...
from django import forms

class CharacterForm(forms.Form):
    name = forms.CharField(max_length = 200)


def investigate(request):
    if request.POST:
        form = CharacterForm(request.POST)
        if form.is_valid():
            submitted  = form.cleaned_data['name']
            new_record = Character(name = submitted)
            new_record.save()
    form = CharacterForm()
    ctx ={}
    all_records = Character.objects.all()
    ctx['staff'] = all_records
    ctx['form']  = form
    return render(request, "investigate.html", ctx)
```

上面定义了CharacterForm类，并通过属性name，说明了输入栏name的类型为字符串，最大长度为200。

在investigate()函数中，我们根据POST，直接创立form对象。该对象可以直接判断输入是否有效，并对输入进行预处理。空白输入被视为无效。

后面，我们再次创建一个空的form对象，并将它交给模板显示。

在模板investigate.html中，我们可以直接显示form对象：

```
<form action="/west/investigate/" method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="Submit">
</form>

{% for person in staff %}
<p>{{ person }}</p>
{% endfor %}
```

如果有多个输入栏，我们可以用相同的方式直接显示整个form，而不是加入许多个<input>标签。

访问`http://127.0.0.1:8000/west/investigate/`，查看效果。

### Admin管理

Django提供一个管理数据库的app，即django.contrib.admin。这是Django最方便的功能之一。通过该app，我们可以直接经由web页面，来管理我们的数据库。这一工具，主要是为网站管理人员使用。

这个app通常已经预装好，你可以在mysite/settings.py中的INSTALLED_APPS看到它。

为了让admin界面管理某个数据模型，我们需要先注册该数据模型到admin。比如，我们之前在west中创建的模型Character。修改west/admin.py:

```
from django.contrib import admin
from west.models import Character
# Register your models here.

admin.site.register(Character)
```

创建管理员：

```
python3 manage.py createsuperuser
```

访问`http://127.0.0.1:8000/admin`，登录后，可以看到管理界面。

这个页面除了west.characters外，还有用户和组信息。它们来自Django预装的Auth模块。

#### 复杂模型

管理页面的功能强大，完全有能力处理更加复杂的数据模型。

先在west/models.py中增加一个更复杂的数据模型：

```
...
class Contact(models.Model):
    name   = models.CharField(max_length=200)
    age    = models.IntegerField(default=0)
    email  = models.EmailField()
    def __str__(self):
        return self.name

class Tag(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    name    = models.CharField(max_length=50)
    def __str__(self):
        return self.name
```

这里有两个表。Tag以Contact为外部键。一个Contact可以对应多个Tag。

我们还可以看到许多在之前没有见过的属性类型，比如IntegerField用于存储整数。

 ![img](https://images0.cnblogs.com/blog/413416/201402/161056513888837.png)

同步数据库:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

在west/admin.py注册多个模型并显示：

```
from django.contrib import admin
from west.models import Character, Contact, Tag
# Register your models here.

admin.site.register([Character, Contact, Tag])
```

 模型将在管理页面显示。

#### 自定义页面

我们可以自定义管理页面，来取代默认的页面。

修改west/admin.py:

```
...
class TagInline(admin.TabularInline):
    model = Tag

class ContactAdmin(admin.ModelAdmin):
    inlines = [TagInline]  # Inline
    fieldsets = (
        ['Main',{
            'fields':('name','email'),
        }],
        ['Advance',{
            'classes': ('collapse',),
            'fields': ('age',),
        }]

    )
    list_display = ('name','age', 'email')
    search_fields = ('name',)

admin.site.register(Contact, ContactAdmin)
admin.site.register([Character])
```

上面定义了一个ContactAdmin类，用以说明管理页面的显示格式。

ContactAdmin中增加list_display属性，让列表显示更多的栏目。

使用search_fields为该列表页增加搜索栏。

使用Inline显示，让Tag附加在Contact的编辑页面上显示。

由于该类对应的是Contact数据模型，我们在注册的时候，需要将它们一起注册。

#### 总结

Django的管理页面有很丰富的数据库管理功能，并可以自定义显示方式，是非常值得使用的工具。

### 用户管理

一个Web应用的用户验证是它的基本组成部分。我们在使用一个应用时，总是从“登录”开始，到“登出”结束。另一方面，用户验证又和网站安全、数据库安全息息相关。HTTP协议是无状态的，但我们可以利用储存在客户端的cookie或者储存在服务器的session来记录用户的访问。 

Django有管理用户的模块，即django.contrib.auth。你可以在mysite/settings.py里看到，这个功能模块已经注册在INSTALLED_APPS中。利用该模块，你可以直接在逻辑层面管理用户，不需要为用户建立模型，也不需要手工去实现会话。

创建新用户

你可以在admin页面直接看到用户管理的对话框，即Users。从这里，你可以在这里创建、删除和修改用户。点击Add增加用户daddy，密码为crazy1992。

#### 建立user app

```
python3 manage.py startapp user
```

#### 登录

我们建立一个简单的表格，用户通过该表格来提交登陆信息，并在Django服务器上验证，如果用户名和密码正确，那么登入用户。

user/templates/login.html

```
<form role="form" action="/user/login/" method="post">
      {% csrf_token %}
      <label>Username</label>
      <input type="text" name='username'>
      <label>Password</label>
      <input name="password" type="password">
      <input type="submit" value="Submit">
 </form>
```

 我们在user/views.py中，定义处理函数user_login()，来登入用户：

```
from django.shortcuts import render, redirect
from django.contrib.auth import *

# Create your views here.
def user_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user     = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect('/')
    ctx = {}
    return render(request, 'login.html',ctx)
```

上面的authenticate()函数，可以根据用户名和密码，验证用户信息。而login()函数则将用户登入。它们来自于django.contrib.auth。

作为替换，我们可以使用contrib.auth.forms.AuthenticationForm，来简化上面的模板和处理函数。

最后在west/urls.py增加url导航。

#### 登出

有时用户希望能销毁会话。我们可以提供一个登出的URL，即/users/logout。登入用户访问该URL，即可登出。在views.py中，增加该URL的处理函数：

```
....
def user_logout(request):
    logout(request)
    return redirect('/')
```

我们修改urls.py，让url对应user_logout()。

访问`http://127.0.0.1/users/logout`，就可以登出用户。

#### 模板中的用户

进一步，用户是否登陆这一信息，也可以直接用于模板。比较原始的方式是把用户信息直接作为环境数据，提交给模板。然而，这并不是必须的。事实上，Django为此提供了捷径：我们可以直接在模板中调用用户信息。比如下面的模板：

mysite/templates/index.html

```
{% if user.is_authenticated %}
  <p>Welcome, my genuine user, my true love.</p>
{% else %}
  <p>Sorry, not login, you are not yet my sweetheart. </p>
{% endif %}
```

不需要环境变量中定义，我们就可以直接在模板中引用user。这里，模板中调用了user的一个方法，is_authenticated，将根据用户的登录情况，返回真假值。需要注意，和正常的Python程序不同，在Django模板中调用方法并不需要后面的括号。

mysite/views.py

```
def first_page(request):
    return render(request, 'index.html')
```

mysite/setting.py

```
INSTALLED_APPS = [
	...
    'mysite',
]
```

访问`http://127.0.0.1:8000/`，查看效果，然后进行登陆登出操作。

#### 用户注册

我们上面利用了admin管理页面来增加和删除用户。这是一种简便的方法，但并不能用于一般的用户注册的情境。我们需要提供让用户自主注册的功能。这可以让站外用户提交自己的信息，生成自己的账户，并开始作为登陆用户使用网站。

用户注册的基本原理非常简单，即建立一个提交用户信息的表格。表格中至少包括用户名和密码。相应的处理函数提取到这些信息后，建立User对象，并存入到数据库中。

我们可以利用Django中的UserCreationForm，比较简洁的生成表格，并在views.py中处理表格：

```
...
from django.contrib.auth.forms import UserCreationForm
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
        return redirect("/")
    form = UserCreationForm()
    ctx = {'form': form}
    return render(request, "register.html", ctx)
```

相应的模板register.html如下：

```
<form action="" method="post">
   {% csrf_token %}
   {{ form.as_p }}
   <input type="submit" value="Register">
</form>
```

修改urls.py，让url对应register()。

访问`http://127.0.0.1/users/register`，进入注册页面。

### Apache

上面都是使用python manage.py runserver来运行服务器。这是一个实验性的web服务器，不适用于正常的站点运行。我们需要一个可以稳定而持续的服务器。这个服务器负责监听http端口，将收到的请求交给Django处理，将Django的回复发还给客户端。

这样的持续性服务器可以有很多选择，比如apache, Nginx, lighttpd等。这里将使用最常见的apache服务器。服务器和Django之间通过Python的web服务接口WSGI连接，因此我们同样需要apache下的mod_wsgi模块。

#### 安装

```
apt-get install apache2
apt-get install apache2-dev
apt-get install libapache2-mod-wsgi
```

新建django.conf： 

```
# Django
WSGIScriptAlias / /var/www/django-demo/mysite/wsgi.py
<Directory /var/www/django-demo/mysite>
<Files wsgi.py>
  Require all granted
</Files>
</Directory>
```

上面的配置中/var/www/django-demo是Django项目所在的位置，而/var/www/django-demo/mysite是Django项目中自动创建的文件。

可以看到，利用WSGIScriptAlias，我们实际上将URL /对应了wsgi接口程序。这样，当我们访问根URL时，访问请求会经由WSGI接口，传递给Django项目mysite。

将 django.conf 加到apache的配置目录中去：

```
cp django.conf /etc/apache2/sites-enabled/
```

#### mod_wsgi

mod_wsgi模块根据python版本的不同是不一样的，因为我们使用的是python3，但系统默认的还是python，使用 `apt-get install libapache2-mod-wsgi`安装的是对应python2的，所以这里我们需要重新安装python3的mod_wsgi模块。

安装：

```
pip3 install mod_wsgi
```

导出：

```
mod_wsgi-express install-module
```

修改原来的mod_wsgi：

```
cd /usr/lib/apache2/modules
mv mod_wsgi.so mod_wsgi.so.bak
ln -s mod_wsgi-py35.cpython-35m-x86_64-linux-gnu.so mod_wsgi.so
```

#### wsgi.py

修改mysite/wsgi.py

```
"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
```

允许远程连接需要修改settting.py：

```
ALLOWED_HOSTS = ['your host ip']
```

配置好后，重启apache2

```
/etc/init.d/apache2 restart
```



