#!/bin/python3

from core.skel import *

sample = """
on x=10..12,y=10..12,z=10..12
on x=11..11,y=11..11,z=11..11
    on x=9..9,y=9..9,z=9..9
"""

sample = """
    on x=10..12,y=10..12,z=10..12
    on x=11..13,y=11..13,z=11..13
    off x=9..11,y=9..11,z=9..11
    on x=10..10,y=10..10,z=10..10
"""

sample="""
    on x=-20..26,y=-36..17,z=-47..7
    on x=-20..33,y=-21..23,z=-26..28
    on x=-22..28,y=-29..23,z=-38..16
    on x=-46..7,y=-6..46,z=-50..-1
    on x=-49..1,y=-3..46,z=-24..28
    on x=2..47,y=-22..22,z=-23..27
    on x=-27..23,y=-28..26,z=-21..29
    on x=-39..5,y=-6..47,z=-3..44
    on x=-30..21,y=-8..43,z=-13..34
    on x=-22..26,y=-27..20,z=-29..19
    off x=-48..-32,y=26..41,z=-47..-37
    on x=-12..35,y=6..50,z=-50..-2
    off x=-48..-32,y=-32..-16,z=-15..-5
    on x=-18..26,y=-33..15,z=-7..46
    off x=-40..-22,y=-38..-28,z=23..41
    on x=-16..35,y=-41..10,z=-47..6
    off x=-32..-23,y=11..30,z=-14..3
    on x=-49..-5,y=-3..45,z=-29..18
    off x=18..30,y=-20..-8,z=-3..13
    on x=-41..9,y=-7..43,z=-33..15
    on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
    on x=967..23432,y=45373..81175,z=27513..53682"""

sample2="""
    on x=-5..47,y=-31..22,z=-19..33
    on x=-44..5,y=-27..21,z=-14..35
    on x=-49..-1,y=-11..42,z=-10..38
    on x=-20..34,y=-40..6,z=-44..1
    off x=26..39,y=40..50,z=-2..11
    on x=-41..5,y=-41..6,z=-36..8
    off x=-43..-33,y=-45..-28,z=7..25
    on x=-33..15,y=-32..19,z=-34..11
    off x=35..47,y=-46..-34,z=-11..5
    on x=-14..36,y=-6..44,z=-16..29
    on x=-57795..-6158,y=29564..72030,z=20435..90618
    on x=36731..105352,y=-21140..28532,z=16094..90401
    on x=30999..107136,y=-53464..15513,z=8553..71215
    on x=13528..83982,y=-99403..-27377,z=-24141..23996
    on x=-72682..-12347,y=18159..111354,z=7391..80950
    on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
    on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
    on x=-52752..22273,y=-49450..9096,z=54442..119054
    on x=-29982..40483,y=-108474..-28371,z=-24328..38471
    on x=-4958..62750,y=40422..118853,z=-7672..65583
    on x=55694..108686,y=-43367..46958,z=-26781..48729
    on x=-98497..-18186,y=-63569..3412,z=1232..88485
    on x=-726..56291,y=-62629..13224,z=18033..85226
    on x=-110886..-34664,y=-81338..-8658,z=8914..63723
    on x=-55829..24974,y=-16897..54165,z=-121762..-28058
    on x=-65152..-11147,y=22489..91432,z=-58782..1780
    on x=-120100..-32970,y=-46592..27473,z=-11695..61039
    on x=-18631..37533,y=-124565..-50804,z=-35667..28308
    on x=-57817..18248,y=49321..117703,z=5745..55881
    on x=14781..98692,y=-1341..70827,z=15753..70151
    on x=-34419..55919,y=-19626..40991,z=39015..114138
    on x=-60785..11593,y=-56135..2999,z=-95368..-26915
    on x=-32178..58085,y=17647..101866,z=-91405..-8878
    on x=-53655..12091,y=50097..105568,z=-75335..-4862
    on x=-111166..-40997,y=-71714..2688,z=5609..50954
    on x=-16602..70118,y=-98693..-44401,z=5197..76897
    on x=16383..101554,y=4615..83635,z=-44907..18747
    off x=-95822..-15171,y=-19987..48940,z=10804..104439
    on x=-89813..-14614,y=16069..88491,z=-3297..45228
    on x=41075..99376,y=-20427..49978,z=-52012..13762
    on x=-21330..50085,y=-17944..62733,z=-112280..-30197
    on x=-16478..35915,y=36008..118594,z=-7885..47086
    off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
    off x=2032..69770,y=-71013..4824,z=7471..94418
    on x=43670..120875,y=-42068..12382,z=-24787..38892
    off x=37514..111226,y=-45862..25743,z=-16714..54663
    off x=25699..97951,y=-30668..59918,z=-15349..69697
    off x=-44271..17935,y=-9516..60759,z=49131..112598
    on x=-61695..-5813,y=40978..94975,z=8655..80240
    off x=-101086..-9439,y=-7088..67543,z=33935..83858
    off x=18020..114017,y=-48931..32606,z=21474..89843
    off x=-77139..10506,y=-89994..-18797,z=-80..59318
    off x=8476..79288,y=-75520..11602,z=-96624..-24783
    on x=-47488..-1262,y=24338..100707,z=16292..72967
    off x=-84341..13987,y=2429..92914,z=-90671..-1318
    off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
    off x=-27365..46395,y=31009..98017,z=15428..76570
    off x=-70369..-16548,y=22648..78696,z=-1892..86821
    on x=-53470..21291,y=-120233..-33476,z=-44150..38147
    off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
    """
