'''
  Using other's thread class to make thread
'''
import time
from threading import Thread
# or you can import threading

def thread_function():
  time.sleep(100)

t1 = Thread(name="something", target=thread_function)
t1.start()

'''
    Daemon thread: is killed when (other non-daemon thread have exited AND main program is ending)
    
    non-start - end
    d-start - sleep5
    
    -> non-start end
    -> main end
        -> d-start killed
'''
dt = Thread(name="", target=thread_function, args=(q, q))
dt.setDaemon(True)
dt.start()

'''
    join() is invoked in the caller thread that spawns a daemon thread. It blocks the caller thread intil...

    when you do join() = allow time for the thread to complete
    there is no purpose to non_daemon.join()
'''

dt.join()

'''
    This is how you implement your own thread instead of using other's class
    
    logging.debug("")
    
1 python 默认参数创建线程后，不管主线程是否执行完毕，都会等待子线程执行完毕才一起退出，有无join结果一样
2 如果创建线程，并且设置了daemon为true，即thread.setDaemon(True), 则主线程执行完毕后自动退出，不会等待子线程的执行结果。而且随着主线程退出，子线程也消亡。
3 join方法的作用是阻塞，等待子线程结束，join方法有一个参数是timeout，即如果主线程等待timeout，子线程还没有结束，则主线程强制结束子线程。
4 如果线程daemon属性为False， 则join里的timeout参数无效。主线程会一直等待子线程结束。
5 如果线程daemon属性为True， 则join里的timeout参数是有效的， 主线程会等待timeout时间后，结束子线程。此处有一个坑，即如果同时有N个子线程join(timeout），那么实际上主线程会等待的超时时间最长为 N ＊ timeout， 因为每个子线程的超时开始时刻是上一个子线程超时结束的时刻。

'''
class MyThread(Thread):
    def run(self):
        print "something"
        return

if __name__ == "__main__":
    for i in range(3):
        t = MyThread()
        t.start

'''
    empty(): see if it is empty
    q.size
    
    dir(q): to see all functions
    
    
    First thing puts in, First thing gets out
    You get out, and you destroy, WHAT THE HECK IS THIS
'''

import Queue
q = Queue.Queue()
q.put(1)


'''
    "Dispatcher"(fire events) communicate with Handler(listener) threads via Queues(data)
    
    multiple events in one queue(), queue() is to store events... okay! That's clear enough.

'''