
## 添加url，并通过HttpResponse类，将数据返回到前端页面

## Python和静态页面分离，通过render方法

## 获取后端数据库信息，动态返回数据库中的数据到前端页面，并展示


## 页面展示

通过上篇我们已经知道如何通过后台管理数据库了

但是我们如何将我们需要的内容展示到前台呢？

如何在前台页面就能够添加内容呢？ 

本篇为大家一一讲解

## 首先写一个前台页面

### 直接返回字符串


```python

[root@youlinux.com ~/djanogweb]# vim djanogweb/urls.py


from django.conf.urls import url
from django.contrib import admin
from app01 import views
'''
	从app01目录下导入views，因为我们需要使用到其中定义的函数
	添加一条新的url，作为访问的入口
	此时url为/first时候，执行views.py下的firstfunc函数的内容
'''
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^first/', views.firstfunc),
]

[root@youlinux.com ~/djanogweb]# vim app01/views.py

from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse
# Create your views here.


def firstfunc(request):
	'''
		此时直接返回HttpResponse 类 即可
	'''
    return HttpResponse('<h1>welcome to http://www.youlinux.com</h1>')
```
![](http://i.imgur.com/TeauCU9.jpg)

### 返回HTML文件

上述中，我们仅仅能返回一个字符串，如果需要返回的内容过大
此种方式不太合适，因此我们可以直接返回一个HTML文件，
然后把字符串都写到这个单独的文件中

```python

[root@youlinux.com ~/djanogweb]# mkdir templates

[root@youlinux.com ~/djanogweb]# vim templates/t1.html

<html>
    <h1>This is second Page</h1>
</html>

[root@youlinux.com ~/djanogweb]# vim djanogweb/settings.py
# 必须告诉django 去哪里找这个文件
```
![](http://i.imgur.com/Mxecszp.jpg)

```python

[root@youlinux.com ~/djanogweb]# vim app01/views.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse

# Create your views here.


def firstfunc(request):
	'''
		render 第一个参数必须是 request 
		第二个参数是文件名，默认在templates下找
	'''
    return render(request,'t1.html')
```

![](http://i.imgur.com/aD1mQt6.jpg)

## 前台返回动态数据

上述两个例子，我们仅仅能够返回一个静态的页面

这种功能太有限制了 

现在我们想从数据库中取出数据

并在前台动态的展示，即数据库中的数据变化了，前台展示内容也会相应的变化

我们可以通过django自带的模板语句和数据库orm操作和完成此种需求

**首先我们需要在数据库中插入一些字段**

可以在后台admin页面完成

### 首先编写views.py文件

```python
为了简单考虑

我们可以首先从数据库中取出book，然后在前台进行展示

[root@youlinux.com ~/djanogweb]# vim app01/views.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse

from app01 import models
'''
	导入models，因为我们需要数据库模型对象
'''
# Create your views here.

def firstfunc(request):
'''
	models.Book.objects.all()获取所有对象
	通过打印我们可以在后台的终端查看输出的内容
	然后通过在render后面多加个参数将books传递给bookfront
	前台通过模板语言获取bookfront的值
'''
    books=models.Book.objects.all()
    print(books)
    return render(request,'t1.html',{'bookfront':books,})

[root@youlinux.com ~/djanogweb]# vim templates/t1.html

<html>
    <h1>This is second Page</h1>

<table border="1">
<caption>书名</caption>
    {% for book in bookfront %}
        <tr>
             <td>{{ book.title }}</td>
        </tr>
    {% endfor %}

</table>

</html>

'''
	前端的bookfront 等于 后端的books变量
	bookfront是个列表,用for来循环
	{% 中间写django模板语言的语法 %}
	{{ 中间写django模板语言的变量 }}
'''

```
![](http://i.imgur.com/oM7V8fN.jpg)


通过下图我可得出，book表中有两条记录
但是都是一样的对象我们不能够很好的分辨它们
此时可以采用 __unicode__方法
![](http://i.imgur.com/UieOunX.jpg)

**简单修改models.py 文件即可**

![](http://i.imgur.com/dc2ZHN6.jpg)

![](http://i.imgur.com/TWYLoib.jpg)

更多内容请参考后续文章



