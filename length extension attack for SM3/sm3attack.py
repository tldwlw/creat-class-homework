from gmssl import sm3, func
import random
import struct
import binascii
from math import ceil

secret = str(random.random())
secrethash = sm3.sm3_hash(func.bytes_to_list(bytes(secret, encoding='utf-8')))
secretlen = len(secret)
padstr = ""
pad = []

xor = lambda a, b:list(map(lambda x, y: x ^ y, a, b))
rotl = lambda x, n:((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)
get_uint32_be = lambda key_data:((key_data[0] << 24) | (key_data[1] << 16) | (key_data[2] << 8) | (key_data[3]))
put_uint32_be = lambda n:[((n>>24)&0xff), ((n>>16)&0xff), ((n>>8)&0xff), ((n)&0xff)]
padding = lambda data, block=16: data + [(16 - len(data) % block)for _ in range(16 - len(data) % block)]
unpadding = lambda data: data[:-data[-1]]
list_to_bytes = lambda data: b''.join([bytes((i,)) for i in data])
bytes_to_list = lambda data: [i for i in data]
random_hex = lambda x: ''.join([random.choice('0123456789abcdef') for _ in range(x)])

IV = [
    1937774191, 1226093241, 388252375, 3666478592,
    2842636476, 372324522, 3817729613, 2969243214,
]

Tj = [
    2043430169, 2043430169, 2043430169, 2043430169, 2043430169, 2043430169,
    2043430169, 2043430169, 2043430169, 2043430169, 2043430169, 2043430169,
    2043430169, 2043430169, 2043430169, 2043430169, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042, 2055708042, 2055708042,
    2055708042, 2055708042, 2055708042, 2055708042
]


def fj(x, y, z, j):
    if 0 <= j and j < 16:
        ret = x ^ y ^ z
    elif 16 <= j and j < 64:
        ret = (x & y) | (x & z) | (y & z)
    return ret

def gj(x, y, z, j):
    if 0 <= j and j < 16:
        ret = x ^ y ^ z
    elif 16 <= j and j < 64:
        ret = (x & y) | ((~ x) & z)
    return ret

def p0(x):
    return x ^ (rotl(x, 9 % 32)) ^ (rotl(x, 17 % 32))

def p1(x):
    return x ^ (rotl(x, 15 % 32)) ^ (rotl(x, 23 % 32))

def cf(vi, bi):
    w = []
    for i in range(16):
        weight = 0x1000000
        data = 0
        for k in range(i*4,(i+1)*4):
            data = data + bi[k]*weight
            weight = int(weight/0x100)
        w.append(data)

    for j in range(16, 68):
        w.append(0)
        w[j] = p1(w[j-16] ^ w[j-9] ^ (rotl(w[j-3], 15 % 32))) ^ (rotl(w[j-13], 7 % 32)) ^ w[j-6]
        str1 = "%08x" % w[j]
    w1 = []
    for j in range(0, 64):
        w1.append(0)
        w1[j] = w[j] ^ w[j+4]
        str1 = "%08x" % w1[j]

    a, b, c, d, e, f, g, h = vi

    for j in range(0, 64):
        ss1 = rotl(
            ((rotl(a, 12 % 32)) +
            e +
            (rotl(Tj[j], j % 32))) & 0xffffffff, 7 % 32
        )
        ss2 = ss1 ^ (rotl(a, 12 % 32))
        tt1 = (fj(a, b, c, j) + d + ss2 + w1[j]) & 0xffffffff
        tt2 = (gj(e, f, g, j) + h + ss1 + w[j]) & 0xffffffff
        d = c
        c = rotl(b, 9 % 32)
        b = a
        a = tt1
        h = g
        g = rotl(f, 19 % 32)
        f = e
        e = p0(tt2)

        a, b, c, d, e, f, g, h = map(
            lambda x:x & 0xFFFFFFFF ,[a, b, c, d, e, f, g, h])

    v_j = [a, b, c, d, e, f, g, h]
    return [v_j[i] ^ vi[i] for i in range(8)]

def myhash(msg, new_v):
    len1 = len(msg)
    reserve1 = len1 % 64
    msg.append(0x80)
    reserve1 = reserve1 + 1
    # 56-64, add 64 byte
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    for i in range(reserve1, range_end):
        msg.append(0x00)

    bit_len = (len1) * 8
    bit_lenstr = [bit_len % 0x100]
    for i in range(7):
        bit_len = int(bit_len / 0x100)
        bit_lenstr.append(bit_len % 0x100)
    for i in range(8):
        msg.append(bit_lenstr[7-i])

    grp_cou = round(len(msg) / 64) - 1

    B = []
    for i in range(0, grp_cou):
        B.append(msg[(i + 1)*64:(i+2)*64])

    V = []
    V.append(new_v)
    for i in range(0, grp_cou):
        V.append(cf(V[i], B[i]))

    y = V[i+1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result


def kdf(z, klen): # z为16进制表示的比特串（str），klen为密钥长度（单位byte）
    klen = int(klen)
    ct = 0x00000001
    rcnt = ceil(klen/32)
    zin = [i for i in bytes.fromhex(z.decode('utf8'))]
    ha = ""
    for i in range(rcnt):
        msg = zin  + [i for i in binascii.a2b_hex(('%08x' % ct).encode('utf8'))]
        ha = ha + myhash(msg)
        ct += 1
    return ha[0: klen * 2]


def guess_hash(oldhash, serlen, m):
    """
    old_hash: secret的hash值
    secret_len: secret的长度
    m: 附加的消息
    hash(secret + padding + m)
    """
    vectors = []
    msg = ""
    # 将old_hash分组，每组8个字节, 并转换为整数
    oldhash_len = len(oldhash)
    for r in range(0, oldhash_len, 8):
        vectors.append(int(oldhash[r:r + 8], 16))

    # 伪造消息
    morr = serlen % 64
    n64 = int(secretlen / 64) * 64
    if serlen > 64:
        for i in range(0,n64 ):
            msg += 'm'
    for i in range(0, morr):#不足64的用m填充
        msg += 'm'
    msg = func.bytes_to_list(bytes(msg, encoding='utf-8'))
    msg = padding(msg)
    msg.extend(func.bytes_to_list(bytes(m, encoding='utf-8')))
    return myhash(msg, vectors)


def padding(msg):#将消息填充为64*n+56
    mlen = len(msg)
    msg.append(0x80)#用0x80做填充的分割
    mlen += 1
    tail = mlen % 64
    range_end = 56
    if tail > range_end:
        range_end = range_end + 64
    for i in range(tail, range_end):#填充0
        msg.append(0x00)
    bit_len = (mlen - 1) * 8
    msg.extend([int(x) for x in struct.pack('>q', bit_len)])
    for j in range(int((mlen - 1) / 64) * 64 + (mlen - 1) % 64, len(msg)):
        global pad
        pad.append(msg[j])
        global padstr
        padstr += str(hex(msg[j]))
    return msg

m = str(random.randint(1,2**16))
hashguess = guess_hash(secrethash, secretlen, m)
new_msg = func.bytes_to_list(bytes(secret, encoding='utf-8'))
new_msg.extend(pad)
new_msg.extend(func.bytes_to_list(bytes(m, encoding='utf-8')))
new_msg_str = secret + padstr + m

new_hash = sm3.sm3_hash(new_msg)

print("生成secret: ",secret)
print("secret hash:" , secrethash)
print("附加消息:", m)
print("hash_guess:",hashguess)
print("new message: \n",new_msg_str)
print("hash(new message):",new_hash)
if new_hash == hashguess:
    print("success!")
else:
    print("fail..")