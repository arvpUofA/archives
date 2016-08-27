#ifndef _ROS_arvp_main_Touch_h
#define _ROS_arvp_main_Touch_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/Header.h"

namespace arvp_main
{

  class Touch : public ros::Msg
  {
    public:
      std_msgs::Header header;
      float touch;

    Touch():
      header(),
      touch(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
      union {
        float real;
        uint32_t base;
      } u_touch;
      u_touch.real = this->touch;
      *(outbuffer + offset + 0) = (u_touch.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_touch.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_touch.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_touch.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->touch);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->header.deserialize(inbuffer + offset);
      union {
        float real;
        uint32_t base;
      } u_touch;
      u_touch.base = 0;
      u_touch.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_touch.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_touch.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_touch.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->touch = u_touch.real;
      offset += sizeof(this->touch);
     return offset;
    }

    const char * getType(){ return "arvp_main/Touch"; };
    const char * getMD5(){ return "330b1a5410947f56c30fbfbbffec47be"; };

  };

}
#endif