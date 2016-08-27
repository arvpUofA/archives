import numpy as np
import cv2
import cv2.cv as cv
from image_crop import ImageCrop
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
	num = 0.45
	#num = 1
	#cap = cv2.VideoCapture('../testvids/horz.avi')
	#cap = cv2.VideoCapture('../testvids/muddyBuoy.mpg')
	cap = cv2.VideoCapture('../testvids/FarNotGoodBouy.mpg')
	#cap = cv2.VideoCapture('../testvids/FarToCloseBuoy.mpg')
	#cap = cv2.VideoCapture('../testvids/UAlbertaPoolBuoy.mpg')
	#cap = cv2.VideoCapture('../testvids/FullBuoy.mpg')
	#cap = cv2.VideoCapture('../testvids/GP010017.MP4')
	#cap = cv2.VideoCapture(1)

	model_svm = cv2.SVM()
	model_svm.load("../svm_red.xml")
	ip = ImageProc()

	timeCount = 0
	start = time.time()
	output = []
	while(1):
		if((timeCount != 0) and ((timeCount % 30) == 0)):
			print(timeCount)
			end = time.time()
			print("frames/s: " + str(timeCount / (end-start)))
			#start = time.time()

		timeCount += 1

		ret, frame = cap.read()
		frame = cv2.resize(frame,None,fx=num, fy=num, interpolation = cv2.INTER_AREA)
		
		frame2 = copy.copy(frame)

		lab = cv2.cvtColor(frame2,cv2.COLOR_BGR2LAB)
		
		#a = a.reshape((m,n))
		#lab = cv2.merge(labs)

		rgbnew = cv2.cvtColor(lab,cv2.COLOR_LAB2BGR)

		new3 = ip.rgb_contrast_correction(copy.copy(frame2))
		rgbsnew = cv2.split(new3)
		
		newG = cv2.GaussianBlur(new3,(7,7),0)
		#print(new3.shape)
		new2 = frame2
		hsv = cv2.cvtColor(new2, cv2.COLOR_BGR2HSV)
		#gray = cv2.cvtColor(hsv,cv2.COLOR_BGR2GRAY)
		hsvs = cv2.split(hsv)

		#rgbs = cv2.split(new2)
		#red = rgbs[2]
		hue = copy.copy(hsvs[0])
		sat = copy.copy(hsvs[1])


		hsv2 = cv2.cvtColor(new3, cv2.COLOR_BGR2HSV)
		hsvs2 = cv2.split(hsv2)
		rgbs2 = cv2.split(new3)
		red2 = rgbs2[2]
		hue2 = copy.copy(hsvs2[0])
		sat2 = copy.copy(hsvs2[1])

		#sat = cv2.GaussianBlur(labs[0],(17,17),0)
		#new4 = ip.adaptive_threshold(hsv, 45, 1)
		#new4 = cv2.adaptiveThreshold(labs[2],255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    	#		cv2.THRESH_BINARY_INV,45,1)
		#new5 = ip.adaptive_threshold(red2, 45, 1)
		#new4 = ip.erode(new4,5,1);
		#new4 = ip.dilate(new4,5,1);

		if ret == True:
			cv2.waitKey(1)
			#(m,n) = hsvs[0].shape
			######################
			##### slow part ###### 
			######################
			H = hsvs2[0].flatten()
			S = hsvs[1].flatten()
			test_vector = []
			for i, hu in enumerate(H):
				test_vector.append([H,S[i]])
			new = np.zeros(len(H))
			new = model_svm.predict_all(np.asarray(test_vector, dtype=np.float32))
			######################
			######################
			#cv2.namedWindow("dog", cv2.WINDOW_NORMAL)
			#new = new.reshape(m,n)
			#cv2.imshow("new",new2)
			#cv2.imshow("red",get_red_mask(hue2))
			#cv2.imshow("yellow",get_yellow_mask(hue2))
			#cv2.imshow("green",get_green_mask(hue2))

			#cv2.imshow("dog",dog(hue))
			#cv2.imshow("sat",dog(sat))
			#cv2.imshow('red',dog(red))
			#cv2.imshow('r',red)

			#cv2.imshow("adred",rgbnew)
			#cv2.imshow("red1",red)
			cv2.imshow('red2',new)

			#cv2.imshow('dog',a)

	cap.release()
	cv2.destroyAllWindows()


