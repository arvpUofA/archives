#ifndef __TOUCH_H_
#define __TOUCH_H_

#include <Arduino.h>
#include <ADC.h>

#include "Device.h"
#include "Timer.h"
#include "RosSettings.h"

#include <arvp_main/Touch.h>

class Touch : public Device {
public:
  Touch():Device(){
    led = TOUCH_LED;  // defined in Settings.h
    pinMode(led, OUTPUT);
  };

  void ros_init() {
    #if(ROS_ENABLED)
      _touchPub = new ros::Publisher( "sensors/touch", &_touchMsg );
      nh.advertise(*_touchPub);
    #endif
  }

  void device_setup() {
    status = DEVICE_UNINTIALIZED;

    _adc = new ADC();
    LOG_INFO( "Touch sensor: setup started;" );
    pinMode(A3, INPUT);

    ////// ADC Setup /////
    _adc->setAveraging(255, ADC_0); // set number of averages
    _adc->setResolution(12, ADC_0); // set bits of resolution
    _adc->setConversionSpeed(ADC_VERY_LOW_SPEED, ADC_0); // change the conversion speed
    _adc->setSamplingSpeed(ADC_VERY_LOW_SPEED, ADC_0); // change the sampling speed

    _adc->enableInterrupts(ADC_0); // enable interrupts BEFORE calling a measurement method
    _adc->startContinuous(A3, ADC_0);

    // timer setup
    _publishTimer.reset();
    _errorTimer.reset();

    status = DEVICE_INITIAZLIED;
    LOG_INFO( "Touch sensor: setup complete;" );
  }

  void device_loop() {
    if(_publishTimer.elapsed(25) && status == DEVICE_RUNNING)
    // publish at 40Hz
    {
      #if(ROS_ENABLED)
        _touchMsg.header.stamp = nh.now();
        _touchPub->publish( &_touchMsg );
      #else
        Serial.print( F("Touch sensor: ") );
        Serial.print( _touchMsg.touch );
        Serial.println(';');
      #endif
    }
    if(_errorTimer.elapsed(5000) ) {
      if(status == DEVICE_RUNNING) LOG_DEBUG("touch: online;");
      if(status == DEVICE_ERROR)   LOG_WARN("touch: error;");
    }
  }

  void readADC() {
    _touchMsg.touch = _adc->analogReadContinuous(ADC_0);
    if(_touchMsg.touch > TOUCH_MAX || _touchMsg.touch < TOUCH_MIN)  // defined in Settings.h
      status = DEVICE_ERROR;
    else
      status = DEVICE_RUNNING;
  }

private:
  ADC * _adc;
  Timer _publishTimer;
  Timer _errorTimer;
  arvp_main::Touch _touchMsg;
  #if(ROS_ENABLED)
    ros::Publisher * _touchPub;
  #endif
};

#endif
