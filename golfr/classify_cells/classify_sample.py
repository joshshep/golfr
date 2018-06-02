#! /usr/bin/env python
import cv2
import numpy as np
import keras
from keras.utils import plot_model
from keras.models import Sequential, load_model
from keras.layers import Dense


def classify_digit(digit_fname, model_fname='../digit_classifier_cnn.model')
    #####################################
    ## load model

    model = load_model(model_fname)


    plot_model(model, to_file='softmax_with.png', show_shapes=True)

    # remove the last layer so we can see the non-binary results
    print len(model.layers)
    some_weights = model.layers[-1].get_weights()
    print "some_weights[0] shape:",some_weights[0].shape
    print "some_weights[1] shape:",some_weights[1].shape
    print some_weights
    #model.pop()
    #model.add(alayer)
    #model.add(Dense(num_classes, weights=some_weights, activation='softmax', name="dense_last"))

    plot_model(model, to_file='softmax_without.png', show_shapes=True)

    print len(model.layers)

    model.outputs = [model.layers[-1].output]
    model.layers[-1].outbound_nodes = []


    ############################################
    ## load sample image
    img = cv2.imread('../test_imgs/number0_bad.jpg')
    print 'orig shape:',img.shape
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    #####################################################3
    ## clean up sample image
    cv2.imwrite('1.png',img)
    ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    img = cv2.bitwise_not(img)
    cv2.imwrite('2.png',img)

    #erosion
    kernel = np.ones((5,5),np.uint8)
    img = cv2.erode(img,kernel,iterations = 1)
    cv2.imwrite('erosion.jpg',img)

    #dilation
    kernel = np.ones((5,5),np.uint8)
    img = cv2.dilate(img,kernel,iterations = 1)
    cv2.imwrite('dilation.jpg',img)


    ######################################
    ## resize sample image to (28,28)
    contoured = img.copy()
    contours,hierarchy = cv2.findContours(contoured, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    img = img[y:y+h,x:x+w]
    print 'cropped shape:',img.shape

    cv2.imwrite('3.png',img)

    pad_top = 0
    pad_bot = 0
    pad_left = 0
    pad_right = 0
    if h > w:
        diff = h - w
        half_diff = diff/2
        pad_left += half_diff
        pad_right += diff - half_diff
    elif w > h:
        diff = w - h
        half_diff = diff/2
        pad_top += half_diff
        pad_bot += diff - half_diff

    img = cv2.copyMakeBorder(img, pad_top,pad_bot,pad_left,pad_right, cv2.BORDER_CONSTANT, value=(0))
    print 'padded shape:',img.shape
    cv2.imwrite('4.png',img)
    pad_top = 4
    pad_bot = 4
    pad_left = 4
    pad_right = 4


    img = cv2.resize(img, (20,20), interpolation = cv2.INTER_AREA)
    img = cv2.copyMakeBorder(img, pad_top,pad_bot,pad_left,pad_right, cv2.BORDER_CONSTANT, value=(0))


    cv2.imwrite('num_cor_size.png',img)
    img = img.astype('float32')
    img /= 255


    img = np.expand_dims(img, 2)
    img = np.expand_dims(img, 0)
    print 'final shape:',img.shape

    ########################################3
    ## print text version
    #img.reshape(28,28)
    for j in range(28):
        for i in range(28):
            #print np.array_repr(img.reshape(28,28)[i]).replace('\n','')
            print '{:>4}'.format(int(255*img.reshape(28,28)[j][i])),
        print
    #ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

    ##################################33
    ## run model on sample
    x = model.predict(img)
    #x = model.predict_proba(img)

    #np.set_printoptions(precision=4)
    np.set_printoptions(suppress=True)

    print x
    digit_val = np.argmax(x)
    print(digit_val)
    return digit_val
    '''
    x = x.reshape(10,1)
    print 'dot',some_weights[0].shape,'by',x.shape
    y = some_weights[0].dot(x)
    y = y.reshape(10)
    print 'some_weights[0].dot(x):',y

    asoftmax = np.multiply(y.T,some_weights[1].reshape(10))
    print 'asoftmax:',asoftmax
    print 'mult:',np.multiply(asoftmax,some_weights[1])
    '''
