#ifndef __OS5000_H_
#define __OS5000_H_

#include <Arduino.h>

#include "Device.h"
#include "Timer.h"
#include "SerialLine.h"
#include "RosSettings.h"

#include <arvp_main/IMU.h>

enum os5000_result {OS5000_OK, OS5000_INVALID_LEN, OS5000_INVALID_START,
     OS5000_NO_CHECKSUM, OS5000_BAD_CHECKSUM, OS5000_UNKNOWN_ERROR};


class OS5000 : public Device {
public:
	OS5000():Device(){
    led = OS5000_LED;
    pinMode(led, OUTPUT);
    pinMode(OS5000_SER_LED, OUTPUT);
  };
  void ros_init();
  void device_setup();
  void device_loop();
  void read_serial();
  void serialConnect();
private:
  arvp_main::IMU _imuMsg;
  #if(ROS_ENABLED)
    ros::Publisher * _imuPub;
  #endif
  SerialLine _lineReader;
	static const char* format;
  uint32_t _prevTime;
  Timer _errorTimer;

	os5000_result parseLine(const char* line, int max, arvp_main::IMU* msg);
	char calcChecksum(const char *line);
};

#endif
