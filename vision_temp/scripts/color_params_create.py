from __future__ import division
import sys
import numpy as np
import cv2
import os
import glob
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import copy
from image_proc import ImageProc
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.mlab as mlab
import csv
"""
Script for creating OPENCV cascadeed classifier 
training images from Video files
"""

ip = ImageProc()
ix,iy = None,None
points = []
img = []

red_rgb = [[],[],[]]
yellow_rgb = [[],[],[]]
green_rgb = [[],[],[]]

red_hue = []
yellow_hue = []
green_hue = []

red_rgb_cor = [[],[],[]]
yellow_rgb_cor = [[],[],[]]
green_rgb_cor = [[],[],[]]

red_hue_cor = []
yellow_hue_cor = []
green_hue_cor = []

red_sat1 = []
yellow_sat1 = []
green_sat1 = []
red_sat2 = []
yellow_sat2 = []
green_sat2 = []

red_value = []
yellow_value = []
green_value = []



hue_sat_red = []
hue_sat_green = []
hue_sat_yellow = []

def save_to_csv(input,filename):
	#a = numpy.asarray(input)

	np.savetxt('../../../imdb/colors/'+filename, input, delimiter=",")

def mouseCB(event,x,y,flags,param):
    global ix,iy,drawing,mode,points, previous, img
    #print(ix,iy)
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(cor_img, (x,y), 2, (0,0,255),-1) 
        if(ix is not None and iy is not None):
        	cv2.line(cor_img,(ix,iy),(x,y),(0,0,255),1)
        ix,iy = x,y  	
    elif event == cv2.EVENT_LBUTTONUP:
    	points.append([ix,iy])

