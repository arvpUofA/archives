// Copyright (C) 2007 by Cristóbal Carnero Liñán
// grendel.ccl@gmail.com
//
// This file is part of cvBlob.
//
// cvBlob is free software: you can redistribute it and/or modify
// it under the terms of the Lesser GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// cvBlob is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// Lesser GNU General Public License for more details.
//
// You should have received a copy of the Lesser GNU General Public License
// along with cvBlob.  If not, see <http://www.gnu.org/licenses/>.
//

#include <cmath>
#include <iostream>
using namespace std;

#ifdef WIN32
#include <cv.h>
#else
#include <opencv/cv.h>
#endif

#include <vision/cvblob.h>

CvLabel cvGreaterBlob(const CvBlobs &blobs)
{
	CvLabel label=0;
	unsigned int maxArea=0;

	for (CvBlobs::const_iterator it=blobs.begin();it!=blobs.end();++it)
	{
		CvBlob *blob=(*it).second;
		//if ((!blob->_parent)&&(blob->area>maxArea))
		if (blob->area>maxArea)
		{
			label=blob->label;
			maxArea=blob->area;
		}
	}

	return label;
}

void cvFilterByArea(CvBlobs &blobs, unsigned int minArea, unsigned int maxArea)
{
	CvBlobs::iterator it=blobs.begin();
	while(it!=blobs.end())
	{
		CvBlob *blob=(*it).second;
		if ((blob->area<minArea)||(blob->area>maxArea))
		{
			delete blob;
			CvBlobs::iterator tmp=it;
			++it;
			blobs.erase(tmp);
		}
		else
			++it;
	}
}

void cvCentralMoments(CvBlob *blob, const IplImage *img)
{
	if (!blob->centralMoments)
	{
		if((img->depth!=IPL_DEPTH_LABEL)||(img->nChannels!=1))
		{
			cerr<<"Error: Image format."<<endl;
			return; /// TODO: Errores.
		}

		//cvCentroid(blob); // Here?

		blob->u11=blob->u20=blob->u02=0.;

		// Only in the bounding box
		CvLabel *imgData=(CvLabel *)img->imageData+(img->widthStep/(img->depth/8))*blob->miny;
		for (unsigned int r=blob->miny;
		r<blob->maxy;
		r++,imgData+=img->widthStep/(img->depth/8))
			for (unsigned int c=blob->minx;c<blob->maxx;c++)
				if (imgData[c]==blob->label)
				{
					double tx=(c-blob->centroid.x);
					double ty=(r-blob->centroid.y);
					blob->u11+=tx*ty;
					blob->u20+=tx*tx;
					blob->u02+=ty*ty;
				}

		blob->centralMoments = true;
	}
}

///////////////////////////////////////////////////////////////////////////////////////////////////
// Based on http://en.wikipedia.org/wiki/HSL_and_HSV

/// \def _HSV2RGB_(H, S, V, R, G, B)
/// \brief Color translation between HSV and RGB.
#define _HSV2RGB_(H, S, V, R, G, B) \
	{ \
	double _h = H/60.; \
	int _hf = floor(_h); \
	int _hi = ((int)_h)%6; \
	double _f = _h - _hf; \
	\
	double _p = V * (1. - S); \
	double _q = V * (1. - _f * S); \
	double _t = V * (1. - (1. - _f) * S); \
	\
	switch (_hi) \
	{ \
	case 0: \
	R = 255.*V; G = 255.*_t; B = 255.*_p; \
	break; \
	case 1: \
	R = 255.*_q; G = 255.*V; B = 255.*_p; \
	break; \
	case 2: \
	R = 255.*_p; G = 255.*V; B = 255.*_t; \
	break; \
	case 3: \
	R = 255.*_p; G = 255.*_q; B = 255.*V; \
	break; \
	case 4: \
	R = 255.*_t; G = 255.*_p; B = 255.*V; \
	break; \
	case 5: \
	R = 255.*V; G = 255.*_p; B = 255.*_q; \
	break; \
	} \
	}
///////////////////////////////////////////////////////////////////////////////////////////////////

struct Color { unsigned char r,g, b; };
typedef std::map<CvLabel, Color> Palete;

