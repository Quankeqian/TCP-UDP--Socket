from socket import *
import time

# 发送信息


def msg_send(content, clientSocket):
    clientSocket.send(("当前为消息的传输").encode('utf-8'))  # 首先告知对方当前进行的是消息的传输
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
    print(sentences)  # 打印接收到的消息
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
    clientSocket.send(("即将传输文件："+filename).encode('utf-8'))
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
    sentence = clientSocket.recv(1024).decode()
    while sentence != "EOF":
        # 将接收的文字写入文件
        file.write(sentence)
        sentence = clientSocket.recv(1024).decode()
    print("文件接收成功！可在当前文件夹下查看")
    return
