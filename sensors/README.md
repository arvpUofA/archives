# Sensors

* Mounts on to `/dev/arvp/sensors` using udev rules
* Publishes:
  * /sensors/imu
  * /sensors/depth
* To calibrate IMU `rostopic pub /sensors/calibrateDepth std_msgs/Empty -1`  
* To switch to serial interface for OS5000 IMU:
  * `rostopic pub /sensors/serialIMU std_msgs/Empty -1`
  * Close the roslaunch window running the sensor node
  * Start serial connection using `cu -l /dev/arvp/sensors -s 115200`
  * LED8 will blink in serial mode
  * To quit serial session, press `/`. This restarts teensy to reestablish ros connection
