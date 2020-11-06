import numpy as np
from utils import *
#{(2n,mn):[T,const_seq]}
conf = {(32,64)  : [22, 7, 2],
        (48,72)  : [22, 8, 3], 
        (48,96)  : [23, 8, 3],
        (64,96)  : [26, 8, 3], 
        (64,128) : [27, 8, 3],
        (96,96)  : [28, 8, 3], 
        (96,144) : [29, 8, 3],
        (128,128): [32, 8, 3], 
        (128,192): [33, 8, 3], 
        (128,256): [34, 8, 3]}

def encrypt_main(n,ck,msg,s_keys):
    ct = ''
    if (len(msg)%32) > 0:
        pad_count = 32 - (len(msg)%32)
        pad_bits = ['0' for i in range(pad_count)]
        msg = msg + ''.join(pad_bits)
    for i in range(int(len(msg)/32)):
        x = msg[(i*32):(i*32)+16]
        y = msg[(i*32)+16:(i*32)+32]
        ct = ct + speck_encrypt(n,ck,s_keys,x,y)
    return ct
        
def speck_encrypt(n,ck,s_keys,x,y):
    T = ck[0]
    for i in range(T):
        x = p_xor(np.binary_repr((int(''.join(list(np.roll(np.array(list(x)),ck[1]))),2) + int(y,2))%(2**n) ,16), s_keys[i])
        y = p_xor(''.join(list(np.roll(np.array(list(y)),-ck[2]))), x)
    return x+y

def decrypt_main(n,ck,ct,s_keys):
    # print(ct)
    msg = ''
    for i in range(int(len(ct)/32)):
        x = ct[(i*32):(i*32)+16]
        y = ct[(i*32)+16:(i*32)+32]
        msg = msg + speck_decrypt(n,ck,s_keys,x,y)
    return msg
        
def speck_decrypt(n,ck,s_keys,x,y):
    T = ck[0]
    for i in range(T-1,-1,-1):
        tmp = np.binary_repr((int(p_xor(x,s_keys[i]),2) - int(''.join(list(np.roll(np.array(list(p_xor(x,y))),ck[2]))),2))%(2**n) ,16)
        x_new = ''.join(list(np.roll(np.array(list(tmp)),-ck[1])))
        y_new = ''.join(list(np.roll(np.array(list(p_xor(x,y))),ck[2])))
        x = x_new
        y = y_new
    return x+y
        

def keygen(m,n,ck,my_key):
    print('Generating keys')
    l = []
    k = []
    l.append(my_key[32:48])
    l.append(my_key[16:32])
    l.append(my_key[0:16])
    k.append(my_key[48:64])
    T = ck[0]
    for i in range(0,T-1):
        l.append(p_xor(np.binary_repr((int(k[i],2) + int(''.join(list(np.roll(np.array(list(l[i])),ck[1]))),2))%(2**n),16), np.binary_repr(i,16)))
        k.append(p_xor(''.join(list(np.roll(np.array(list(k[i])),-ck[2]))), l[i+3]))
    return k
        
def speck():
    ch = 1
    if ch>=1 and ch<=10:
        print('Chosen configuration: Speck(',str(list(conf.keys())[ch-1][0]),'/',str(list(conf.keys())[ch-1][1]),')')
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
    s_keys = keygen(m,n,conf[ck],my_key)
    ed= input('Press E for encryption or D for decryption:\n')
    if ed == 'E':
        ct = encrypt_main(n,conf[ck],msg,s_keys)
        print('Encrypted text:\n',hex(int(ct,2)))
        f = open('ciphertext.txt', 'w')
        f.write(ct)
        f.close()
    elif ed == 'D':
        ct = open('ciphertext.txt', 'r').read()    
        res = decrypt_main(n,conf[ck],ct,s_keys)
        res_msg = bits2string(res)
        print('Decrypted message:\n',res_msg)
    else:
        print('Wrong choice! Try again.')

if __name__ == "__main__":
    speck()