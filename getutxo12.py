#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import json
import urllib.request as req

addr = '1Dorian4RoXcnBv9hnQ4Y2C1an6NJ4UrjX'

url = 'https://blockchain.info/unspent?active=%s' % addr
resp = req.urlopen(url)

utxo_set = json.loads(resp.read())["unspent_outputs"]

print(utxo_set)
for utxo in utxo_set:
  print("%s:%d - %ld Satoshis" % (utxo['tx_hash'], utxo['tx_output_n'], utxo['value']))