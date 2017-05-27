# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from app01 import forms

# Create your views here.

def book_modelform(request):
    form=forms.BookModelForm()
    if request.method == "POST":
        print(request.POST)
	form=forms.BookModelForm(request.POST)
        if form.is_valid():
	    print("form is ok")
            print(form.cleaned_data)
            form.save()
    return render(request,'t1.html',{'book_form':form},)

