import numpy as np
from numpy import logical_xor as xor
import random

def init_lfsr():
    l1 = {}
    l2 = {}
    l3 = {}
    #lfsr1 configuartion
    l1['reg'] = np.zeros((19,1),dtype=int)
    l1['clk_bit'] = 8
    l1['tap_bit'] = [13,16,17,18]
    #lfsr2 configuration
    l2['reg'] = np.zeros((22,1),dtype=int)
    l2['clk_bit'] = 10
    l2['tap_bit'] = [20,21]
    #lfsr3 configuration
    l3['reg'] = np.zeros((23,1),dtype=int)
    l3['clk_bit'] = 10
    l3['tap_bit'] = [7,20,21,22]
    return l1,l2,l3

def clk_with_bits(k,l1,l2,l3):
    for i in k:
        lsb = xor(xor(xor(xor(int(l1['reg'][l1['tap_bit'][3]]),int(l1['reg'][l1['tap_bit'][2]])),int(l1['reg'][l1['tap_bit'][1]])),int(l1['reg'][l1['tap_bit'][0]])),int(i))
        l1['reg'] = np.roll(l1['reg'], 1)
        l1['reg'][0] = int(lsb)
        
        lsb = xor(xor(int(l2['reg'][l2['tap_bit'][1]]),int(l2['reg'][l2['tap_bit'][0]])),int(i))
        l2['reg'] = np.roll(l2['reg'], 1)
        l2['reg'][0] = int(lsb)
        
        lsb = xor(xor(xor(xor(int(l3['reg'][l3['tap_bit'][3]]),int(l3['reg'][l3['tap_bit'][2]])),int(l3['reg'][l3['tap_bit'][1]])),int(l3['reg'][l3['tap_bit'][0]])),int(i))
        l3['reg'] = np.roll(l3['reg'], 1)
        l3['reg'][0] = int(lsb)
        
    return l1,l2,l3

def clk_majority_vote(l1,l2,l3):
    for i in range(100):
#        print(int(l1['reg'][l1['clk_bit']]),int(l2['reg'][l2['clk_bit']]),int(l3['reg'][l3['clk_bit']]))
        major_bit = int((int(l1['reg'][l1['clk_bit']])&int(l2['reg'][l2['clk_bit']])) | (int(l2['reg'][l2['clk_bit']])&int(l3['reg'][l3['clk_bit']])) | (int(l1['reg'][l1['clk_bit']])&int(l3['reg'][l3['clk_bit']])))
#        print(major_bit)
        if int(l1['reg'][l1['clk_bit']]) == major_bit:
            lsb = xor(xor(xor(int(l1['reg'][l1['tap_bit'][3]]),int(l1['reg'][l1['tap_bit'][2]])),int(l1['reg'][l1['tap_bit'][1]])),int(l1['reg'][l1['tap_bit'][0]]))
            l1['reg'] = np.roll(l1['reg'], 1)
            l1['reg'][0] = int(lsb)
        
        if int(l2['reg'][l2['clk_bit']]) == major_bit:
            lsb = xor(int(l2['reg'][l2['tap_bit'][1]]),int(l2['reg'][l2['tap_bit'][0]]))
            l2['reg'] = np.roll(l2['reg'], 1)
            l2['reg'][0] = int(lsb)
            
        if int(l3['reg'][l3['clk_bit']]) == major_bit:
            lsb = xor(xor(xor(int(l3['reg'][l3['tap_bit'][3]]),int(l3['reg'][l3['tap_bit'][2]])),int(l3['reg'][l3['tap_bit'][1]])),int(l3['reg'][l3['tap_bit'][0]]))
            l3['reg'] = np.roll(l3['reg'], 1)
            l3['reg'][0] = int(lsb)
        
    return l1,l2,l3

