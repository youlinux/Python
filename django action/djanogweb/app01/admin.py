# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

import models


def make_forbidden(modeladmin,request,queryset):
    queryset.update(status='forbidden')
make_forbidden.short_description='set to forbidden'
    


class BookAdmin(admin.ModelAdmin):
    list_display=('id','title','publisher','publication_date','status')
    search_fields=('title','publisher__name')
    list_filter=('publisher','publication_date')
    list_editable=('title','publication_date')
    list_per_page=5
    filter_horizontal=('authors',) # for Many to Many
    raw_id_fields=('publisher',) # for F Key
    actions=[make_forbidden,]
    


admin.site.register(models.Author)
admin.site.register(models.Book,BookAdmin)
admin.site.register(models.Publisher)