cv2.namedWindow('image')
cv2.setMouseCallback('image',mouseCB)
esc = False
cap_index = 0
cap_array = ['../testvids/muddyBuoy.mpg','../testvids/FarNotGoodBouy.mpg','../testvids/FarToCloseBuoy.mpg']
#cap = cv2.VideoCapture('../testvids/horz.avi')
#cap = cv2.VideoCapture('../testvids/pool1.avi')
cap = cv2.VideoCapture(cap_array[cap_index])
#cap = cv2.VideoCapture('../testvids/FarNotGoodBouy.mpg')
#cap = cv2.VideoCapture('../testvids/UAlbertaPoolBuoy.mpg')
#cap = cv2.VideoCapture('../testvids/FullBuoy.mpg')
#cap = cv2.VideoCapture('../testvids/BrightWaterBuoy.mpg')
#cap = cv2.VideoCapture('../testvids/GP010017.MP4')
#cap = cv2.VideoCapture(1)
while(not esc):
	ret, img = cap.read()
	img = cv2.resize(img,None,fx=.45, fy=.45, interpolation = cv2.INTER_AREA)
	cimg = copy.copy(img)
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	cor_img = ip.rgb_contrast_correction(copy.copy(cimg))
	hsv_cor = cv2.cvtColor(cor_img,cv2.COLOR_BGR2HSV)
	while(1):
		cv2.imshow("image", cor_img)
		key = cv2.waitKey(1)
		#print(key)
		#print("c",ord('c'))
		if key == ord('r') or key == ord('g') or key == ord('y'):
			ix = None
			iy = None
			if(len(points) >= 3):
				[x,y,z] = img.shape
				mask1 = np.zeros([x,y], dtype=np.uint8)
				mask2 = np.zeros(img.shape, dtype=np.uint8)
				pts = np.array(points, np.int32)
				pts = pts.reshape((-1,1,2))
				poly_roi_norm = cv2.fillPoly(mask1,[pts],255)
				
				[B1,G1,R1] = cv2.split(cimg)
				[B2,G2,R2] = cv2.split(cor_img)
				[H,S,V] = cv2.split(hsv)
				[Hc,Sc,Vc] = cv2.split(hsv_cor)

				B1 = B1[mask1 > 0] 
				G1 = G1[mask1 > 0]
				R1 = R1[mask1 > 0]
				new1 = np.vstack((B1,G1,R1))

				B2 = B2[mask1 > 0] 
				G2 = G2[mask1 > 0]
				R2 = R2[mask1 > 0]
				new2 = np.vstack((B2,G2,R2))

				H1 = H[mask1>0]
				H2 = Hc[mask1>0]

				V1 = V[mask1>0]
				V2 = Vc[mask1>0]

				S1 = S[mask1>0]
				S2 = Sc[mask1>0]

				hue_sat = [H2,S1]
				print("Value normal: ",cv2.mean(V1))
				print("Value corrected: ",cv2.mean(V2))
				print("RGB corrected: ",cv2.mean(B2),cv2.mean(G2),cv2.mean(R2))
			

				if(key == ord('r')):
					red_rgb = np.hstack((red_rgb,new1))
					red_rgb_cor = np.hstack((red_rgb_cor,new2))
					red_hue = np.hstack((red_hue,H1))
					red_hue_cor = np.hstack((red_hue_cor,H2))
					red_sat2 = np.hstack((red_sat2,S2))
					red_sat1 = np.hstack((red_sat1,S1))
					red_value = np.hstack((red_value,V2))
					#hue_sat_red = np.hstack((hue_sat_red,hue_sat))
					for i, h in enumerate(H2):
						hue_sat_red.append([h,S1[i]])
					#hue_sat_red.append(hue_sat)
					print("Red num: {}".format(red_rgb.shape))
					print("Red mean rgb: {}".format(np.mean(red_rgb,axis=1)))
					print("Red mean rgb cor: {}".format(np.mean(red_rgb_cor,axis=1)))
					print("Red mean hue: {}".format(np.mean(red_hue)))
					print("Red mean hue cor: {}".format(np.mean(red_hue_cor)))
				elif(key == ord('g')):
					green_rgb = np.hstack((green_rgb,new1))
					green_rgb_cor = np.hstack((green_rgb_cor,new2))
					green_hue = np.hstack((green_hue,H1))
					green_hue_cor = np.hstack((green_hue_cor,H2))
					green_sat1 = np.hstack((green_sat1,S1))
					green_sat2 = np.hstack((green_sat2,S2))
					green_value = np.hstack((green_value,V2))
					#hue_sat_green.append(hue_sat)
					for i, h in enumerate(H2):
						hue_sat_green.append([h,S1[i]])
					#hue_sat_green = np.hstack((hue_sat_green,hue_sat))
					print("Green num: {}".format(green_rgb.shape))
					print("green mean rgb: {}".format(np.mean(green_rgb,axis=1)))
					print("green mean rgb cor: {}".format(np.mean(green_rgb_cor,axis=1)))
					print("green mean hue: {}".format(np.mean(green_hue)))
					print("green mean hue cor: {}".format(np.mean(green_hue_cor)))
				elif(key == ord('y')):
					yellow_rgb = np.hstack((yellow_rgb,new1))
					yellow_rgb_cor = np.hstack((yellow_rgb_cor,new2))
					yellow_hue = np.hstack((yellow_hue,H1))
					yellow_hue_cor = np.hstack((yellow_hue_cor,H2))
					yellow_sat1 = np.hstack((yellow_sat1,S1))
					yellow_sat2 = np.hstack((yellow_sat2,S2))
					yellow_value = np.hstack((yellow_value,V2))
					#hue_sat_yellow = np.hstack((hue_sat_yellow,hue_sat))
					#hue_sat_yellow.append(hue_sat)
					for i, h in enumerate(H2):
						hue_sat_yellow.append([h,S1[i]])
					print("Yellow num: {}".format(yellow_rgb.shape))
					print("yellow mean rgb: {}".format(np.mean(yellow_rgb,axis=1)))
					print("yellow mean rgb cor: {}".format(np.mean(yellow_rgb_cor,axis=1)))
					print("yellow mean hue: {}".format(np.mean(yellow_hue)))
					print("yellow mean hue cor: {}".format(np.mean(yellow_hue_cor)))

				cv2.imshow("Binary",mask1)
			points = []
			break
		elif key == ord('q'):
			esc = True
			break
		elif key == ord('s'):
			ix = None
			iy = None
			break
		elif(key == ord('n')):
			print("new video")
			cap_index += 1
			if(cap_index >= len(cap_array)):
				cap_index = 0
			cap = cv2.VideoCapture(cap_array[cap_index])
		elif(key == ord('t')):
			print("training svm")
			svm_params = dict( kernel_type = cv2.SVM_LINEAR,
                    svm_type = cv2.SVM_ONE_CLASS,
                    gamma=0.1,nu=0.1,coef0=0.1)
			svm = cv2.SVM()
			red223 = (np.float32(np.array(hue_sat_red)))
			print((np.float32(np.array(hue_sat_red))).dtype)	
			print(red223[0:4])
			svm.train(np.float32(np.array(hue_sat_red)),np.float32(np.ones(len(hue_sat_red))), params=svm_params)
			svm.save('svm_red.xml')

			svm = cv2.SVM()
			svm.train(np.float32(np.array(hue_sat_green)),np.float32(np.ones(len(hue_sat_green))), params=svm_params)
			svm.save('svm_green.xml')

			svm = cv2.SVM()
			svm.train(np.float32(np.array(hue_sat_yellow)),np.float32(np.ones(len(hue_sat_yellow))), params=svm_params)
			svm.save('svm_yellow.xml')
			break
		elif(key == ord('c')):
			ix = None
			iy = None
			if(len(points) >= 3):
				[x,y,z] = img.shape
				mask1 = np.zeros([x,y], dtype=np.uint8)
				mask2 = np.zeros(img.shape, dtype=np.uint8)
				pts = np.array(points, np.int32)
				pts = pts.reshape((-1,1,2))
				poly_roi_norm = cv2.fillPoly(mask1,[pts],255)
				
				[B1,G1,R1] = cv2.split(cimg)
				[B2,G2,R2] = cv2.split(cor_img)
				[H,S,V] = cv2.split(hsv)
				[Hc,Sc,Vc] = cv2.split(hsv_cor)

				B1 = B1[mask1 > 0] 
				G1 = G1[mask1 > 0]
				R1 = R1[mask1 > 0]
				new1 = np.vstack((B1,G1,R1))

				B2 = B2[mask1 > 0] 
				G2 = G2[mask1 > 0]
				R2 = R2[mask1 > 0]
				new2 = np.vstack((B2,G2,R2))

				H1 = H[mask1>0]
				H2 = Hc[mask1>0]

				V1 = V[mask1>0]
				V2 = Vc[mask1>0]
				S1 = S[mask1>0]
				S2 = Sc[mask1>0]


				print("Value normal: ",cv2.mean(V1))
				print("Value corrected: ",cv2.mean(V2))
				print("Sat normal: ",cv2.mean(S1))
				print("Sat corrected: ",cv2.mean(S2))
				print("hue normal: ",cv2.mean(H1))
				print("Hue corrected: ",cv2.mean(H2))
				print("RGB corrected: ",cv2.mean(B2)[0],cv2.mean(G2)[0],cv2.mean(R2)[0])
				print("RGB : ",cv2.mean(B1)[0],cv2.mean(G1)[0],cv2.mean(R1)[0])
				print("--------------------------------------------------")
			points = []
			break
			



