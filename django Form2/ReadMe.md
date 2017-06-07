
## django Form class

```python

forms.py

# 导入forms类
from django import forms

# NameForm 继承 forms.Form
class NameForm(forms.Form):
	# <lable> 标签
	# max_length 验证最长字段长度
    your_name=forms.CharField(label='Your name',max_length=100)

等价于如下的HTML原生标签

<label for="your_name">Your name：</label> 
<input id="your_name" type = "text" name = "your_name" maxlength = "100" required />

views.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse

# Create your views here.

from . import forms

'''
如果是GET方法,直接返回表单的内容
如果是POST方法,并且输入的数据合法,则返回字符串'OK'
'''
def get_name(request):
    if request.method == 'POST':
		＃创建的表单实例，并使用从请求数据填充它
        form=forms.NameForm(request.POST)
		# 检查是否是有效的 (非空,长度没有达到最大值)
        if form.is_valid():
            return HttpResponse('OK')
	# 如果是GET 或者 任何其他方法,我们会创建一个空的form
    else:
        form=forms.NameForm()

    return render(request,'name.html',{'form':form,})

name.html

<form action='/yourname/' method="post">
{% csrf_token %}
{{ form }}
<input type="submit" value="Submit"/>
</form>

```

![](http://i.imgur.com/Kiqowia.jpg)

![](http://i.imgur.com/KJZf9ig.jpg)

![](http://i.imgur.com/jo4wk9x.jpg)