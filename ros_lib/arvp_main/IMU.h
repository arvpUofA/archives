#ifndef _ROS_arvp_main_IMU_h
#define _ROS_arvp_main_IMU_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "std_msgs/Header.h"

namespace arvp_main
{

  class IMU : public ros::Msg
  {
    public:
      std_msgs::Header header;
      float heading;
      float pitch;
      float roll;
      float accel[3];
      float mag[3];
      float gyro[3];
      float temp;

    IMU():
      header(),
      heading(0),
      pitch(0),
      roll(0),
      accel(),
      mag(),
      gyro(),
      temp(0)
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
      for( uint8_t i = 0; i < 3; i++){
      union {
        float real;
        uint32_t base;
      } u_acceli;
      u_acceli.real = this->accel[i];
      *(outbuffer + offset + 0) = (u_acceli.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_acceli.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_acceli.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_acceli.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->accel[i]);
      }
      for( uint8_t i = 0; i < 3; i++){
      union {
        float real;
        uint32_t base;
      } u_magi;
      u_magi.real = this->mag[i];
      *(outbuffer + offset + 0) = (u_magi.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_magi.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_magi.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_magi.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->mag[i]);
      }
      for( uint8_t i = 0; i < 3; i++){
      union {
        float real;
        uint32_t base;
      } u_gyroi;
      u_gyroi.real = this->gyro[i];
      *(outbuffer + offset + 0) = (u_gyroi.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_gyroi.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_gyroi.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_gyroi.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->gyro[i]);
      }
      union {
        float real;
        uint32_t base;
      } u_temp;
      u_temp.real = this->temp;
      *(outbuffer + offset + 0) = (u_temp.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_temp.base >> (8 * 1)) & 0xFF;
      *(outbuffer + offset + 2) = (u_temp.base >> (8 * 2)) & 0xFF;
      *(outbuffer + offset + 3) = (u_temp.base >> (8 * 3)) & 0xFF;
      offset += sizeof(this->temp);
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
      for( uint8_t i = 0; i < 3; i++){
      union {
        float real;
        uint32_t base;
      } u_acceli;
      u_acceli.base = 0;
      u_acceli.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_acceli.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_acceli.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_acceli.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->accel[i] = u_acceli.real;
      offset += sizeof(this->accel[i]);
      }
      for( uint8_t i = 0; i < 3; i++){
      union {
        float real;
        uint32_t base;
      } u_magi;
      u_magi.base = 0;
      u_magi.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_magi.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_magi.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_magi.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->mag[i] = u_magi.real;
      offset += sizeof(this->mag[i]);
      }
      for( uint8_t i = 0; i < 3; i++){
      union {
        float real;
        uint32_t base;
      } u_gyroi;
      u_gyroi.base = 0;
      u_gyroi.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_gyroi.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_gyroi.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_gyroi.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->gyro[i] = u_gyroi.real;
      offset += sizeof(this->gyro[i]);
      }
      union {
        float real;
        uint32_t base;
      } u_temp;
      u_temp.base = 0;
      u_temp.base |= ((uint32_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_temp.base |= ((uint32_t) (*(inbuffer + offset + 1))) << (8 * 1);
      u_temp.base |= ((uint32_t) (*(inbuffer + offset + 2))) << (8 * 2);
      u_temp.base |= ((uint32_t) (*(inbuffer + offset + 3))) << (8 * 3);
      this->temp = u_temp.real;
      offset += sizeof(this->temp);
     return offset;
    }

    const char * getType(){ return "arvp_main/IMU"; };
    const char * getMD5(){ return "6b503d68437b7a8e85a109566f7de4f5"; };

  };

}
#endif