#! /usr/bin/env python
from __future__ import print_function
from golfr.find_grid_points.find_grid_points import find_grid_points
import sys, traceback


def test_find_grid_points():
    fname = '../imgs/golfr_test_imgs/ex0.jpg'
    try:
        find_grid_points(fname)
    except:
        print('Exception: in finding grid points of {}'.format(fname))
        print ('-'*60)
        traceback.print_exc(file=sys.stdout)
        print ('-'*60)

if __name__ == '__main__':
    test_find_grid_points()
