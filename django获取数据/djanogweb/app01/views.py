# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse

from app01 import models
# Create your views here.

def firstfunc(request):
    books=models.Book.objects.all()
    print(books)
    return render(request,'t1.html',{'bookfront':books,}) 

