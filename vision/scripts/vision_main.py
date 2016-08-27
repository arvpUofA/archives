#!/usr/bin/python
from gui import GUI
import rospy
from imgsource import ROSLive
import traceback
import time
from arvp_main.msg import TargetInfo, IMU, Depth  
import tasks
import vision.srv
from optparse import OptionParser

OLD_PUB_TYPE = True

class Vision:
    def __init__(self, src, gui=False, publish=False, camera='horiz'):
        self.rosPub = None
        self.task = None
        self.camera = camera
        if src == ROSLive:
            self.initROS(gui, publish, camera)
        else:
            self.src = src
        if gui:
            self.gui = GUI(self, startPaused=(not self.src.live))
        else:
            self.gui = None
    
    def initROS(self, gui, publish, camera):
        nodename = 'vision'
        anon = False
        if gui:
            nodename += "_GUI"
            anon = True
        rospy.init_node(nodename, anonymous=anon)
        self.src = ROSLive(camera)
        updateParamsSvcName = '/%s/UpdateParams' % camera
        if publish:
            if OLD_PUB_TYPE:
                self.rosPub = {
                    'horiz': rospy.Publisher("/vision/horiz", IMU, queue_size=10),
                    'vert': rospy.Publisher("/vision/vert", Depth, queue_size=10),
                    'angle': rospy.Publisher("/vision/angle", IMU, queue_size=10), 
                }
                self.msg = {
                    'horiz': IMU(),
                    'vert': Depth(),
                    'angle': IMU(),
                }
            else:
                self.rosPub = rospy.Publisher("/%s/targetInfo" % camera, TargetInfo, queue_size=10)
                self.msg = TargetInfo()
            if not gui:
                rospy.Service(updateParamsSvcName, vision.srv.UpdateParams, self.rosParamsUpdated)
        if gui and not publish:
            self.rosSendUpdateParams = rospy.ServiceProxy(updateParamsSvcName, vision.srv.UpdateParams)
    
    def setTask(self, task):
        self.task = task
        if isinstance(self.src, ROSLive):
            if rospy.has_param(self.getROSParamName()):
                self.setInitialParams(rospy.get_param(self.getROSParamName()))
                print "initial"
                for n,proc in self.task.chain.chain.iteritems():
                    print n, proc.params
    
    def shouldRun(self):
        if isinstance(self.src, ROSLive):
            return (not rospy.is_shutdown())
        else:
            return True
    
    def run(self):
        while self.shouldRun():
            try:
                img = self.src.getNextFrame()
                if img is None:
                    rospy.logwarn("did not get image!")
                    continue
                targetInfo = self.proc(img)
                #print "target info", targetInfo
                if self.gui:
                    if self.procGUI(img) == 'quit':
                        break
                if targetInfo is not None and self.rosPub:  
                    if OLD_PUB_TYPE:
                        self.publishOld(targetInfo)
                    else:                  
                        self.publish(targetInfo)
            except KeyboardInterrupt:
                break
            except NotImplementedError:
                print "Operation not implemented yet."
            except:
                traceback.print_exc()
                time.sleep(0.1)
                
    def proc(self, img):
        if self.gui: 
            self.gui.lock.acquire()
            if self.gui.paused:
                img = img.copy()
        result = self.task.proc(img)
        if self.gui: 
            self.gui.lock.release()
        return result
                
    def procGUI(self, img):
        while self.gui.paused:
            cmd = self.gui.cmdQueue.get()
            if cmd == 'step forward' or cmd == 'resume':
                break
            if cmd == 'step backward' and not self.src.live:
                self.src.seekToPrev()
                break
            if cmd == 'reproc':
                self.proc(img)
            if cmd == 'quit':
                return cmd
    
    def setInitialParams(self, params):
        for procName,params in params.iteritems():
            self.setParams(procName, params)
    
    def setParams(self, procName, params):
        for pName,pValue in params.iteritems():
            self.updateParam(procName, pName, pValue)
    
    def updateParam(self, procName, pName, pValue):
        if procName not in self.task.chain.chain: return
        self.task.chain.chain[procName].updateParam(pName, pValue)
        if isinstance(self.src, ROSLive) and self.gui and not self.rosPub:
            rospy.set_param(self.getROSParamName(procName, pName), pValue)
            try:
                self.rosSendUpdateParams(procName)
            except (rospy.exceptions.ROSException, rospy.service.ServiceException):
                rospy.logwarn("Cannot update parameters on EC node")
    
    def getROSParamName(self, procName="", pName=""):
        return "/%s/%s/%s/%s" % (self.camera, self.task.__class__.__name__, procName, pName)
    
    def rosParamsUpdated(self, req):
        newparams = rospy.get_param(self.getROSParamName(req.imgproc))
        self.setParams(req.imgproc, newparams)
        rospy.loginfo("updating params  for %s: %s" % (req.imgproc, newparams))
        print self.task.chain.chain[req.imgproc].params
        return True
    
    def publish(self, targetInfo):
        self.msg.header.stamp = rospy.Time.now()
        self.msg.x,self.msg.y,self.msg.angle = targetInfo 
        self.rosPub.publish(self.msg)
    
    def publishOld(self, targetInfo):
        x,y,angle = targetInfo
        self.msg['horiz'].header.stamp = rospy.Time.now()
        self.msg['horiz'].heading = 100-x
        self.rosPub['horiz'].publish(self.msg['horiz'])
        self.msg['vert'].header.stamp = rospy.Time.now()
        self.msg['vert'].depth = y
        self.rosPub['vert'].publish(self.msg['vert'])

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-g", dest="gui", action="store_true", help="enable gui")
    parser.add_option("-p", dest="publish", action="store_true", help="publish target info")
    (options, args) = parser.parse_args()
    if options.publish:
        print "Will publish target info"
    
    vision = Vision(ROSLive, gui=options.gui, publish=options.publish)
    vision.setTask(tasks.BuoyHoughCircles(vision)) 
    vision.run()
