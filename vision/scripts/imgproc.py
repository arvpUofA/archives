import cv2
import numpy as np
from collections import OrderedDict
import ctypes, os

class ImgProc(object):
    def __init__(self, name, src,chain):
        self.params = {}
        self.paramInfo = OrderedDict({})
        self.chLbls = []
        self.name = name
        self.src = src
        self.chain = chain
        self.imgResult = True
        
    def updateParam(self, pName, pValue):
        self.params[pName] = pValue
        self.paramsUpdated()
    
    def paramsUpdated(self):
        pass
    
    def initParam(self, pName, default, maxVal):
        self.params[pName]= default
        self.paramInfo[pName] = maxVal

class ImgProcNative(ImgProc):
    def __init__(self, *args,**kwargs):
        super(ImgProcNative, self).__init__(*args,**kwargs)
        lib = ctypes.CDLL("libimgProcNative.so")
        self.nativeFunc = getattr(lib,self.__class__.__name__)
        self.nativeFunc.restype = ctypes.c_int32
        self.nativeFunc.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)]
        self.fn = "/dev/shm/imgproc.bmp"
        
    def callNative(self, img, ret):
        #TODO: pass image instead...
        cv2.imwrite(self.fn, img)
        return self.nativeFunc(self.fn, ret)


class RectROI(ImgProc):    
    def proc(self, img):
        if self.params:
            return img[self.params['topLeft']['y']:self.params['bottomRight']['y'],
                   self.params['topLeft']['x']:self.params['bottomRight']['x']]
        else:
            return img

"""
circular ROI
    http://answers.opencv.org/question/18784/crop-image-using-hough-circle/?answer=18796#post-id-18796
    https://stackoverflow.com/questions/10632195/define-image-roi-with-opencv-in-c
"""

class RedChannel(ImgProc):
    def proc(self, img):
        return img[..., 2]

class GaussianBlur(ImgProc):
    def __init__(self, *args,**kwargs):
        super(GaussianBlur, self).__init__(*args,**kwargs)
        self.initParam('blur', 0, 10)
    
    def proc(self, img):
        blur = self.params['blur']
        if not blur or (blur % 2 == 0):
            return img
        return cv2.GaussianBlur(img,(self.params['blur'],self.params['blur']),0)

class HSV(ImgProc):
    def __init__(self, *args,**kwargs):
        super(HSV, self).__init__(*args,**kwargs)
        self.chLbls = ['H', 'S', 'V']

    def getChLbls(self):
        return 
    def proc(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

class FilterInRange(ImgProc):
    def __init__(self, *args,**kwargs):
        super(FilterInRange, self).__init__(*args,**kwargs)
        self.chLbls = self.src.chLbls
        if not self.chLbls:
            self.chLbls = ['R','G','B']
        for chLbl in self.chLbls:
            self.initParam("%smin" % chLbl, 0, 255)
            self.initParam("%smax" % chLbl, 255, 255)
        self.thresh = {}
        self.paramsUpdated()
    
    def paramsUpdated(self):
        for minmax in 'min','max':
            vals = []
            for ch in self.chLbls:
                pname = "%s%s" % (ch, minmax)
                vals.append(self.params[pname])
            vals.reverse()
            self.thresh[minmax] = np.array(vals, dtype=np.uint8)
        
    def proc(self, img):
        return cv2.inRange(img, self.thresh['min'], self.thresh['max'])


class FilterHigh(ImgProc):
    lowerb = np.array([0,0,0], dtype=np.uint8)
    upperb = np.array([240,240,255], dtype=np.uint8)
    
    def __init__(self, *args,**kwargs):
        super(FilterHigh, self).__init__(*args,**kwargs)
        self.initParam("R", 0, 255)
        self.initParam("G", 240, 255)
        self.initParam("B", 240, 255)
        self.upper = np.array([255,255,255], dtype=np.uint8)
        self.paramsUpdated()

    def paramsUpdated(self):
        thr = []
        for c in 'B','G','R':
            thr.append(self.params[c])
        self.lower = np.array(thr, dtype=np.uint8)
    
    def proc(self, img):
        mask =  cv2.inRange(img, self.lower, self.upper)
        img = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(mask))
        return img

class ThresholdToZero(ImgProc):
    def __init__(self, *args,**kwargs):
        super(ThresholdToZero, self).__init__(*args,**kwargs)
        self.initParam('thresh', 0, 255)
    
    def proc(self, img):
        _,img = cv2.threshold(img, self.params['thresh'], 0, cv2.THRESH_TOZERO)
        return img
    
