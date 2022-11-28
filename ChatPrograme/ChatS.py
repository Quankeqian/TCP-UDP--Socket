
from concurrent.futures import ThreadPoolExecutor
from socket import *
import time

# 发送文件


def file_send(filename, clientSocket):
    # 异常处理 文件不存在则返回错误信息
    try:
        file = open(filename, encoding='utf-8')
    except FileNotFoundError:
        print("没找到文件，请检查你的输入")
    sentences = []
    content = file.read()
    # clientSocket.send(("即将传输文件："+filename).encode('utf-8'))
    time.sleep(0.1)
    # 将content切割成长度为1024的一段段文字 最后一段<=1024
    while len(content) > 0:
        sentences.append(content[:min(len(content), 1024)])
        content = content[min(len(content), 1024):]  # 割了就扔掉
    # 循环发送切割后的文字段
    for sentence in sentences:
        # 将字符串类型转换成字节类型后发送
        clientSocket.send(sentence.encode('utf-8'))
        time.sleep(0.1)
    clientSocket.send("EOF".encode())  # 最后自动发送EOF表示消息传输完毕
    time.sleep(0.1)
    return

# 接收文件


def file_recv(filename, clientSocket):
    file = open(filename, "w", encoding='utf-8')
    sentence = clientSocket.recv(1024).decode('utf-8')
    while sentence != "EOF":
        # 将接收的文字写入文件
        file.write(sentence)
        sentence = clientSocket.recv(1024).decode('utf-8')
    print("服务器收到文件！可在当前文件夹下查看")
    return


# 发送信息


def msg_send(content, clientSocket):
    # clientSocket.send(("当前为消息的传输").encode('utf-8'))  # 首先告知对方当前进行的是消息的传输
    time.sleep(0.1)  # 防止粘包
    sentences = []
    # 将content切割成长度为1024的一段段字符串 最后一段<=1024
    while len(content) > 0:
        sentences.append(content[:min(len(content), 1024)])
        content = content[min(len(content), 1024):]  # 割了就扔掉
    # 循环发送切割后的消息段
    for sentence in sentences:
        # 将字符串类型转换成字节类型后发送
        clientSocket.send(sentence.encode('utf-8'))
        time.sleep(0.1)
    clientSocket.send("EOF".encode())  # 最后自动发送EOF表示消息传输完毕
    time.sleep(0.1)

# 接收消息


# 接收消息


def msg_recv(clientSocket):
    sentences = ""
    sentence = clientSocket.recv(1024).decode('utf-8')
    while sentence != "EOF":  # 消息传输未完毕
        sentences += sentence  # 拼接字符串
        sentence = clientSocket.recv(1024).decode('utf-8')  # 继续接收
    # print(sentences)  # 打印接收到的消息
    return sentences

# 服务器收取来自客户端的消息或文件


def recv_proc(connectionSocket):
    link = connectionSocket.recv(1024).decode('utf-8')
    link = link.split(":")  # 以 : 进行分隔成两个字符串
    from_link = link[0]
    to_link = link[1]
    global conn_pool  # 使用维护的连接 若想在函数内部对函数外的变量进行操作，就需要在函数内部声明其为global
    # 如果接收方不存在且不是服务器Server
    if not conn_pool.get(to_link) and to_link != "Server":  # get()函数返回指定键的value
        users = ""
        for key, value in conn_pool.items():  # items() 函数作用：以列表返回可遍历的(键, 值) 元组数组。
            users += key+' '
        connectionSocket.send("Message From Server".encode('utf-8'))
        time.sleep(0.1)
        connectionSocket.send(("NotExist%s" % users).endcode('utf-8'))
        return 2, "", "", ""
    sentences = ""
    parse = connectionSocket.recv(1024).decode('utf-8')
    print(parse)  # 测试测试测试
    # 判断是文件、退出标志还是信息
    if parse[:4] == "file":
        sentences = parse
        file_recv(parse[5:], connectionSocket)
    elif parse == ":q":  # 退出连接
        sentences = parse
        return 1, sentences, from_link, to_link
    elif parse == "msg":
        sentences = msg_recv(connectionSocket)
    return 0, sentences, from_link, to_link
# 服务端发


def send_proc(parse, from_link, to_link):
    global conn_pool
    if parse == ":q":
        conn_pool[from_link].send(("Message From Server").encode('utf-8'))
        time.sleep(0.1)
        conn_pool[from_link].send(parse.encode('utf-8'))
        return 1

    connectionSocket = conn_pool[to_link]
    print("用户 %s 向用户 %s 发送消息" % (from_link, to_link))
    if to_link != "Server":  # 不是和服务器聊天，而是和其他用户
        connectionSocket.send(("Message From %s" % from_link).encode())
        connectionSocket.send(parse.encode('utf-8'))
    else:
        print("Receive from %s:" % name, end='')
    if parse[0:4] == "file":
        if to_link != "Server":
            file_send(parse[5:], connectionSocket)
        print("文件转发成功")
    else:
        if to_link != "Server":
            msg_send(parse, connectionSocket)
        else:
            print(parse)
    return 0

# 服务器作为一个中转站，先接收，再发送


def main_proc(connectionSocket, name):
    global conn_pool
    while 1:
        fg, parse, from_link, to_link = recv_proc(connectionSocket)
        if fg == 2:  # 如果接收方不存在且不是服务器Server
            continue
        fg = send_proc(parse, from_link, to_link)
        if fg == 1:  # 退出连接
            break

    del conn_pool[name]  # 连接关闭，删除映射关系
    print("用户 %s 已下线（断开连接）" % name)
    connectionSocket.close()


serverPort = 2121
# 创建套接字
serverSocker = socket(AF_INET, SOCK_STREAM)
serverSocker.bind(('', serverPort))
serverSocker.listen(1)
global conn_pool  # 维护的连接
conn_pool = dict()  # 用户名：打开的tcp连接
conn_pool["Server"] = serverPort
print("我已经准备好提供服务啦")
# 创建线程池 最多为5个用户建立“群聊”
pool = ThreadPoolExecutor(max_workers=5)
while 1:
    connectionSocket, addr = serverSocker.accept()
    name = connectionSocket.recv(1024).decode('utf-8')  # 接收线程名保存在name中
    while conn_pool.get(name):
        connectionSocket.send("用户名已存在，请重新输入！".encode('utf-8'))
        name = connectionSocket.recv(1024).decode('utf-8')  # 重新接收
    connectionSocket.send("加入聊天成功！".encode('utf-8'))
    conn_pool[name] = connectionSocket
    print("与来自 %s 的用户 %s 建立连接" % (str(addr), name))
    # connectionSocket,name是函数main_proc的参数
    pool.submit(main_proc, connectionSocket, name)
pool.shutdown(wait=True)  # wait=True表示关闭线程池之前需要等待所有工作线程结束
