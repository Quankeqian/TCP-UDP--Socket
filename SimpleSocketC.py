import socket
# 创建客户端套接字
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 发起和服务器的TCP连接
clientSocket.connect(('127.0.0.1', 6666))
while 1:
    msg = input('please input')
    # 防止空消息
    if not msg:
        continue
    clientSocket.sendall(msg.encode('utf-8'))
    if msg == '1':
        break
clientSocket.close()
