#ifndef __Device_H_
#define __Device_H_

#include <Arduino.h>

#define MAX_DEVICES 5

enum device_status {
  DEVICE_DEAD,
  DEVICE_UNINTIALIZED,
  DEVICE_INITIAZLIED,
  DEVICE_RUNNING,
  DEVICE_ERROR
};

class Device {
private:
  String name;

public:
  int ID;
  uint8_t status;
  uint8_t led;
  Device();
  virtual void ros_init();
  virtual void device_setup();
  virtual void device_loop();
};


class DeviceManager {
private:
  static Device *devices[MAX_DEVICES];
  static void controlLed(uint8_t led, uint8_t status);

public:
  static int device_count;
  static void registerDevice(Device *device);
  static void doDeviceLoops();
  static void doDeviceSetups();
  static void doRosInits();
  static void doLedStatus();
};


void OutputData();

#endif
