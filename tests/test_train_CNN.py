#! /usr/bin/env python
from __future__ import print_function
from golfr.train_CNN.mnist_cnn import gen_digit_classifier

import sys, traceback

def test_train_CNN():
    try:
        gen_digit_classifier(epochs=50)
    except:
        print('Exception: generate digit classifier')
        print ('-'*60)
        traceback.print_exc(file=sys.stdout)
        print ('-'*60)
        print('test FAILED')
        return False
    print('test PASSED')
    return True

if __name__ == '__main__':
    test_train_CNN()