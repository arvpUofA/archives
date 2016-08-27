#ifndef __Settings_H_
#define __Settings_H_

// must be the first file to be included

// OceanServer IMU
#define HAS_OS5000      (1)
#define OS5000_LED       6
#define OS5000_SER_LED	 8

// OpenROV Depth Sensor
#define HAS_MS5803      (1)
#define MS5803_LED       7


// Resistive Touch Sensor
#define HAS_TOUCH       (0)
#define TOUCH_MIN        0
#define TOUCH_MAX       4095
#define TOUCH_LED        5

#define ROS_ENABLED     (1) // ROS Enabled

#endif
