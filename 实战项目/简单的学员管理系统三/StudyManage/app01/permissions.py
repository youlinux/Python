


# 写一个装饰器
'''
    装饰器的基本语法
    def outer()
        def inner()
            pass
        :return inner

'''

from django.core.urlresolvers import resolve
from django.shortcuts import render,redirect

# 字典的key为数据库中权限的名称
# 字典的values 第一个为 url 别名 动态的
# 第二个为请求方法
# 第三个为参数

perm_dic = {
    'view_customer_list': ['customer_list','GET',[]],
    'view_customer_info': ['customer_detail','GET',[]],
    'edit_own_customer_info': ['customer_detail','POST',['qq','name']],
}

def perm_check(*args,**kwargs):
    request = args[0] # 被装饰的函数传递过来的 args[0]
    # 将一个url 转换为与其对应的别名 通过resolve方法
    # >> > resolve("/crm/customers/3/").url_name
    # 'customer_detail'  对应的别名 在urls.py中定义的别名
    url_resovle_obj = resolve(request.path_info)
    current_url_namespace = url_resovle_obj.url_name
    #app_name = url_resovle_obj.app_name #use this name later
    print("url namespace:",current_url_namespace)
    matched_flag = False # find matched perm item
    matched_perm_key = None

    # 如果current_url_namespace为空
    # 则说明没有url别名
    # 直接返回true
    if current_url_namespace is not None:#if didn't set the url namespace, permission doesn't work
        print("find perm...")
        for perm_key in perm_dic: # 循环字典
            perm_val = perm_dic[perm_key]
            # 格式必须要满足三个值
            if len(perm_val) == 3:#otherwise invalid perm data format
                # 第一个是url别名
                # 第二个是请求方法
                # 第三个是请求参数
                url_namespace,request_method,request_args = perm_val
                print(url_namespace,current_url_namespace)
                if url_namespace == current_url_namespace: #matched the url 判断请求url是否相等
                    if request.method == request_method:#matched request method 判断请求方法是否相等
                        if not request_args:#if empty , pass 没有参数时,直接匹配
                            matched_flag = True
                            matched_perm_key = perm_key # perm_key 为字典的key 即url别名
                            print('mtched...')
                            break #no need looking for  other perms 匹配到一个即可,不需要再往下走
                        else:
                            for request_arg in request_args: #might has many args 有多个参数时

                                # 反射
                                # getattr(obj, "method")
                                request_method_func = getattr(request,request_method) #get or post mostly
                                #print("----->>>",request_method_func.get(request_arg))
                                if request_method_func.get(request_arg) is not None:
                                    matched_flag = True # the arg in set in perm item must be provided in request data
                                else:
                                    matched_flag = False # 如果有一个参数没匹配上,直接退出
                                    print("request arg [%s] not matched" % request_arg)
                                    break #no need go further
                            if matched_flag == True: # means passed permission check ,no need check others
                                print("--passed permission check--")
                                matched_perm_key = perm_key
                                break

    else:#permission doesn't work
        return True
    '''
        判断用户有没有某个权限
        >>> from app01 import models
        >>> user1=models.UserProfile.objects.last()
        >>> user1
        <UserProfile: youlinux.com>
        
        >>> user1
        <UserProfile: youlinux.com>
        
        >>> user1.user.has_perm('app01.test_course')
        True
        
        然后我们去除youlinux.com 用户的权限
        
        在执行上述命令(要先退出终端)
        
        >>> user1.user.has_perm('app01.test_course')
        False 
        # 此时便是 False
    '''
    if matched_flag == True:
        #pass permission check
        perm_str = "app01.%s" %(matched_perm_key) # url别名
        if request.user.has_perm(perm_str): # 判断用户是否有权限
            print("\033[42;1m--------passed permission check----\033[0m")
            return True
        else:
            print("\033[41;1m ----- no permission ----\033[0m")
            print(request.user,perm_str)
            return False
    else:
        print("\033[41;1m ----- no matched permission  ----\033[0m")
def check_permission(func):
    def wrapper(*args,**kwargs):
        print("---start check perms",args[0])
        if not perm_check(*args,**kwargs):
            # args[0] 被装饰的函数传递过来的 request 相当于 *args
            return render(args[0],'crm/403.html') # 没有权限直接跳转403页面
        return func(*args,**kwargs) # 要装饰的函数
        #print("---done check perms")
    return wrapper