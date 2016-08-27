#ifndef _ROS_diagnostics_Status_h
#define _ROS_diagnostics_Status_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/Header.h"

namespace diagnostics
{

  class Status : public ros::Msg
  {
    public:
      std_msgs::Header header;
      bool imu;
      bool depth;
      bool motor;

    Status():
      header(),
      imu(0),
      depth(0),
      motor(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
      union {
        bool real;
        uint8_t base;
      } u_imu;
      u_imu.real = this->imu;
      *(outbuffer + offset + 0) = (u_imu.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->imu);
      union {
        bool real;
        uint8_t base;
      } u_depth;
      u_depth.real = this->depth;
      *(outbuffer + offset + 0) = (u_depth.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->depth);
      union {
        bool real;
        uint8_t base;
      } u_motor;
      u_motor.real = this->motor;
      *(outbuffer + offset + 0) = (u_motor.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->motor);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->header.deserialize(inbuffer + offset);
      union {
        bool real;
        uint8_t base;
      } u_imu;
      u_imu.base = 0;
      u_imu.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->imu = u_imu.real;
      offset += sizeof(this->imu);
      union {
        bool real;
        uint8_t base;
      } u_depth;
      u_depth.base = 0;
      u_depth.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->depth = u_depth.real;
      offset += sizeof(this->depth);
      union {
        bool real;
        uint8_t base;
      } u_motor;
      u_motor.base = 0;
      u_motor.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->motor = u_motor.real;
      offset += sizeof(this->motor);
     return offset;
    }

    const char * getType(){ return "diagnostics/Status"; };
    const char * getMD5(){ return "20074be1d97860d2dcf97405ebc53e1f"; };

  };

}
#endif