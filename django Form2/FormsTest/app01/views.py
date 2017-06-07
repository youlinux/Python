# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse

# Create your views here.

from . import forms

def get_name(request):
    if request.method == 'POST':
        form=forms.NameForm(request.POST)
        if form.is_valid():
	    return HttpResponse('OK')
    else:
	form=forms.NameForm()

    return render(request,'name.html',{'form':form,})


