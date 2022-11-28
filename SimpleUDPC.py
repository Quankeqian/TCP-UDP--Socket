from socket import *
udp_cli = socket(AF_INET, SOCK_DGRAM)
while 1:
    msg = input('input:')
    udp_cli.sendto(msg.encode('utf-8'), ('127.0.0.1', 666))
    data, addr = udp_cli.recvfrom(1024)
    print(data.decode('utf-8'))
