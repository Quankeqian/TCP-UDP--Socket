from socket import *
c = socket(AF_INET, SOCK_STREAM)
c.connect(('127.0.0.1', 2121))
# 接收欢迎消息：
print(c.recv(1024).decode('utf-8'))
while 1:
    msg = input('please input')
    # 防止空消息
    if not msg:
        continue
    c.sendall(msg.encode('utf-8'))
    print(c.recv(1024).decode('utf-8'))
# c.send(b'exit')
c.close()
