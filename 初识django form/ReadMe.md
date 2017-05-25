
## 使用django 自带的form

```python

# vim djanogweb/urls.py

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^bookform/',views.book_form),
]


# vim app01/forms.py
'''
新建一个文件
用来定义django自带的form类
'''

# 首先导入form类
from django import forms

# 定义一个BookForm类
# 创建两个对象
# title,publication_date
class BookForm(forms.Form):
    title=forms.CharField(max_length=10)
    #publisher_id=forms.IntegerField(widget=forms.Select)
    publication_date=forms.DateField()



# vim app01/views.py

from app01 import forms
def book_form(request):
    form=forms.BookForm()
    if request.method=="POST":
        print(request.POST)
        form=forms.BookForm(request.POST)
        if form.is_valid():
            print("form is OK")
            print(form.cleaned_data)
            form_data=form.cleaned_data
            print(form_data)
            form_data['publisher_id']=request.POST.get('publisher_id')
            book_obj=models.Book(**form_data)
            book_obj.save()
        else:

			# 自带错误提示
            print(form.errors)

    publisher_list=models.Publisher.objects.all()
    return render(request,'form.html',{'book_form':form,'publishers':publisher_list,})


'''
此时我们并没有实现select下拉列表的功能
可以借助前端实现

'''

# vim templates/form.html

<h1>hello world</h1>

<div>
<form action="" method="post"> {% csrf_token %}
    {{ book_form }}
    <select name="publisher_id">
        {% for publisher in publishers %}
            <option value="{{ publisher.id }}">{{ publisher.name }} </option>
        {% endfor %}
    </select>
    <input type="submit" value="新建图书">
</form>
</div>


```

![](http://i.imgur.com/LelpYsB.jpg)

![](http://i.imgur.com/njAEJYN.jpg)

![](http://i.imgur.com/ONZxY6V.jpg)

![](http://i.imgur.com/4XKJkzg.jpg)







