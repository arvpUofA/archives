#!/usr/bin/env python
from __future__ import division
import numpy as np
import cv2
import cv2.cv as cv
import copy

"""
Testing different image processing methods in OpenCV
"""
class ImageProc():

	def __init__(self):
		pass

	def adaptive_threshold(self,img, size, method):
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img = cv2.GaussianBlur(img,(7,7),0)
		#frames = cv2.split(img)
		#img = frames[1]		
		#img2 = 255 - img
		if(size % 2 == 0):
			size += 1

		if(method == 0):    
			th = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
    			cv2.THRESH_BINARY_INV,size,1)
		elif(method == 1):
			th = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    			cv2.THRESH_BINARY_INV,size,1)		
		return th

	def otsuThreshold(self, img):
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		ret,th = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		th = self.erode(th,3,1)
		th = self.dilate(th,5,2)

		return th


	def erodeAndDilate(self,img, kernelSize, it1, it2, it3):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		if(it2 != 0):
			dilation = cv2.dilate(img,kernel,iterations = it2)
		erosion = cv2.erode(dilation,kernel,iterations = it1)
		#if(it3 != 0):
		#	erosion = cv2.erode(erosion,kernel,iterations = it3)
		return erosion

	def erode(self,img,kernelSize,iterations):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		erosion = cv2.erode(img,kernel,iterations = iterations)
		return erosion

	def dilate(self,img,kernelSize,iterations):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		dilate = cv2.dilate(img,kernel,iterations = iterations)
		return dilate

	"""
	Reduce number of image colors using K means 
	"""
	def color_quantize(self,img, numClusters):
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		Z = hsv.reshape((-1,3))
		Z = np.float32(Z)
	    
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
		K = numClusters
		ret,label,center=cv2.kmeans(Z,K,criteria,10,cv2.KMEANS_PP_CENTERS)
	    
		center = np.uint8(center)
		res = center[label.flatten()]
		res2 = res.reshape((img.shape))
		#convert back to bgr
		bgr = cv2.cvtColor(res2,54)

		return bgr

	def getContours(self,img, minArea, maxLength, circularity, aratioDiff):
		img = copy.copy(img)
		contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		contours = np.asarray(contours)
		contoursNew = []

		for c in contours:
			perimeter = cv2.arcLength(c,True)
			x,y,w,h = cv2.boundingRect(c)
			aspect_ratio = float(w)/h

			if((abs(aspect_ratio-1) < aratioDiff)):
				area = cv2.contourArea(c)
				if(area < minArea):
					continue
				if(perimeter > 0):
					circularNum = (4 * np.pi * area) / (perimeter * perimeter)
					if(circularNum < circularity):
						continue
				elif(area < minArea):
					continue
				contoursNew.append(c)
		return contoursNew


	def drawHoughCircles(self,img,circles):
		if(circles != None):
			for i in circles[0,:]:
				cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
				cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
		return img

	def get_color_string(self,mean_val,hue=False,value=False):
		if value:
			if(mean_val < 30):
				return "black"
			elif(mean_val > 250):
				return "white"
			else:
				return None

		if hue:
			if(mean_val <= 13 or mean_val > 165):
				return "red"
			elif(mean_val > 13 and mean_val <= 49):
				return "yellow"
			elif(mean_val > 70 and mean_val < 80):
				return "green"
			else:
				return None
		else:
			if(mean_val[2] == max(mean_val) and np.ceil(mean_val[0]) >= np.floor(mean_val[1])):
				return "red"
			elif(mean_val[2] >= max(mean_val) and mean_val[1] > mean_val[0]):
				return "yellow"
			elif(mean_val[1] == max(mean_val)):
				return "green"
			else:
				return "unknown"

	def color_equalization(self, img):
		channels = cv2.split(img)
		channels[0] = cv2.equalizeHist(channels[0])
		channels[1] = cv2.equalizeHist(channels[1])
		channels[2] = cv2.equalizeHist(channels[2])
		img = cv2.merge(channels)
		return img

	def get_mean_rgb(self, img):
		mean_val = cv2.mean(img)
		return mean_val

	def get_mean_hue(self, img):
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		mean_val = cv2.mean(hsv)
		return mean_val[0]	

	def rgb_contrast_correction(self,img):
		imgs = cv2.split(img)
		r_avg = np.average(imgs[2].flatten())
		g_avg = np.average(imgs[1].flatten())
		b_avg = np.average(imgs[0].flatten())
		r_max = np.max(imgs[2].flatten())
		g_max = np.max(imgs[1].flatten())
		b_max = np.max(imgs[0].flatten())

		t_max = max(r_max,g_max,b_max)

		r_min = np.min(imgs[2].flatten())
		g_min = np.min(imgs[1].flatten())
		b_min = np.min(imgs[0].flatten())

		t_min = min(r_min,g_min,b_min)

		imgs[0] = imgs[0].astype(np.float32)
		imgs[1] = imgs[1].astype(np.float32)
		imgs[2] = imgs[2].astype(np.float32)

		diff = (t_max - t_min)
		
		imgs[2] = (imgs[2] - r_min)*np.true_divide((255 - r_min),(r_max-r_min)) + r_min

		if(g_avg > b_avg):
			imgs[1] = (imgs[1] - g_min)*np.true_divide((g_max - 0),(g_max-g_min))
			imgs[0] = (imgs[0] - b_min)*np.true_divide((255 - 0),(b_max-b_min))
		else:
			imgs[0] = (imgs[0] - b_min)*np.true_divide((b_max - 0),(b_max-b_min))
			imgs[1] = (imgs[1] - g_min)*np.true_divide((255 - 0),(g_max-g_min))
		
		imgs[0] = imgs[0].astype(np.uint8)
		imgs[1] = imgs[1].astype(np.uint8)
		imgs[2] = imgs[2].astype(np.uint8)

		new_img = cv2.merge(imgs)
		return new_img
	
	def hsv_contrast_correction(self,img):
		#img = img.astype(np.float32)
		hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

		hsvs = cv2.split(hsv)

		s_min = hsvs[1].min()
		v_min = hsvs[2].min()

		s_max = hsvs[1].max()
		v_max = hsvs[2].max()

		hsvs[1] = (hsvs[1] - s_min)*np.true_divide((255 - 0),(s_max-s_min))
		hsvs[2] = (hsvs[2] - v_min)*np.true_divide((255 - 0),(v_max-v_min))

		hsvs[0] = hsvs[0].astype(np.uint8)
		hsvs[1] = hsvs[1].astype(np.uint8)
		hsvs[2] = hsvs[2].astype(np.uint8)

		hsv = cv2.merge(hsvs)

		final_rgb = cv2.cvtColor(hsv,54)
		return final_rgb
