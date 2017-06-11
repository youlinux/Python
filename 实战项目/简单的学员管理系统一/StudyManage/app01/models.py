from django.db import models

# Create your models here.

from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User # 用户认证模块

# 写在此次可以被多个表共享
class_type_choices = (('online', u'网络班'),
                      ('offline_weekend', u'面授班(周末)',),
                      ('offline_fulltime', u'面授班(脱产)',),
                      )  # 默认存到数据库的是前面的内容

# 内部员工表
class UserProfile(models.Model):
    '''
        内部员工表
        继承 + 扩展
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
    name = models.CharField(u"姓名",max_length=32) # 扩展
    # school = models.ForeignKey('School')
    def __str__(self):
        return self.name

    class Meta:  # 定义一个元类
        verbose_name = u'员工信息表'
        verbose_name_plural = u"员工信息表"

# 校区表
class School(models.Model):
    name = models.CharField(u"校区名称",max_length=64,unique=True) #校区名字不能重复
    addr = models.CharField(u"地址",max_length=128)
    staffs = models.ManyToManyField('UserProfile',blank=True)
    def __str__(self): # Python 2  unicode
        return self.name

    class Meta:  # 定义一个元类
        verbose_name = u'校区信息表'
        verbose_name_plural = u"校区信息表"


# 课程表
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
        permissions=(('test_course','删除课程'),)

# 班级列表
class ClassList(models.Model):

    # 班级 --> 第几期 第几期
    # 哪个课程
    course = models.ForeignKey('Course')
    course_type = models.CharField(u"课程类型",choices=class_type_choices,max_length=32)
    semester = models.IntegerField(u"学期")
    start_date = models.DateField(u"开班日期")
    graduate_date = models.DateField(u"结业日期",blank=True,null=True)
    teachers = models.ManyToManyField(UserProfile,verbose_name=u"讲师")


    #def __unicode__(self):
    #    return "%s(%s)" %(self.course.name,self.course_type)

    class Meta: # 定义一个元类
        verbose_name = u'班级列表'
        verbose_name_plural = u"班级列表"
        unique_together = ("course","course_type","semester") # 此三个字段之和的值唯一
    def __str__(self):
        return "%s (%s)" %(self.course,self.get_course_type_display())
        # return "%s (%s)" % (self.course, self.course_type)

# 客户表 --> 未报名,已报名
class Customer(models.Model):
    qq = models.CharField(u"QQ号",max_length=64,unique=True) # 唯一值,确定客户身份
    name = models.CharField(u"姓名",max_length=32,blank=True,null=True) # 名字不是必填字段
    phone = models.BigIntegerField(u'手机号',blank=True,null=True) # blank admin层面可以为空
    stu_id = models.CharField(u"学号",blank=True,null=True,max_length=64) # null 数据库层面可以为空
    #id = models.CharField(u"身份证号",blank=True,null=True,max_length=128)
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

    # 'self' 或者 'Customer' 关联自己 必须添加related_name="internal_referral" 需要一个额外的字段,在数据库中 反向关联
    #referral_from = models.ForeignKey('self',verbose_name=u"转介绍自学员",help_text=u"若此客户是转介绍自内部学员,请在此处选择内部学员姓名",
    #                                 blank=True,null=True,related_name="internal_referral")
    referral_from = models.ForeignKey('self', verbose_name=u"转介绍自学员", help_text=u"若此客户是转介绍自内部学员,请在此处选择内部学员姓名",
                                      blank=True, null=True,)


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
    # 或者将中文写到第一个参数,也代表显示中文,和 verbose_name 的效果类似
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

    consultant = models.ForeignKey(UserProfile,verbose_name=u"跟踪人")
    date = models.DateField(u"跟进日期",auto_now_add=False) # 创建时 日期自动添加

    def __str__(self):
        return u"%s, %s" %(self.customer,self.status)

    class Meta:
        verbose_name = u'客户咨询跟进记录'
        verbose_name_plural = u"客户咨询跟进记录"


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
        return u"%s,学员:%s,纪录:%s, 成绩:%s" %(self.course_record,self.student.qq,self.record,self.get_score_display())

    class Meta:
        verbose_name = u'学员学习纪录'
        verbose_name_plural = u"学员学习纪录"
        unique_together = ('course_record','student')


