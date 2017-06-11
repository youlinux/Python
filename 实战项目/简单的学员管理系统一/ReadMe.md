
## 学员管理系统设计开发


### 1、数据库模型设计篇


#### (a)、内部员工表

```python
class UserProfile(models.Model):
    '''
        内部员工表
        继承(User表 系统自带) + 扩展(name 为自己添加的一个字段)
        user字段和 User(系统自动的User表关联),省去了我们自己去验证的步骤,并且是OneToOneField
        name为另一个字段
    '''
    user = models.OneToOneField(User) # 继承
    # 唯一约束 关联系统自带的User表 一对一
    '''
    User 表中有一个用户 youlinux
    UserProfile 表中有一个用户 youlinux
    两张表的用户相关联,要有唯一性
    所以是 OneToOneField
    '''
    # 由于是 OneToOneField 在数据库中显示为 user_id
    # python2 汉字前面需要添加u python3不需要
    name = models.CharField(u"姓名",max_length=32) # 扩展
    # school = models.ForeignKey('School')
    def __str__(self):  # 设置在admin中显示的字段名
        return self.name

    class Meta:  # 定义一个元类
		verbose_name = u'员工信息表' # 设置在admin中显示的表名
		verbose_name_plural = u"员工信息表"

```

![](http://i.imgur.com/UtdMqLW.jpg)

![](http://i.imgur.com/dEAEqVH.jpg)

```

内部员工表
MariaDB [StudyCRM]> select * from app01_userprofile;
+----+--------------+---------+
| id | name         | user_id |
+----+--------------+---------+
|  2 | youlinux.com |       2 |
+----+--------------+---------+


系统自带的User表
MariaDB [StudyCRM]> select * from auth_user\G
          id: 2
    password: pbkdf2_sha256$36000$uvLvRwWZO3YN$OzABVOTckxP9sTSokSFf11AwNSPVjzVBNS9piK/dgOY=
  last_login: NULL
is_superuser: 0
    username: youlinux
  first_name: 
   last_name: 
       email: 
    is_staff: 0
   is_active: 1
 date_joined: 2017-06-01 13:22:47
2 rows in set (0.00 sec)


此时内部员工 youlinux.com 用户
便和user表用户 youlinux 相关联

app01_userprofile.user_id = auth_user.id

同时由于设置了 OneToOneField 所以是一一对应的
要添加内部员工,首先需要添加系统用户才行

```

![](http://i.imgur.com/iU371yd.jpg)


#### (b)、校区信息表

```python
# 校区表
class School(models.Model):
    name = models.CharField(u"校区名称",max_length=64,unique=True) #校区名字不能重复 唯一键
    addr = models.CharField(u"地址",max_length=128)
    # 一个校区可以有多个员工,一个员工可以属于多个校区 ManyToManyField
    staffs = models.ManyToManyField('UserProfile',blank=True)
    def __str__(self): # 
        return self.name

    class Meta:  # 定义一个元类
        verbose_name = u'校区信息表'
        verbose_name_plural = u"校区信息表"

```

![](http://i.imgur.com/wcnKwNb.jpg)

```

MariaDB [StudyCRM]> select * from app01_school;
+----+---------------+--------------+
| id | name          | addr         |
+----+---------------+--------------+
|  2 | 测试校区1     | 北京           |
+----+---------------+--------------+


MariaDB [StudyCRM]> select * from app01_userprofile;
+----+--------------+---------+
| id | name         | user_id |
+----+--------------+---------+
|  1 | adminSXJ     |       1 |
|  2 | youlinux.com |       2 |
+----+--------------+---------+

# 多对多关系,model 类会自动帮我们生成这个表 表名+字段名
# 学校id为2的 有两个员工,员工id分别为1和2
# 既 测试校区1 有两个员工 adminSXJ 和 youlinux.com
MariaDB [StudyCRM]> select * from app01_school_staffs;
+----+-----------+----------------+
| id | school_id | userprofile_id |
+----+-----------+----------------+
|  3 |         2 |              1 |
|  4 |         2 |              2 |
+----+-----------+----------------+

MariaDB [StudyCRM]> desc app01_school;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int(11)      | NO   | PRI | NULL    | auto_increment |
| name  | varchar(64)  | NO   | UNI | NULL    |                |
| addr  | varchar(128) | NO   |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+

# UNI PRI

```

#### (c)、课程信息表

```python
# 课程表
'''
这个表比较简单
仅仅说明了课程的名称(不能重复)
面授班价格
网络班价格
课程简介
'''
class Course(models.Model):
    name = models.CharField(u"课程名称",max_length=128,unique=True) # 课程名称不能重复
    price = models.IntegerField(u"面授价格")
    online_price = models.IntegerField(u"网络班价格")
    brief = models.TextField(u"课程简介")
    def __str__(self):
        return self.name

    class Meta:  # 定义一个元类
        verbose_name = u'课程表'
        verbose_name_plural = u"课程表"

```

![](http://i.imgur.com/5zM3gBW.jpg)

```
MariaDB [StudyCRM]> select * from app01_course;
+----+-----------------------+-------+--------------+-------------------------+
| id | name                  | price | online_price | brief                   |
+----+-----------------------+-------+--------------+-------------------------+
|  1 | Python自动化开发       |  9999 |         8888 | Python入门到放弃          |
|  2 | linux高级架构          |  4444 |         3333 | linux从入门到放弃         |
+----+-----------------------+-------+--------------+-------------------------+

```

#### (d)、班级列表

```python
# 定义一个元组
# 元组里面是一个一个的字典
class_type_choices = (('online', u'网络班'),
                      ('offline_weekend', u'面授班(周末)',),
                      ('offline_fulltime', u'面授班(脱产)',),
                      )  # 默认存到数据库的是字典的key的值


# 班级列表
class ClassList(models.Model):
    # 该班级上的课程
    # 一个班级可以上多个课程
    course = models.ForeignKey('Course')
    # 课程类型 使用 choices 进行下列框的选择
    course_type = models.CharField(u"课程类型",choices=class_type_choices,max_length=32)
    semester = models.IntegerField(u"学期")
    start_date = models.DateField(u"开班日期")
    graduate_date = models.DateField(u"结业日期",blank=True,null=True)

    # 一个班级可以有多个讲师
    # 一个讲师可以带多个班级
    teachers = models.ManyToManyField(UserProfile,verbose_name=u"讲师")

    class Meta: # 定义一个元类
        verbose_name = u'班级列表'
        verbose_name_plural = u"班级列表"
        '''
        	此三个字段之和的值唯一
        	例如
        	course Python入门到放弃
        	course_type 网络班
        	semester 第一期
        	这个记录只能有一条
        	不能出现多条
        '''
        unique_together = ("course","course_type","semester")

    def __str__(self):
    	# self.course_type 默认显示的是字典中key的值,也就是数据库中的值
    	# self.get_course_type_display 显示为字典中value的值,
        return "%s (%s)" %(self.course,self.get_course_type_display())

```

![](http://i.imgur.com/girJntR.jpg)

![](http://i.imgur.com/cGZ5kxl.jpg)

![](http://i.imgur.com/ARVyalA.jpg)

![](http://i.imgur.com/1tLfkfz.jpg)

```
# 数据库中 course_type 默认显示的是字典中key的值
MariaDB [StudyCRM]> select * from app01_classlist;
+----+------------------+----------+------------+---------------+-----------+
| id | course_type      | semester | start_date | graduate_date | course_id |
+----+------------------+----------+------------+---------------+-----------+
|  1 | online           |       14 | 2017-06-13 | NULL          |         1 |
|  2 | offline_fulltime |       14 | 2017-06-06 | NULL          |         2 |
+----+------------------+----------+------------+---------------+-----------+


MariaDB [StudyCRM]> desc app01_classlist;
# MUL 可以重复
# 其他字段省略
+---------------+-------------+------+-----+---------+----------------+
| Field         | Type        | Null | Key | Default | Extra          |
+---------------+-------------+------+-----+---------+----------------+
| course_id     | int(11)     | NO   | MUL | NULL    |                |
+---------------+-------------+------+-----+---------+----------------+



MariaDB [StudyCRM]> select * from app01_course;
+----+-----------------------+-------+--------------+-------------------------+
| id | name                  | price | online_price | brief                   |
+----+-----------------------+-------+--------------+-------------------------+
|  1 | Python自动化开发      |  9999 |         8888 | Python入门到放弃        |
|  2 | linux高级架构         |  4444 |         3333 | linux从入门到放弃       |
+----+-----------------------+-------+--------------+-------------------------+


app01_classlist.course_id 和 app01_course.id 相对应


# UserProfile表 和 ClassList的teacher 字段 为多对多的关系
# 所以会多出一张表
MariaDB [StudyCRM]> select * from app01_classlist_teachers;
+----+--------------+----------------+
| id | classlist_id | userprofile_id |
+----+--------------+----------------+
|  1 |            1 |              1 |
|  2 |            2 |              1 |
|  3 |            3 |              1 |
|  4 |            3 |              2 |
+----+--------------+----------------+

```

![](http://i.imgur.com/Y9qeqlN.jpg)


#### (e)、客户信息表

```python
# 客户表 
class Customer(models.Model):
    qq = models.CharField(u"QQ号",max_length=64,unique=True) # 唯一值,确定客户身份
    name = models.CharField(u"姓名",max_length=32,blank=True,null=True) # 名字不是必填字段
    phone = models.BigIntegerField(u'手机号',blank=True,null=True) # blank admin层面可以为空
    stu_id = models.CharField(u"学号",blank=True,null=True,max_length=64) # null 数据库层面可以为空

    # 和班级列表一个套路
    source_type = (('qq',u"qq群"),
                   ('referral',u"内部转介绍"),
                   ('51cto',u"51cto"),
                   ('agent',u"招生代理"),
                   ('others',u"其它"),
                   ) # 来源渠道
    source = models.CharField(u'客户来源',max_length=64, choices=source_type,default='qq')

    # 如果是内部转介绍,需要知道是谁转介绍的
    # 介绍者和被介绍者都是客户,既都是Customer表
    # 既自己关联自己

    # 'self' 或者 'Customer' 关联自己  需要一个额外的字段,在数据库中 反向关联
    # 此时数据库中customer表中会多出一个字段 referral_from_id(和外键一样)
    # classForeignKey（othermodel，on_delete，** options）
    # To create a recursive relationship – an object that has a many-to-one relationship with itself – use 
    # models.ForeignKey('self', on_delete=models.CASCADE).
    # 更为详细的步骤详见django官方文档
    referral_from = models.ForeignKey('self',verbose_name=u"转介绍自学员",help_text=u"若此客户是转介绍自内部学员,请在此处选择内部学员姓名",
    							      blank=True,null=True,)

    # 咨询的课程
    # 一个学生可以咨询多个课程,
    # 课程种类比较多,并且可能动态的增加或者减少,所以单独使用一张表来记录
    course = models.ForeignKey(Course,verbose_name=u"咨询课程")

    # 班级类型
    class_type = models.CharField(u"班级类型",max_length=64,choices=class_type_choices,default='offline_weekend') # 可供django admin选择

    # 咨询的内容
    customer_note = models.TextField(u"客户咨询内容详情",help_text=u"客户咨询的大概情况,客户个人信息备注等...")

    status_choices = (('signed',u"已报名"),
                      ('unregistered',u"未报名"),
                      ('graduated',u"已毕业"),
                      ) # 客户状态

    status = models.CharField(u"状态",choices=status_choices,max_length=64,default=u"unregistered",help_text=u"选择客户此时的状态")

    # 该客户的课程顾问是谁
    # 关联员工表
    # verbose_name 代表使该字段在admin上显示中文
    # 或者将中文写到第一个参数,也代表显示中文, ForeignKey,ManyToManyField,OneToOneField 第一个参数必须为modeltable
    # 所以可以使用 verbose_name 的效果类似
    consultant = models.ForeignKey(UserProfile,verbose_name=u"课程顾问")

    # auto_now_add 当前时间
    date = models.DateField(u"咨询日期",auto_now_add=True)

    # 如果客户已报名
    # 需要知道客户所报名的班级
    # 可以同时报多个班级
    # 只有已报名的学员才需要填写该字段
    class_list = models.ManyToManyField('ClassList',verbose_name=u"已报班级",blank=True)

    def __str__(self):
        return "%s,%s" %(self.qq,self.name )

	class Meta:  # 定义一个元类
		verbose_name = u'客户信息表'
		verbose_name_plural = u"客户信息表"


```

```
# referral_from_id 是模型添加的
# 用来记录自己关联自己的信息
MariaDB [StudyCRM]> select * from app01_customer\G
              id: 7
              qq: 890
            name: NULL
           phone: NULL
          stu_id: NULL
          source: others
      class_type: offline_weekend
   customer_note: 没有任何意义没有任何意向
          status: unregistered
            date: 2017-06-04
   consultant_id: 1
       course_id: 2
referral_from_id: 3
7 rows in set (0.00 sec)


MariaDB [StudyCRM]> select * from app01_customer_class_list;
+----+-------------+--------------+
| id | customer_id | classlist_id |
+----+-------------+--------------+
|  1 |           2 |            1 |
|  2 |           4 |            2 |
|  3 |           5 |            1 |
|  4 |           5 |            2 |
|  5 |           6 |            1 |
|  6 |           6 |            2 |
+----+-------------+--------------+

```

![](http://i.imgur.com/WAWAfya.jpg)


#### (f)、客户追踪记录

```python
# 客户追踪记录
class ConsultRecord(models.Model):

    # 当然和客户表项关联
    customer = models.ForeignKey(Customer,verbose_name=u"所咨询客户")
    note = models.TextField(u"跟进内容...")
    status_choices = ((1,u"近期无报名计划"),
                      (2,u"2个月内报名"),
                      (3,u"1个月内报名"),
                      (4,u"2周内报名"),
                      (5,u"1周内报名"),
                      (6,u"2天内报名"),
                      (7,u"已报名"),
                      )
    status = models.IntegerField(u"状态",choices=status_choices,help_text=u"选择客户此时的状态")

    # 课程顾问
    consultant = models.ForeignKey(UserProfile,verbose_name=u"跟踪人")
    date = models.DateField(u"跟进日期",auto_now_add=True) # 创建时 日期自动添加

    def __str__(self):
        return u"%s, %s" %(self.customer,self.status)

    class Meta:
        verbose_name = u'客户咨询跟进记录'
        verbose_name_plural = u"客户咨询跟进记录"

```

```

MariaDB [StudyCRM]> select * from app01_consultrecord;
+----+--------------------------------+--------+------------+---------------+-------------+
| id | note                           | status | date       | consultant_id | customer_id |
+----+--------------------------------+--------+------------+---------------+-------------+
|  1 | 测试测试测试成为                 |      1 | 2017-06-01 |             1 |           1 |
+----+--------------------------------+--------+------------+---------------+-------------+

```

![](http://i.imgur.com/Kooydet.jpg)


####  (g)、学生上课记录表

```python
# 每一天的上课记录
# 每一天的课程,对应多个学生的记录
class CourseRecord(models.Model):
    course = models.ForeignKey(ClassList,verbose_name=u"班级(课程)")
    day_num = models.IntegerField(u"节次",help_text=u"此处填写第几节课或第几天课程...,必须为数字")
    date = models.DateField(auto_now_add=True,verbose_name=u"上课日期")
    teacher = models.ForeignKey(UserProfile,verbose_name=u"讲师")
    def __str__(self):
        return u"%s 第%s天" %(self.course,self.day_num)
    class Meta:
        verbose_name = u'上课纪录'
        verbose_name_plural = u"上课纪录"
        unique_together = ('course','day_num') # 唯一
```

```
MariaDB [StudyCRM]> select * from app01_courserecord;
+----+---------+------------+-----------+------------+
| id | day_num | date       | course_id | teacher_id |
+----+---------+------------+-----------+------------+
|  1 |       1 | 2017-06-01 |         1 |          2 |
|  2 |       3 | 2017-06-01 |         2 |          1 |
+----+---------+------------+-----------+------------+

```

![](http://i.imgur.com/qCCBvUd.jpg)


#### (h)、学生成绩记录表

```python
# 学生记录表
class StudyRecord(models.Model):
    course_record = models.ForeignKey(CourseRecord, verbose_name=u"第几天课程")
    student = models.ForeignKey(Customer,verbose_name=u"学员")
    record_choices = (('checked', u"已签到"),
                      ('late',u"迟到"),
                      ('noshow',u"缺勤"),
                      ('leave_early',u"早退"),
                      )
    record = models.CharField(u"上课纪录",choices=record_choices,default="checked",max_length=64)
    score_choices = ((100, 'A+'),
                     (90,'A'),
                     (85,'B+'),
                     (80,'B'),
                     (70,'B-'),
                     (60,'C+'),
                     (50,'C'),
                     (40,'C-'),
                     (0,'D'),
                     (-1,'N/A'),
                     (-100,'COPY'),
                     (-1000,'FAIL'),
                     )
    score = models.IntegerField(u"本节成绩",choices=score_choices,default=-1)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(u"备注",max_length=255,blank=True,null=True)

    def __str__(self):
    	# self.student.qq student字段关联customer表
    	# self.student.qq 取出来的是customer表的qq字段
        return u"%s,学员:%s,纪录:%s, 成绩:%s" %(self.course_record,self.student.qq,self.record,self.get_score_display())

    class Meta:
        verbose_name = u'学员学习纪录'
        verbose_name_plural = u"学员学习纪录"
        unique_together = ('course_record','student') # 唯一
```

```

MariaDB [StudyCRM]> select * from app01_studyrecord;
+----+---------+-------+---------------------+------+------------------+------------+
| id | record  | score | date                | note | course_record_id | student_id |
+----+---------+-------+---------------------+------+------------------+------------+
|  1 | checked |    90 | 2017-06-01 13:34:47 | NULL |                1 |          1 |
|  2 | late    |    -1 | 2017-06-01 13:35:20 | NULL |                2 |          1 |
+----+---------+-------+---------------------+------+------------------+------------+

```


![](http://i.imgur.com/CuoAsPl.jpg)


![](http://i.imgur.com/8ioAOdJ.jpg)


## 此时我们的基本的表结构已经创建完毕了


### 前端页面设计

#### 引入bootstrap

##### 首先选择一个页面

http://v3.bootcss.com/getting-started/

将页面下载下来之后，导入到我们的django项目中。
(需要用到bootstrap的样式和jquery.js)

之后我们便可以对此页面做简单的修改


### 前端获取数据


#### view.Py

```python

from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from . import models
from app01 import forms
# Create your views here.


def customers(request):

    # 首先使用orm操作
    # 读取customer表的所有数据
    # 只有当真正遍历的时候，才会去真正的取数据
    # 获取Customer 表的全部信息
    customers_obj=models.Customer.objects.all()

    # 每页显示一条数据
    paginator=Paginator(customers_obj,1)

    # 获取前端传递过来的数据 第几页传递过来
    page=request.GET.get('page')
    try:
        customers_1=paginator.page(page)

    #如果页码不是一个整数,
    except PageNotAnInteger:
        # 返回第一页
        customers_1=paginator.page(1)

    # 请求的页码超过最后一页时
    except EmptyPage:
        # 返回最后一页
        customers_1=paginator.page(paginator.num_pages)

    return render(request,'crm/customers.html',{'customers_list':customers_1,})



'''
下面简单看下官方关于分页的介绍
'''

>>> from django.core.paginator import Paginator
>>> objects = ['john', 'paul', 'george', 'ringo']  
>>> p = Paginator(objects, 2)  # 将objects对象分成2页

>>> p.count  # 全部的内容
4
>>> p.num_pages # 一共有4部分内容,每页2个,一个2页
2
>>> type(p.page_range)  # `<type 'rangeiterator'>` in Python 2.
<class 'range_iterator'>
>>> p.page_range 
range(1, 3)

>>> page1 = p.page(1)
>>> page1
<Page 1 of 2>  # 页面范围 1,2
>>> page1.object_list
['john', 'paul']

>>> page2 = p.page(2)
>>> page2.object_list
['george', 'ringo']
>>> page2.has_next() # 判断page2是否还有下一页
False
>>> page2.has_previous() #判断page2是否还有上一页
True
>>> page2.has_other_pages() # 判断除了page2是否还有其他页码
True
>>> page2.next_page_number() # page2的下一页 会抛出异常
Traceback (most recent call last):
...
EmptyPage: That page contains no results
>>> page2.previous_page_number()
1
>>> page2.start_index() # The 1-based index of the first item on this page
3
>>> page2.end_index() # The 1-based index of the last item on this page
4

>>> p.page(0)
Traceback (most recent call last):
...
EmptyPage: That page number is less than 1
>>> p.page(3)
Traceback (most recent call last):
...
EmptyPage: That page contains no results

```


#### crm/customers.html

```python
# 基础 base.html页面
{% extends 'base.html' %}

# 固定语法 load 后跟一个函数名
# 此结构必须严格按照一定的规范来写
# 更多模板便签请移步官方文档 
# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/
{% load custom_tags %}

# 重写父页面
{% block page_header %}
customers 客户信息列表
{% endblock %}

# 重写父页面
{% block page_context %}

# like <Page 1 of 3>
{{ customers_list }}

# 引用bootstrap样式
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

    	# 每一个 customer 是 Customer 模型的对象
        {% for customer in customers_list %}
            <tr>
                <td>{{ customer.id }}</td>
                <td>{{ customer.qq }}</td>
                <td>{{ customer.name }}</td>
                <td>{{ customer.source }}</td>
                <td>{{ customer.course }}</td>
                <td>{{ customer.get_class_type_display }}</td>

                <!--样式名 和 类名相同-->
                # customer.status | youlinux_upper   customer.status的值作为youlinux_upper的一个参数传递到后端
                # 后端python函数处理之后,使用return 在返回给前端.实现后端数据的处理,前端接收
                <td class="{{ customer.status }}">{{ customer.status | youlinux_upper }}</td> <!--| truncatechars:2-->
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

    '''
    	>>> page2.paginator.page_range
			xrange(1, 4)

		>>> p.page_range
		xrange(1, 4)

		在此例子中,类似p变量没有传递过来
		所以只能采取此种方式

    '''
    # 引用bootstrap样式
    {% for page_num in customers_list.paginator.page_range %}
         {% if page_num == customers_list.number %}
            <li class="active"><a href="?page={{ page_num }}">{{ page_num }} </a></li>
         {% else %}
             <li class=""><a href="?page={{ page_num }}">{{ page_num }} </a></li>
         {% endif %}
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


##### 模板标签包结构

```python
app01/
    __init__.py
    models.py
    templatetags/
        __init__.py
        custom_tags.py
    views.py


custom_tags.py

from django import template

# 自定义模板注册到template模板中去
register = template.Library()

# 注册为一个过滤语法
@register.filter
def youlinux_upper(val):
    print("----val values--->:",val)
    return val.upper()

```

![](http://i.imgur.com/yqaeS2P.jpg)


![](http://i.imgur.com/PvPEOSU.jpg)


![](http://i.imgur.com/g3tiE2f.jpg)

 