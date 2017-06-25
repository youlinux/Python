from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from . import models
from app01 import forms
# Create your views here.
from app01.permissions import check_permission




@check_permission
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

@check_permission
def customer_detail(request,customer_id):
    print(customer_id)
    customer_obj=models.Customer.objects.get(id=customer_id)
    if request.method == "POST":
        form = forms.CustomerModel(request.POST,instance=customer_obj)
        print(request.POST) # 查看POST传递的参数
        print('errorsucc-->',form.errors)
        if form.is_valid(): # 此时去掉该判断,仍然可以正常执行,说明内部应该有判断modelform
            form.save()
            base_url = '/'.join(request.path.split('/')[:-2])
            print('error-->',form.errors)
            return HttpResponseRedirect(base_url)

    else:
        form=forms.CustomerModel(instance=customer_obj)
        print('url',request.path)
        base_url='/'.join(request.path.split('/')[:-2])
        print('base_url',base_url)
        print('errorsucc-->', form.errors)
    return render(request,'crm/customer_detail.html',{'customer_form':form})
