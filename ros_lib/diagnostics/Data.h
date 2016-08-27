#ifndef _ROS_diagnostics_Data_h
#define _ROS_diagnostics_Data_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/Header.h"

namespace diagnostics
{

  class Data : public ros::Msg
  {
    public:
      std_msgs::Header header;
      float heading;
      float pitch;
      float roll;
      float depth;
      uint8_t kill;
      float horLeft;
      float horRight;
      float verLeft;
      float verRight;
      float cpuTemp;
      float cpuUsage;
      float memUsage;
      const char* coreURI;

    Data():
      header(),
      heading(0),
      pitch(0),
      roll(0),
      depth(0),
      kill(0),
      horLeft(0),
      horRight(0),
      verLeft(0),
      verRight(0),
      cpuTemp(0),
      cpuUsage(0),
      memUsage(0),
      coreURI("")
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
      union {
        float real;
        uint32_t base;
      } u_heading;
      u_heading.real = this->heading;
      *(outbuffer + offset + 0) = (u_heading.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_heading.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_heading.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_heading.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->heading);
      union {
        float real;
        uint32_t base;
      } u_pitch;
      u_pitch.real = this->pitch;
      *(outbuffer + offset + 0) = (u_pitch.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_pitch.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_pitch.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_pitch.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->pitch);
      union {
        float real;
        uint32_t base;
      } u_roll;
      u_roll.real = this->roll;
      *(outbuffer + offset + 0) = (u_roll.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_roll.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_roll.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_roll.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->roll);
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
      *(outbuffer + offset + 0) = (this->kill >> (8 * 0)) & 0xFF;
      offset += sizeof(this->kill);
      union {
        float real;
        uint32_t base;
      } u_horLeft;
      u_horLeft.real = this->horLeft;
      *(outbuffer + offset + 0) = (u_horLeft.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_horLeft.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_horLeft.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_horLeft.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->horLeft);
      union {
        float real;
        uint32_t base;
      } u_horRight;
      u_horRight.real = this->horRight;
      *(outbuffer + offset + 0) = (u_horRight.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_horRight.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_horRight.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_horRight.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->horRight);
      union {
        float real;
        uint32_t base;
      } u_verLeft;
      u_verLeft.real = this->verLeft;
      *(outbuffer + offset + 0) = (u_verLeft.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_verLeft.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_verLeft.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_verLeft.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->verLeft);
      union {
        float real;
        uint32_t base;
      } u_verRight;
      u_verRight.real = this->verRight;
      *(outbuffer + offset + 0) = (u_verRight.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_verRight.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_verRight.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_verRight.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->verRight);
      union {
        float real;
        uint32_t base;
      } u_cpuTemp;
      u_cpuTemp.real = this->cpuTemp;
      *(outbuffer + offset + 0) = (u_cpuTemp.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_cpuTemp.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_cpuTemp.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_cpuTemp.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->cpuTemp);
      union {
        float real;
        uint32_t base;
      } u_cpuUsage;
      u_cpuUsage.real = this->cpuUsage;
      *(outbuffer + offset + 0) = (u_cpuUsage.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_cpuUsage.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_cpuUsage.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_cpuUsage.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->cpuUsage);
      union {
        float real;
        uint32_t base;
      } u_memUsage;
      u_memUsage.real = this->memUsage;
      *(outbuffer + offset + 0) = (u_memUsage.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_memUsage.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_memUsage.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_memUsage.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->memUsage);
      uint32_t length_coreURI = strlen(this->coreURI);
      memcpy(outbuffer + offset, &length_coreURI, sizeof(uint32_t));
      offset += 4;
      memcpy(outbuffer + offset, this->coreURI, length_coreURI);
      offset += length_coreURI;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->header.deserialize(inbuffer + offset);
      union {
        float real;
        uint32_t base;
      } u_heading;
      u_heading.base = 0;
      u_heading.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_heading.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_heading.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_heading.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->heading = u_heading.real;
      offset += sizeof(this->heading);
      union {
        float real;
        uint32_t base;
      } u_pitch;
      u_pitch.base = 0;
      u_pitch.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_pitch.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_pitch.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_pitch.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->pitch = u_pitch.real;
      offset += sizeof(this->pitch);
      union {
        float real;
        uint32_t base;
      } u_roll;
      u_roll.base = 0;
      u_roll.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_roll.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_roll.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_roll.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->roll = u_roll.real;
      offset += sizeof(this->roll);
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
      this->kill =  ((uint8_t) (*(inbuffer + offset)));
      offset += sizeof(this->kill);
      union {
        float real;
        uint32_t base;
      } u_horLeft;
      u_horLeft.base = 0;
      u_horLeft.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_horLeft.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_horLeft.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_horLeft.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->horLeft = u_horLeft.real;
      offset += sizeof(this->horLeft);
      union {
        float real;
        uint32_t base;
      } u_horRight;
      u_horRight.base = 0;
      u_horRight.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_horRight.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_horRight.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_horRight.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->horRight = u_horRight.real;
      offset += sizeof(this->horRight);
      union {
        float real;
        uint32_t base;
      } u_verLeft;
      u_verLeft.base = 0;
      u_verLeft.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_verLeft.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_verLeft.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_verLeft.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->verLeft = u_verLeft.real;
      offset += sizeof(this->verLeft);
      union {
        float real;
        uint32_t base;
      } u_verRight;
      u_verRight.base = 0;
      u_verRight.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_verRight.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_verRight.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_verRight.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->verRight = u_verRight.real;
      offset += sizeof(this->verRight);
      union {
        float real;
        uint32_t base;
      } u_cpuTemp;
      u_cpuTemp.base = 0;
      u_cpuTemp.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_cpuTemp.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_cpuTemp.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_cpuTemp.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->cpuTemp = u_cpuTemp.real;
      offset += sizeof(this->cpuTemp);
      union {
        float real;
        uint32_t base;
      } u_cpuUsage;
      u_cpuUsage.base = 0;
      u_cpuUsage.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_cpuUsage.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_cpuUsage.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_cpuUsage.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->cpuUsage = u_cpuUsage.real;
      offset += sizeof(this->cpuUsage);
      union {
        float real;
        uint32_t base;
      } u_memUsage;
      u_memUsage.base = 0;
      u_memUsage.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_memUsage.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_memUsage.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_memUsage.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->memUsage = u_memUsage.real;
      offset += sizeof(this->memUsage);
      uint32_t length_coreURI;
      memcpy(&length_coreURI, (inbuffer + offset), sizeof(uint32_t));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_coreURI; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_coreURI-1]=0;
      this->coreURI = (char *)(inbuffer + offset-1);
      offset += length_coreURI;
     return offset;
    }

    const char * getType(){ return "diagnostics/Data"; };
    const char * getMD5(){ return "7af9e9db21edf974f2a5d8b2e11e3f52"; };

  };

}
#endif