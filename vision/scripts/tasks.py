import imgproc
import cv2
import numpy as np

class VisionTask(object):
    def __init__(self, vision):
        self.vision = vision
        self.chain = imgproc.ProcChain(vision)
        
    def proc(self, img):
        return self.chain.proc(img)
    
    def toPercent(self, img, x, y):
        height,width,_ = img.shape
        return x*100.0/width, y*100.0/height

class BuoyHoughCircles(VisionTask):
    def __init__(self, *args,**kwargs):
        super(BuoyHoughCircles, self).__init__(*args, **kwargs)
        self.chain.add(imgproc.RedChannel)
        self.chain.add(imgproc.GaussianBlur)
        self.chain.add(imgproc.HoughCircles)
    
    def proc(self, img):
        circles = super(BuoyHoughCircles, self).proc(img)
        if circles is None:
            if self.vision.gui:
                self.chain.curImg['HoughCircles'] = self.chain.curImg['roi']
            return None
        else:
            x,y,radius =  circles[0][0]
            xPercent, yPercent = self.toPercent(self.chain.curImg['roi'], x, y)
            targetInfo = xPercent,yPercent,0
            if self.vision.gui:
                try:
                    self.showTargetInfo(circles)
                except Exception as e:
                    print e
            return targetInfo
    
    def showTargetInfo(self, circles):
        oimg = self.chain.curImg['roi'].copy()
        for i in range(circles.shape[1]):
            c = circles[0][i]
            x,y,radius = c
            minx,maxx = x-radius,x+radius
            miny,maxy = y-radius,y+radius
            if minx < 0: minx = 0
            if miny < 0: miny = 0
            circRect = oimg[miny:maxy, minx:maxx]
            mean = cv2.mean(circRect) 
            print (x,y), mean
            cv2.circle(oimg, (x,y), radius, (0, 0, 255), 3, cv2.CV_AA)
            cv2.circle(oimg, (x,y), 2, (0, 255, 0), 3, cv2.CV_AA) # draw center of circle
        print
        self.chain.curImg['HoughCircles'] = oimg

class BuoyColorOnly(VisionTask):
    def __init__(self, *args,**kwargs):
        super(BuoyColorOnly, self).__init__(*args, **kwargs)
        self.chain.add(imgproc.HSV)
        self.chain.add(imgproc.FilterInRange, "HSV filter")
        self.chain.add(imgproc.ErodeAndDilate)
        self.chain.add(imgproc.BlobDetectBiggest)
    
    def proc(self, img):
        blobInfo = super(BuoyColorOnly, self).proc(img)
        if not blobInfo:
            if self.vision.gui:
                self.chain.curImg['BlobDetectBiggest'] = self.chain.curImg['roi']
            return None
        else:
            x,y,minx,maxx,miny,maxy,angle = blobInfo
            xPercent, yPercent = self.toPercent(img, x, y)
            targetInfo = xPercent,yPercent,0
            if self.vision.gui:
                try:
                    self.showTargetInfo(blobInfo)
                except Exception as e:
                    print e
            return targetInfo
        
    def showTargetInfo(self, blobInfo):
        x,y,minx,maxx,miny,maxy,angle = blobInfo
        oimg = self.chain.curImg['roi'].copy()
        cv2.circle(oimg, (x,y), 5, (255,255,255))
        cv2.rectangle(oimg,(minx,miny), (maxx,maxy), 255)
        self.chain.curImg['BlobDetectBiggest'] = oimg

class PathRect(VisionTask):
    def __init__(self, *args,**kwargs):
        super(PathRect, self).__init__(*args, **kwargs)
        self.chain.add(imgproc.RedChannel)
        self.chain.add(imgproc.GaussianBlur)
        self.chain.add(imgproc.CannyEdge)
        self.chain.add(imgproc.FindContours)
    
    def proc(self, img):
        contours = super(PathRect, self).proc(img)
        oimg = self.chain.curImg['roi'].copy()
        for cnt in contours:
            if cv2.contourArea(cnt) < 1:
                continue
            rect = cv2.minAreaRect(cnt)
            ((x,y),(width,height),angle) = rect
            print x,y,width,height,angle
            if self.vision.gui:
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(oimg,[box],0,(0,0,255),2)
        print
        self.chain.curImg['FindContours'] = oimg
        
        
