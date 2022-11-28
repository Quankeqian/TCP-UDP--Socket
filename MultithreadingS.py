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
print('The server is ready to receive')
while 1:
    # 接收一个新连接
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
