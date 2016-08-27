#include <vision/BlobDetect.h>

int BlobDetectBiggest(const char* path, int* data) {
	IplImage* filtered = cvLoadImage (path, 0);
	if (!filtered) {
		fprintf(stderr, "Blob Detector: cannot load image\n");
		return -1;
	}
	CvBlobs* blobs = new CvBlobs();
	IplImage* labelImg = cvCreateImage(cvGetSize(filtered),IPL_DEPTH_LABEL,1);
	cvLabel(filtered, labelImg, *blobs);
	unsigned int maxArea = 0;
	CvBlob *biggestBlob = NULL;
	for (CvBlobs::const_iterator it=blobs->begin(); it!=blobs->end(); ++it) {
		CvBlob *blob = it->second;
		if (blob->area >= maxArea) {
			maxArea = blob->area;
			biggestBlob = blob;
		}
	}
	int rv;
	if (biggestBlob) {
		*data++ = (int)biggestBlob->centroid.x;
		*data++ = (int)biggestBlob->centroid.y;
		*data++ = biggestBlob->minx;
		*data++ = biggestBlob->maxx;
		*data++ = biggestBlob->miny;
		*data++ = biggestBlob->maxy;

		cvCentralMoments(biggestBlob,labelImg);
		*data++ = (int)(cvAngle(biggestBlob)*57.2957795);
		rv = 1;
	}
	else
		rv = 0;


	cvReleaseBlobs(*blobs);
	delete blobs;
	cvReleaseImage(&filtered);
	cvReleaseImage(&labelImg);
	return rv;
}
