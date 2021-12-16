#!/bin/python3

from core.skel import *

sample = """8A004A801A8002F478"""
sample="620080001611562C8802118E34"
# sample = "D2FE28"
# sample="38006F45291200"
# sample="EE00D40C823060"
answer1 = None
answer2 = None

"""
01100010000000001000000000000000000101100001000101010110001011001000100000000010000100011000111000110100
VVVTTTILLLLLLLLLLLVVVTTTILLLLLLLLLLLLLLLVVVTTTAAAAAVVVTTTAAAAAVVVTTTILLLLLLLLLLLVVVTTTAAAAAVVVTTTAAAAA
5, 0             2 0  0   22             0  4  10   5  4  11   1  0   2  packets  0 4  12   3  4   13
"""
def parse(input):
    data = [x for x in input.splitlines() if x][0]
    return data

def bit(msg, pos):
    x = int(msg[pos//4], 16)
    return 1 if x & (8 >> (pos % 4)) else 0

def binary(msg):
    return ''.join([str(bit(msg, x)) for x in range(len(msg)*4)] )

# Every packet begins with a standard header: the first three bits encode the packet version, and the next three bits
# encode the packet type ID. These two values are numbers; all numbers encoded in any packet are represented as binary
# with the most significant bit first. For example, a version encoded as the binary sequence 100 represents the number
# 4.
# 110100101111111000101000
# VVVTTTAAAAABBBBBCCCCC

def deci(msg):
    return int(msg, 2)

def header(msg):
    v = deci(msg[:3])
    t = deci(msg[3:6])
    return (msg[6:], {"ver": v, "type": t} )

def literal(msg):
    c = 1
    a = 0
    while c:
        c = deci(msg[0])
        a = a*16 + deci(msg[1:5])
        msg = msg[5:]

    return (msg, a)


def oper(msg):
    x = []
    # print(f"oper: {msg}")
    if msg[0]=='0':
        l = deci(msg[:16])
        subpacks = msg[16:16+l]
        msg = msg[16+l:]
        # print(f"decoding {l} bits")
        while len(subpacks)>4:
            subpacks, pack = packet(subpacks)
            # print(f"packet={pack}  msg={subpacks}")
            x.append(pack)

    else:
        packets = deci(msg[1:12])
        msg = msg[12:]
        # print(f"decoding {packets} packets")
        for p in range(packets):
            msg, pack = packet(msg)
            # print(f"packet={pack}  msg={msg}")
            x.append(pack)

    return (msg, x)

def packet(msg):
    # p1 = f"packet: {msg}"
    msg,pack = header(msg)
    # print(f"{p1} {pack}")
    if pack["type"] == 4:
        msg, pack["data"] = literal(msg)
    else:
        msg, pack["data"] = oper(msg)

    return (msg, pack)

def vers(pack):
    # print(f"vers: {pack}")
    if "ver" in pack:
        yield pack["ver"]

        try:
            for sub in pack["data"]:
                yield from vers(sub)
        except:
            pass

def part1(msg, part2=False):
    msg = binary(msg)
    msg,pack = packet(msg)
    return sum(list(vers(pack)))

def eval(pack):
    if pack["type"] == 4:
        return pack["data"]

    subs = [eval(x) for x in pack["data"]]
    if pack["type"] == 0:  # sum
        return sum(subs)
    elif pack["type"] == 1:  # product
        x = 1
        for d in subs:
            x *= d
        return x
    elif pack["type"] == 2:  # min
        return min(subs)
    elif pack["type"] == 3:  # max
        return max(subs)
    elif pack["type"] == 5:  # gt
        return 1 if subs[0] > subs[1] else 0
    elif pack["type"] == 6:  # lt
        return 1 if subs[0] < subs[1] else 0
    elif pack["type"] == 7:  # eq
        return 1 if subs[0] == subs[1] else 0


def part2(msg):
    msg = binary(msg)
    msg,pack = packet(msg)
    return eval(pack)


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)