answer1 = None
answer2 = None

def parse(input):
    lines = [parse_fields(x,digits+alpha+'-') for x in input.splitlines() if x]
    return lines

def part1(input, part2=False):
    cells = set()

    for row in input:
        cmd,_,x0,x1,_,y0,y1,_,z0,z1 = row
        x0=int(x0)
        y0=int(y0)
        z0=int(z0)
        x1=int(x1)
        y1=int(y1)
        z1=int(z1)
        on = cmd == 'on'
        x0,x1 = sorted([x0,x1])
        y0,y1 = sorted([y0,y1])
        z0,z1 = sorted([z0,z1])

        if x1 < -50 or x0 > 50: continue
        if y1 < -50 or y0 > 50: continue
        if z1 < -50 or z0 > 50: continue
        x0 = max(x0,-50)
        y0 = max(y0,-50)
        z0 = max(z0,-50)
        x1 = min(x1,50)
        y1 = min(y1,50)
        z1 = min(z1,50)

        # print([cmd,x0,x1,y0,y1,z0,z1])
        for x in range(x0,x1+1):
            for y in range(y0,y1+1):
                for z in range(z0,z1+1):
                    if on:
                        cells.add((x,y,z))
                    else:
                        if (x,y,z) in cells:
                            cells.remove((x,y,z))
        sz = (x1-x0+1)*(y1-y0+1)*(z1-z0+1)
        print(row, len(cells), sz)
    return len(cells)


def overlap_segment(a0,a1,b0,b1):
    if a1 < b0 or a0 > b1:
        return []
    return sorted([a0,a1,b0,b1])[1:3]


def overlap(cube1, cube2):
    xsplit = overlap_segment(*cube1[0:2], *cube2[0:2])
    ysplit = overlap_segment(*cube1[2:4], *cube2[2:4])
    zsplit = overlap_segment(*cube1[4:6], *cube2[4:6])

    if xsplit and ysplit and zsplit:
        print("Cubes overlap", cube1, cube2, xsplit, ysplit, zsplit)
        return True

    return False

def inside(cube1, cube2):
    xa0,xa1,ya0,ya1,za0,za1 = cube1
    xb0,xb1,yb0,yb1,zb0,zb1 = cube2

    return xa0 >= xb0 and xa1 <= xb1 and ya0 >= yb0 and ya1 <= yb1 and za0 >= zb0 and za1 <= zb1


def cube_size(cube):
    x0,x1,y0,y1,z0,z1 = cube
    return (x1-x0+1) * (y1-y0+1) * (z1-z0+1)

