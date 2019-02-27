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



