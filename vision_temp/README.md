### Computer vision and image enhancment tests

Contours steps:
 1. AdaptiveThreshold
     - cv2.adaptiveThreshold (Mean)
 2. Erode and Dilate 
     - cv2.erode, cv2.dilate
 3. Find Contours 
     - cv2.findContours  
 
![alt tag](https://github.com/arvpUofA/vision_temp/blob/master/screenshots/blobdetect.png)

Hough circle steps:
 1. AdaptiveThreshold
     - cv2.adaptiveThreshold (Guassian)
 2. Erode and Dilate 
     - cv2.erode, cv2.dilate
 3. Blur image and get Laplacian 
     - cv2.GaussianBlur, cv2.Laplacian
 4. Hough Circle  
     - cv2.HoughCircles  

 Note: On GoPro footage  
![alt tag](https://github.com/arvpUofA/vision_temp/blob/master/screenshots/houghcircle.png)

Color Quantize:
  - uses cv2.kmeans 
  Note: on GOPRO footage  
![alt tag](https://github.com/arvpUofA/vision_temp/blob/master/screenshots/kmeansGoPro.png)