# Split cube at cx; leave cx in 2nd cube
def cleave_x(cube, cx):
    x0,x1,y0,y1,z0,z1 = cube
    cubes = set()
    if x1 < cx or x0 > cx:
        return set([cube])

    cubes.add((x0,cx-1,y0,y1,z0,z1))
    cubes.add((cx,x1,y0,y1,z0,z1))
    return cubes

# Split cube at cy; leave cy in 2nd cube
def cleave_y(cube, cy):
    x0,x1,y0,y1,z0,z1 = cube
    cubes = set()
    if y1 < cy or y0 > cy:
        return set([cube])

    cubes.add((x0,x1,y0,cy-1,z0,z1))
    cubes.add((x0,x1,cy,y1,z0,z1))
    return cubes

# Split cube at cz; leave cz in 2nd cube
def cleave_z(cube, cz):
    x0,x1,y0,y1,z0,z1 = cube
    cubes = set()
    if z1 < cz or z0 > cz:
        return set([cube])

    cubes.add((x0,x1,y0,y1,z0,cz-1))
    cubes.add((x0,x1,y0,y1,cz,z1))
    return cubes

# Split cube at x, y and z
def cleave(cube, x, y, z):
    cubes = cleave_x(cube, x)
    c2 = set()
    for c in cubes:
        c2 |= cleave_y(c, y)
    c3 = set()
    for c in c2:
        c3 |= cleave_z(c, z)
    return c3

# returns a set of cubes that define the up-to-8 cubes that do not intersect cube2 and the one that does
def intersect(cube1, cube2):
    xa0,ya0,za0,xa1,ya1,za1 = cube1
    xb0,yb0,zb0,xb1,yb1,zb1 = cube2

    xsplit = overlap_segment(*cube1[0:2], *cube2[0:2])
    if xsplit:
        ysplit = overlap_segment(*cube1[2:4], *cube2[2:4])
        if ysplit:
            zsplit = overlap_segment(*cube1[4:6], *cube2[4:6])
            if zsplit:
                tcubes1 = cleave(cube1, xsplit[0], ysplit[0], zsplit[0])
                cubes1 = set()
                for c in tcubes1:
                    cubes1 |= cleave(c, xsplit[1], ysplit[1], zsplit[1])

                tcubes2 = cleave(cube2, xsplit[0], ysplit[0], zsplit[0])
                cubes2 = set()
                for c in tcubes2:
                    cubes2 |= cleave(c, xsplit[1], ysplit[1], zsplit[1])

                return (cubes1, cubes2)

    return (set([cube1]), set([cube2]))

# If cubes don't intersect, return None
# else return {cube1 - cube2}
def remove_cube(cube1, cube2):
    if inside(cube1, cube2):
        return set()
    elif inside(cube2, cube1):
        return set([cube1])

    c1, c2 = intersect(cube1, cube2)
    # print(f"  c1: {sum([cube_size(x) for x in c1])} {c1}")
    # print(f"  c2: {sum([cube_size(x) for x in c2])} {c2}")
    if len(c1)==1 and len(c2)==1 and c1 != c2:
        # No overlap
        return None

    return c1 - c2


# If cubes don't intersect, return None
# else return {cube1 + (cube2 - cube1)}
def add_cube(cube1, cube2):
    if inside(cube1, cube2):
        return set([cube2])
    elif inside(cube2, cube1):
        return set([cube1])

    c1, c2 = intersect(cube1, cube2)
    # print(f"  c1: {sum([cube_size(x) for x in c1])} {c1}")
    # print(f"  c2: {sum([cube_size(x) for x in c2])} {c2}")
    if len(c1)==1 and len(c2)==1 and c1 != c2:
        # No overlap
        return None
    # ans = set([cube1])
    # for c in c2:
    #     if not inside(c, cube1):
    #         ans.add(c)
    # return ans
    return c1 | c2

# def add_cuboid(cuboids, cube):
#     add = set()
#     remove = set()
#     for c in cuboids:
#         c1 = add(c, cube)
#         if c1 is None:
#             continue

#         # Cubes overlap
#         remove.add(c)
#         add |= c1
#     if not remove:
#         # There was no overlap
#         cuboids.add(cube)
#     else:
#         # FIXME: We may overlap with more than one original cube. In that case, we will add duplicate
#         # regions for our "add". How do we weed out duplicates? Do I have to cross-add every cube with each other?
#         for cc in remove:
#             cuboids.remove(cc)
#         for cc in add:
#             cuboids.add(cc)