#mean_red_rgb = np.mean(red_rgb,axis=1)
#mean_yellow_rgb = np.mean(yellow_rgb,axis=1)
#mean_green_rgb = np.mean(green_rgb,axis=1)

#mean_red_rgb_cor = np.mean(red_rgb_cor,axis=1)
#mean_yellow_rgb_cor = np.mean(yellow_rgb_cor,axis=1)
#mean_green_rgb_cor = np.mean(green_rgb_cor,axis=1)

#red_hue1 = red_hue[red_hue < 90]
#red_hue2 = red_hue[red_hue >= 90]

#mean_red_hue1 = np.mean(red_hue1)
#mean_red_hue2 = np.mean(red_hue2)
#mean_yellow_hue = np.mean(yellow_hue)
#mean_green_hue = np.mean(green_hue)

red_hue_cor1 = red_hue_cor[red_hue_cor < 90]
red_hue_cor2 = red_hue_cor[red_hue_cor >= 90]
mean_red_hue_cor1 = np.mean(red_hue_cor1)
mean_red_hue_cor2 = np.mean(red_hue_cor2)
mean_yellow_hue_cor = np.mean(yellow_hue_cor)
mean_green_hue_cor = np.mean(green_hue_cor)


#print("Mean: ",np.transpose(mean_red_rgb))
#C1 = np.transpose(red_rgb) - (mean_red_rgb)
#C2 = np.transpose(yellow_rgb) - (mean_yellow_rgb)
#C3 = np.transpose(green_rgb) - (mean_green_rgb)

#cov_red_rgb = 1/red_rgb.shape[1] * np.dot(np.transpose(C1),C1)
#cov_yellow_rgb = 1/yellow_rgb.shape[1] * np.dot(np.transpose(C2),C2)
#cov_green_rgb = 1/green_rgb.shape[1] * np.dot(np.transpose(C3),C3)

#C1 = np.transpose(red_rgb_cor) - (mean_red_rgb_cor)
#C2 = np.transpose(yellow_rgb_cor) - (mean_yellow_rgb_cor)
#C3 = np.transpose(green_rgb_cor) - (mean_green_rgb_cor)

