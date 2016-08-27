#ifndef _ROS_au_core_MCBaseSpeed_h
#define _ROS_au_core_MCBaseSpeed_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/Header.h"

namespace au_core
{

  class MCBaseSpeed : public ros::Msg
  {
    public:
      std_msgs::Header header;
      float baseSpeed;

    MCBaseSpeed():
      header(),
      baseSpeed(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
      union {
        float real;
        uint32_t base;
      } u_baseSpeed;
      u_baseSpeed.real = this->baseSpeed;
      *(outbuffer + offset + 0) = (u_baseSpeed.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_baseSpeed.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_baseSpeed.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_baseSpeed.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->baseSpeed);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->header.deserialize(inbuffer + offset);
      union {
        float real;
        uint32_t base;
      } u_baseSpeed;
      u_baseSpeed.base = 0;
      u_baseSpeed.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_baseSpeed.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_baseSpeed.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_baseSpeed.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->baseSpeed = u_baseSpeed.real;
      offset += sizeof(this->baseSpeed);
     return offset;
    }

    const char * getType(){ return "au_core/MCBaseSpeed"; };
    const char * getMD5(){ return "a4885391ac937098db0bfa113a142dfd"; };

  };

}
#endif