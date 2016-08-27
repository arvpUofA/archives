#!/usr/bin/env python
from __future__ import print_function
import sys
import rospy
from image_proc import ImageProc
from buoy_detect import BlobDetector, HSVBlobDetect, SatBlobDetector
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA
from std_msgs.msg import Int16
from cv_bridge import CvBridge, CvBridgeError
from dynamic_reconfigure.server import Server
from vision_temp.cfg import VisionBridgeConfig


class VisionBridge:
    """
    Converts ROS formatted images to OpenCV formatted and publishes vision
    """
    def __init__(self):
        """Constructor"""
        self.bridge = CvBridge()
        self.ip = ImageProc()
        self.hsv_thresholder = HSVBlobDetect()
        self.sat_thres = SatBlobDetector()
        self.blob_detector = BlobDetector()
        self.front_img = None
        self.bottom_img = None
        self.gotColors = False
        self.process_color = 'red'
        rospy.init_node('image_bridge', anonymous=True)
        self.srv = Server(VisionBridgeConfig, self.reconfigure)

        # publishers
        self.front_pub = rospy.Publisher("front_view", Image, queue_size=5)
        self.algorithm_pub = rospy.Publisher("buoy_detection", Image, queue_size=1)
        self.binary_pub = rospy.Publisher("binary", Image, queue_size=1)
        #self.center_pub = rospy.Publisher("/vision/buoy_center", Point, queue_size=5)
        self.rgb_pub = rospy.Publisher("/vision/front_mean_rgb", ColorRGBA, queue_size=5)
        self.hue_pub = rospy.Publisher("/vision/front_mean_hue", Int16, queue_size=5)
        self.red_buoy_pub = rospy.Publisher("/vision/red_buoy", Point, queue_size=1)
        self.yellow_buoy_pub = rospy.Publisher("/vision/yellow_buoy", Point, queue_size=1)
        self.green_buoy_pub = rospy.Publisher("/vision/green_buoy", Point, queue_size=1)

        # subscribers
        self.image_sub = rospy.Subscriber("/front/camera/image_raw", Image,
                                          self.sub_front_callback, queue_size=1)
        #self.image_sub = rospy.Subscriber("/cv_camera/image_raw", Image,
        #                                  self.sub_front_callback, queue_size=1)
        self.image_sub = rospy.Subscriber("/bottom/camera/image_raw", Image,
                                          self.sub_bottom_callback, queue_size=1)

    def reconfigure(self, config, level):
        rospy.loginfo("dynamic_reconfigure")
        self.buoy_detection = config.buoy_detection

        self.blob_detector.setAttributes(min_area=config.min_area, max_length=config.max_length,
                                        circularity=config.circularity_min,
                                        aspect_ratio_diff=config.aspect_ratio_diff)

        self.blob_detector.setAttributes(ad_size=config.ad_size, ad_method=config.ad_guassian,
                                        erode_size=config.erosion_size,
                                        erode_iterations=config.erosion_iterations,
                                        dilate_size=config.dilation_size,
                                        dilate_iterations=config.dilation_iterations)

        self.sat_thres.setAttributes(ad_size=config.ad_size,
                                        erode_size=config.erosion_size,
                                        erode_iterations=config.erosion_iterations,
                                        dilate_size=config.dilation_size,
                                        dilate_iterations=config.dilation_iterations)

        self.hsv_thresholder.setAttributes(erode_size=config.erosion_size,
                                        erode_iterations=config.erosion_iterations,
                                        dilate_size=config.dilation_size,
                                        dilate_iterations=config.dilation_iterations)


        self.hsv_thresholder.setAttributes(min_area=config.min_area, max_length=config.max_length,
                                        circularity=config.circularity_min,
                                        aspect_ratio_diff=config.aspect_ratio_diff)

        self.hsv_thresholder.setAttributes(red_high_upper=config.red_high_upper,red_high_lower=config.red_high_lower,
                                            red_low_upper=config.red_low_upper,red_low_lower=config.red_low_lower,
                                            yellow_upper=config.yellow_upper,yellow_lower=config.yellow_lower,
                                            green_upper=config.green_upper,green_lower=config.green_lower)

        return config

    def sub_front_callback(self, data):
        try:
            rospy.set_param('image_center_point', {'x': data.width / 2, 'y': data.height / 2})
            self.screen_center = [data.width / 2, data.height / 2]
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.front_img = cv_image
        except CvBridgeError as e:
            print(e)

    def sub_bottom_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.bottom_img = cv_image
        except CvBridgeError as e:
            print(e)

    def get_front_image(self):
            return self.front_img

    def publish_front_view(self):
        img = self.get_front_image()
        self.front_pub.publish(self.bridge.cv2_to_imgmsg(img, encoding='passthrough'))

    def publish_bottom_view(self):
        bottom = self.getBottomImage()
        self.bottom_pub.publish(self.bridge.cv2_to_imgmsg(bottom, "bgr8"))

    def publish_algorithm(self):
        front = self.get_front_image()
        # Adaptive thresholding
        if(self.buoy_detection == 1):
            img, binary = self.blob_detector.process(front, 1)
            self.algorithm_pub.publish(self.bridge.cv2_to_imgmsg(img,
                                       encoding='bgr8'))
            self.binary_pub.publish(self.bridge.cv2_to_imgmsg(binary,
                                    encoding='passthrough'))

            centers = self.blob_detector.getCenters()
            msg = Point()
            for c in centers:
                msg.x = centers[0][0]
                msg.y = centers[0][1]
                msg.z = centers[0][2]
                if(centers[0][3] == 'red'):
                    self.red_buoy_pub.publish(msg)
                elif(centers[0][3] == 'yellow'):
                    self.yellow_buoy_pub.publish(msg)
                elif(centers[0][3] == 'green'):
                    self.green_buoy_pub.publish(msg)
        # HSV Thresholding
        elif(self.buoy_detection == 2):
            img,binary = self.hsv_thresholder.process(front)
            self.algorithm_pub.publish(self.bridge.cv2_to_imgmsg(img, encoding='bgr8'))
            self.binary_pub.publish(self.bridge.cv2_to_imgmsg(binary,
                                    encoding='passthrough'))
            centers = self.hsv_thresholder.getCenters()
            msg = Point()
            if(len(centers) > 0):
                msg.x = centers[0][0]
                msg.y = centers[0][1]
                msg.z = centers[0][2]
                if(centers[0][3] == 'red'):
                    self.red_buoy_pub.publish(msg)
                    print("red: {}".format(msg.z))
                elif(centers[0][3] == 'yellow'):
                    self.yellow_buoy_pub.publish(msg)
                    print("yellow: {}".format(msg.z))
                else:
                    self.green_buoy_pub.publish(msg)
                    print("green: {}".format(msg.z))
        #Sat Adaptive thresholding
        elif(self.buoy_detection == 3):
            img, binary = self.sat_thres.process(front)
            self.algorithm_pub.publish(self.bridge.cv2_to_imgmsg(img,
                                       encoding='bgr8'))
            self.binary_pub.publish(self.bridge.cv2_to_imgmsg(binary,
                                    encoding='passthrough'))

            centers = self.sat_thres.getCenters()
            msg = Point()
            for c in centers:
                msg.x = centers[0][0]
                msg.y = centers[0][1]
                msg.z = centers[0][2]
                if(centers[0][3] == 'red'):
                    self.red_buoy_pub.publish(msg)
                elif(centers[0][3] == 'yellow'):
                    self.yellow_buoy_pub.publish(msg)
                elif(centers[0][3] == 'green'):
                    self.green_buoy_pub.publish(msg)
            
    def publish_mean_color(self):
        hue = Int16()
        rgb = ColorRGBA()
        hue.data = self.ip.get_mean_hue(self.get_front_image())
        mean_vals = self.ip.get_mean_rgb(self.get_front_image())
        rgb.b = mean_vals[0]
        rgb.g = mean_vals[1]
        rgb.r = mean_vals[2]
        self.rgb_pub.publish(rgb)
        self.hue_pub.publish(hue)

    def main(self, args):
        rate = rospy.Rate(40)
        while(not rospy.is_shutdown()):
            if(self.front_img is not None):
                self.publish_algorithm()
                self.publish_mean_color()

            rate.sleep()

if __name__ == '__main__':
    bridge = VisionBridge()
    bridge.main(sys.argv)
