#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import hashlib
import time

max_nonce = 2 ** 32;
hash = hashlib.sha256()

def proof_of_work(header, diff_bits):
    
    # 计算困难目标
    target = 2 ** (256-diff_bits)
    for nonce in range(max_nonce):
        input = str(header) + str(nonce)
        hash.update(input.encode('utf-8'))
        hash_result = hash.hexdigest()
        
        if int(hash_result, 16) < target:
            print("幸运数为 %d" % nonce)
            print("哈希值为 %s" % hash_result)
            return (hash_result, nonce)
    print("Failed after %d (max_nonce)" % nonce)
    return nonce

if __name__ == '__main__':
    
    nonce = 0
    hash_result = ''
    
    # 困难度从 0 到 32 
    for diff_bit in range(32):
        
        diff = 2 ** diff_bit
        print("diff :%1d (%d bits)" % (diff, diff_bit))
        
        print("开始查找...")
        start_time = time.time()
        
        new_block = 'test block with transactions ' + hash_result
        (hash_result, nonce) = proof_of_work(new_block, diff_bit)
        
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        print("耗时: %.4f 秒" % elapsed_time)
        
