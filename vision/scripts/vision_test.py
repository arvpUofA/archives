#!/usr/bin/python

import sys
sys.path.insert(0, '/opt/opencv/lib/python2.7/dist-packages')

import os
import imgsource
from vision_main import Vision  # @UnresolvedImport
from glob import glob
import tasks


def getBag(bagFile, cameraName):
    path = os.path.expanduser("~/catkin/bagfiles/") + bagFile
    return imgsource.ROSBagSource(path, cameraName)

def getTestImgs():
    files = sorted(glob(os.path.expanduser("~/catkin/src/vision/test_imgs/*")))
    return imgsource.ImageFiles(files)

def runTest(src, task, initialParams={}, publish=False): 
    v = Vision(src, gui=True,publish=publish)
    v.setTask(task(v))
    v.setInitialParams(initialParams)
    v.run()

def runTestBuoyHoughCircles(src, roi={}):
    initialParams = {
        'roi': roi,
        'GaussianBlur': {'blur': 5},
        'HoughCircles': {'edge': 180, 'min_dist': 30, 'circ_thresh': 17}
    }
    runTest(src, tasks.BuoyHoughCircles, initialParams)

def runTestBuoyColorOnly(src, roi={}):
    initialParams = {
        'roi': roi,
        'HSV filter': {'Hmin': 144, 'Smax': 158},
        'ErodeAndDilate': {'erode': 4, 'dilate': 4},
    }
    runTest(src, tasks.BuoyColorOnly, initialParams)

runTestBuoyHoughCircles(getTestImgs())
#runTestBuoyColorOnly(getTestImgs())

# src = imgsource.VideoSource("gopro/2015_06_21/100GOPRO/GOPR0005.MP4", resize=(853, 480))
# src.seek(30*1000)
# runTestBuoyHoughCircles(src)

# roi = {'topLeft': {'x':170, 'y': 110}, 'bottomRight': {'x': 480, 'y':315}}
# runTestBuoyHoughCircles(getBag('2015-07-12-13-56-09.bag', 'horiz'), roi)
