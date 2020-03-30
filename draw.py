from display import *
from matrix import *
from math import *

def add_polygon( points, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    #just ad all 3 of the points
    add_point(points, x0, y0, z0)
    add_point(points, x1, y1, z1)
    add_point(points, x2, y2, z2)

def draw_polygons( matrix, screen, color ):
    counter = 0
    #loop throuh matrix vectors 3 at a time
    while counter < len(matrix)-1:
        v0 = matrix[counter]
        v1 = matrix[counter+1]
        v2 = matrix[counter+2]
        V1 = [(v1[0] - v0[0]), (v1[1] - v0[1]), (v1[2] - v0[2])]
        V2 = [(v2[0] - v0[0]), (v2[1] - v0[1]), (v2[2] - v0[2])]
        M = cross_product(V1, V2)
        #gotta make sure you got atleast 3 points in the matrix
        if M[2] > 0:
            draw_line(int(v0[0]), int(v0[1]), int(v1[0]), int(v1[1]), screen, color)
            draw_line(int(v1[0]), int(v1[1]), int(v2[0]),int(v2[1]), screen, color)
            draw_line(int(v2[0]),int(v2[1]),int(v0[0]),int(v0[1]),screen, color)
        counter += 3


def add_box( points, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(points,x,y,z,x,y1,z,x1,y1,z)
    add_polygon(points,x1,y,z,x,y,z,x1,y1,z)
    #back
    add_polygon(points,x1,y,z1,x1,y1,z1,x,y1,z1)
    add_polygon(points,x,y,z1,x1,y,z1,x,y1,z1)
    #top
    add_polygon(points,x,y,z1,x,y,z,x1,y,z)
    add_polygon(points,x1,y,z1,x,y,z1,x1,y,z)
    #bottom
    add_polygon(points,x,y1,z,x,y1,z1,x1,y1,z1)
    add_polygon(points,x1,y1,z,x,y1,z,x1,y1,z1)
    #left
    add_polygon(points,x,y,z1,x,y1,z1,x,y1,z)
    add_polygon(points,x,y,z,x,y,z1,x,y1,z)
    #right
    add_polygon(points,x1,y,z,x1,y1,z,x1,y1,z1)
    add_polygon(points,x1,y,z1,x1,y,z,x1,y1,z1)

def add_sphere( edges, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step
    curr = 0
    next = 0

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):
            curr = (lat * step) + longt
            if lat == step - 2:
                next = longt
            else:
                next = curr + step
            if longt == 0:
                add_polygon(edges, points[curr][0], points[curr][1], points[curr][2], points[curr + 1][0], points[curr + 1][1], points[curr + 1][2], points[next+1][0], points[next+1][1], points[next+1][2])
            elif longt == step-2:
                add_polygon(edges, points[curr][0], points[curr][1], points[curr][2], points[curr + 1][0], points[curr + 1][1], points[curr + 1][2], points[next][0], points[next][1], points[next][2])
            else:
                add_polygon(edges, points[curr][0], points[curr][1], points[curr][2], points[curr + 1][0], points[curr + 1][1], points[curr + 1][2], points[next][0], points[next][1], points[next][2])
                add_polygon(edges, points[next][0], points[next][1], points[next][2], points[curr + 1][0], points[curr + 1][1], points[curr + 1][2], points[next+1][0], points[next+1][1], points[next+1][2])


def generate_sphere( cx, cy, cz, r, step ):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus( edges, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):
            curr = (lat*step) + longt
            if lat == lat_stop - 1:
                next = longt
            else:
                next = curr + step
            if not longt == longt_stop - 1:
                add_polygon(edges, points[curr][0], points[curr][1], points[curr][2], points[next][0], points[next][1], points[next][2], points[next+1][0], points[next+1][1], points[next+1][2])
                add_polygon(edges, points[next+1][0], points[next+1][1], points[next+1][2], points[curr + 1][0], points[curr + 1][1], points[curr + 1][2], points[curr][0], points[curr][1], points[curr][2])
            else:
                if lat == lat_stop - 1:
                    extreme = 0
                else:
                    extreme = curr + step - longt
                add_polygon(edges, points[curr][0], points[curr][1], points[curr][2], points[next][0], points[next][1], points[next][2], points[extreme][0], points[extreme][1], points[extreme][2])
                add_polygon(edges, points[extreme][0], points[extreme][1], points[extreme][2], points[curr - longt][0], points[curr - longt][1], points[curr - longt][2], points[curr][0], points[curr][1], points[curr][2])


def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points

def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1
    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
