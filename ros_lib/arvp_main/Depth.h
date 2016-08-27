#ifndef _ROS_arvp_main_Depth_h
#define _ROS_arvp_main_Depth_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/Header.h"

namespace arvp_main
{

  class Depth : public ros::Msg
  {
    public:
      std_msgs::Header header;
      uint32_t abs_pressure;
      float depth;

    Depth():
      header(),
      abs_pressure(0),
      depth(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
      *(outbuffer + offset + 0) = (this->abs_pressure >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (this->abs_pressure >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (this->abs_pressure >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (this->abs_pressure >> (8 * 3)) & 0xFF;
      offset += sizeof(this->abs_pressure);
      union {
        float real;
        uint32_t base;
      } u_depth;
      u_depth.real = this->depth;
      *(outbuffer + offset + 0) = (u_depth.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_depth.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_depth.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_depth.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->depth);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->header.deserialize(inbuffer + offset);
      this->abs_pressure =  ((uint32_t) (*(inbuffer + offset)));
      this->abs_pressure |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->abs_pressure |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      this->abs_pressure |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      offset += sizeof(this->abs_pressure);
      union {
        float real;
        uint32_t base;
      } u_depth;
      u_depth.base = 0;
      u_depth.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_depth.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_depth.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_depth.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->depth = u_depth.real;
      offset += sizeof(this->depth);
     return offset;
    }

    const char * getType(){ return "arvp_main/Depth"; };
    const char * getMD5(){ return "78282a0531bfea0e9249bca352264684"; };

  };

}
#endif