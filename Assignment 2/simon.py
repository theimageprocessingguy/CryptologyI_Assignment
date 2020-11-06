import numpy as np
from utils import *
#{(2n,mn):[T,const_seq]}
conf = {(32,64)  : [32, 0],
        (48,72)  : [36, 0], 
        (48,96)  : [36, 1],
        (64,96)  : [42, 2], 
        (64,128) : [44, 3],
        (96,96)  : [52, 2], 
        (96,144) : [54, 3],
        (128,128): [68, 2], 
        (128,192): [69, 3], 
        (128,256): [72, 4]}

z = ['11111010001001010110000111001101111101000100101011000011100110',
     '10001110111110010011000010110101000111011111001001100001011010',
     '10101111011100000011010010011000101000010001111110010110110011',
     '11011011101011000110010111100000010010001010011100110100001111',
     '11010001111001101011011000100000010111000011001010010011101111']


def encrypt_main(ck,msg,s_keys):
    ct = ''
    if (len(msg)%32) > 0:
        pad_count = 32 - (len(msg)%32)
        pad_bits = ['0' for i in range(pad_count)]
        msg = msg + ''.join(pad_bits)
    for i in range(int(len(msg)/32)):
        x = msg[(i*32):(i*32)+16]
        y = msg[(i*32)+16:(i*32)+32]
        ct = ct + simon_encrypt(ck[0],s_keys,x,y)
    return ct
        
def simon_encrypt(T,s_keys,x,y):
    for i in range(T):
        tmp = x
        rot_x = p_and(''.join(list(np.roll(np.array(list(x)),-1))), ''.join(list(np.roll(np.array(list(x)),-8))))
        x = p_xor( p_xor(y,rot_x), p_xor(''.join(list(np.roll(np.array(list(x)),-2))), s_keys[i]) )
        y = tmp
    return x+y

def decrypt_main(ck,ct,s_keys):
    # print(ct)
    msg = ''
    for i in range(int(len(ct)/32)):
        x = ct[(i*32):(i*32)+16]
        y = ct[(i*32)+16:(i*32)+32]
        msg = msg + simon_decrypt(ck,s_keys,x,y)
    return msg
        
def simon_decrypt(ck,s_keys,x,y):
    T = ck[0]
    for i in range(T-1,-1,-1):
        tmp = y
        rot_y = p_and(''.join(list(np.roll(np.array(list(y)),-1))), ''.join(list(np.roll(np.array(list(y)),-8))))
        y = p_xor( p_xor(x,rot_y), p_xor(''.join(list(np.roll(np.array(list(y)),-2))), s_keys[i]) )
        x = tmp
    return x+y
        

def keygen(m,ck,my_key):
    print('Generating keys')
    s_keys = []
    s_keys.append(my_key[48:64])
    s_keys.append(my_key[32:48])
    s_keys.append(my_key[16:32])
    s_keys.append(my_key[0:16])
    T = ck[0]
    for i in range(m,T):
        tmp = ''.join(list(np.roll(np.array(list(s_keys[i-1])),3)))
        if m == 4:
            tmp = p_xor(tmp,s_keys[i-3])
        tmp = p_xor(tmp,''.join(list(np.roll(np.array(list(tmp)),1))))
        s_keys.append(p_xor(p_xor(p_not(s_keys[i-m]),tmp),p_xor(np.binary_repr(int(z[ck[1]][((i-m)%62)]),16),np.binary_repr(3,16))))
    return s_keys

def simon():
    ch = 1
    if ch>=1 and ch<=10:
        print('Chosen configuration: Simon(',str(list(conf.keys())[ch-1][0]),'/',str(list(conf.keys())[ch-1][1]),')')
    ck = (list(conf.keys())[ch-1][0],list(conf.keys())[ch-1][1])
    n = int(ck[0]/2)
    m = int(ck[1]/n)
    c = int(2 ** n - 4)
    # print(c,m,n,conf[ck])
    
    msg = open('sample_msg.txt', 'r').read()
    msg = string2bits(msg)
    my_key = open('key.txt', 'r').read()
    my_key = my_key.split('\n')[0]
    print('Message is: ',hex(int(msg,2)))
    print('Key is: ',hex(int(my_key,2)))
    s_keys = keygen(m,conf[ck],my_key)
    ed= input('Press E for encryption or D for decryption:\n')
    if ed == 'E':
        ct = encrypt_main(conf[ck],msg,s_keys)
        print('Encrypted text:\n',hex(int(ct,2)))
        f = open('ciphertext.txt', 'w')
        f.write(ct)
        f.close()
    elif ed == 'D':
        ct = open('ciphertext.txt', 'r').read()
        ct = ct.split('\n')[0]
        res = decrypt_main(conf[ck],ct,s_keys)
        res_msg = bits2string(res)
        print('Decrypted message:\n',res_msg)
    else:
        print('Wrong choice! Try again.')
    

if __name__ == "__main__":
    simon()