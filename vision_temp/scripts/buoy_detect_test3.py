import numpy as np
import cv2
import cv2.cv as cv
from buoy_detect import BlobDetector
from image_proc import ImageProc
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import time
import copy

globalImg=None

# import the necessary packages
import numpy as np
import cv2

def dog(gray):
	one = cv2.GaussianBlur(gray,(5,5),0)
	two = cv2.GaussianBlur(gray,(3,3),0)
	return two - one

def get_red_mask(hue):
    mask_red1 = cv2.inRange(hue,0,13)
    mask_red2 = cv2.inRange(hue,165,180)
    mask_red = cv2.bitwise_or(mask_red1,mask_red2)
    #mask_red = self.ip.erode(mask_red,self.erode_size,self.erode_iterations)
    #mask_red = self.ip.dilate(mask_red,self.dilate_size,self.dilate_iterations)
    return mask_red

def get_yellow_mask(hue):
    mask_yellow = cv2.inRange(hue,14,50)
    #mask_red = self.ip.erode(mask_yellow,self.erode_size,self.erode_iterations)
    #mask_red = self.ip.dilate(mask_yellow,self.dilate_size,self.dilate_iterations)
    return mask_yellow

def get_green_mask(hue):
    mask_green = cv2.inRange(hue,51,90)
    #mask_green = self.ip.erode(mask_green,self.erode_size,self.erode_iterations)
    #mask_green = self.ip.dilate(mask_green,self.dilate_size,self.dilate_iterations)
    return mask_green

"""
Testing buoy detection
"""
if __name__ == '__main__':

	FIRST = True
	#videos on google drive
	num = 0.5
	#num = 1
	#cap = cv2.VideoCapture('../testvids/horz.avi')
	#cap = cv2.VideoCapture('../testvids/muddyBuoy.mpg')
	#cap = cv2.VideoCapture('../testvids/FarNotGoodBouy.mpg')
	cap = cv2.VideoCapture('../testvids/FarToCloseBuoy.mpg')
	#cap = cv2.VideoCapture('../testvids/BrightWaterBuoy.mpg')
	#cap = cv2.VideoCapture('../testvids/UAlbertaPoolBuoy.mpg')
	#cap = cv2.VideoCapture('../testvids/FullBuoy.mpg')
	#cap = cv2.VideoCapture('../testvids/pool3buoy.avi')
	#cap = cv2.VideoCapture('../testvids/GP010017.MP4')
	#cap = cv2.VideoCapture(1)
	#cap.set(cv2.cv.CV_CAP_PROP_FORMAT, cv2.cv.CV_32F)
	#cap.set(cv2.cv.CV_CAP_PROP_FOURCC, cv.CV_FOURCC("Y", "1", "6", " "))

	ip = ImageProc()

	timeCount = 0
	start = time.time()
	output = []
	while(1):
		new_start = time.time()
		if((timeCount != 0) and ((timeCount % 30) == 0)):
			print(timeCount)
			end = time.time()
			#print("frames/s: " + str(timeCount / (end-start)))
			#start = time.time()

		timeCount += 1

		ret, frame = cap.read()
		#frame = np.array(frame, dtype=np.float32)
		print(frame.shape)
		frame = cv2.resize(frame,None,fx=num, fy=num, interpolation = cv2.INTER_AREA)

		frame2 = copy.copy(frame)
		#lab = cv2.cvtColor(frame2,cv2.COLOR_BGR2LAB)

		#a = a.reshape((m,n))
		#lab = cv2.merge(labs)

		#rgbnew = cv2.cvtColor(lab,cv2.COLOR_LAB2BGR)
		new3 = ip.rgb_contrast_correction(frame2)
        cv2.imshow("normal", frame2)
        cv2.imshow("CC", new3)
        k = cv2.waitKey(-1)
        new2 = frame2
        hsv = cv2.cvtColor(new2, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(new3, cv2.COLOR_BGR2HSV)
        cv2.imshow("HSV",hsv)
        cv2.imshow("HSV2",hsv2)
        gray = cv2.cvtColor(new3,cv2.COLOR_BGR2GRAY)
        hsvs = cv2.split(hsv)
        hsvs2 = cv2.split(hsv2)
        rgbs = cv2.split(new3)
        red = rgbs[2]
        hue2 = copy.copy(hsvs2[0])
        hue = copy.copy(hsvs[0])
        sat = copy.copy(hsvs[1])
        sat2 = copy.copy(hsvs2[1])
        cv2.imshow("sat2",sat2)
        cv2.imshow("sat",sat)
        cv2.imshow("hue2",hue2)
        cv2.imshow("hue",hue)
        mask_red1 = cv2.inRange(hsv2,np.array([170,0,0]),np.array([180,255,255]))
        mask_red2 = cv2.inRange(hsv2,np.array([0,0,0]),np.array([15,255,255]))
        mask_red = cv2.bitwise_or(mask_red1,mask_red2)
        new_end = time.time()
        if((timeCount % 30) == 0):
            print("FPS: ",1/(new_end-new_start))

	cap.release()
	cv2.destroyAllWindows()
