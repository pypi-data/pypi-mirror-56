#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from sycavision import sycaregister
from sycavision import sycacolor
from sycavision import sycashape
import pyfiglet
import os
req = argparse.ArgumentParser()
req.add_argument("-r", "--register", required=False, help="Register your device and your team (example using -r yes)")
req.add_argument("-p", "--proccesstype", required=False, help="Proccess type (c = color , sc = shape circle, sl = shape line")

args = vars(req.parse_args())
teamregister = args["register"]
prtyp = args["proccesstype"]



def main():
	sycamore = pyfiglet.figlet_format("Sycamore #8208")
	print(sycamore)

def register():
	sycaregister.register()

def color():
	teamno = open(str(os.getcwd())+"/teamno.sycavision","r")
	teamno = teamno.read()
	camera = open(str(os.getcwd())+"/teamcamera.sycavision","r")
	camera = camera.read()
	color = open(str(os.getcwd())+"/teamcolor.sycavision","r")
	color = color.read()
	upper = (sycaregister.colors[color]["upper"])
	lower = (sycaregister.colors[color]["lower"])
	sycacolor.vision(teamno,upper,lower,camera)

def circle():
	teamno = open(str(os.getcwd())+"/teamno.sycavision","r")
	teamno = teamno.read()
	camera = open(str(os.getcwd())+"/teamcamera.sycavision","r")
	camera = camera.read()
	sycashape.circle(teamno,camera)

def line():
	teamno = open(str(os.getcwd())+"/teamno.sycavision","r")
	teamno = teamno.read()
	camera = open(str(os.getcwd())+"/teamcamera.sycavision","r")
	camera = camera.read()
	color = open(str(os.getcwd())+"/teamcolor.sycavision","r")
	color = color.read()
	upper = (sycaregister.colors[color]["upper"])
	lower = (sycaregister.colors[color]["lower"])
	sycashape.line(teamno,upper,lower,camera)

main()

if(teamregister is not None):
	register()

if(prtyp == "c"):
	color()
elif(prtyp=="sc"):
	circle()
elif(prtyp=="sl"):
	line()
