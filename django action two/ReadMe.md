
##　django action 显示颜色

```python
models.py

from django.utils.html import format_html

def colored_status(self):
	'''
		定义一个颜色的函数
		format_html 将HTML转换为样式
		colored_status.short_description 定义显示的名字
	'''
	if self.status == "published":
		format_td=format_html(<'span style="padding:2px;background-color:yellowgreen;color:white">已出版</span>')
	elif self.status == "producing":
		format_td=format_html(<'span style="padding:2px;background-color:red;color:white">出版中</span>')
	elif self.status == "forbidden":
		format_td=format_html(<'span style="padding:2px;background-color:yellow;color:white">禁止</span>')
	return format_td
colored_status.short_description='status'


admin.py 中

数据库中添加字段

```

![](http://i.imgur.com/dPLX5gE.jpg)




