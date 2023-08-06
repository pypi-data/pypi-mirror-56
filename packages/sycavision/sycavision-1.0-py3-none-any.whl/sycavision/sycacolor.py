#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
from networktables import NetworkTables
import numpy as np
import argparse
import cv2
import time
import imutils
x = 0 #programın ileride hata vermemesi için x 0 olarak tanımlıyorum
y = 0 # programın ileride hata vermemesi için y 0 olarak tanımlıyorum
radius = 0
def vision(teamno,upper,lower,cameraa):

    NetworkTables.initialize(server='roborio-{}-frc.local'.format(teamno)) # Roborio ile iletişim kuruyoruz
    table = NetworkTables.getTable("sycavision") # table oluşturuyoruz

    low1 = lower.split(",")
    up1= upper.split(",")
    
    #sari rengin algilanmasi
    colorLower = (int(low1[0]),int(low1[1]),int(low1[2]))
    colorUpper = (int(up1[0]),int(up1[1]),int(up1[2]))
    #converter.py ile convert ettiğiniz rengi buraya giriniz
    camera = cv2.VideoCapture(int(cameraa)) # kameradan
    while True: #yazılımımız çalıştığı sürece aşağıdaki işlemleri tekrarla


         (grabbed, frame) = camera.read() # grabbed ve frame değişkenini camera.read olarak tanımlıyoruz.
         frame = imutils.resize(frame, width=320,height=240) # görüntü genişliğini 600p yapıyoruz
         frame = imutils.rotate(frame, angle=0) # görüntüyü sabitliyoruz

      
         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # görüntüyü hsv formatına çeviriyoruz

         mask = cv2.inRange(hsv, colorLower, colorUpper) # hsv formatına dönen görüntünün bizim belirttiğimiz renk sınırları içerisinde olanları belirliyor
         mask = cv2.erode(mask, None, iterations=2) # bizim renklerimizi işaretliyor
         mask = cv2.dilate(mask, None, iterations=2) # bizim renklerimizin genişliğini alıyor


         cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    	 cv2.CHAIN_APPROX_SIMPLE)[-2]
         center = None


         if len(cnts) > 0:

    		     c = max(cnts, key=cv2.contourArea)
    		     ((x, y), radius) = cv2.minEnclosingCircle(c)
    		     M = cv2.moments(c)
    		     center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


    		     if radius > 1: #algılanacak hedefin minumum boyutu
    			     cv2.circle(frame, (int(x), int(y)), int(radius),
    				 (0, 255, 255), 2)
    			     cv2.circle(frame, center, 5, (0, 0, 255), -1)
         else:
            x = 0 ##değerlerin sıfırlanması
            y = 0
            radius = 0

         print("x : ", x)
         print("y : ", y)
         print("r : ", radius)

         table.putNumber("xloc", x) # roborioya değeri göndermek
         table.putNumber("yloc", y)
         table.putNumber("rloc", radius)
         cv2.putText(frame, "Sycavision developed by #8208",(50,450),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)
         cv2.imshow("Sycavision - Color", frame)
         cv2.waitKey(1)