import cv2
from threading import Thread, Lock
from Queue import Queue
import sys
import traceback
import time

class ImgWin():
    def __init__(self, name, gui, params = {}, paramInfo = {}):
        self.name = name
        self.img = None
        self.visible = False
        self.params = params
        self.paramInfo = paramInfo
        self.gui = gui
    
    def show(self):
        cv2.namedWindow(self.name, cv2.WINDOW_AUTOSIZE )
        self.addParamControls()
        self.loadWindowParameters()
        self.visible = True
        self.update()
    
    def hide(self):
        cv2.destroyWindow(self.name)
        self.visible = False
    
    def loadWindowParameters(self):
        pass
    
    def saveWindowParameters(self):
        pass
    
    def addParamControls(self):
        for pname,maxVal in self.paramInfo.iteritems():
            if isinstance(maxVal, int):
                cv2.createTrackbar(pname,self.name,self.params[pname],maxVal,self.trackBarUpdate)
    
    def trackBarUpdate(self, val):
        #TODO: combine and call setParams instead...
        for pname in self.paramInfo:
            self.gui.vision.updateParam(self.name, pname, cv2.getTrackbarPos(pname, self.name))
        self.gui.cmdQueue.put("reproc")
    
    def update(self):
        if self.visible and self.img is not None:
            cv2.imshow(self.name, self.img)
        
    def setImg(self, img):
        self.img = img
        self.update()
        
    def circle(self, x, y):
        if self.visible and self.img is not None:
            imgC = self.img.copy()
            cv2.circle(imgC, (x,y), 5, (255,255,255))
            cv2.imshow(self.name, imgC)

KeyCodes = {'right': 65363, 'left': 65361}
class GUI:
    def __init__(self, vision, startPaused):
        self.vision = vision
        self.paused = startPaused
        self.wins = {}
        self.cmdQueue = Queue()
        self.task = None
        self.lock = Lock()
        Thread(target=self.run, args=(), name="Vision GUI").start()
    
    def run(self):
        #TODO: only update when new image or cur image reprocessed
        while self.vision.shouldRun():
            try:
                if self.task != self.vision.task:
                    self.task = self.vision.task
                    self.removeAllWins()
                    self.initWins()
                if self.task:
                    with self.lock:
                        self.update()
                k = cv2.waitKey(100)
                if self.handleKey(k) == 'quit':
                    break
            except:
                traceback.print_exc()
                time.sleep(0.1)
            
    def initWins(self):
        self.addWin('orig', True)
        for imgProc in self.task.chain.chain.itervalues():
            self.addWin(imgProc.name, True, imgProc.params, imgProc.paramInfo)
            
    def removeAllWins(self):
        for win in self.wins.keys():
            self.removeWin(win)
            
    def addWin(self, name, show, params = {}, paramInfo={}):
        self.wins[name] = ImgWin(name, self, params, paramInfo)
        if show:
            self.wins[name].show()
    
    def removeWin(self, name):
        self.wins[name].hide()
        del self.wins[name]
        
    def update(self):
        for name in self.wins:
            cur = self.task.chain.curImg
            if name in cur:
                self.wins[name].setImg(cur[name])
    
    def handleKey(self, k):
        if k == ord(' '):
            self.paused = not self.paused
            if not self.paused:
                self.cmdQueue.put("resume")
        if k == KeyCodes['right'] or k == ord('x'):
            self.cmdQueue.put('step forward')
        if k == KeyCodes['left'] or k == ord('z'):
            self.cmdQueue.put('step backward')
        if k == ord('s'):
            for win in self.wins.itervalues():
                win.saveWindowParameters()
        if k == ord('q') or k == 27:
            self.cmdQueue.put('quit')
            return 'quit'
