#! /usr/bin/env python
from __future__ import print_function
from golfr.find_grid_points.filter_points import group_points

from os import listdir
from os.path import abspath, basename, join
import sys, traceback
import pandas as pd
import cv2


def test_filter_points():
    data_dir = 'filter_pnts_data/'
    df = pd.read_csv(join(data_dir, 'pnts_unfiltered.csv'), index_col=False)
    centroids = df.values#.tolist()

    hori_lines = cv2.imread(join(data_dir, 'hori_lines.jpg'), 1)
    vert_lines = cv2.imread(join(data_dir, 'vert_lines.jpg'), 1)
    
    try:
        group_points(centroids, vert_lines, hori_lines)
    except:
        print('Exception: couldn\'t group points')
        print ('-'*60)
        traceback.print_exc(file=sys.stdout)
        print ('-'*60)
        print('test FAILED')
        return
    print('test not necessarily failed')
    return True
if __name__ == '__main__':
    test_filter_points()