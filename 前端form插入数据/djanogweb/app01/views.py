# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from app01 import forms

# Create your views here.

def test(request):
    return HttpResponse('succ')


from app01 import models

def db_handle(request):
    if request.method=='POST':
        print(request.POST)
        book_name=request.POST.get('name')
        publisher_id=request.POST.get('publisher_id')
        print('==>',request.POST.get('author_ids'))
        author_ids=request.POST.getlist('author_ids')
        print(book_name,publisher_id,author_ids)
        
        new_book=models.Book(
            title=book_name,
            publisher_id=publisher_id,
            publication_date='2017-05-22'       
        )

        new_book.save()
        new_book.authors.add(*author_ids)
        #new_book.authors.add(1,2,3,4)


    books=models.Book.objects.all()
    publisher_list=models.Publisher.objects.all()
    author_list=models.Author.objects.all()
    
    return render(request,'t1.html',{'books':books,'publishers':publisher_list,'authors':author_list,}) 


