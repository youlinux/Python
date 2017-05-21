
## 开始的第一个django项目。

## 可以使用django自带的admin页面操作数据库。

## 通过此实例，可以对django有个大概的了解。

## 版本信息

系统版本:centos7
python版本:Python 2.7.5
django版本:1.11.1

如果系统存在其他版本的Python，可以使用pyenv，构建一个Python 2.7.5的环境

![](http://i.imgur.com/1nbWC5H.png)

## 创建一个django项目

```shell
[root@youlinux.com ~]# pip install django # 确保django模块存在
[root@youlinux.com ~]# django-admin startproject djanogweb  #创建一个名字为djangoweb的工程

[root@youlinux.com ~]# ls djanogweb/  
# 此时会自动生成该目录，并且该目录下有子目录和文件
djanogweb  manage.py

[root@youlinux.com ~]# cd djanogweb/ #进入该目录下


```
![](http://i.imgur.com/sKxd3Yl.jpg)


```
[root@youlinux.com ~/djanogweb]# python manage.py startapp app01 
# 创建一个名为app01的项目(djangowb是一个工程，该工程下可以包含多个项目)

[root@youlinux.com ~/djanogweb]# tree
.
├── app01
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── djanogweb
│   ├── __init__.py
│   ├── __init__.pyc
│   ├── settings.py
│   ├── settings.pyc
│   ├── urls.py
│   └── wsgi.py
└── manage.py

3 directories, 14 files
# 此时该目录下会多出许多的内容
```

## 配置使用数据库

```python
[root@youlinux.com ~/djanogweb]# vim djanogweb/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'youlinux', #确保此数据库已存在
        'HOST':'127.0.0.1',
        'PORT':'3306',
        'USER':'root',
        'PASSWORD':'123456',
    }
}

# 将原来的DATABASES字典替换掉，
# 需要确保 'NAME' 后面的库名事先在数据库中存在

```
同时需要在settings中注册app01

![](http://i.imgur.com/z9mkpyc.jpg)

### 创建数据库对象模型

```python
[root@youlinux.com ~/djanogweb]# vim app01/models.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models # 首先导入模块

# Create your models here.

class Publisher(models.Model):  
'''
    定义一个类 Publisher 继承 models.Model；
	以下每个对象相当于数据库中的一个字段；
	models.CharField 表示 该字段是 char类型；
	max_length=xx 表示 最大长度为 30；
	同理 URLField 代表URL类型。
'''
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    city=models.CharField(max_length=60)
    state_province=models.CharField(max_length=30)
    country=models.CharField(max_length=50)
    website=models.URLField()

class Author(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=40)
    email=models.EmailField()

    def __unicode__(self):
	'''
		当我们打印Author列表时，无法区别它们；
		打印出来的内容型如；
		[<Author: author object>, <Author: author object>]；
		添加此方法后，便可以区分出来；
		详见后续内容。
	'''
        return '<%s %s>'%(self.first_name,self.last_name)

class Book(models.Model):
'''
	对于Book这个表，他和Author和Publisher两张表都有关联；
	一本书 可以有 多个作者
	一个作者 可以写 多本书
	所以此处 Book表的authors 对应 Author表 并且是多对多的关系，使用 ManyToManyField

	一本书 只能被一个出版社进行出版
	一个出版社 可以出版 多本书
	所以此处 Book表的publisher字段 对应 Publisher表 并且是一对多的关系，使用 ForeignKey(外键)
'''
    title=models.CharField(max_length=100)
    authors=models.ManyToManyField(Author)
    publisher=models.ForeignKey(Publisher)
    publication_date=models.DateField()
```

### 生成配置文件

```python
[root@youlinux ~/djanogweb]# python manage.py makemigrations
Migrations for 'app01':
  app01/migrations/0001_initial.py:
    - Create model Author
    - Create model Book
    - Create model Publisher
    - Add field publisher to book

# 生成配置文件

[root@youlinux.com ~/djanogweb]# ls app01/migrations/0001_initial.py
# 此文件就是刚刚执行的命令生成的

[root@youlinux.com ~/djanogweb]# cat app01/migrations/0001_initial.py
# 如果大家有兴趣可以看看该文件的内容

# 此时数据库中还没有真正的内容
```

### 根据配置文件创建数据库相关的内容
```python
[root@youlinux.com ~/djanogweb]# python manage.py migrate
Operations to perform:
  Apply all migrations: admin, app01, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying app01.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying sessions.0001_initial... OK

# 此时我们进入数据库看看发生了什么变化

MariaDB [(none)]> use youlinux

MariaDB [youlinux]> show tables;
+----------------------------+
| Tables_in_youlinux         |
+----------------------------+
| app01_author               |
| app01_book                 |
| app01_book_authors         |
| app01_publisher            |
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
+----------------------------+
14 rows in set (0.00 sec)

# 我们只定义了3个对象，也就是说我们应该只有3个表，其他的表从哪里来的？
# 这个是django自带的后台管理生成的；
# 下面我们来介绍如何使用后台进行管理。

```

## 登录django后台

### 首先我们需要先创建一个管理员账号和密码

```python
[root@youlinux.com ~/djanogweb]# python manage.py createsuperuser
```
![](http://i.imgur.com/qvvlM3O.jpg)

### 启动django
```python
[root@youlinux.com ~/djanogweb]# python manage.py runserver 0.0.0.0:8000
```
![](http://i.imgur.com/9D2ZTTG.jpg)

### 进入管理后台

![](http://i.imgur.com/a0Mdchk.jpg)

按照提示将对应的IP加入到 ALLOWED_HOSTS 中即可

```python

vim settings.py

ALLOWED_HOSTS = [
    u'192.168.193.148',
]
```

此时刷新网页即可
不需要重新启动，任何修改django会自动重启

![](http://i.imgur.com/9g8tE2T.jpg)

输入正确的账号和密码，即可进入管理界面

![](http://i.imgur.com/MoeCMMr.jpg)

此时并没有显示我们自己创建的三张表
应为此时我们并没有将这三个类注册到admin管理中

下面进行注册

```python

[root@youlinux.com ~/djanogweb]# vim app01/admin.py

import models
'''
	导入models，既我们自己写的数据库对象
	然后将三个类进行注册。
'''
admin.site.register(models.Author)
admin.site.register(models.Book)
admin.site.register(models.Publisher)

```

此时刷新网页，发现刚刚的三个表已经能够显示了

![](http://i.imgur.com/g0TfA9R.jpg)


#### url为何是IP后面加上admin?

此时我们可以查看urls.py文件

```python

[root@youlinux.com ~/djanogweb]# cat djanogweb/urls.py

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

```

### 管理

此时我们便可以对此三张表就行操作了

**增**
**删**
**改**
**查**

都可以通过页面进行操作


更多内容请参考后续文章


