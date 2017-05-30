
```python

# admin.py

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

import models

'''
	改变默认的admin的样式
	此处简单的列举几个
'''
class BookAdmin(admin.ModelAdmin):
    list_display=('id','title','publisher','publication_date')
    search_fields=('title','publisher__name')
    list_filter=('publisher','publication_date')
    list_editable=('title','publication_date')
    list_per_page=5
    filter_horizontal=('authors',) # for Many to Many
    raw_id_fields=('publisher',) # for F Key
    

'''
	将这三个表注册到admin中
	接受admin的管理
'''
admin.site.register(models.Author)
admin.site.register(models.Book,BookAdmin)
admin.site.register(models.Publisher)

```