import cv2
import numpy as np
import cv2.cv as cv

"""
Class for cropping front facing camera images 
"""
class ImageCrop:
    
    def __init__(self,*args):
        self.x = 200
        self.y = 200
        self.radius = 250
        self.param1 = 100
        self.param2 = 30
        self.rad = 120
        self.minR = 0
        self.maxR = 0

        if len(args) == 5:
            self.param1 = args[0]
            self.param2 = args[1]
            self.rad = args[2]
            self.minR = args[3]
            self.maxR = args[4]


    def getCircle(self,image):

        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(img,5)
        #circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1,120,
         #                          param1=100,param2=30,minRadius=0,maxRadius=0)
        circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1,self.radius,
                                   param1=self.param1,param2=self.param2,minRadius=self.minR,maxRadius=self.maxR)
        circles = np.uint16(np.around(circles))
        #print(circles[0])
        self.x = circles[0][0][0]
        self.y = circles[0][0][1]
        self.radius = circles[0][0][2]

    def crop_image(self,img):
        height,width,depth = img.shape
    
        #draw circle and apply mask 
        circle_img = np.zeros((height,width), np.uint8)
        cv2.circle(circle_img,(self.x,self.y),self.radius,1,thickness=-1)
        masked_img = cv2.bitwise_and(img, img, mask=circle_img)

        return masked_img