# def remove_cuboid(cuboids, cube):
#     add = set()
#     remove = set()
#     for c in cuboids:
#         c1 = remove(c, cube)
#         if c1 is None:
#             continue

#         # Cubes overlap
#         remove.add(c)
#         add |= c1
#     for cc in remove:
#         cuboids.remove(cc)
#     for cc in add:
#         cuboids.add(cc)

def dupes(cubes):
    for x in range(9,14):
        for y in range(9,14):
            for z in range(9,14):
                testcube = (x,x,y,y,z,z)
                dups = [cube for cube in cubes if inside(testcube, cube) ]
                if len(dups) > 1:
                    print(f"overlap here {testcube}:    {dups}")

def diff(cubes1, cubes2):
    for x in range(9,14):
        for y in range(9,14):
            for z in range(9,14):
                testcube = (x,x,y,y,z,z)
                any1 = not not [cube for cube in cubes1 if inside(testcube, cube) ]
                any2 = not not [cube for cube in cubes2 if inside(testcube, cube) ]
                if any1 != any2:
                    print(f"missing cube {testcube}:")
                    for c in sorted(list(cubes1)):
                        print(f"   {cube_size(c)}  {c}")
                    print("---")
                    for c in sorted(list(cubes2)):
                        print(f"   {cube_size(c)}  {c}")
                    return True
    return False

def total_size(cubes):
    return sum([cube_size(x) for x in cubes])

def part2(input):
    cuboids = set()

    # prev = (0,0,0,0,0,0)

    for row in input:
        cmd,_,x0,x1,_,y0,y1,_,z0,z1 = row
        x0=int(x0)
        y0=int(y0)
        z0=int(z0)
        x1=int(x1)
        y1=int(y1)
        z1=int(z1)
        x0,x1 = sorted([x0,x1])
        y0,y1 = sorted([y0,y1])
        z0,z1 = sorted([z0,z1])

        cube = (x0,x1,y0,y1,z0,z1)

        add = set()
        remove = set()
        for c in cuboids:
            if cmd == 'on':
                c1 = add_cube(c, cube)
            else:
                c1 = remove_cube(c, cube)

            if c1 is None:
                continue

            # Cubes overlap
            remove.add(c)
            add |= c1
        if not remove and cmd == 'on':
            # There was no overlap; add the virgin cube
            cuboids.add(cube)
        else:
            for cc in remove:
                cuboids.remove(cc)

            # We may overlap with more than one original cube. In that case, we will add duplicate regions for our
            # "add". How do we weed out duplicates? Do I have to cross-add every cube with each other before I add them?
            while True:
                # print("Loop:",len(add), total_size(add))
                # dupes(add)
                newadd = set()
                ADD = list(add)
                for A in range(len(ADD)):
                    newadd_b = set()
                    a = ADD[A]
                    for B in range(A+1,len(ADD)):
                        b = ADD[B]
                        c1 = add_cube(a,b)
                        if c1 is None:
                            continue

                        newadd_b |= c1
                    if newadd_b:
                        newadd |= newadd_b
                    else:
                        # print(f"No overlap: {cube_size(a)}  {a}")
                        newadd.add(a)
                assert not diff(add, newadd)
                print(total_size(add))
                print(total_size(newadd))
                diff(add, newadd)
                if frozenset(add) == frozenset(newadd):
                    break
                if total_size(add) == total_size(newadd):
                    break
                add = newadd

            for cc in add:
                cuboids.add(cc)

        # XXX
        # dupes(cuboids)

        # c1,c2 = intersect(cube, prev)
        # print(row, len(c1), len(c2))
        # assert cube_size(cube) == sum([cube_size(x) for x in c1])
        # prev = cube
        print(row, f"Num cubes={len(cuboids)}, Total size={sum([cube_size(x) for x in cuboids])}")

    return sum([cube_size(x) for x in cuboids])

from aocd import data
data=""
runAll(sample, data, parse, part1, part2, answer1, answer2)