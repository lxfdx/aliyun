from Crypto.Cipher import AES
import string
import random
import base64
import struct
import socket
from binascii import b2a_hex,a2b_hex
import requests
import json
import time
import hashlib

def getrandomstr(n):
	rule = string.ascii_letters + string.digits
	randomstr = random.sample(rule,n)
	return ''.join(randomstr)

def encode(text):
	text_length = len(text)
	amount_to_pad = 32 - (text_length % 32)
	if amount_to_pad == 0:
		amount_to_pad = 32
	pad = chr(amount_to_pad)
	return text + pad * amount_to_pad

def decode(text):
	pad = ord(text[-1])
	if pad<1 or pad>32:
		pad=0
	return text[:len(text)-pad]

def decrypto(text):
	key1 = '1234567890123456789012345678901234567890123='.encode('utf-8')
	key = base64.b64decode(key1)
	cryptor = AES.new(key,AES.MODE_CBC,key[:16])
	b64decode = base64.b64decode(text)
	plain_text = cryptor.decrypt(b64decode)
	content1 = plain_text[16:]
	content_length = int(b2a_hex(content1[:4]).decode('utf-8'),16)
	content = content1[4:content_length+4].decode('utf-8')
	conjson = json.loads(content)
	corpid = content1[content_length+4:]
	#print('The data from dingding:')
	#print('='*100)
	#print(conjson)
	EventType = conjson['EventType']
	return content

def encrypto(text):
	key1 = '1234567890123456789012345678901234567890123='.encode('utf-8')
	key = base64.b64decode(key1)
	cryptor = AES.new(key,AES.MODE_CBC,key[:16])
	text_to_encrypt = getrandomstr(16) + struct.pack('I',socket.htonl(len(text))).decode('utf-8') + text + 'ding614949de72a0b8a2'
	text = encode(text_to_encrypt)
	jiami = cryptor.encrypt(text.encode('utf-8'))
	result = base64.b64encode(jiami)
	return result.decode('utf-8')
