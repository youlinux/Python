
## django 之 HTML form表单

### 以下选取关键代码作出说明

#### 实现数据库中数据的实时展示，并可以通过前端页面进行添加


```python

# 首先添加一条路由

# vim djanogweb/urls.py

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^testpage/',views.db_handle),
]


def db_handle(request):

	# 默认获取数据的方法是get,提交数据为post
    if request.method=='POST':
        print(request.POST)
		'''
		name为前端HTMLform表单提交过来的数据
		publisher_id,author_ids均是
		
		'''
        book_name=request.POST.get('name')
        publisher_id=request.POST.get('publisher_id')
        print('==>',request.POST.get('author_ids'))
        author_ids=request.POST.getlist('author_ids')
        print(book_name,publisher_id,author_ids)

		# Book类 在 models.py 已经定义过
        new_book=models.Book(
            title=book_name,
            publisher_id=publisher_id,
            publication_date='2017-05-22'
        )
		
		# 使上述配置生效
        new_book.save()

		'''

		由于传过来的作者可能有多个
		所有采用此种方式添加
		* --> 列表
		** --> 字典

		'''
        new_book.authors.add(*author_ids)
        #new_book.authors.add(1,2,3,4)

	'''

	如果方法为GET
	则为获取数据

	'''
    books=models.Book.objects.all()
    publisher_list=models.Publisher.objects.all()
    author_list=models.Author.objects.all()

    return render(request,'t1.html',{'books':books,'publishers':publisher_list,'authors':author_list,})

```

```python

# vim templates/t1.html

'''
books为后端传递过来的值
使用django的模板语言进行循环展示
'''

<ul>
{% for i in books %}
    <li>{{ i.title}}</li>
{% endfor %}
</ul>

'''
使用原生的HTML表单进行验证
表单中name的值传递到后端 如：
<input type="text" name="name">
 <select name="publisher_id">
<select name="author_ids" multiple="multiple">
中将 name，publisher_id，author_ids的值到底到后端
通过 request.POST.get() 来接收
'''
<form method="post" action="/testpage/"> {% csrf_token %}
    book name:<input type="text" name="name">
    <input type="submit" value="添加新书">
    <select name="publisher_id">
        {% for publisher in publishers %}
        <option value="{{ publisher.id }}">{{ publisher.name }}</option>
        {% endfor %}
    </select>
    <select name="author_ids" multiple="multiple">
        {% for author in authors %}
        <option value="{{ author.id }}">{{ author.first_name}}{{ author.last_name }}</option>
        {% endfor %}
    </select>
</form>

```

## 效果如下

![](http://i.imgur.com/rP0GLMB.jpg)



                                                                                                            

