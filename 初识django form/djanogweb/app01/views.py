# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from app01 import forms

# Create your views here.

def test(request):
    return HttpResponse('succ')


from app01 import models

def book_form(request):
    form=forms.BookForm()
    if request.method=="POST":
        print(request.POST)
        form=forms.BookForm(request.POST)
        if form.is_valid():
            print("form is OK")
            print(form.cleaned_data)
            form_data=form.cleaned_data
            print(form_data)
            form_data['publisher_id']=request.POST.get('publisher_id')
            book_obj=models.Book(**form_data)
            book_obj.save()
        else:
            print(form.errors)

    publisher_list=models.Publisher.objects.all()
    print(form)
    return render(request,'form.html',{'book_form':form,'publishers':publisher_list,})
    

