
## 简单学籍管理系统之二

```
新增
    可以查看某个客户的详细信息，
    并可以在前端直接对数据库进行修改
    并对数据进行判断(非空字段不允许提交)
```

`数据库模型和之前一样`

```python

# forms.py

#  不同的导入方式,使用的方式不同
from django.forms import ModelForm,forms
from . import models

# 继承ModelForm 类
class CustomerModel(ModelForm):
    class Meta:
    	# Customer 客户表
    	# model 对象关联Customer表的所有字段
    	# 既把Customer表的所有字段当成一个一个的表单
        model = models.Customer
        # exclude 除了哪个字段
        # 为空表示全部字段
        exclude=()

    # 重写父类的 __init__ 方法
    def __init__(self,*args,**kwargs):
    	# 继承父类,将父类原有的 *args,**kwargs 拿过来使用
        super(CustomerModel,self).__init__(*args,**kwargs)
        # self.fields['qq'].widget.attrs["class"]="form-control" # bootstrap
        '''
        	此段代码主要为了修饰显示的样式
        '''
        for fieldname in self.base_fields:
            field = self.base_fields[fieldname]
            field.widget.attrs=({'class':'form-control'})  
```

![](http://i.imgur.com/1TqEZpX.jpg)

![](http://i.imgur.com/Hm7KpYN.jpg)


```python

# views.py

# 客户详情页
# customer_id 为urls传递过来的参数
def customer_detail(request,customer_id):
    print(customer_id)
    # 在数据库中获取该id对应的所有字段数据
    customer_obj=models.Customer.objects.get(id=customer_id)
    if request.method == "POST":
    	# 修改 instance 为参数
        form = forms.CustomerModel(request.POST,instance=customer_obj)
        if form.is_valid(): # 此时去掉该判断,仍然可以正常执行,说明内部应该有判断modelform
            form.save()
            # 例如 /crm/customers/1/ 转换为 /crm/customers/
            base_url = '/'.join(request.path.split('/')[:-2])
            # 返回到指定的页面
            return HttpResponseRedirect(base_url)

    else: # 如果请求的方法为GET
    	# 获取数据
        form=forms.CustomerModel(instance=customer_obj)
    return render(request,'crm/customer_detail.html',{'customer_form':form})

```


```html

customer_detail.html

{% extends 'base.html' %}
# 加载模板标签
{% load custom_tags %}
{% block page_header %}
    客户详细信息列表
{% endblock %}


{% block page_context %}
# 自己写form 应用bootstrap样式
<form method="post"  class="form-horizontal"> {% csrf_token %}
{#  {{ customer_form }}#}
    {% for field in customer_form %}
  <div class="form-group">
  # 判断是否为必填项
  # 如果是必填项
  # label名字 加* 并加粗显示
      {% if field.field.required %}
            <label  class="col-sm-2 control-label">*{{ field.label }}</label>
      {% else %}
            <label  style="font-weight: normal" class="col-sm-2 control-label">{{ field.label }}</label>
      {% endif %}
    <div class="col-sm-10">
      {{ field }} # 显示获取到的值
      {{ field.errors }}
{#        {% if field.errors %}#}
{#        <ul>#}
{#           {% for error in field.errors %}#}
{#               <li style="color:red">{{ error }}</li>#}
{#               {% endfor %}#}
{#        </ul>#}
{#        {% endif %} 不知道为何不显示错误信息#}
    </div>
  </div>
    {% endfor %}
    <div class="col-sm-12">
        <input class="btn btn-success pull-right" type="submit" value="Save">
    </div>
</form>
{% endblock %}
```
![](http://i.imgur.com/ea56Q85.jpg)

```html

customers.html

{% extends 'base.html' %}

# 模板标签
{% load custom_tags %}
{% block page_header %}
customers 客户信息列表
{% endblock %}

{% block page_context %}

{{ customers_list }}
<table class="table table-hover">
    <thead>
        <tr>
            <th>ID</th>
            <th>qq</th>
            <th>姓名</th>
            <th>渠道</th>
            <th>咨询课程</th>
            <th>课程类型</th>
            <th>状态</th>
            <th>课程顾问</th>
            <th>日期</th>
        </tr>
    </thead>
    <tbody>
        {% for customer in customers_list %}
            <tr>
{# <td><a href="/crm/customers/{{ customer.id }}">{{ customer.id }}</a></td>#}
				# 使用动态的url  (url别名) customer.id 为接收过来的参数
                <td><a href="{% url 'customer_detail' customer.id %}">{{ customer.id }}</a></td>
                <td>{{ customer.qq }}</td>
                <td>{{ customer.name }}</td>
                <td>{{ customer.source }}</td>
                <td>{{ customer.course }}</td>
                <td>{{ customer.get_class_type_display }}</td>

                <!--样式名 和 类名相同-->
                # youlinux_upper 为后端的一个函数名
                # 将 customer.status 的值传递给后端的 函数
                # 后端函数处理过之后在使用return 返回回来
                <td class="{{ customer.status }}">{{ customer.status| youlinux_upper }}</td> <!--| truncatechars:2-->
                <td>{{ customer.consultant }}</td>
                <td>{{ customer.date }}</td>
            </tr>
        {% endfor %}
    </tbody>
</table>

<div class="pagination">

<nav>
  <ul class="pagination">
    {% if customers_list.has_previous %}
    <li class=""><a href="?page={{ customers_list.previous_page_number }}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>
    {% endif %}
    <!--<li class="active"><a href="#">1 <span class="sr-only">(current)</span></a></li>-->
    {% for page_num in customers_list.paginator.page_range %} # 循环每一页

    	# guess_page 为后端的一个函数名
    	# customers_list.number 和 page_num 作为两个参数 传递给后端函数
    	# 后端函数将结果使用return返回回来

    	# page_num 1,2,3,...最后一页
    	# customers_list.number 当前页码
        {% guess_page customers_list.number page_num %}
    {% endfor %}
    {% if customers_list.has_next %}
      <li class=""><a href="?page={{ customers_list.next_page_number }}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>
    {% endif %}
  </ul>
</nav>


<span class="step-links">
    {% if customers_list.has_previous %}
        <a href="?page={{ customers_list.previous_page_number }}">previous</a>
    {% endif %}

    <span class="current">
        Page {{ customers_list.number }} of {{ customers_list.paginator.num_pages }}.
    </span>

    {% if customers_list.has_next %}
        <a href="?page={{ customers_list.next_page_number }}">next</a>
    {% endif %}
</span>
</div>

{% endblock %}

```


```python
custom_tags.py

# 自定义模板注册到template模板中去
register = template.Library()

# 注册为一个过滤语法
@register.filter
def youlinux_upper(val):
    print("----val values--->:",val)
    return val.upper()

'''
current_page=1
第一次循环 current_page=1,loop_num=1
1-1<3
abs(1,2)<3
abc(1,3)<3
abs(1,4)<3 不符合
此时第四页不再显示出来

current_page=5
abs(2,5)<3 不符合
abs(3,5)<3 符合
abs(4,5)<3 符合
abs(5,5)<3 符合
abs(6,5)<3 符合
abs(7,5)<3 符合
abs(8,5)<3 不符合
所以显示3,4,5,6,7 页码
'''
@register.simple_tag # 装饰器,详情请见官方文档
def guess_page(current_page,loop_num):
    offset = abs(current_page-loop_num)
    if offset < 3:
            if current_page == loop_num:
                page_ele='''
                        <li class="active"><a href="?page=%s">%s</a></li>
                       '''%(loop_num,loop_num)
            else:
                page_ele='''
                        <li class=""><a href="?page=%s">%s</a></li>
                       '''%(loop_num,loop_num)
            return format_html(page_ele)
    return ''
# 为了防止其他页码显示none 所以使用返回'' 空字符串
```

![](http://i.imgur.com/jKU0TIj.jpg)