def gen_keystream(l1,l2,l3):
    ks = []
    for i in range(228):
        ks.append(int(xor(xor(int(l1['reg'][-1]),int(l2['reg'][-1])),int(l3['reg'][-1]))))
        major_bit = int((int(l1['reg'][l1['clk_bit']])&int(l2['reg'][l2['clk_bit']])) | (int(l2['reg'][l2['clk_bit']])&int(l3['reg'][l3['clk_bit']])) | (int(l1['reg'][l1['clk_bit']])&int(l3['reg'][l3['clk_bit']])))
        
        if int(l1['reg'][l1['clk_bit']]) == major_bit:
            lsb = xor(xor(xor(int(l1['reg'][l1['tap_bit'][3]]),int(l1['reg'][l1['tap_bit'][2]])),int(l1['reg'][l1['tap_bit'][1]])),int(l1['reg'][l1['tap_bit'][0]]))
            l1['reg'] = np.roll(l1['reg'], 1)
            l1['reg'][0] = int(lsb)
        
        if int(l2['reg'][l2['clk_bit']]) == major_bit:
            lsb = xor(int(l2['reg'][l2['tap_bit'][1]]),int(l2['reg'][l2['tap_bit'][0]]))
            l2['reg'] = np.roll(l2['reg'], 1)
            l2['reg'][0] = int(lsb)
            
        if int(l3['reg'][l3['clk_bit']]) == major_bit:
            lsb = xor(xor(xor(int(l3['reg'][l3['tap_bit'][3]]),int(l3['reg'][l3['tap_bit'][2]])),int(l3['reg'][l3['tap_bit'][1]])),int(l3['reg'][l3['tap_bit'][0]]))
            l3['reg'] = np.roll(l3['reg'], 1)
            l3['reg'][0] = int(lsb)
        
    ks.reverse()
    ks = "".join(map(str, ks)) 
    return ks

    
if __name__ == "__main__":
    #Step 1 - Initializing the LFSRs
    lfsr1, lfsr2, lfsr3 = init_lfsr()
    
    #Step 2 - Clocking LFSRs with session key
    print('Menu: \n1. Generate random 64 bit session key.\n2. Input a 64 bit session key.\n3. Use default 64 bit session key.\nEnter your choice : ')
    ch = input()
    sess_key = ''
    if ch == '1':
        for i in range(0,64):
            sess_key = sess_key + str(random.randint(0,1))
    elif ch == '2':
        print('Please enter 64 bit key: ')
        sess_key = input()
        if len(sess_key) != 64:
            print('Invalid key')
            exit()
    elif ch == '3':
        sess_key = ['0101','1101','1111','1010',
                    '0010','0110','1010','1000',
                    '1111','0100','1101','0010',
                    '1101','0111','1001','1010']
        sess_key = ''.join(sess_key)
    else:
        print('Wrong choice')
        exit()
    lfsr1, lfsr2, lfsr3 = clk_with_bits(sess_key,lfsr1,lfsr2,lfsr3)
    
    #Step 3 - Clocking LFSRs with frame counter
    print('Menu: \n1. Generate random 22 bit frame counter.\n2. Input a 22 bit frame counter.\n3. Use default 22 bit frame counter.\nEnter your choice : ')
    ch = input()
    frame_counter = ''
    if ch == '1':
        for i in range(0,22):
            frame_counter = frame_counter + str(random.randint(0,1))
    elif ch == '2':
        print('Please enter 22 bit frame counter: ')
        frame_counter = input()
        if len(frame_counter) != 22:
            print('Invalid frame counter')
            exit()
    elif ch == '3':
        frame_counter = ['11','1010','1011','0011','1100','1011']
        frame_counter = ''.join(frame_counter)
    else:
        print('Wrong choice')
        exit()
    lfsr1, lfsr2, lfsr3 = clk_with_bits(frame_counter,lfsr1,lfsr2,lfsr3)
    
    #Step 4 - Clocking LFSRs with majority vote
    lfsr1, lfsr2, lfsr3 = clk_majority_vote(lfsr1,lfsr2,lfsr3)
    
    #Step 5 - Production of key stream
    keystream = gen_keystream(lfsr1,lfsr2,lfsr3)
    print('Keystream is: ',keystream)
    