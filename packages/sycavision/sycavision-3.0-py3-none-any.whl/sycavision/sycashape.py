#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import argparse
import cv2
import cv2 as CV 
from networktables import NetworkTables

def circle(teamno,cameraa):
	NetworkTables.initialize(server='roborio-{}-frc.local'.format(teamno)) # Roborio ile iletişim kuruyoruz
	table = NetworkTables.getTable("sycavision") # table oluşturuyoruz
	cap = cv2.VideoCapture(int(cameraa)) # webcamin bagli oldugu yer
	while(True):
		# goruntu yakalama
		ret, frame = cap.read()
		# goruntuyu grilestir
		output = frame.copy()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# goruntuyu blurlastir
		gray = cv2.GaussianBlur(gray,(5,5),0);
		gray = cv2.medianBlur(gray,5)
		gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
	            cv2.THRESH_BINARY,11,3.5)
		kernel = np.ones((5,5),np.uint8)
		gray = cv2.erode(gray,kernel,iterations = 1)
		gray = cv2.dilate(gray,kernel,iterations = 1)
		#circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 300, param1=30, param2=25, minRadius=0, maxRadius=0) #python2 icin
		circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 300, param1=40, param2=80, minRadius=0, maxRadius=0) # python3 icin 
	    # (x−xcenter)2+(y−ycenter)2=r2   (xcenter,ycenter) 
		# kalibre
		# daireyi is40
		if circles is not None:
			circles = np.round(circles[0, :]).astype("int")
			for (x, y, r) in circles:
				cv2.circle(output, (x, y), r, (0, 255, 0), 4)
				cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
				print ("X kordinat: ", x)
				print ("Y Kordinat: ", y)
				print ("Radius: ", r)
				table.putNumber("xloc", x) # roborioya değeri göndermek
				table.putNumber("yloc", y)
				table.putNumber("rloc", r)
		cv2.putText(output, "Sycavision developed by #8208",(50,450),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)
		cv2.imshow('Sycavision - Circle',output) # ekranda göster
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()
	cv2.destroyAllWindows()


def line(teamno,upper,lower,cameraa):
	NetworkTables.initialize(server='roborio-{}-frc.local'.format(teamno)) # Roborio ile iletişim kuruyoruz
	table = NetworkTables.getTable("sycavision") # table oluşturuyoruz
	low1 = lower.split(",")
	up1 = upper.split(",")

	cam = cv2.VideoCapture(int(cameraa)) # webcamin bagli oldugu yer
	while True:
		ret, orig_frame = cam.read()
		if not ret:
			cam = cv2.VideoCapture(0)
			continue
		frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		low = np.array([int(low1[0]),int(low1[1]),int(low1[2])])
		up = np.array([int(up1[0]),int(up1[1]),int(up1[2])])
		mask = cv2.inRange(hsv, low, up)
		edges = cv2.Canny(mask, 75, 150)

		lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)
		if lines is not None:
			for line in lines:
				x1, y1, x2, y2 = line[0]
				cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

				x = x2 -x1
				y = y2-y1
				print("x: ", x)
				print("y: ", y)
				table.putNumber("xloc", x) # roborioya değeri göndermek
				table.putNumber("yloc", y)
		else:
			x = 0
			y = 0
		cv2.putText(frame, "Sycavision developed by #8208",(50,450),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1,cv2.LINE_AA)
		cv2.imshow('Sycavision - Line', frame)
		cv2.waitKey(1)