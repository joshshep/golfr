#! /usr/bin/env python
from __future__ import print_function
from golfr.classify_cells.classify_sample import classify_digit

from os import listdir
from os.path import abspath, basename, join
import sys, traceback

def test_classify_cells():
    sample_digits_path = '../imgs/sample_digits'

    fnames = [join(sample_digits_path, f) for f in listdir(sample_digits_path)]
    print (fnames)
    num_correct = 0
    for fname in fnames:
        #extract the correct digit from the filename
        cor_digit = int(basename(fname)[0])
        try:
            #run the CNN on the sample image
            est_digit = classify_digit(fname)
        except Exception as e:
            print('Exception: couldn\'t classify {}'.format(fname))
            print ('-'*60)
            traceback.print_exc(file=sys.stdout)
            print ('-'*60)
            continue
        if est_digit != cor_digit:
            print('Incorrect result classifying {}: {} (correct={})'.format(fname, est_digit, cor_digit))
        else:
            num_correct += 1
    if num_correct != len(fnames):
        print('test FAILED')
    else:
        print('test PASSED')
    print('{}/{} digits correctly classified'.format(num_correct, len(fnames)))
    return True
if __name__ == '__main__':
    test_classify_cells()