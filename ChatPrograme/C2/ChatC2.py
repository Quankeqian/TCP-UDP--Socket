from socket import *
from threading import Thread
import time

# 发送信息


def msg_send(content, clientSocket):
    clientSocket.send(("当前为消息的传输:").encode('utf-8'))  # 首先告知对方当前进行的是消息的传输
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


def msg_recv(clientSocket):
    sentences = ""
    sentence = clientSocket.recv(1024).decode('utf-8')
    while sentence != "EOF":  # 消息传输未完毕
        sentences += sentence  # 拼接字符串
        sentence = clientSocket.recv(1024).decode('utf-8')  # 继续接收
    print(sentences, file=fw)  # 打印接收到的消息
    fw.flush()
    return

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
    fil = open(filename, "w", encoding='utf-8')
    sentence = clientSocket.recv(1024).decode()
    while sentence != "EOF":
        # 将接收的文字写入文件
        fil.write(sentence)
        sentence = clientSocket.recv(1024).decode()
    # print("已成功接收文件！可在当前文件夹下查看", file=fil)  # 打印接收到的消息
    fil.flush()
    print("文件接收成功！可在当前文件夹下查看", file=fw)
    fw.flush()
    return


# 发送线程
def send_proc(clientSocket, name):
    fg = True  # 信号
    while fg:
        to_name = input("请输入你想要聊天的对象：")
        clientSocket.send((name+":"+to_name).encode('utf-8'))  # 告知服务器收发双方名字
        time.sleep(0.5)  # 阻塞 等待收线程完成
        global exist
        if exist:
            exist = False  # ？？？？
            continue

        parse = input("请选择服务：\nfile:文件名\nmsg\n:q\n")
        clientSocket.send(parse.encode('utf-8'))
        if parse == "msg":
            content = input("请输入消息：")
            # msg_send(content,clientSocket)
            clientSocket.send(content.encode('utf-8'))
            clientSocket.send(("EOF").encode('utf-8'))
        elif parse[:4] == "file":
            file_send(parse[5:], clientSocket)
        elif parse == ":q":
            print(("您已下线"))
            clientSocket.close()
# 收线程


def recv_proc(clientSocket):
    fg = True
    while fg:
        from_whom = clientSocket.recv(1024).decode('utf-8')  # 来自谁
        parse = clientSocket.recv(1024).decode('utf-8')  # 内容是
        if parse[:4] == "file":
            print('\n%s(文件)' % from_whom, end=":", file=fw)
            fw.flush()
            file_recv(parse[5:], clientSocket)
        elif parse == ":q":
            fg = False  # 退出循环
        elif parse[:8] == "NotExist":
            print('%s' % from_whom, end=':')  # 输出Message From Server
            print("User Not Found")
            print("User list: %s" % parse[8:])
            global exist
            exist = True  # 没找到接收方
        else:
            print('\n%s' % from_whom, end=':', file=fw)
            fw.flush()
            msg_recv(clientSocket)
    return


severName = '127.0.0.1'
severPort = 2121
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((severName, severPort))

name = input("请输入你用于交流的用户名:")
clientSocket.send(name.encode('utf-8'))  # 发送给服务器校验（是否重复）并注册(加入字典)
reply = clientSocket.recv(1024).decode('utf-8')  # 接收服务器的校验结果
while reply == "用户名已存在":
    print(reply)
    name = input("请输入你用于交流的用户名:")
    clientSocket.send(name.encode('utf-8'))
    reply = clientSocket.recv(1024).decode('utf-8')
print(reply)
fw = open(name+'.output', "w", encoding='utf-8')  # 开一个文件当做用户的聊天框
fw.write("这里是%s的聊天框" % name)
fw.flush()  # 将缓冲区中的数据立刻写入文件

global exist  # 用于确定接收方是否存在的信号量
exist = False
# 开启收、发的线程
send_task = Thread(target=send_proc, args=(clientSocket, name))
recv_task = Thread(target=recv_proc, args=(clientSocket,))
send_task.start()
recv_task.start()
send_task.join()  # 使用join函数，主线程将被阻塞，一直等待被使用了join方法的线程运行完成
recv_task.join()
