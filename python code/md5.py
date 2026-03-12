#md5.py
import struct

def leftrotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xffffffff

def pad(msg):
    ml = len(msg) * 8
    msg += b'\x80'
    while (len(msg) % 64) != 56:
        msg += b'\x00'
    msg += struct.pack('<Q', ml)
    return msg

def digest2state(digest):
    return list(struct.unpack("<4I", digest))

def state2digest(state):
    return struct.pack("<4I", *state)

s = [
7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21
]

K = [int(abs(__import__("math").sin(i+1)) * (2**32)) & 0xffffffff for i in range(64)]

def process(state, block):

    a,b,c,d = state
    M = list(struct.unpack("<16I", block))

    for i in range(64):

        if i < 16:
            f = (b & c) | (~b & d)
            g = i
        elif i < 32:
            f = (d & b) | (~d & c)
            g = (5*i + 1) % 16
        elif i < 48:
            f = b ^ c ^ d
            g = (3*i + 5) % 16
        else:
            f = c ^ (b | ~d)
            g = (7*i) % 16

        f = (f + a + K[i] + M[g]) & 0xffffffff
        a = d
        d = c
        c = b
        b = (b + leftrotate(f, s[i])) & 0xffffffff

    return [
        (state[0] + a) & 0xffffffff,
        (state[1] + b) & 0xffffffff,
        (state[2] + c) & 0xffffffff,
        (state[3] + d) & 0xffffffff
    ]
