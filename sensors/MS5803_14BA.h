#ifndef __MS5803_14BA_H_
#define __MS5803_14BA_H_
#include <Arduino.h>
#include <Timer.h>

#include "Device.h"
#include "RosSettings.h"

#include <arvp_main/Depth.h>

// I2C address for sensor
#define MS5803_14BA_I2C_ADDRESS 0x76

// Density of water
#define DENSITY   1.019716

// constants for conversion precision
enum precision {
  ADC_256  = 0x00,
  ADC_512  = 0x02,
  ADC_1024 = 0x04,
  ADC_2048 = 0x06,
  ADC_4096 = 0x08
};

// define measurement type
enum measurement {
  PRESSURE = 0x00,
  TEMPERATURE = 0x10
};

// Commands
#define CMD_RESET     0x1E
#define CMD_ADC_READ  0x00
#define CMD_ADC_CONV  0x40
#define CMD_PROM      0xA0

class MS5803_14BA : public Device {
public:
  MS5803_14BA():Device(){
    led = MS5803_LED;
    pinMode(led, OUTPUT);
    _isCalibrating = false;
  };
  void ros_init();
  void device_setup();
  void device_loop();
  void reset(void);

  void calibrate(void);

private:
  int32_t _temperature_actual;
	int32_t _pressure_actual;
  int32_t _baseline_pressure;

  arvp_main::Depth _depthMsg;
  #if(ROS_ENABLED)
    ros::Publisher * _depthPub;
  #endif

  Timer samplingTimer;
  Timer _errorTimer;

  uint16_t coefficient[8];

  bool _isCalibrating;

  void getMeasurements(precision _precision);
  uint32_t getADCconversion(measurement _measurement, precision _precision);	// Retrieve ADC result
  uint8_t crc4(uint16_t n_prom[]);
  void sendCommand(uint8_t command);
};

#endif
