from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from . import models
from app01 import forms
# Create your views here.




def customers(request):

    # 首先使用orm操作
    # 读取customer表的所有数据
    # 只有当真正遍历的时候，才会去真正的取数据
    customers_obj=models.Customer.objects.all()

    # 每页显示一条数据
    paginator=Paginator(customers_obj,1)

    # 获取前端传递过来的数据
    page=request.GET.get('page')
    try:
        customers_1=paginator.page(page)

    #第一次请求时,page为空
    except PageNotAnInteger:
        # 返回第一页
        customers_1=paginator.page(1)

    # 请求的页码超过最后一页时
    except EmptyPage:
        # 返回最后一页
        customers_1=paginator.page(paginator.num_pages)

    return render(request,'crm/customers.html',{'customers_list':customers_1,})




