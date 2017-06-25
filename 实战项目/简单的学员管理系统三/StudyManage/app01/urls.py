"""StudyManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from app01 import views

urlpatterns = [
    url(r'^$',views.dashboard),
    # 可以给前端调用
    # 可以给permissions调用
    # 如果需要权限控制,必须写 name =
    url(r'customers/$',views.customers,name='customer_list'),
    # 为url起个别名
    url(r'customers/(\d+)/$',views.customer_detail,name='customer_detail'),
]
