import cv2
import numpy as np
import serial
import time
import os
from shutil import copyfile
import subprocess

#Myserial = serial.Serial('/dev/ttyACM0',9600)

SETUP_TRAINING = False
IMG_TO_COLLECT = 300

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
face_img = 0
img_index = 0

def setup(img_index):
  os.mkdir('..//data/person1')
  while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
      tmp_img = img[y:y+h, x:x+w]
      face_img = cv2.resize(tmp_img, (192, 192))

    if (len(faces)) == 0:
      #Myserial.write('N')
      print ("No face is detected")
    elif (len(faces)) == 1:
      #Myserial.write('Y')
      print ("Face is detected")
      #cv2.imshow('img', face_img)
      #collect 10 training images
      cv2.imwrite("../data/peron1/" + str(img_index) + ".jpg", face_img)
      img_index += 1
      if(img_index % 50 == 0):
        print('img_index == ' + str(img_index))
      if(img_index == IMG_TO_COLLECT):
        break
    k = cv2.waitKey(1) & 0xFF == ord('q')
    if k == 27:
      break
  #Extrapolate images
  '''  base_folder = '../data/person1/'
  index = 10
  img1 = cv2.imread(base_folder + '0.jpg')
  img2 = cv2.imread(base_folder + '1.jpg')
  img3 = cv2.imread(base_folder + '2.jpg')
  img4 = cv2.imread(base_folder + '3.jpg')
  img5 = cv2.imread(base_folder + '4.jpg')
  img6 = cv2.imread(base_folder + '5.jpg')
  img7 = cv2.imread(base_folder + '6.jpg')
  img8 = cv2.imread(base_folder + '7.jpg')
  img9 = cv2.imread(base_folder + '8.jpg')
  img10 = cv2.imread(base_folder + '9.jpg')
  for i in range(29):
    cv2.imwrite(base_folder + str(index) + '.jpg', img1)
    index += 1
    cv2.imwrite(base_folder + str(index) + '.jpg', img2)
    index += 1
    cv2.imwrite(base_folder + str(index) + '.jpg', img3)
    index += 1
    cv2.imwrite(base_folder + str(index) + '.jpg', img4)
    index += 1
    cv2.imwrite(base_folder + str(index) + '.jpg', img5)
    index += 1
    cv2.imwrite(base_folder + str(index) + '.jpg', img6)
    index += 1
    cv2.imwrite(base_folder + str(index) + '.jpg', img7)
    index += 1
    cv2.imwrite(base_folder + str(index) + '.jpg', img8)
    index += 1
    cv2.imwrite(base_folder + str(index) + '.jpg', img9)
    index += 1
    cv2.imwrite(base_folder + str(index) + '.jpg', img10)
    index += 1'''
  #Train model and bring the model in workspace
  #os.system("python3 retrain.py --image_dir ../data")

  print('Training model...!')
  process = subprocess.Popen('python3 retrain.py --image_dir ../data', shell=True, stdout=subprocess.PIPE)
  process.wait()

  copyfile('/tmp/output_graph.pb', 'model/output_graph.pb')
  copyfile('/tmp/output_labels.txt', 'model/output_labels.txt')


if(SETUP_TRAINING):
  setup(img_index)
while True:
  ret, img = cap.read()
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  for (x,y,w,h) in faces:
    tmp_img = img[y:y+h, x:x+w]
    face_img = cv2.resize(tmp_img, (192, 192))

  if (len(faces)) == 0:
    #Myserial.write('N')
    #print ("No face is detected")
    pass
  elif (len(faces)) == 1:
    #Myserial.write('Y')
    print ("Face is detected")
    #cv2.imshow('img', face_img)
    # face recognition here
    cv2.imwrite('images/toBeClassified.jpg', face_img)
    import subprocess

    out = os.popen('python3 label_image.py --graph=model/output_graph.pb --labels=model/output_labels.txt --input_layer=Placeholder --output_layer=final_result --image=images/toBeClassified.jpg').read()
    print('out = ' + str(out))
    classification_output = out.split()
    if(float(classification_output[1]) > 0.6):
      print('CLASSIFIED AS ' + str(classification_output[0]))

  k = cv2.waitKey(1) & 0xFF == ord('q')
  if k == 27:
    break

cap.release()
cv2.destroyAllWindows()