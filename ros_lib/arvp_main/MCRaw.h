#ifndef _ROS_arvp_main_MCRaw_h
#define _ROS_arvp_main_MCRaw_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/Header.h"

namespace arvp_main
{

  class MCRaw : public ros::Msg
  {
    public:
      std_msgs::Header header;
      float horLeft;
      float horRight;
      float verLeft;
      float verRight;
      float strLeft;
      float strRight;

    MCRaw():
      header(),
      horLeft(0),
      horRight(0),
      verLeft(0),
      verRight(0),
      strLeft(0),
      strRight(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->header.serialize(outbuffer + offset);
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
      } u_strLeft;
      u_strLeft.real = this->strLeft;
      *(outbuffer + offset + 0) = (u_strLeft.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_strLeft.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_strLeft.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_strLeft.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->strLeft);
      union {
        float real;
        uint32_t base;
      } u_strRight;
      u_strRight.real = this->strRight;
      *(outbuffer + offset + 0) = (u_strRight.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_strRight.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_strRight.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_strRight.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->strRight);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->header.deserialize(inbuffer + offset);
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
      } u_strLeft;
      u_strLeft.base = 0;
      u_strLeft.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_strLeft.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_strLeft.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_strLeft.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->strLeft = u_strLeft.real;
      offset += sizeof(this->strLeft);
      union {
        float real;
        uint32_t base;
      } u_strRight;
      u_strRight.base = 0;
      u_strRight.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_strRight.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_strRight.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_strRight.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->strRight = u_strRight.real;
      offset += sizeof(this->strRight);
     return offset;
    }

    const char * getType(){ return "arvp_main/MCRaw"; };
    const char * getMD5(){ return "dfe601170e9d980125888b8cefa95b18"; };

  };

}
#endif