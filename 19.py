#!/bin/python3

from core.skel import *

sample = """
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
"""
answer1 = None
answer2 = None

def parse(input):
    lines = [parse_fields(x,digits+alpha+'-') for x in input.splitlines() if x]
    scanner = []
    for x in lines:
        if x[1] == "scanner":
            scanner.append(set())
        else:
            scanner[-1].add(tuple([int(a) for a in x]))

    return scanner

# Rotate given scanner around x axis (y becomes z)
def rotate_x(s):
    return set([ (x,z,-y) for x,y,z in s])

# Rotate given scanner around x axis (y becomes z)
def rotate_y(s):
    return set([ (-z,y,x) for x,y,z in s])

# Rotate given scanner around x axis (y becomes z)
def rotate_z(s):
    return set([ (-y,x,z) for x,y,z in s])

def translate(s, pos):
    X,Y,Z = pos
    return set([ (x+X, y+Y, z+Z) for x,y,z in s] )

sloc = []
# Returns set of beacons from t rotated/translated into s coord space, if overlap detected
def overlap(s,t):

    for sb in s:
        sx, sy, sz = sb
        for tb in t:
            tx, ty, tz = tb
            # assume beacons sb and tb are the same beacon in the same scanner orientation
            # Find location of scanner t relative to s
            # Determine if there are 12 matching beacons in this location
            torigin = (sx-tx, sy-ty, sz-tz)
            ts = translate(t, torigin)

            common = ts.intersection(s)
            if len(common) >= 12:
                print("Found map; scanner is at ", torigin)
                sloc.append(torigin)
                return ts
    return set()

def rotated(s, memo={}):
    already = set()
    r = frozenset(s)
    if r in memo:
        for x in memo[r]:
            yield x
    else:
        # Try every rotation
        for rx in range(4):
            r = rotate_x(r)
            for ry in range(4):
                r = rotate_y(r)
                for rz in range(4):
                    r = frozenset(rotate_z(r))
                    if r in already:
                        continue
                    already.add(r)

                    yield r
        memo[r] = already

def rotate(s,t):
    memo = set()
    for r in rotated(t):
        common = overlap(s,r)
        if common:
            return common
    return set()

def manhattan(a,b):
    x,y,z = a
    X,Y,Z = b

    return abs(x-X) + abs(y-Y) + abs(z-Z)

def part1(scanner, part2=False):
    global sloc
    map = scanner[0]
    sloc = [(0,0,0)]

    # Beacons rotated into place relative to scanner 0
    fixed = scanner[0:1]
    unknown = scanner[1:]

    while True:
        found = []
        new = []
        for x in range(len(unknown)):
            t = frozenset(unknown[x])
            for s in fixed:
                match = rotate(s, t)
                if match:
                    found.append(x)
                    new.append(match)
                    map |= match
                    print(f"Matched scanner {x+1} of {len(unknown)}  beacons={len(map)}  scanners={len(sloc)}")
                    break

        found.reverse()
        print(found)
        for x in found:
            del unknown[x]
        fixed = new
        if not found:
            break

    c = 0
    for s in sloc:
        c+=1
        print(f"{c}: {s}")
    dist = []
    for i in range(len(sloc)-1):
        for j in range(i+1,len(sloc)):
            dist.append((manhattan(sloc[i], sloc[j]), sloc[i], sloc[j]))
    print("  ", max(dist))

    return len(map)


def part2(input):
    pass


from aocd import data
runAll(sample, data, parse, part1, part2, answer1, answer2)
