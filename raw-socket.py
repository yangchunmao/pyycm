#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import socket
import struct
import binascii

rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(
    0x0800))

pkt = rawSocket.recvfrom(2048)

print(pkt)