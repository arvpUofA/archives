# Diagnostics node for AquaUrsa (2015)

// Todo: Implement cpuTemp

Publishes:
* diagnostics/leds - controls the LED strips on the robot (Red on error, green on kill switch engaged)
* diagnostics/data - publishes diagnostics data
* diagnostics/status - publishes status of every node

Subscribes:
* /motor/feedback - gets motor feedback
* /motor/killSig - gets status of the kill switch
* /sensors/imu - gets imu data
* /sensors/depth - gets depth data

Custom messages:
* /diagnostics/LEDs:

	```
	uint8 BLUE=0
	uint8 GREEN=1
	uint8 RED=2
	uint8 led_type
	uint16 timeout  // setting timeout as 0 turns it off
	```
* /diagnostics/Data (collection of topics at lower data rate [10Hz]):
	```
	Header header
	float32 heading
	float32 pitch
	float32 roll
	float32 depth

	uint8 kill
	float32 horLeft
	float32 horRight
	float32 verLeft
	float32 verRight

	float32 cpuTemp
	float32 cpuUsage
	float32 memUsage

	String coreURI
	```
* /diagnostics/Status:
	```
	Header header

	bool imu
	bool depth
	bool motor
	```
