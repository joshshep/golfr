import cv2
import numpy as np
import keras
from keras.utils import plot_model
from keras.models import Sequential, load_model
from keras.datasets import mnist
from keras import backend as K

model = load_model('handwriting_classifier_cnn_linearsoftmax_989perc.model')


# input image dimensions
img_rows, img_cols = 28, 28

(x_train, y_train), (x_test, y_test) = mnist.load_data()


#the data, shuffled and split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_train /= 255
print 'x_train shape:', x_train.shape
good_x = np.expand_dims(x_train[0],0)
print 'expanded x_train[0] shape:', good_x.shape


for j in range(28):
    for i in range(28):
        #print np.array_repr(img.reshape(28,28)[i]).replace('\n','')
        print '{:>4}'.format(int(255*good_x.reshape(28,28)[j][i])),
    print

res = model.predict(good_x)
print res
print(np.argmax(res))