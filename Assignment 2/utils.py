def string2bits(s=''):
    return ''.join([bin(ord(x))[2:].zfill(8) for x in s])
    

def bits2string(b=None):
    str_val= ''
    for i in range(0, len(b), 8):
        if int(b[i:i+8],2) > 0:
            str_val = str_val + chr(int(b[i:i+8],2))
    return str_val

def p_not(x):
    notmap = {'0': '1', '1': '0'}
    return ''.join([notmap[a] for a in x])

def p_xor(x,y):
    xormap = {('0', '1'): '1', ('1', '0'): '1', ('1', '1'): '0', ('0', '0'): '0'}
    return ''.join([xormap[a, b] for a, b in zip(x, y)])

def p_and(x,y):
    xormap = {('0', '1'): '0', ('1', '0'): '0', ('1', '1'): '1', ('0', '0'): '0'}
    return ''.join([xormap[a, b] for a, b in zip(x, y)])
