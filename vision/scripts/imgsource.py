from cv_bridge import CvBridge
import rosbag
import cv2
import rospy
import sensor_msgs.msg
import threading

class ImageSource(object):
    def __init__(self, resize=None):
        self.live = False
        self.resize = resize
    
    def getNextFrame(self):
        img = self.getNextImage()
        if img is None and not self.live:
            self.seek(0)
            img = self.getNextImage()
        if img is not None and self.resize:
            img = cv2.resize(img, self.resize) 
        return img

class ROSSource(ImageSource):
    def __init__(self, cameraName, *args,**kwargs):
        super(ROSSource, self).__init__(*args,**kwargs)
        self.bridge = CvBridge()
        self.topic =  "/%s/camera/image_raw" % cameraName
        
    def getOCVImage(self, msg):
        return self.bridge.imgmsg_to_cv2(msg, "bgr8")
    
class ROSLive(ROSSource):
    def __init__(self, *args,**kwargs):
        super(ROSLive, self).__init__(*args,**kwargs)
        rospy.loginfo("Subscribing to %s" % self.topic)
        rospy.Subscriber(self.topic, sensor_msgs.msg.Image, self.newROSImage)
        self.live = True
        self.curImg = None
        self.hasNew = threading.Condition()
    
    def newROSImage(self, msg):
        self.hasNew.acquire()
        self.curImg = self.getOCVImage(msg) 
        self.hasNew.notify()
        self.hasNew.release()
    
    def getNextImage(self):
        self.hasNew.acquire()
        while self.curImg is None and not rospy.is_shutdown():
            self.hasNew.wait(1)
        img = self.curImg
        self.curImg = None
        self.hasNew.release()
        return img
        
class ROSBagSource(ROSSource):
    def __init__(self, bagfname, *args,**kwargs):
        super(ROSBagSource, self).__init__(*args, **kwargs)
        self.bag = rosbag.Bag(bagfname)
        self.seek(0)
        
    def seek(self, pos):
        if pos != 0: 
            raise NotImplementedError()
        self.msgIter = self.bag.read_messages(topics=self.topic)
    def seekToPrev(self):
        raise NotImplementedError()
    def getNextImage(self):
        _,msg,_ = self.msgIter.next()
        return self.getOCVImage(msg)

class bidirectional_iterator(object):
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    def next(self):
        try:
            result = self.collection[self.index]
            self.index += 1
        except IndexError:
            raise StopIteration
        return result

    def prev(self):
        self.index -= 1
        if self.index < 0:
            raise StopIteration
        return self.collection[self.index]

    def __iter__(self):
        return self

class ImageFiles(ImageSource):
    def __init__(self, files, bayer=False, *args,**kwargs):
        super(ImageFiles, self).__init__(*args,**kwargs)
        if not files:
            raise Exception("No files given to ImageFiles source")
        self.files = files
        self.bayer = bayer
        self.seek(0)
        
    def seek(self, pos):
        if pos != 0: 
            raise NotImplementedError()
        self.iterator = bidirectional_iterator(self.files)
        
    def seekToPrev(self):
        self.iterator.index -= 2
        
    def getNextImage(self):
        try:
            fn = self.iterator.next()
        except StopIteration:
            return None 
        print fn
        color = int(self.bayer == False)
        img = cv2.imread(fn, color)
        if self.bayer:
            img = cv2.cvtColor(img, cv2.COLOR_BAYER_BG2BGR)
        return img

class VideoSource(ImageSource):
    def __init__(self, videoFile, *args,**kwargs):
        super(VideoSource, self).__init__(*args,**kwargs)
        self.cap = cv2.VideoCapture(videoFile)
        self.seek(0)
    
    def seek(self, pos):
        self.cap.set(cv2.cv.CV_CAP_PROP_POS_MSEC, pos)
    
    def getNextImage(self):
        _,img = self.cap.read()
        return img