class ThreshToZeroInv3Ch(ImgProc):
    def __init__(self, *args,**kwargs):
        super(ThreshToZeroInv3Ch, self).__init__(*args,**kwargs)
        self.initParam('thresh1', 0, 255)
        self.initParam('thresh2', 0, 255)
        self.initParam('thresh3', 0, 255)
        
    def proc(self, img):
        img = img.copy()
        img1,img2,img3 = img[..., 2],img[..., 1],img[..., 0]
        _,img1 = cv2.threshold(img1, self.params['thresh1'], 0, cv2.THRESH_TOZERO_INV)
        _,img2 = cv2.threshold(img2, self.params['thresh2'], 0, cv2.THRESH_TOZERO_INV)
        _,img3 = cv2.threshold(img3, self.params['thresh3'], 0, cv2.THRESH_TOZERO_INV)
        img[..., 2],img[..., 1],img[..., 0] = img1,img2,img3 
        return img

class ErodeAndDilate(ImgProc):
    def __init__(self, *args,**kwargs):
        super(ErodeAndDilate, self).__init__(*args,**kwargs)
        for p in 'erode','dilate':
            self.initParam(p, 0, 10)
        self.kerns = {}
        self.paramsUpdated()
    
    def paramsUpdated(self):
        for op in self.paramInfo:
            if self.params[op]:
                self.kerns[op] = np.ones((self.params[op], self.params[op]),np.uint8)
            else:
                self.kerns[op] = None
    
    def proc(self, img):
        if self.kerns['erode'] is not None:
            img = cv2.erode(img, self.kerns['erode'])
        if self.kerns['dilate'] is not None:
            img = cv2.dilate(img, self.kerns['dilate'])
        return img

class BGSubtr(ImgProc):
    def __init__(self, *args,**kwargs):
        super(BGSubtr, self).__init__(*args,**kwargs)
        self.fgbg = cv2.BackgroundSubtractorMOG2()
        
    def proc(self, img):
        img = self.fgbg.apply(img, learningRate=0.001)
        _,img = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)
        return img

class CannyEdge(ImgProc):
    #seperate param for threshold2?
    def __init__(self, *args,**kwargs):
        super(CannyEdge, self).__init__(*args,**kwargs)
        self.initParam('edge', 0, 255)
    
    def proc(self, img):
        return cv2.Canny(img,self.params['edge'],self.params['edge'] * 2)

class FindContours(ImgProc):
    def proc(self, img):
        contours,_ = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return contours

class HoughCircles(ImgProc):
    def __init__(self, *args,**kwargs):
        super(HoughCircles, self).__init__(*args,**kwargs)
        self.imgResult = False
        self.initParam('edge', 0, 255)
        self.initParam('min_dist', 0, 50)
        self.initParam('circ_thresh', 0, 50)        
    
    def proc(self, img):
        md,et,ct = self.params['min_dist'], self.params['edge'], self.params['circ_thresh']
        if not(md and et and ct):
            return None
        
        return cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 1,
                                    md, np.array([]), et*2, ct)

class BlobDetectBiggest(ImgProcNative):
    def __init__(self, *args,**kwargs):
        super(BlobDetectBiggest, self).__init__(*args,**kwargs)
        self.imgResult = False
        data = [0] * 7
        self.arr = (ctypes.c_int * len(data))(*data)
        
    def proc(self, img):
        rv = self.callNative(img, self.arr)
        if rv == 1:
            return list(self.arr)
        else:
            return None

class ProcChain:
    def __init__(self, vision):
        self.vision = vision
        self.chain = OrderedDict({})
        self.curImg = {}
        self.lastImgProc = None
        self.add(RectROI, 'roi')
    
    def add(self, imgProc, name=None, src=None):
        if not name:
            name = imgProc.__name__
        if name in self.chain:
            raise Exception("imgproc %s already exists in chain" % name)
        if src:
            if src not in self.chain:
                raise Exception("source %s does not exist in chain" % src)
            src = self.chain[src]
        else:
            src = self.lastImgProc
        imgProc = imgProc(name,src,self)
        self.lastImgProc = imgProc
        self.chain[name] = imgProc

    def proc(self, img):
        self.curImg = {'orig':img}
        lastResult = img
        for imgProc in self.chain.itervalues():
            if imgProc.src:
                src = self.curImg[imgProc.src.name]
            else:
                src = lastResult
            result = imgProc.proc(src)
            if imgProc.imgResult:
                self.curImg[imgProc.name] = result
            lastResult = result 
        return lastResult
    
    def __repr__(self):
        return str(self.chain)
