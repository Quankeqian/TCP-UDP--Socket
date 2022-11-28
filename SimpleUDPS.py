from socket import *

udp_ser = socket(AF_INET, SOCK_DGRAM)
udp_ser.bind(('127.0.0.1', 666))
print("The UDP-server is ready to receive")
while 1:
    msg, adrr = udp_ser.recvfrom(1024)
    modmsg = msg.decode().upper()
    udp_ser.sendto(modmsg.encode(), adrr)
