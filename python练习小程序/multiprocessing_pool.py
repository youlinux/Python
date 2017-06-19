import os,time,random # from random import random
from multiprocessing import Pool # 导入类 多进程下的 进程池

def long_time_tasl(name): # name变量接受 主函数传递过来的i变量的值
    print('Run task {} {}'.format(name,os.getpid())) # 输出当前进程的pid
    start = time.time() # 1497886458.758105 时间戳
    time.sleep(random.random() * 3)
    end = time.time()
    print('taks {} runs {} seconds'.format(name,(end - start)))

if __name__ == '__main__':
    print('Parent process {}'.format(os.getpid())) # 获取当前进程的pid
    p = Pool(10) # 设定10个线程池
    for i in range(15):
        # 执行 long_time_tasl 函数 参数为i
        p.apply_async(long_time_tasl,args=(i,)) #此时最多有10个线程在运行   非阻塞 apply阻塞函数
    print('Waiting for all subprocess done...')
    p.close()
    # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    p.join()  # 开始等待子进程
    print('All subprocess done')

'''
Parent process 22834 首先打印出父进程的pid
Waiting for all subprocess done...
Run task 0 22870  非阻塞
Run task 1 22871
Run task 2 22872
Run task 3 22873
Run task 4 22874
Run task 5 22875
Run task 6 22876
Run task 7 22877
Run task 8 22878
Run task 9 22879
taks 3 runs 0.13139867782592773 seconds
Run task 10 22873
taks 4 runs 0.5731551647186279 seconds
Run task 11 22874
taks 6 runs 1.3143348693847656 seconds
Run task 12 22876
taks 10 runs 1.416567087173462 seconds
Run task 13 22873
taks 5 runs 1.585859775543213 seconds
Run task 14 22875
taks 0 runs 1.9770333766937256 seconds
taks 7 runs 1.9951438903808594 seconds
taks 9 runs 2.009171485900879 seconds
taks 14 runs 0.6898910999298096 seconds
taks 11 runs 1.898632287979126 seconds
taks 1 runs 2.642512083053589 seconds
taks 2 runs 2.686354637145996 seconds
taks 12 runs 1.501657485961914 seconds
taks 8 runs 2.9703335762023926 seconds
taks 13 runs 2.9068305492401123 seconds
All subprocess done 


在linux系统上 使用ps | aux 命令 可以查看到如下进程 
root     22834  3.3  0.5 405832 11092 pts/2    Sl+  23:38   0:00 python a.py  pid 和上述输出一致
root     22870  0.0  0.4 184636  8372 pts/2    S+   23:38   0:00 python a.py
root     22871  0.0  0.4 184636  8380 pts/2    S+   23:38   0:00 python a.py
root     22872  0.0  0.4 184636  8384 pts/2    S+   23:38   0:00 python a.py
root     22873  0.0  0.4 184636  8380 pts/2    S+   23:38   0:00 python a.py
root     22874  0.0  0.4 184636  8384 pts/2    S+   23:38   0:00 python a.py
root     22875  0.0  0.4 184636  8384 pts/2    S+   23:38   0:00 python a.py
root     22876  0.0  0.4 184636  8384 pts/2    S+   23:38   0:00 python a.py
root     22877  0.0  0.4 184636  8384 pts/2    S+   23:38   0:00 python a.py
root     22878  0.0  0.4 184636  8176 pts/2    S+   23:38   0:00 python a.py
root     22879  0.0  0.4 184636  8384 pts/2    S+   23:38   0:00 python a.py

'''