#! /usr/bin/env python

import sys
import cv2
import os
from ...definitions import ROOT_DIR

DEBUG_OUTPUT_DIR = os.path.join(ROOT_DIR, 'debug/inter_imgs')
#TEST_IMG_DIR = os.path.join(ROOT_DIR, 'pipe_output')

def _imwrite(fname,nimg):
    if not __debug__:
        return

    #TODO: is there a better way to have a static variable?
    try:
        imwrite.i += 1
    except AttributeError:
        if __debug__:
            ensure_path_exists(DEBUG_OUTPUT_DIR)
        imwrite.i = 0
    complete_fname = os.path.join(DEBUG_OUTPUT_DIR, '_'+str(imwrite.i).zfill(2)+'_'+fname)
    print 'writing \''+complete_fname+'\'...'
    cv2.imwrite(complete_fname,img)

'''
Parameter: in_fname: a string representing a path to an image
returns: a list of tuples (x,y) representing the points of the grid corners
'''
def find_grid_points(in_fname):
    import numpy as np

    img = cv2.imread(in_fname)
    imwrite("orig.jpg", img)
    orig_img = img.copy()
    #blur
    img = cv2.GaussianBlur(img,(5,5),0)

    #ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    threshWidth = 135
    th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,threshWidth,2)

    #this is the key
    # 61 -> 95 looks pretty good too (also 135)
    #th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,61,2)
    '''
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


    edges = cv2.Canny(gray,100,200,apertureSize = 3)
    '''
    #cv2.imwrite('_thresholded.jpg',thresh2)
    #invert image
    th3 = cv2.bitwise_not(th3)
    imwrite('adap_thresholded_blur.jpg',th3)


    #erosion
    kernel = np.ones((5,5),np.uint8)
    res = cv2.erode(th3,kernel,iterations = 1)
    imwrite('erosion_blur.jpg',res)

    #dilation
    kernel = np.ones((5,5),np.uint8)
    res = cv2.dilate(res,kernel,iterations = 1)
    imwrite('dilation_blur.jpg',res)

    ################################
    ## vertical lines
    kernelx = cv2.getStructuringElement(cv2.MORPH_RECT,(2,10))

    dx = cv2.Sobel(res,cv2.CV_16S,1,0)
    dx = cv2.convertScaleAbs(dx)
    cv2.normalize(dx,dx,0,255,cv2.NORM_MINMAX)
    ret,close = cv2.threshold(dx,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #cv2.imwrite("2_vertical_threshold.jpg",close)
    close = cv2.morphologyEx(close,cv2.MORPH_DILATE,kernelx,iterations = 1)
    #cv2.imwrite("225_vertical_morph.jpg",close)

    contour, hier = cv2.findContours(close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        x,y,w,h = cv2.boundingRect(cnt)
        if h/w > 10:
            cv2.drawContours(close,[cnt],0,255,-1)
        else:
            cv2.drawContours(close,[cnt],0,0,-1)
    close = cv2.morphologyEx(close,cv2.MORPH_CLOSE,None,iterations = 2)
    closex = close.copy()

    imwrite('vertical_lines_blur.jpg',closex)

    ################################
    ## horizontal lines
    kernely = cv2.getStructuringElement(cv2.MORPH_RECT,(10,2))
    #TEST
    dy = cv2.Sobel(res,cv2.CV_16S,0,2)
    #dy = cv2.Sobel(preproc_res,cv2.CV_16S,0,2)
    dy = cv2.convertScaleAbs(dy)
    cv2.normalize(dy,dy,0,255,cv2.NORM_MINMAX)
    ret,close = cv2.threshold(dy,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    close = cv2.morphologyEx(close,cv2.MORPH_DILATE,kernely,iterations=1)

    contour, hier = cv2.findContours(close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        x,y,w,h = cv2.boundingRect(cnt)
        if w/h > 10:
            cv2.drawContours(close,[cnt],0,255,-1)
        else:
            cv2.drawContours(close,[cnt],0,0,-1)

    close = cv2.morphologyEx(close,cv2.MORPH_DILATE,None,iterations = 2)
    closey = close.copy()

    imwrite('hori_lines_blur.jpg',closey)

    #############################################
    ## and hori and vert lines
    res = cv2.bitwise_and(closex,closey)
    imwrite('AND_lines.jpg',res)


    ##############################################
    #combine close points (dilation)
    kernel = np.ones((5,5),np.uint8)
    res = cv2.dilate(res,kernel,iterations = 3)
    imwrite('merge_intersections.jpg',res)


    ############################################
    ## vectorize points
    contour, hier = cv2.findContours(res,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    centroids = []
    img_points = orig_img.copy()
    for cnt in contour:
        mom = cv2.moments(cnt)
        try:
            (x,y) = int(mom['m10']/mom['m00']), int(mom['m01']/mom['m00'])
            cv2.circle(img_points,(x,y),10,(0,255,0),-1)
            centroids.append((x,y))
        except:
            pass

    imwrite('grid_points.jpg',img_points)

    return centroids
