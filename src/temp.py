
import tensorflow as tf

from os import listdir, remove
from os.path import isfile, join
onlyfiles = [f for f in listdir('model') if isfile(join('model', f))]
index = 0

for file in onlyfiles:
    fn = 'model/' + str(file)
    with tf.Graph().as_default():
        try:
            image_contents = tf.read_file(fn)
            image = tf.image.decode_jpeg(image_contents, channels=3)
            init_op = tf.initialize_all_tables()
            with tf.Session() as sess:
                sess.run(init_op)
                tmp = sess.run(image)
        except:
            remove('model/' + file)
            index += 1
print(index)

'''
index = 10
import cv2

img1 = cv2.imread('../data/hamza/0.jpg')
img2 = cv2.imread('../data/hamza/1.jpg')
img3 = cv2.imread('../data/hamza/2.jpg')
img4 = cv2.imread('../data/hamza/3.jpg')
img5 = cv2.imread('../data/hamza/4.jpg')
img6 = cv2.imread('../data/hamza/5.jpg')
img7 = cv2.imread('../data/hamza/6.jpg')
img8 = cv2.imread('../data/hamza/7.jpg')
img9 = cv2.imread('../data/hamza/8.jpg')
img10 = cv2.imread('../data/hamza/9.jpg')

for i in range(29):
    cv2.imwrite('../data/hamza/' + str(index) + '.jpg',img1)
    index += 1
    cv2.imwrite('../data/hamza/' + str(index) + '.jpg',img2)
    index += 1
    cv2.imwrite('../data/hamza/' + str(index) + '.jpg',img3)
    index += 1
    cv2.imwrite('../data/hamza/' + str(index) + '.jpg',img4)
    index += 1
    cv2.imwrite('../data/hamza/' + str(index) + '.jpg',img5)
    index += 1
    cv2.imwrite('../data/hamza/' + str(index) + '.jpg',img6)
    index += 1
    cv2.imwrite('../data/hamza/' + str(index) + '.jpg',img7)
    index += 1
    cv2.imwrite('../data/hamza/' + str(index) + '.jpg',img8)
    index += 1
    cv2.imwrite('../data/hamza/' + str(index) + '.jpg',img9)
    index += 1
    cv2.imwrite('../data/hamza/' + str(index) + '.jpg',img10)
    index += 1
'''

exit()



import numpy as np
import glob
import cv2
base_folder = "../data/hamza/"

hamza_label = [0]

X_data = []
Y_data = []
files = glob.glob (base_folder + "*.jpg")
print(base_folder + "hamza/resized/")
for myFile in files:
    image = cv2.imread (myFile)
    X_data.append (image)
    Y_data.append(hamza_label)
print('X_data shape:', np.array(X_data).shape)
print('Y_data shape:', np.array(Y_data).shape)

train_images = np.array(X_data)
train_labels = np.array(Y_data)
test_images = np.array(X_data)
test_labels = np.array(Y_data)

print('Training data shape : ', train_images.shape, train_labels.shape)
print('Testing data shape : ', test_images.shape, test_labels.shape)