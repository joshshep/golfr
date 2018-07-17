#! /usr/bin/env python
from __future__ import print_function

import cv2
import numpy as np
import struct
import pandas as pd
import random
from os.path import join
from golfr.definitions import ROOT_DIR
'''

Given a bunch of points, we want to be able to 
    - filter out extraneous points
    - fill in missed points
    - identify a logical grid by grouping sqaures of points e.g.
        +----+----+----+----+----+----+-----------------
        |  0 |  1 |  2 |  3 |  4 |  5 | etc ...
        +----+----+----+----+----+----+-----------------
        |  6 |  7 |  8 |  9 | 10 | 11 | etc ...
        +----+----+----+----+----+----+-----------------
        |  etc...
    
'''

def num_2_hextup(num):
    return (
        (num >> 16) & 0xff,
        (num >>  8) & 0xff,
         num        & 0xff
    )
def arr_2_hexstr(arr):
    return '{:02X}{:02X}{:02X}'.format(arr[0], arr[1], arr[2])
def num_2_hexstr(num):
    return arr_2_hexstr(num_2_hextup(num))
def get_distinct_colors():
    '''distinct_colors = [
        0xFFB300,    # Vivid Yellow
        0x803E75,    # Strong Purple
        0xFF6800,    # Vivid Orange
        0xA6BDD7,    # Very Light Blue
        0xC10020,    # Vivid Red
        0xCEA262,    # Grayish Yellow
        0x817066,    # Medium Gray

        0x007D34,    # Vivid Green
        0xF6768E,    # Strong Purplish Pink
        0x00538A,    # Strong Blue
        0xFF7A5C,    # Strong Yellowish Pink
        0x53377A,    # Strong Violet
        0xFF8E00,    # Vivid Orange Yellow
        0xB32851,    # Strong Purplish Red
        0xF4C800,    # Vivid Greenish Yellow
        0x7F180D,    # Strong Reddish Brown
        0x93AA00,    # Vivid Yellowish Green
        0x593315,    # Deep Yellowish Brown
        0xF13A13,    # Vivid Reddish Orange
        0x232C16     # Dark Olive Green
    ]'''
    #TODO: how do I reference a (non-python) file that's in a submodule?
    # I think it should stay in the package but specifying the directory explicitly
    # probably isn't the solution
    df = pd.read_csv(join(ROOT_DIR,'find_grid_points/crayola120colors.txt'), sep='\t', skiprows=[0],  index_col=False)
    
    #print(df.values[:, 1:4])
    return df.values[:, 1:4]
def get_on_pixel_in_region(pnt, img, fill_radius=3):
    if np.any(img[pnt[1], pnt[0]]):
        return tuple(pnt)
    
    #the centroid doesn't lie on a fillable area
    #so let's check the region around
    #TODO: fill_radius will *not* need to be so high (hopefully it  would equal 0)
    # when vertical_lines isn't the outer-most contours
    h, w = img.shape[:2]
    
    # note: ideally we'd work inside out
    bbox_range_x = range(
        max(pnt[0] - fill_radius, 0),
        min(pnt[0] + fill_radius + 1, w)
    )
    bbox_range_y = range(
        max(pnt[1] - fill_radius, 0),
        min(pnt[1] + fill_radius + 1, h)
    )
    for y in bbox_range_y:
        for x in bbox_range_x:
            #print('img[{:04d},{:04d}] == {}'.format(x,y,img[y,x]))
            if np.any(img[y, x]): # NOT black
                return x, y
    return
def group_points(pnts, vertical_lines, horizontal_lines):
    #print('vertical_lines shape: {}'.format(vertical_lines.shape))
    
    # maxval, thresh
    #floodx = vertical_lines.copy() #cv2.cvtColor(vertical_lines, cv2.COLOR_GRAY2RGB)
    distinct_colors = get_distinct_colors()
    distinct_colors_remain = [(int(c[0]), int(c[1]), int(c[2])) for c in distinct_colors.tolist()]
    random.shuffle(distinct_colors_remain)
    #print(distinct_colors_remain)
    
    #h, w, chs = floodx.shape
    h, w = vertical_lines.shape[:2]
    mask = np.zeros((h+2,w+2), np.uint8)
    _, floody = cv2.threshold(vertical_lines, 127, 255, cv2.THRESH_BINARY)
    i = 0
    lines = {}
    FILL_RADIUS = 7
    CIRCLE_RADIUS = 20
    for pnt in pnts:
        flood_origin = get_on_pixel_in_region(pnt, floody, fill_radius=FILL_RADIUS)
        if not flood_origin:
            raise Exception('couldn\'t find an ON pixel near the centroid (x,y)==({},{})'.format(pnt[0],pnt[1]))
        
        pix_color = floody[flood_origin[1],flood_origin[0]]
        #print ('color to fill: {}'.format(pix_color))
        
        #get string
        hexstr = arr_2_hexstr(pix_color)
        if hexstr in lines: #no need to floodfill, we already have
            lines[hexstr].append(pnt)
            #print('pix_color: {}'.format(clean_color))
            
            # TODO: why do I need this list-comprehension?
            # I got "pix_color" from the floody numpy ndarr
            #DEBUG: draw indicator circle
            cv2.circle(floody, tuple(pnt), CIRCLE_RADIUS, [int(x) for x in pix_color])
        else: #flood a new color
            if len(distinct_colors_remain) <= 0:
                #raise Warning('not enough unique colors')
                raise Exception('not enough unique colors ({})'.format(
                     len(lines)))
            
            col_tup = distinct_colors_remain.pop() #num_2_hextup(distinct_colors[len(lines)%len(distinct_colors)])
            cv2.floodFill(floody, mask, flood_origin, col_tup)
            hexstr = arr_2_hexstr(col_tup)
            #add the color to the lines
            lines[hexstr] = [pnt]
            
            #DEBUG: draw indicator circle
            cv2.circle(floody, tuple(pnt), CIRCLE_RADIUS, col_tup)
            
        
        i += 1

    for color in lines:
        print('color: 0x{}'.format(color))
        for pnt in lines[color]:
            print('  x,y:  {:04d}, {:04d}'.format(pnt[0],pnt[1]))
    print('num lines: {}'.format(len(lines)))
    print('{} unique colors remaining ({:.2f}%)'.format(len(distinct_colors_remain),100.0*len(distinct_colors_remain)/distinct_colors.shape[0]))
    cv2.imwrite('floody.jpg', floody)
    #floody[np.array_equal(floody, np.ndarray([255,255,255]))] = np.ndarray([0,0,0])
    #print (np.where( np.array_equal(floody, np.ndarray([255,255,255])) ))
    #https://stackoverflow.com/a/25823710


















