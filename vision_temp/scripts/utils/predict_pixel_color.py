import numpy as np
import cv2
import copy
from image_proc import ImageProc
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
"""
mean_red_hue_cor1 = np.load("../color_params/mean_red_hue_cor1-1.npy")
mean_red_hue_cor2 = np.load("../color_params/mean_red_hue_cor2-1.npy")
cov_red_hue_cor1 = np.load("../color_params/cov_red_hue_cor1-1.npy")
cov_red_hue_cor2 = np.load("../color_params/cov_red_hue_cor2-1.npy")

mean_green_hue_cor = np.load("../color_params/mean_green_hue_cor-1.npy")
cov_green_hue_cor = np.load("../color_params/cov_green_hue_cor-1.npy")
mean_yellow_hue_cor = np.load("../color_params/mean_yellow_hue_cor-1.npy")
cov_yellow_hue_cor = np.load("../color_params/cov_yellow_hue_cor-1.npy")
"""
def get_model1(self):
    mean_red1 = np.load("../color_params/mean_red_hue_cor1-1.npy")
    mean_red2 = np.load("../color_params/mean_red_hue_cor2-1.npy")
    cov_red1 = np.load("../color_params/cov_red_hue_cor1-1.npy")
    cov_red2 = np.load("../color_params/cov_red_hue_cor2-1.npy")

    mean_green = np.load("../color_params/mean_green_hue_cor-1.npy")
    cov_green = np.load("../color_params/cov_green_hue_cor-1.npy")
    mean_yellow = np.load("../color_params/mean_yellow_hue_cor-1.npy")
    cov_yellow = np.load("../color_params/cov_yellow_hue_cor-1.npy")
    red = {'red_mean1':mean_red1,'red_mean2':mean_red2,
            'red_var1':cov_red1,'red_var2': cov_red2}
    green = {'green_mean':mean_green,'green_var':cov_green}
    yellow = {'yellow_mean':mean_yellow,'yellow_var':cov_yellow}
    return red,yellow,green

def get_model2(self):
    mean_red1 = np.load("../color_params/mean_red_hue_cor1-2.npy")
    mean_red2 = np.load("../color_params/mean_red_hue_cor2-2.npy")
    cov_red1 = np.load("../color_params/cov_red_hue_cor1-2.npy")
    cov_red2 = np.load("../color_params/cov_red_hue_cor2-2.npy")

    mean_green = np.load("../color_params/mean_green_hue_cor-2.npy")
    cov_green = np.load("../color_params/cov_green_hue_cor-2.npy")
    mean_yellow = np.load("../color_params/mean_yellow_hue_cor-2.npy")
    cov_yellow = np.load("../color_params/cov_yellow_hue_cor-2.npy")
    red = {'red_mean1':mean_red1,'red_mean2':mean_red2,
            'red_var1':cov_red1,'red_var2': cov_red2}
    green = {'green_mean':mean_green,'green_var':cov_green}
    yellow = {'yellow_mean':mean_yellow,'yellow_var':cov_yellow}
    return red,yellow,green



mean_red_hue_cor1 = np.load("../color_params/mean_red_hue_cor1-2.npy")
mean_red_hue_cor2 = np.load("../color_params/mean_red_hue_cor2-2.npy")
cov_red_hue_cor1 = np.load("../color_params/cov_red_hue_cor1-2.npy")
cov_red_hue_cor2 = np.load("../color_params/cov_red_hue_cor2-2.npy")

mean_green_hue_cor = np.load("../color_params/mean_green_hue_cor-2.npy")
cov_green_hue_cor = np.load("../color_params/cov_green_hue_cor-2.npy")
mean_yellow_hue_cor = np.load("../color_params/mean_yellow_hue_cor-2.npy")
cov_yellow_hue_cor = np.load("../color_params/cov_yellow_hue_cor-2.npy")


print("Red")
print(mean_red_hue_cor1,np.sqrt(cov_red_hue_cor1))
print(mean_red_hue_cor2,np.sqrt(cov_red_hue_cor2))
print("Yellow")
print(mean_yellow_hue_cor,np.sqrt(cov_yellow_hue_cor))
print("Green")
print(mean_green_hue_cor,np.sqrt(cov_green_hue_cor))


time.sleep(3)
#cap = cv2.VideoCapture(1)
#cap = cv2.VideoCapture('../testvids/horz.avi')
#cap = cv2.VideoCapture('../testvids/muddyBuoy.mpg')
#cap = cv2.VideoCapture('../testvids/FarNotGoodBouy.mpg')
#cap = cv2.VideoCapture('../testvids/UAlbertaPoolBuoy.mpg')
cap = cv2.VideoCapture('../testvids/FullBuoy.mpg')
#cap = cv2.VideoCapture('../testvids/BrightWaterBuoy.mpg')
#cap = cv2.VideoCapture('../testvids/GP010017.MP4')
#cap = cv2.VideoCapture(1)

def prob_gaussian(sample,mean,variance):
	px = (1/np.sqrt(2*np.pi*np.sqrt(variance)))*np.exp(-((sample-mean)**2)/(2*variance))
	#print(px)
	return px*100

