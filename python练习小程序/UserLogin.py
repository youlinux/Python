# 简单练习题

'''
输入用户名密码
认证成功后显示欢迎信息
输错三次后锁定
'''

import sys,os

os.system('clear') # 调用系统命令 清屏 此命令使用于Linux系统

i = 0

while i < 3:
    name = input("请输入用户名: ")

    lock_file=open('account_lock.txt','r+')
    lock_list = lock_file.readlines()
    # print(lock_list)  ['sixijie \n', 'youlinux\n', 'helloworld\n']
    for lock_line in lock_list:
        lock_line = lock_line.strip('\n') # 去掉readlines 方法后面的空格,否则会有两个空格
        if name == lock_line:
            sys.exit('用户 %s 已经被锁定，退出' %name)

    user_file = open('account.txt','r')
    user_list = user_file.readlines()
    for user_line in user_list:
        # print(user_line.strip('\n'))
        (user,password) = user_line.strip('\n').split() # 将用户名和密码按照空格 分别赋值给 user,password
        # print('user=%s password=%s' %(user,password))
        if name == user:
            j = 0
            while j < 3:
                passwd = input('请输入密码: ')
                if passwd == password:
                    print('欢迎登陆管理平台,用户 %s' %name)
                    sys.exit(0)
                else:
                    if j!=2:
                        print('用户%s密码错误,请重新输入,还有%d次机会'%(name,2-j))
                j+=1
            else:
                lock_file.write(name + '\n')
                sys.exit('用户 %s 达到最大登陆此时,将被锁定并退出' %name)
        else:
            pass
    else:
        if i!=2:
            print('用户%s不存在,情感重新输入,还有%d次机会' %(name,2-i))
    i+=1
else:
    sys.exit('用户%s不存在,退出' %name)

lock_file.close()
user_file.close()