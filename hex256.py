#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import hashlib

hash= hashlib.sha256()

text = '我是杨春茂'

for nonce in range(10):
    input = text + str(nonce)
    hash.update(input.encode('utf-8'))
    print(input, '=>', hash.hexdigest())