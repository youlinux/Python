# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.utils.html import format_html
                                                                                                     
class Publisher(models.Model):
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    city=models.CharField(max_length=60)
    state_province=models.CharField(max_length=30)
    country=models.CharField(max_length=50)
    website=models.URLField()

class Author(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=40)
    email=models.EmailField()

    def __unicode__(self):
	return '<%s %s>'%(self.first_name,self.last_name)
    class Meta:
        verbose_name_plural=u'作者'


class Book(models.Model):
    title=models.CharField(max_length=100)
    authors=models.ManyToManyField(Author)
    publisher=models.ForeignKey(Publisher)
    publication_date=models.DateField()
    status_choices=(
		    ('published',u'已出版'),
		    ('producing',u'出版中'),
		    ('forbidden',u'禁书'), 
 		   )
    status=models.CharField(choices=status_choices,max_length=32,default='producing')



    def colored_status(self):
        if self.status == "published":
            format_td=format_html('<span style="padding:2px;background-color:yellowgreen;color:white">已出版</span>')
        elif self.status == "producing":
	    format_td=format_html('<span style="padding:2px;background-color:red;color:white">出版中</span>')
        elif self.status == "forbidden":
	    format_td=format_html('<span style="padding:2px;background-color:yellow;color:white">禁止</span>')
        return format_td
    colored_status.short_description='status'
