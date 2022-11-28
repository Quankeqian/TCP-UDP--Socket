from concurrent.futures import ThreadPoolExecutor
from socket import *
import threading
import time


def tcplink(sock, addr):
    print('Accept new connection from%s:%s...' % addr)
    sock.send(b'Welcome!')
    while 1:
        data = sock.recv(1024)
        time.sleep(1)
        if data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello,%s' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed' % addr)


s = socket(AF_INET, SOCK_STREAM)
s.bind(('127.0.0.1', 9998))
s.listen(5)  # 等待连接的最大数量是5
# 创建线程池 指定工作线程数量为5
pool = ThreadPoolExecutor(max_workers=5)
print('The server-P is ready to receive')
while 1:
    # 接收一个新连接
    sock, addr = s.accept()
    # 创建线程任务，提交到线程池
    pool.submit(tcplink, sock, addr)
# 关闭线程池
pool.shutdown(wait=True)  # wait=True表示关闭线程池之前需要等待所有工作线程结束
