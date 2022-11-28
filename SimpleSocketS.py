import socket

# 指定IP为本机IP 端口号任意指定为6666
ip_port = ('127.0.0.1', 6666)
# 最多可以连接back_log个客户端
back_log = 1
# 创建一个TCP套接字
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 对socket的配置重用ip和端口号
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 绑定端口号
serverSocket.bind(ip_port)  # 绑定哪个ip就要运行在哪台机器上
# 设置半连接池
serverSocket.listen(back_log)  # 让服务器聆听来自客户的TCP请求

print('The server is ready to receive')
while 1:
    # 阻塞等待，创建连接
    connectionSocket, addr = serverSocket.accept()  # 当客户敲门，创建了一个新的套接字，为这个客户服务
    while 1:
        try:
            msg = connectionSocket.recv(1024).decode('utf-8')  # 将报文转化为字符串
            if msg == '1':
                connectionSocket.close()
            print("服务器收到消息：", msg)
        except Exception as e:  # 异常检查
            break
serverSocket.close()
