#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import os
import socket
import struct
import time

#获取本机IP
my_ID = os.getpid() & 0xFFFF
print(my_ID)

ip_addr = "baidu.com"
ICMP_ECHO_REQUEST = 8

def checksum(source_string):
    """
    I'm not too confident that this is right but testing seems
    to suggest that it gives the same answers as in_cksum in ping.c
    """
    sum = 0
    countTo = (len(source_string)/2)*2
    count = 0
    while count<countTo:
        thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
        sum = sum + thisVal
        sum = sum & 0xffffffff # Necessary?
        count = count + 2

    if countTo<len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff # Necessary?

    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff

    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer

#Socket
icmp = socket.getprotobyname('icmp')
try:
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
except socket.error:
    raise

ip = socket.gethostbyname(ip_addr)
print(ip)

# Header is type (8), code (8), checksum (16), id (16), sequence (16)
my_checksum = 0

header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, my_checksum, my_ID, 1)
print(header)
byte_in_double = struct.calcsize('d')
data = (192 - byte_in_double) * "Q"
print(data)
data = struct.pack('d', time.clock()) + str.encode(data) 
print(data)

my_checksum = checksum(header + data)
print(my_checksum)

