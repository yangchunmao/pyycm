#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import bitcoin
import hashlib


def from_string_to_bytes(a):
    return a if isinstance(a, bytes) else bytes(a, 'utf-8')

# 1K3RDEX75fhCo51aBCPThoQaZ2ktzU8rTu
# 038c8d4b695642ca1596957c74227963749ff0a25a547215a1c4e270c15dd470fa
# 18CWsZEQx9MKbqCAVWxDdtJkvxiP3ZvKgy
public_key = (63573444708645788551525965362271093873960097116568677635116892889812617687290, 22583425878611188324968380756771882163167123594493880232298905946219789350615)

hex_public_key_x = bitcoin.encode(public_key[0], '16')
hex_public_key_y = bitcoin.encode(public_key[1], '16')

#128/2 = 64byte + b'04'括号 = 65byte
print('Public Key Len is: ', len(hex_public_key_x) + len(hex_public_key_y))
#从公钥生成比特币地址步骤
#65byte
byte_public_key = bitcoin.encode_pubkey(public_key, 'bin')
print('Byte Public Key is: ', byte_public_key, len(byte_public_key))

##############################################################
# 压缩公钥
compressed_public_key = bitcoin.encode_pubkey(public_key, 'bin_compressed')
byte_public_key = compressed_public_key
##############################################################
#sha256 
sha256_public_key = hashlib.sha256(byte_public_key).digest()
print('Sha256 Public Key is: ', sha256_public_key, len(sha256_public_key))
#hash160
hash160_public_key = hashlib.new('ripemd160', sha256_public_key).digest()
print('Hash160 Public Key is: ', hash160_public_key, len(hash160_public_key))
version = 0
# version+hash160(SHA-256(public key))
inp_fmtd_public_key = bytes([version]) + hash160_public_key
print('Inp Fmtd Public Key is:', inp_fmtd_public_key)

leadingzbytes = 0
for x in inp_fmtd_public_key:
    if x != 0:
        break
    leadingzbytes += 1
    
print('Leadingzbytes is:', leadingzbytes)

# checksum 
checksum = hashlib.sha256(hashlib.sha256(from_string_to_bytes(inp_fmtd_public_key)).digest()).digest()[:4]
print('Check Sum is:', checksum)

# 地址
addr = '1' * leadingzbytes + bitcoin.encode(bitcoin.decode(inp_fmtd_public_key+checksum, 256), 58)
print('Addr is:', addr)



