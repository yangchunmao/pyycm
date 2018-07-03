#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import socket
import struct
import binascii


# 安装struct.pack()函数封装帧
rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(
    0x0800))

# 从套接字中接收数据
pkt = rawSocket.recvfrom(2048)
print(pkt)

# 提出MAC帧头, 14字节(bytes) = 6字节目标mac地址, 6字节源mac地址, 2字节内部协议类型
eHeader = pkt[0][:14]
print(eHeader)
# 通过struct.unpack() !6s6s2s 解析
eHdr = struct.unpack('!6s6s2s', eHeader)
print(eHdr[0])
print(eHdr[1])
print(eHdr[2])

# IP头为4Bytes的整数倍,最小的长度为 4*5 = 20 bytes; 不包含option和padding字段
eIpHeader = pkt[0][14:34]

# 12s, 4s, 4s 进行过滤区分！标示转换网络字节序，前12字节为版本、头部长度、服务类型、总长度、标志等其他选项，后面的两个四字节依次为源IP地址和目的IP地址。
ipHdr = struct.unpack('!12s4s4s', eIpHeader)

print('源IP地址 %s' % ipHdr[1])
print('目的IP地址 %s' % ipHdr[2])

tcpHeader = pkt[0][34:54]
tcp_hdr = struct.unpack("!HH16s",tcpHeader)

print(tcp_hdr)

