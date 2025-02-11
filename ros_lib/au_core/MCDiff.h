#ifndef _ROS_au_core_MCDiff_h
#define _ROS_au_core_MCDiff_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/Header.h"

namespace au_core
{

  class MCDiff : public ros::Msg
  {
    public:
      std_msgs::Header header;
      float differential;

    MCDiff():
      header(),
      differential(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
      union {
        float real;
        uint32_t base;
      } u_differential;
      u_differential.real = this->differential;
      *(outbuffer + offset + 0) = (u_differential.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_differential.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_differential.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_differential.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->differential);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->header.deserialize(inbuffer + offset);
      union {
        float real;
        uint32_t base;
      } u_differential;
      u_differential.base = 0;
      u_differential.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_differential.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_differential.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_differential.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->differential = u_differential.real;
      offset += sizeof(this->differential);
     return offset;
    }

    const char * getType(){ return "au_core/MCDiff"; };
    const char * getMD5(){ return "07c213dd75a8d9cf8eca0e6a98baf560"; };

  };

}
#endif