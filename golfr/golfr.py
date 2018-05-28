#! /usr/bin/env python
# I will take this stackoverflow page to my very grave
#http://stackoverflow.com/questions/10196198/how-to-remove-convexity-defects-in-a-sudoku-square
TEST_IMG_DIR = 'test_imgs'
PIPE_OUTPUT_DIR = 'pipe_output'

if len(sys.argv) == 1:
    main(TEST_IMG_DIR+'/1.jpg')
else:
    for in_fname in sys.argv[1:]:
        main(in_fname)
########################################
### hough
'''

gray = cv2.cvtColor(thresh2,cv2.COLOR_BGR2GRAY)

edges = cv2.bitwise_not(th3)

minLineLength = 200
maxLineGap = 2
lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap)
for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite('hough.png',img)
'''
