#!/bin/python3

from core.skel import *

def parse(input):
    lines = [parse_fields(x,digits+alpha+'-') for x in input.splitlines() if x]

    instructions = []
    for row in lines:
        if not row:
            continue
        cmd,_,x0,x1,_,y0,y1,_,z0,z1 = row
        x0,x1 = sorted([int(x0),int(x1)])
        y0,y1 = sorted([int(y0),int(y1)])
        z0,z1 = sorted([int(z0),int(z1)])

        cube = (x0,x1,y0,y1,z0,z1)

        instructions.append((cmd == 'on', cube))

    return instructions

def part1(input, part2=False):
    cells = set()

    for row in input:
        on, cube = row

        x0,x1,y0,y1,z0,z1 = cube

        if x1 < -50 or x0 > 50: continue
        if y1 < -50 or y0 > 50: continue
        if z1 < -50 or z0 > 50: continue

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


# Return the endpoints where two 1-dimensional line segments overlap, or [] if they don't
#        a0         a1
# --------===========
#             *     *
# ------------===========
#            b0         b1
def overlap_segment(a0,a1,b0,b1):
    if a1 < b0 or a0 > b1:
        return []
    # given four endpoints, the overlap points of the two segments are the middle two points when sorted
    return sorted([a0,a1,b0,b1])[1:3]

def cube_size(cube):
    x0,x1,y0,y1,z0,z1 = cube
    return (x1-x0+1) * (y1-y0+1) * (z1-z0+1)

# Split cube at cx; leave cx in 2nd cube
def cleave_x(cube, cx):
    x0,x1,y0,y1,z0,z1 = cube
    if x1 < cx or x0 > cx:
        return set([cube])

    cubes = set()
    if x0 < cx:
        cubes.add((x0,cx-1,y0,y1,z0,z1))
    cubes.add((cx,x1,y0,y1,z0,z1))
    return cubes

# Split cube at cy; leave cy in 2nd cube
def cleave_y(cube, cy):
    x0,x1,y0,y1,z0,z1 = cube
    if y1 < cy or y0 > cy:
        return set([cube])

    cubes = set()
    if y0 < cy:
        cubes.add((x0,x1,y0,cy-1,z0,z1))
    cubes.add((x0,x1,cy,y1,z0,z1))
    return cubes

# Split cube at cz; leave cz in 2nd cube
def cleave_z(cube, cz):
    x0,x1,y0,y1,z0,z1 = cube
    if z1 < cz or z0 > cz:
        return set([cube])

    cubes = set()
    if z0 < cz:
        cubes.add((x0,x1,y0,y1,z0,cz-1))
    cubes.add((x0,x1,y0,y1,cz,z1))
    return cubes

# Split cube at x, y and z
def cleave_1point(cube, x, y, z):
    x_cleaved = cleave_x(cube, x)
    xy_cleaved = set()
    for c in x_cleaved:
        xy_cleaved |= cleave_y(c, y)
    xyz_cleaved = set()
    for c in xy_cleaved:
        xyz_cleaved |= cleave_z(c, z)
    return xyz_cleaved

def cleave_2points(cube, p1, p2):
    temp = cleave_1point(cube, *p1)
    ans = set()
    # Cleave all resulting subcubes at point 2
    for c in temp:
        ans |= cleave_1point(c, *p2)
    return ans

# returns a pair of sets of cubes that define the sliced-up cubes from cube1 and from cube2
def intersect(cube1, cube2):
    xsplit = overlap_segment(*cube1[0:2], *cube2[0:2])
    if xsplit:
        ysplit = overlap_segment(*cube1[2:4], *cube2[2:4])
        if ysplit:
            zsplit = overlap_segment(*cube1[4:6], *cube2[4:6])
            if zsplit:
                # Cleave two cubes at the two opposite points where the cubes intersect
                point1 = (xsplit[0], ysplit[0], zsplit[0])
                point2 = (xsplit[1]+1, ysplit[1]+1, zsplit[1]+1)

                cubes1 = cleave_2points(cube1, point1, point2)
                cubes2 = cleave_2points(cube2, point1, point2)

                return (cubes1, cubes2)

    return (set([cube1]), set([cube2]))

# If cubes don't intersect, return None
# else return {cube1 - cube2}
def remove_cube(cube1, cube2):
    c1, c2 = intersect(cube1, cube2)
    if len(c1)==1 and len(c2)==1 and c1 != c2:
        # No overlap
        return None

    return c1 - c2

def remove_from_cuboids(cuboids, cube):
    add = set()
    remove = set()
    ## Remove cube
    for c in cuboids:
        c1 = remove_cube(c, cube)
        if c1 is None:
            continue

        # Cubes overlap
        remove.add(c)
        add |= c1

    cuboids -= remove
    cuboids |= add
    return cuboids

def part2(input):
    total = 0
    for a,add in enumerate(input):
        keep, cube = add
        print(f"{a+1}. {' on' if keep else 'off'} {cube}")
        if not keep:
            continue
        univ = frozenset([cube])
        for sub in input[a+1:]:
            univ = remove_from_cuboids(univ, sub[1])
        size = sum([cube_size(x) for x in univ])
        total += size
    return total #sum([cube_size(x) for x in cubes])

from aocd import data
runAll('', data, parse, part1, part2, None, None)