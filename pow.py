#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import hashlib
import time

# 最大的随机数
max_nonce = 2**32
m = hashlib.sha256()

#工作量证明
def proof_of_work(header, diff):
    #难度
    target = 2**(256-diff)
    for nonce in range(max_nonce):
        input = str(header) + str(nonce)
        m.update(input.encode('utf-8'))
        hash_result = m.hexdigest()
        
        if int(hash_result, 16) < target:
            print("哈希值 = %s, 幸运数 = %d." %(hash_result,nonce))
            return (hash_result, nonce)
    


#header = u'yangchunmao'
#diff = 10
#proof_of_work(header, diff)

if __name__ == '__main__' :
    
    start = 0
    hash_r = ''
    
    for diff_bit in range(32):
        
        diff = 2 ** diff_bit
        print("困难度 :%1d (%d bits)" % (diff, diff_bit))
        
        print('查找开始...')
        start_time = time.time()
        
        new_block = 'test block with transactions ' + hash_r
        (hash_r, nonce) = proof_of_work(new_block, diff_bit) 
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("耗时: %.4f 秒" % elapsed_time)        
        