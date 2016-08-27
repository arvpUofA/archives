#ifndef __ROS_SETTINGS_H_
#define __ROS_SETTINGS_H_

#include <Arduino.h>
#include <ros.h>
#include "Settings.h"

#if(ROS_ENABLED)
  extern ros::NodeHandle nh;
#endif

// print statement
#if(ROS_ENABLED)
  #define LOG_INFO( DATA ) nh.loginfo( DATA )
#else
  #define LOG_INFO( DATA ) Serial.println( F(DATA) )
#endif

#if(ROS_ENABLED)
  #define LOG_DEBUG( DATA ) nh.logdebug( DATA )
#else
  #define LOG_DEBUG( DATA ) Serial.println( F(DATA) )
#endif

#if(ROS_ENABLED)
  #define LOG_WARN( DATA ) nh.logwarn( DATA )
#else
  #define LOG_WARN( DATA ) Serial.println( F(DATA) )
#endif

#endif
