#ifndef _ROS_SERVICE_Calibrate_h
#define _ROS_SERVICE_Calibrate_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace au_sensors
{

static const char CALIBRATE[] = "au_sensors/Calibrate";

  class CalibrateRequest : public ros::Msg
  {
    public:

    CalibrateRequest()
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
     return offset;
    }

    const char * getType(){ return CALIBRATE; };
    const char * getMD5(){ return "d41d8cd98f00b204e9800998ecf8427e"; };

  };

  class CalibrateResponse : public ros::Msg
  {
    public:
      uint32_t baseline;

    CalibrateResponse():
      baseline(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      *(outbuffer + offset + 0) = (this->baseline >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->baseline >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->baseline >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->baseline >> (8 * 3)) & 0xFF;
      offset += sizeof(this->baseline);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      this->baseline =  ((uint32_t) (*(inbuffer + offset)));
      this->baseline |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->baseline |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      this->baseline |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      offset += sizeof(this->baseline);
     return offset;
    }

    const char * getType(){ return CALIBRATE; };
    const char * getMD5(){ return "1b8b7c0689e7ebbbd47c7a31eece2d65"; };

  };

  class Calibrate {
    public:
    typedef CalibrateRequest Request;
    typedef CalibrateResponse Response;
  };

}
#endif
