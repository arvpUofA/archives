#ifndef _ROS_arvp_main_KillSig_h
#define _ROS_arvp_main_KillSig_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace arvp_main
{

  class KillSig : public ros::Msg
  {
    public:
      uint8_t kill;
      enum { KILL_ENGAGE = 0 };
      enum { KILL_DISENGAGE = 1 };

    KillSig():
      kill(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      *(outbuffer + offset + 0) = (this->kill >> (8 * 0)) & 0xFF;
      offset += sizeof(this->kill);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      this->kill =  ((uint8_t) (*(inbuffer + offset)));
      offset += sizeof(this->kill);
     return offset;
    }

    const char * getType(){ return "arvp_main/KillSig"; };
    const char * getMD5(){ return "e3d1493836e85d48c57df183432373bd"; };

  };

}
#endif