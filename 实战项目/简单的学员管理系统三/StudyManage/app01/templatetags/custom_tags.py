from django import template
from django.utils.html import  format_html

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

# 需要重启django
