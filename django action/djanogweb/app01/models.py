# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

                                                                                                     
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
