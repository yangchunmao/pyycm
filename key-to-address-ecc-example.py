#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import bitcoin

# Generate a random private key
valid_private_key = False

while not valid_private_key:
    private_key = bitcoin.random_key()
    decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')    
    valid_private_key = 0 < decoded_private_key < bitcoin.N
print('Private Key (hex) is: ', private_key, len(private_key))
print('Private Key (decimal) is: ', decoded_private_key, len(str(decoded_private_key)))

# 10进制的私钥转化为WIF格式
wif_encoded_private_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
print('Private Key (WIF) is: ', wif_encoded_private_key, len(wif_encoded_private_key))

# 添加后缀 '01', 表明这是一个压缩私钥
compressed_private_key = private_key + '01'
print('Private Key Compressed (hex) is: ', compressed_private_key)

# WIF 钱包Wallet导入Import格式Format
# WIF压缩格式私钥
# wif_compressed_private_key = bitcoin.encode_privkey(bitcoin.decode_privkey(compressed_private_key, 'hex'), 'wif_compressed')
# wif_compressed 算法已经添加了01后缀, 辨识为压缩私钥
wif_compressed_private_key = bitcoin.encode_privkey(decoded_private_key, 'wif_compressed')
print('Private Key (WIF-Compressed) is: ', wif_compressed_private_key)

# 通过ECDSA算法形成公钥
public_key = bitcoin.fast_multiply(bitcoin.G, decoded_private_key)
print('Public Key (x, y) coordinates is: ', public_key)

# hex编码, 转换前缀为 04
hex_encoded_public_key = bitcoin.encode_pubkey(public_key, 'hex')
print('Public Key (hex) is: ', hex_encoded_public_key)

# 压缩公钥, 根据y坐标奇,偶树前缀
(public_key_x, public_key_y) = public_key
compressed_prefix = '02' if (public_key_y % 2) == 0 else '03'
hex_compressed_public_key = compressed_prefix + (bitcoin.encode(public_key_x, 16).zfill(64))
print('Compressed Public Key (hex) is: ', hex_compressed_public_key)

# 从公钥生成比特币地址
print('Bitcoin Address (b58check) is: ', bitcoin.pubkey_to_address(public_key))

# 从压缩的公钥生成压缩的比特币地址
print('Compressed Bitcoin Address (b58check) is: ', bitcoin.pubkey_to_address(hex_compressed_public_key))

