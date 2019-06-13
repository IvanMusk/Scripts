# 批量ping ip，多线程版
import threading
import subprocess
import time
from queue import Queue

WORD_THREAD = 100

IP_QUEUE = Queue() 
for i in range(1,255):
    IP_QUEUE.put('202.118.32.' + str(i))
def ping_ip():
    while not IP_QUEUE.empty():
        ip = IP_QUEUE.get()
        res = subprocess.call('ping -c 2 -w 5 %s' % ip,shell=True,stdout=subprocess.PIPE)	# <-linux; win: ping -n
        if res == 0:
            print(ip)

if __name__ == '__main__':
    threads = []
    start_time = time.time()
    for i in range(WORD_THREAD):
        thread = threading.Thread(target=ping_ip)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print('Total time:%s' % (time.time() - start_time))