#ifndef _ROS_arvp_main_MCBaseSpeed_h
#define _ROS_arvp_main_MCBaseSpeed_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/Header.h"

namespace arvp_main
{

  class MCBaseSpeed : public ros::Msg
  {
    public:
      std_msgs::Header header;
      uint8_t type;
      float baseSpeed;
      enum { MC_HORIZ = 0 };
      enum { MC_VERT = 1 };
      enum { MC_STRAFE = 2 };

    MCBaseSpeed():
      header(),
      type(0),
      baseSpeed(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
      *(outbuffer + offset + 0) = (this->type >> (8 * 0)) & 0xFF;
      offset += sizeof(this->type);
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
      this->type =  ((uint8_t) (*(inbuffer + offset)));
      offset += sizeof(this->type);
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

    const char * getType(){ return "arvp_main/MCBaseSpeed"; };
    const char * getMD5(){ return "67b91b071161f08c9608dcaf3d751870"; };

  };

}
#endif