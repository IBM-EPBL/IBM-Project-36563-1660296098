# -*- coding: utf-8 -*-
"""Videos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CHBuR8IlEfBytplSElHAqQ5rYM49LBAD
"""

import cv2
import numpy as np
 # Creating a VideoCapture object to read the video
cap = cv2.VideoCapture('sample.mp4')
  while (cap.isOpened()):
  ret, frame = cap.read()

    frame = cv2.resize(frame, (540, 380), fx = 0, fy = 0,

                         interpolation = cv2.INTER_CUBIC)

    cv2.imshow('Frame', frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    Thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,

                                           cv2.THRESH_BINARY_INV, 11, 2)
 

    cv2.imshow('Thresh', Thresh)

    # define q as the exit button

    if cv2.waitKey(25) & 0xFF == ord('q'):
 break
 
# release the video capture object
cap.release()
# Closes all the windows currently opened.
cv2.destroyAllWindows()