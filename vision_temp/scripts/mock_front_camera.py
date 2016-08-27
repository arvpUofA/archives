#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np

class UsbCamera:
	def __init__(self):
		self.bridge = CvBridge()
		rospy.init_node('usb_camera', anonymous=True)
		self.image_pub = rospy.Publisher("/front/camera/image_raw",Image,queue_size=1)
		#self.orb=cv2.ORB()
	def main(self,args):
		rate = rospy.Rate(15)
		#cap = cv2.VideoCapture('../testvids/pool3buoy.avi')
		cap = cv2.VideoCapture(1)
		#cap = cv2.VideoCapture("../testvids/horz.avi")
		#cap = cv2.VideoCapture('../testvids/muddyBuoy.mpg')
		#cap = cv2.VideoCapture('../testvids/FarNotGoodBouy.mpg')
		#cap = cv2.VideoCapture('../testvids/UAlbertaPoolBuoy.mpg')
		#cap = cv2.VideoCapture('../testvids/FullBuoy.mpg')
		#cap = cv2.VideoCapture('../testvids/BrightWaterBuoy.mpg')
		#cap = cv2.VideoCapture('../testvids/GP010017.MP4')
		#cap = cv2.VideoCapture('../testvids/front_comp.avi')
		while(not rospy.is_shutdown()):
			rate.sleep()
			ret, frame = cap.read()
			#frame = cv2.resize(frame,None,fx=0.45, fy=0.45, interpolation = cv2.INTER_AREA)
			print(np.shape(frame))
			# find the keypoints with ORB
			#kp = self.orb.detect(frame,None)
			# compute the descriptors with ORB
			#kp, des = self.orb.compute(frame, kp)
			#frame = cv2.drawKeypoints(frame,kp,color=(0,255,0), flags=0)
			#cv2.imshow("orb",frame)
			#cv2.waitKey(1)
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(frame,encoding='bgr8'))

if __name__ == '__main__':
    camera = UsbCamera()
    camera.main(sys.argv)
