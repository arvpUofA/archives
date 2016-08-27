import sys
import numpy as np
import cv2
import os
import glob
from image_crop import ImageCrop
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import copy
"""
Script for creating OPENCV cascadeed classifier 
training images from Video files
"""
drawing = False
mode = True
ix,iy = -1,-1
rects = []
current = []
previous = []
img = []

count = 1
buoy = len(glob.glob('../../../imdb/buoy/*.jpg'))
background = len(glob.glob('../../../imdb/bg/*.jpg'))


def mouseCB(event,x,y,flags,param):
    global ix,iy,drawing,mode,rects, previous, img

    if event == cv2.EVENT_LBUTTONDOWN:
    	previous = copy.copy(img)
        cv2.circle(img, (x,y), 2, (0,0,255),-1) 
        if(not drawing):
        	ix,iy = x,y
        	drawing = True  	
    elif event == cv2.EVENT_MOUSEMOVE:
    	if drawing == True:
    		img = copy.copy(previous)
    		cv2.rectangle(img,(ix,iy),(x,y),(0,0,255),1)

    elif event == cv2.EVENT_LBUTTONUP:
    	cv2.rectangle(img,(ix,iy),(x,y),(0,0,255),1)
    	rects.append([ix,iy,abs(ix-x),abs(iy-y)])
        drawing = False
        



cv2.namedWindow('image')
cv2.setMouseCallback('image',mouseCB)
esc = False
cap = cv2.VideoCapture('../testvids/30-29.avi')
#cap = cv2.VideoCapture('../testvids/muddyBuoy.mpg')
#cap = cv2.VideoCapture('../testvids/FarNotGoodBouy.mpg')
#cap = cv2.VideoCapture('../testvids/UAlbertaPoolBuoy.mpg')
#cap = cv2.VideoCapture('../testvids/FullBuoy.mpg')
#cap = cv2.VideoCapture('../testvids/BrightWaterBuoy.mpg')
#cap = cv2.VideoCapture('../testvids/GP010017.MP4')
#cap = cv2.VideoCapture(1)
while(not esc):
	previous = []
	rects = []
	ret, img = cap.read()
	#img = cv2.resize(img,None,fx=0.4, fy=0.4, interpolation = cv2.INTER_AREA)
	cimg = copy.copy(img)
	print ("count: " + str(count))
	print ("buoy: " + str(buoy))
	print ("bg: ") + str(background)
	count = count + 1
	#print(image)
	while(1):
		cv2.imshow("image", img)
		key = cv2.waitKey(1)
		if key == ord('z'):
			if(len(rects) > 0):
				buoy = buoy + 1
				cv2.imwrite('../../../imdb/buoy/buoy' + str(buoy)+'.jpg',cimg)
				with open("../../../imdb/info.dat", "a") as info:
					info.write('buoy/buoy' + str(buoy)+'.jpg  '+str(len(rects)))
					for rect in rects:	
						info.write("  {} {} {} {} ".format(rect[0],rect[1],rect[2],rect[3]))
					info.write('\n')
			break
		elif key == ord('s'):
			if(len(rects) > 0):
				buoy = buoy + 1
				cv2.imwrite('../../../imdb/buoy/buoy' + str(buoy)+'.jpg',cimg)
				with open("../../../imdb/info.dat", "a") as info:
					info.write('buoy/buoy' + str(buoy)+'.jpg  '+str(len(rects)))
					for x,y,w,h in rects:	
						info.write("  {} {} {} {} ".format(x,y,w,h))
						cv2.imwrite('../../../imdb/buoy2/buoy' + str(buoy)+'.jpg',cimg[y:(y+h),x:(x+w)])
					info.write('\n')
			break
		elif key == ord('q'):
			esc = True
			break
		elif key == ord('b'):
			background += 1
			cv2.imwrite('../../../imdb/bg/bg' + str(background)+'.jpg',cimg)
			with open("../../../imdb/bg.txt", "a") as info:
				info.write('bg/bg' + str(background)+'.jpg\n')
			break
		elif key == ord('c'):
			if(len(rects) > 0):
				rects.pop()
				img = copy.copy(previous)
		elif key == ord('s'):
			break



	
		
	




	