def prob_multivariate_gaussian(sample,mean,cov,dete,inverse):
	D = len(sample)
	diff = sample - mean
	px = (1/(((2*np.pi)**(3/2))*(dete**(0.5))))*np.exp(-0.5*(tmp))
	return px*1000000000

def threshold_with_value(img,mean,std_dev):
	hsvs = cv2.split(img)
	hue = hsvs[0]

	mask = cv2.inRange(hue,mean-std_dev,mean+std_dev)
	#cv2.imshow("mask1",mask)
	#cv2.waitKey(0)
	return mask

thres = 0.01
ip = ImageProc()

while(True):
	ret, img = cap.read()
	ef = copy.copy(img)
	img = ip.rgb_contrast_correction(img)
	img = cv2.resize(img,None,fx=0.4, fy=0.4, interpolation = cv2.INTER_AREA)
	ef = cv2.resize(ef,None,fx=0.4, fy=0.4, interpolation = cv2.INTER_AREA)
	cimg = copy.copy(img)
	#cv2.imshow("img",cimg)
	#cv2.waitKey(0)
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	hsvs = cv2.split(hsv)
	 
	n,m = hsvs[0].shape
	a = hsvs[0].reshape(n*m)
	px1 = np.zeros(len(a))
	px3 = np.zeros(len(a))
	b = np.reshape(img,(m*n,3))
	px2 = np.zeros(len(a))
	mask1 = np.zeros([n,m], dtype=np.uint8)
	mask2 = np.zeros([n,m], dtype=np.uint8)
	mask3 = np.zeros([n,m], dtype=np.uint8)
	
	#mask3 = threshold_with_value(hsv,mean_yellow_hue_cor,np.sqrt(cov_yellow_hue_cor))
	#mask4 = threshold_with_value(hsv,mean_green_hue_cor,np.sqrt(cov_green_hue_cor/2))
	mask2 = threshold_with_value(hsv,mean_red_hue_cor2,np.sqrt(cov_red_hue_cor2))
	mask1 = threshold_with_value(hsv,mean_red_hue_cor1,np.sqrt(cov_red_hue_cor1))
	#mask2 = threshold_with_value(hsv,mean_red_hue_cor2,np.sqrtqrt(cov_red_hue_cor2))

	bew_mask = cv2.bitwise_or(mask1,mask2)
	#bew_mask = cv2.bitwise_or(bew_mask,mask3)
	#ew_mask = cv2.bitwise_or(bew_mask,mask4)
	#cv2.imshow("mask1",mask1)
	mask = cv2.inRange(hsvs[0],71,78)
	#maskl = cv2.inRange(hsvs[0],50,70)
	#masku = cv2.inRange(hsvs[0],85,165)
	#bew_mask = cv2.bitwise_or(maskl,masku)

	edges = cv2.Canny(hsvs[0],75,85)
	#laplacian = cv2.Laplacian(hsvs[0],cv2.CV_64F)

	cv2.imshow("normal",edges)
	cv2.imshow("corrected",bew_mask)
	cv2.imshow("eshape",img)
	key = cv2.waitKey(0)
		if key == ord("a"):
		fig = plt.figure(1)
		n, bins, patches = plt.hist(a.astype(int), 75)
		l = plt.plot(bins)
		plt.title('hue')
		plt.show()

	"""
	dete = np.linalg.det(cov_red_rgb_cor)
	inverse = np.linalg.inv(cov_red_rgb_cor)

	for row in range(0,m*n):
		px2[row] = prob_multivariate_gaussian(b[row,:],mean_red_rgb_cor,cov_red_rgb_cor,dete,inverse)
		#if(px2[row] > 0.0001):
		#	print(px2[row])
	pu2 = np.mean(px2)
	#print(pu2)
	
	mask1 = np.ma.masked_greater(px2,0.000000001)
	
	#mask1 = np.logical_and((px2>(pu2-thres)),(px2 < (pu2+thres)))
	mask1 = np.reshape(mask1,(n,m))
	#print(mask1)
	
	#print(mask1)
	"""
	"""
	for i,pixel in enumerate(a):
		px1[i] = prob_gaussian(pixel,mean_red_hue_cor1,cov_red_hue_cor1)
		px3[i] = prob_gaussian(pixel,mean_red_hue_cor2,cov_red_hue_cor2)


	mask2 = np.ma.masked_greater(px1,0.000000001)
	mask3 = np.ma.masked_greater(px3,0.0000001)
	pu2 = np.mean(px1)
	#print(pu2)
	#mask2 = (px1>(pu2-thres)) & (px1 < (pu2+thres))
	mask2 = np.reshape(mask2,(n,m))
	pu2 = np.mean(px3)
	#print(pu2)
	#mask3 = (px3>(pu2-thres)) & (px3 < (pu2+thres))
	mask3 = np.reshape(mask3,(n,m))
	mask_new = np.logical_or(mask2,mask3)
	#print(mask_new)
	#print(mask2)
	"""
	#cv2.imshow("img",cimg)
	#cv2.waitKey()
	#time.sleep(0.01)
	print("Done")

		




