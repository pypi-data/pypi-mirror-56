#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
colors = {
	"red": {"upper": "255, 255, 255",
			"lower":"171, 160, 60"},

	"blue": {"upper": "126, 255, 255",
			"lower":"94, 80, 2"},

	"brown": {"upper": "30,255,255", 
			"lower":"20,100,100"},

	"green": {"upper": "102, 255, 255",
			"lower":"25, 52, 72"},

	"orange": {"upper": "25, 255, 255",
			"lower":"10, 100, 20"},

	"pink": {"upper": "11,255,255",
			"lower":"10,100,100"},

	"black": {"upper": "50,50,100",
			"lower":"0,0,0"},

	"purple": {"upper": "120, 255, 255",
			"lower":"80, 10, 10]"},

	"yellow": {"upper": "44, 255, 255",
			"lower":"24, 100, 100"},

	"white": {"upper": "0,0,255",
			"lower":"0,0,0"},
}


def register():
	teamno = input("Team Number: ")
	camera = input("Your Camera Device (usb(if using usb camera, just type the camera port example:0),ipcamera(just type camera ip): ")
	color = input("color you want to detect (example: red , yellow) (Optional): ")
	files = open(str(os.getcwd())+"/teamno.sycavision", "w")
	files.write(teamno)
	files.close()
	files = open(str(os.getcwd())+"/teamcamera.sycavision", "w")
	files.write(camera)
	files.close()
	files = open(str(os.getcwd())+"/teamcolor.sycavision", "w")
	files.write(color)
	files.close()

	print("Your number is {} registered in Sycavision".format(teamno))
