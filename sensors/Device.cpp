#include "Device.h"

Device::Device() {
  DeviceManager::registerDevice(this);
  status = DEVICE_DEAD;
}

// virtual functions: populated by children
void Device::ros_init() {

}

void Device::device_setup() {

}

void Device::device_loop() {

}

////////////////////////////////////////////

void DeviceManager::registerDevice(Device *device) {
  devices[device_count] = device;
  device_count++;
}

void DeviceManager::doDeviceLoops() {
  for(int i=0; i<device_count; i++) {
    // loop through every device
    devices[i]->device_loop();
  }
}

void DeviceManager::doDeviceSetups() {
  for(int i=0; i<device_count; i++) {
    devices[i]->device_setup();
  }
}

void DeviceManager::doRosInits() {
  for(int i=0; i<device_count; i++) {
    devices[i]->ros_init();
  }
}

void DeviceManager::doLedStatus() {
  for(int i=0; i<device_count; i++) {
    controlLed(devices[i]->led, devices[i]->status);
  }
}

void DeviceManager::controlLed(uint8_t led, uint8_t status) {
  switch(status) {
    case DEVICE_ERROR:
    case DEVICE_DEAD: digitalWrite(led, LOW); break;
    case DEVICE_INITIAZLIED:
    case DEVICE_RUNNING: digitalWrite(led, HIGH); break;
    case DEVICE_UNINTIALIZED: digitalWrite(led, !digitalRead(led)); break;
  }
}

// initialize device manager data
int DeviceManager::device_count = 0;
Device *DeviceManager::devices[MAX_DEVICES];

////////////////////////////////////////////
