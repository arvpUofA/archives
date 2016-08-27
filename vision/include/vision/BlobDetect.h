#ifndef BLOBDETECT_H
#define BLOBDETECT_H

#include <stdio.h>
#include <sys/time.h>
#include <opencv/cv.h>
#include <opencv/highgui.h>
#include <vision/cvblob.h>

extern "C" {
	int BlobDetectBiggest(const char* path, int* data);
}
#endif