void cvRenderBlobs(const IplImage *imgLabel, const CvBlobs &blobs, IplImage *imgSource, IplImage *imgDest)
{
	unsigned short mode=0x000f;
	if((imgLabel->depth!=IPL_DEPTH_LABEL)||(imgLabel->nChannels!=1))
	{
		cerr<<"Error: Label image format."<<endl;
		return; /// TODO: Errores.
	}

	if((imgDest->depth!=IPL_DEPTH_8U)||(imgDest->nChannels!=3))
	{
		cerr<<"Error: Output image format."<<endl;
		return; /// TODO: Errores.
	}

	/*if (mode&CV_BLOB_RENDER_COLOR)
	{
		Palete pal;

		unsigned int colorCount = 0;
		for (CvBlobs::const_iterator it=blobs.begin(); it!=blobs.end(); ++it)
		{
			CvLabel label = (*it).second->label;

			Color color;

			_HSV2RGB_((double)((colorCount*77)%360), .5, 1., color.r, color.g, color.b);
			colorCount++;

			pal[label] = color;
		}

		CvLabel *labels = (CvLabel *)imgLabel->imageData;
		unsigned char *source = (unsigned char *)imgSource->imageData;
		unsigned char *imgData = (unsigned char *)imgDest->imageData;

		for (unsigned int r=0; r<imgLabel->height; r++,
		labels+=imgLabel->widthStep/(imgLabel->depth/8),
		source+=imgSource->widthStep/(imgSource->depth/8), imgData+=imgDest->widthStep/(imgDest->depth/8))
			for (unsigned int c=0; c<imgLabel->width; c++)
			{
				if (labels[c])
				{
					Color color = pal[labels[c]];

					imgData[imgDest->nChannels*c+0] = (unsigned char)((1.-alpha)*source[imgSource->nChannels*c+0]+alpha*color.b);
					imgData[imgDest->nChannels*c+1] = (unsigned char)((1.-alpha)*source[imgSource->nChannels*c+1]+alpha*color.g);
					imgData[imgDest->nChannels*c+2] = (unsigned char)((1.-alpha)*source[imgSource->nChannels*c+2]+alpha*color.r);
				}
			}
	}*/

	if (mode)
	{
		CvBlob *biggestBlob;
		unsigned int maxArea = 0;
		for (CvBlobs::const_iterator it=blobs.begin(); it!=blobs.end(); ++it) {
			CvBlob *blob = it->second;
			//printf("blob %d has area %d and centre (%.2f, %.2f)\n", it->first, blob->area, blob->centroid.x, blob->centroid.y);
			if (blob->area >= maxArea) {
				maxArea = blob->area;
				biggestBlob = blob;
			}
		}

		if (maxArea == 0)
			return;

		/*for (CvBlobs::const_iterator it=blobs.begin(); it!=blobs.end(); ++it)*/

		{
			//CvBlob *blob=(*it).second;
			CvBlob *blob=biggestBlob;

			if (mode&CV_BLOB_RENDER_TO_LOG)
			{
				std::clog << "Blob " << blob->label << std::endl;
				std::clog << " - Bounding box: (" << blob->minx << ", " << blob->miny << ") - (" << blob->maxx << ", " << blob->maxy << ")" << std::endl;
				std::clog << " - Bounding box area: " << (1 + blob->maxx - blob->minx) * (1 + blob->maxy - blob->miny) << std::endl;
				std::clog << " - Area: " << blob->area << std::endl;
				std::clog << " - Centroid: (" << blob->centroid.x << ", " << blob->centroid.y << ")" << std::endl;
				std::clog << std::endl;
			}

			if (mode&CV_BLOB_RENDER_TO_STD)
			{
				std::cout << "Blob " << blob->label << std::endl;
				std::cout << " - Bounding box: (" << blob->minx << ", " << blob->miny << ") - (" << blob->maxx << ", " << blob->maxy << ")" << std::endl;
				std::cout << " - Bounding box area: " << (1 + blob->maxx - blob->minx) * (1 + blob->maxy - blob->miny) << std::endl;
				std::cout << " - Area: " << blob->area << std::endl;
				std::cout << " - Centroid: (" << blob->centroid.x << ", " << blob->centroid.y << ")" << std::endl;
				std::cout << std::endl;
			}

			if (mode&CV_BLOB_RENDER_BOUNDING_BOX)
				cvRectangle(imgDest,cvPoint(blob->minx,blob->miny),cvPoint(blob->maxx,blob->maxy),CV_RGB(255.,0.,0.));

			if (mode&CV_BLOB_RENDER_ANGLE)
			{
				cvCentralMoments(blob,imgLabel);
				double angle = cvAngle(blob);

				double x1,y1,x2,y2;

				x1=blob->centroid.x-.005*blob->area*cos(angle);
				y1=blob->centroid.y-.005*blob->area*sin(angle);
				x2=blob->centroid.x+.005*blob->area*cos(angle);
				y2=blob->centroid.y+.005*blob->area*sin(angle);
				cvLine(imgDest,cvPoint(int(x1),int(y1)),cvPoint(int(x2),int(y2)),CV_RGB(0.,255.,0.));
			}

			if (mode&CV_BLOB_RENDER_CENTROID)
			{
				cvLine(imgDest,cvPoint(int(blob->centroid.x)-3,int(blob->centroid.y)),cvPoint(int(blob->centroid.x)+3,int(blob->centroid.y)),CV_RGB(0.,0.,255.));
				cvLine(imgDest,cvPoint(int(blob->centroid.x),int(blob->centroid.y)-3),cvPoint(int(blob->centroid.x),int(blob->centroid.y)+3),CV_RGB(0.,0.,255.));
			}
		}
	}
}

// Returns radians
double cvAngle(CvBlob *blob)
{
	if (blob->centralMoments)
		return .5*atan2(2.*blob->u11,(blob->u20-blob->u02));
	else
	{
		cerr<<"Error: Central moments aren't calculated."<<endl;
		return 0.; /// TODO: Errors.
	}
}