#cov_red_rgb_cor = 1/red_rgb_cor.shape[1] * np.dot(np.transpose(C1),C1)
#cov_yellow_rgb_cor = 1/yellow_rgb_cor.shape[1] * np.dot(np.transpose(C2),C2)
#cov_green_rgb_cor = 1/green_rgb_cor.shape[1] * np.dot(np.transpose(C3),C3)

#C1 = red_hue1 - mean_red_hue1
#C2 = red_hue2 - mean_red_hue1
#print(mean_red_hue1)
#print(mean_red_hue2)
#C3 = yellow_hue - mean_yellow_hue
#C4 = green_hue - mean_green_hue

#cov_red_hue1 = 1/len(red_hue1) * np.sum(C1**2)
#if(len(red_hue2) > 0):
#	cov_red_hue2 = 1/len(red_hue2) * np.sum(C2**2)
#else:
#	cov_red_hue2 = 0
#cov_yellow_hue = 1/len(yellow_hue) * np.sum(C3**2)
#cov_green_hue = 1/len(green_hue) * np.sum(C4**2)

C1 = red_hue_cor1 - mean_red_hue_cor1
C2 = red_hue_cor2 - mean_red_hue_cor2
print(mean_red_hue_cor1)
print(mean_red_hue_cor2)
C3 = yellow_hue_cor - mean_yellow_hue_cor
C4 = green_hue_cor - mean_green_hue_cor

if(len(red_hue_cor1) > 0):
	cov_red_hue_cor1 = 1/len(red_hue_cor1) * np.sum(C1**2)
if(len(red_hue_cor2)> 0):
	cov_red_hue_cor2 = 1/len(red_hue_cor2) * np.sum(C2**2)
else:
	cov_red_hue_cor2 = 0
cov_yellow_hue_cor = 1/len(yellow_hue_cor) * np.sum(C3**2)
cov_green_hue_cor = 1/len(green_hue_cor) * np.sum(C4**2)

"""
extra = "-2"
np.save('../color_params/mean_red_rgb'+extra, mean_red_rgb)
np.save('../color_params/cov_red_rgb'+extra, cov_red_rgb)
np.save('../color_params/mean_yellow_rgb'+extra, mean_yellow_rgb)
np.save('../color_params/cov_yellow_rgb'+extra, cov_yellow_rgb)
np.save('../color_params/mean_green_rgb'+extra, mean_green_rgb)
np.save('../color_params/cov_green_rgb'+extra, cov_green_rgb)

np.save('../color_params/mean_red_rgb_cor'+extra, mean_red_rgb_cor)
np.save('../color_params/cov_red_rgb_cor'+extra, cov_red_rgb_cor)
np.save('../color_params/mean_yellow_rgb_cor'+extra, mean_yellow_rgb_cor)
np.save('../color_params/cov_yellow_rgb_cor'+extra, cov_yellow_rgb_cor)
np.save('../color_params/mean_green_rgb_cor'+extra, mean_green_rgb_cor)
np.save('../color_params/cov_green_rgb_cor'+extra, cov_green_rgb_cor)

np.save('../color_params/mean_red_hue1'+extra, mean_red_hue1)
np.save('../color_params/cov_red_hue1'+extra, cov_red_hue1)
np.save('../color_params/mean_red_hue2'+extra, mean_red_hue2)
np.save('../color_params/cov_red_hue2'+extra, cov_red_hue2)
np.save('../color_params/mean_yellow_hue'+extra, mean_yellow_hue)
np.save('../color_params/cov_yellow_hue'+extra, cov_yellow_hue)
np.save('../color_params/mean_green_hue'+extra, mean_green_hue)
np.save('../color_params/cov_green_hue'+extra, cov_green_hue)

np.save('../color_params/mean_red_hue_cor1'+extra, mean_red_hue_cor1)
np.save('../color_params/cov_red_hue_cor1'+extra, cov_red_hue_cor1)
np.save('../color_params/mean_red_hue_cor2'+extra, mean_red_hue_cor2)
np.save('../color_params/cov_red_hue_cor2'+extra, cov_red_hue_cor2)
np.save('../color_params/mean_yellow_hue_cor'+extra, mean_yellow_hue_cor)
np.save('../color_params/cov_yellow_hue_cor'+extra, cov_yellow_hue_cor)
np.save('../color_params/mean_green_hue_cor'+extra, mean_green_hue_cor)
np.save('../color_params/cov_green_hue_cor'+extra, cov_green_hue_cor)
"""
np.save('../color_params/red_hue_array', red_hue_cor)
np.save('../color_params/green_hue_array', green_hue_cor)
np.save('../color_params/yellow_hue_array', yellow_hue_cor)

