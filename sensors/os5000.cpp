#include "Settings.h"
#if(HAS_OS5000)

#include "os5000.h"

// Restart Macro
#define CPU_RESTART_ADDR (uint32_t *)0xE000ED0C
#define CPU_RESTART_VAL 0x5FA0004
#define CPU_RESTART (*CPU_RESTART_ADDR = CPU_RESTART_VAL);

const char* OS5000::format = "$C%fP%fR%fT%fMx%fMy%fMz%fAx%fAy%fAz%f";

void OS5000::ros_init() {
  #if(ROS_ENABLED)
    _imuPub = new ros::Publisher( "sensors/imu", &_imuMsg );
    nh.advertise(*_imuPub);
  #endif
}

void OS5000::device_setup() {
  status = DEVICE_UNINTIALIZED;
  LOG_INFO( "OS5000: setup started;" );
  _lineReader.begin(Serial1, 115200, '\n');
  _prevTime = 0;
  _errorTimer.reset();
	status = DEVICE_INITIAZLIED;
  LOG_INFO( "OS5000: setup complete;");
}

void OS5000::device_loop() {
	if(_lineReader.isComplete()) {
    _prevTime = millis();
    char * line = _lineReader.getLine();
    os5000_result res = parseLine(line, 100, &_imuMsg);
		if(res == OS5000_OK) {
      status = DEVICE_RUNNING;
      #if(ROS_ENABLED)
        _imuMsg.header.stamp = nh.now();
        _imuPub->publish( &_imuMsg );
      #else
        Serial.print("h:");
  			Serial.print(_imuMsg.heading);
  			Serial.print("; p:");
  			Serial.print(_imuMsg.pitch);
  			Serial.print("; r:");
  			Serial.print(_imuMsg.roll);
  			Serial.println(";");
      #endif
		} else {
      status = DEVICE_ERROR;
      if(_errorTimer.elapsed(5000)) {
  			switch(res) {
          case OS5000_INVALID_LEN: LOG_WARN("OS5000: error (invalid len);"); break;
          case OS5000_INVALID_START: LOG_WARN("OS5000: error (invalid start);"); break;
          case OS5000_NO_CHECKSUM: LOG_WARN("OS5000: error (no checksum);"); break;
          case OS5000_BAD_CHECKSUM: LOG_WARN("OS5000: error (bad checksum);"); break;
          case OS5000_UNKNOWN_ERROR:
          default: LOG_WARN("OS5000: error (unknown);"); break;
        }
      }
    }
  }

  if(_errorTimer.elapsed(5000)) {
    // check update time
    if(millis() - _prevTime > 100) {
      LOG_WARN("OS5000: Serial read error");
      status = DEVICE_ERROR;
    }
    if(status == DEVICE_RUNNING) {
      LOG_DEBUG("OS5000: online;");
    }
  }
}

void OS5000::read_serial() {
  _lineReader.read();
}

void OS5000::serialConnect() {
  Timer kickTimer;
  kickTimer.reset();
  bool blink = false;

  LOG_INFO("OS5000 Serial Connection");
  LOG_WARN("sensors: Turning off ROS. Close this before starting serial connection.");

  // restart Serial comm
  Serial.flush();   Serial.end();
  Serial1.flush();  Serial1.end();
  Serial.begin(115200);
  Serial1.begin(115200);
  while(!Serial); // wait for connection

  while(1) {

    if(Serial.available()) {
      char inp = Serial.read();
      
      if(inp == '/') break;
      Serial1.write( inp );
    }
    
    if(Serial1.available())
      Serial.write( Serial1.read() );  
    
    if(kickTimer.elapsed(500)) {
      // kick dog
      noInterrupts();
      WDOG_REFRESH = 0xA602;
      WDOG_REFRESH = 0xB480;
      interrupts();
      
      // blink led
      digitalWrite(OS5000_SER_LED, blink); blink = !blink;  
    }  
  }

  CPU_RESTART;
}

os5000_result OS5000::parseLine(const char* line, int max, arvp_main::IMU* msg) {
  int rv;
  unsigned int checksum;

  int len = strnlen(line, max);

  if(!len || len > 100)  // TODO: what is the max valid length?
    return OS5000_INVALID_LEN;

  if(line[0] != '$')
    return OS5000_INVALID_START;

  rv = sscanf(line + (len-4), "*%2x", &checksum);
  if(rv != 1)
    return OS5000_NO_CHECKSUM;

  if(calcChecksum(line) != checksum)
    return OS5000_BAD_CHECKSUM;

  rv = sscanf(line, format, \
    &msg->heading, &msg->pitch, &msg->roll, \
    &msg->temp, \
    &msg->mag[0], &msg->mag[1], &msg->mag[2], \
    &msg->accel[0], &msg->accel[1], &msg->accel[2]);

  if(rv != 10)
   return OS5000_UNKNOWN_ERROR;

  msg->header.frame_id = 0;
  msg->gyro[0] = 0; msg->gyro[1] = 0; msg->gyro[2] = 0;
  return OS5000_OK;
}

char OS5000::calcChecksum(const char *line) {
  char cksum = 0;
  for(const char *c=line+1; *c != '*'; *c++)
    cksum ^= *c;
  return cksum;
}

#endif
