
##　比form 更好用的类 modelform

```python

forms.py

from django import forms
from app01 import models

# 定义一个BookModelForm 继承 modelfrom
class BookModelForm(forms.ModelForm):
	# 定义一个meta类
    class Meta:
    	# 在models模型中引入Book表(对象)
        model=models.Book
        # 仅仅显示两个字段
        #fields=('title','publication_date')
        # 全部显示
        exclude=()
        # 定义前端的样式,前端写style 类名为 form-control
        widgets = {
	    'title':forms.TextInput(attrs={'class':'form-control'}),	
	}





views.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from app01 import forms

# Create your views here.

def book_modelform(request):
	# 请求方法为get时,不需要回去数据
    form=forms.BookModelForm()

    '''
    如果请求方式为post
    通过request.POST获取前端传递过来的数据
    '''
    if request.method == "POST":
    	# 在终端日志中打印,方便调试
        print(request.POST)
	form=forms.BookModelForm(request.POST)
		# modelform自带的判断
        if form.is_valid():
	    print("form is ok")
            print(form.cleaned_data)
            # 直接将数据保存咋数据库中
            form.save()
    # 返回指定的前端页面,并应用模板语言
    return render(request,'t1.html',{'book_form':form},)


t1.html


<html>
# 定义一个form表单,post方式提交
<form method='post'> {% csrf_token %}
    <style type="text/css">
    	# 后端引用了该样式
        .form-control{
  	    background-color:red;
	}
        # 前端自己引用
        .form-ele {
	    padding:20px;
	}
    </style>
    <!--{{ book_form }}--!>
    {% for i in book_form  %}
    '''
    	输出每个字段的名字 i.name
    	输出每个字段的提示框 i
    	输出每个字段的错误提示 i.errors
    '''
        <div class='form-ele'>{{ i.name }} {{ i }} {{ i.errors }}</div>
    {% endfor %}
    <input type="submit" value="新建图书">
</form>
</html>


```

![](http://i.imgur.com/KGKYMCL.jpg)