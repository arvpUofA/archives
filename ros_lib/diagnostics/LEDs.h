#ifndef _ROS_diagnostics_LEDs_h
#define _ROS_diagnostics_LEDs_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace diagnostics
{

  class LEDs : public ros::Msg
  {
    public:
      uint8_t led_type;
      uint16_t timeout;
      enum { BLUE = 0 };
      enum { GREEN = 1 };
      enum { RED = 2 };

    LEDs():
      led_type(0),
      timeout(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      *(outbuffer + offset + 0) = (this->led_type >> (8 * 0)) & 0xFF;
      offset += sizeof(this->led_type);
      *(outbuffer + offset + 0) = (this->timeout >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->timeout >> (8 * 1)) & 0xFF;
      offset += sizeof(this->timeout);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      this->led_type =  ((uint8_t) (*(inbuffer + offset)));
      offset += sizeof(this->led_type);
      this->timeout =  ((uint16_t) (*(inbuffer + offset)));
      this->timeout |= ((uint16_t) (*(inbuffer + offset + 1))) << (8 * 1);
      offset += sizeof(this->timeout);
     return offset;
    }

    const char * getType(){ return "diagnostics/LEDs"; };
    const char * getMD5(){ return "cee83c65aa54c5ba8ce8d224f2854393"; };

  };

}
#endif