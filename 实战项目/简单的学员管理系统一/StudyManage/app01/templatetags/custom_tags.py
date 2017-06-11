from django import template

# 自定义模板注册到template模板中去
register = template.Library()

# 注册为一个过滤语法
@register.filter
def youlinux_upper(val):
    print("----val values--->:",val)
    return val.upper()




# 需要重启django