"""
fig = plt.figure(1)

ax1 = fig.add_subplot(111, projection='3d', title="rgb_norm")
ax1.scatter(np.random.choice(red_rgb[0,:],size=10000,replace=False),np.random.choice(red_rgb[1,:],size=10000,replace=False)
							,np.random.choice(red_rgb[2,:],size=10000,replace=False),c='r',marker='^')
ax1.scatter(np.random.choice(yellow_rgb[0,:],size=10000,replace=False), np.random.choice(yellow_rgb[1,:],size=10000,replace=False)
							, np.random.choice(yellow_rgb[2,:],size=10000,replace=False), c='y', marker='o')
ax1.scatter(np.random.choice(green_rgb[0,:],size=10000,replace=False), np.random.choice(green_rgb[1,:],size=10000,replace=False)
							, np.random.choice(green_rgb[2,:],size=10000,replace=False), c='g', marker='8')


fig = plt.figure(2)

ax2 = fig.add_subplot(111, projection='3d', title="rgb_corrected")
ax2.scatter(np.random.choice(red_rgb_cor[0,:],size=10000,replace=False),np.random.choice(red_rgb_cor[1,:],size=10000,replace=False)
							,np.random.choice(red_rgb_cor[2,:],size=10000,replace=False),c='r',marker='^')
ax2.scatter(np.random.choice(yellow_rgb_cor[0,:],size=10000,replace=False), np.random.choice(yellow_rgb_cor[1,:],size=10000,replace=False)
							, np.random.choice(yellow_rgb_cor[2,:],size=10000,replace=False), c='y', marker='o')
ax2.scatter(np.random.choice(green_rgb_cor[0,:],size=10000,replace=False), np.random.choice(green_rgb_cor[1,:],size=10000,replace=False)
							, np.random.choice(green_rgb_cor[2,:],size=10000,replace=False), c='g', marker='8')
plt.show()
"""
"""
fig = plt.figure(3)
n, bins, patches = plt.hist(red_hue.astype(int), 50)
l = plt.plot(bins)
plt.title('red')

fig = plt.figure(4)
n, bins, patches = plt.hist(yellow_hue.astype(int), 50)
l = plt.plot(bins)
plt.title('yellow')

fig = plt.figure(5)
n, bins, patches = plt.hist(green_hue.astype(int), 50)
l = plt.plot(bins)
plt.title('green')

fig = plt.figure(6)
n, bins, patches = plt.hist(red_hue_cor.astype(int), 50)
l = plt.plot(bins)
plt.title('red_hue_cor')

fig = plt.figure(7)
n, bins, patches = plt.hist(yellow_hue_cor.astype(int), 50)
l = plt.plot(bins)
plt.title('yellow_hue_cor')

fig = plt.figure(8)
n, bins, patches = plt.hist(green_hue_cor.astype(int), 50)
l = plt.plot(bins)
plt.title('green_hue_cor')
"""



fig = plt.figure(9)
n, bins, patches = plt.hist(red_sat1.astype(int), 50)
l = plt.plot(bins)
plt.title('red sat')

fig = plt.figure(10)
n, bins, patches = plt.hist(yellow_sat1.astype(int), 50)
l = plt.plot(bins)
plt.title('yellow sat')

fig = plt.figure(11)
n, bins, patches = plt.hist(green_sat1.astype(int), 50)
l = plt.plot(bins)
plt.title('green sat')


fig = plt.figure(12)
n, bins, patches = plt.hist(red_sat2.astype(int), 50)
l = plt.plot(bins)
plt.title('red sat cor')

fig = plt.figure(13)
n, bins, patches = plt.hist(yellow_sat2.astype(int), 50)
l = plt.plot(bins)
plt.title('yellow sat cor')

fig = plt.figure(14)
n, bins, patches = plt.hist(green_sat2.astype(int), 50)
l = plt.plot(bins)
plt.title('green sat cor')

"""
fig = plt.figure(12)
n, bins, patches = plt.hist(red_value.astype(int), 50)
l = plt.plot(bins)
plt.title('red_value')

fig = plt.figure(13)
n, bins, patches = plt.hist(yellow_value.astype(int), 50)
l = plt.plot(bins)
plt.title('yellow_value')

fig = plt.figure(14)
n, bins, patches = plt.hist(green_value.astype(int), 50)
l = plt.plot(bins)
plt.title('green_value')
"""

plt.show()
