#include "Settings.h"
#if(HAS_MS5803)

#include <Timer.h>
#include <i2c_t3.h>
#include <EEPROM.h>
#include "MS5803_14BA.h"
#include "Device.h"

void MS5803_14BA::ros_init() {
  #if(ROS_ENABLED)
    _depthPub = new ros::Publisher( "sensors/depth", &_depthMsg );
    nh.advertise(*_depthPub);
  #endif
}

void MS5803_14BA::device_setup() {
  status = DEVICE_UNINTIALIZED;
  LOG_INFO( "MS5803: setup started;");

  Wire.begin(I2C_MASTER, MS5803_14BA_I2C_ADDRESS, I2C_PINS_18_19, I2C_PULLUP_EXT, I2C_RATE_400);
  delay(10);

  // reset sensor
  reset();

  uint8_t highByte = 0, lowByte = 0;
  // get calibration constants
  for(uint8_t i=0; i<8; i++) {
    sendCommand( CMD_PROM + (i * 2) );
    Wire.requestFrom(MS5803_14BA_I2C_ADDRESS, 2, 50);
    if(Wire.available()) {
      highByte = Wire.read();
      lowByte = Wire.read();
    }
    coefficient[i] = (highByte << 8) | lowByte;
  }
  switch(Wire.status()) {
    case I2C_WAITING:  break;
    case I2C_ADDR_NAK: LOG_WARN("MS5803: Slave addr not acknowledged\n"); return; break;
    case I2C_DATA_NAK: LOG_WARN("MS5803: Slave data not acknowledged\n"); return; break;
    case I2C_ARB_LOST: LOG_WARN("MS5803: Bus Error\n"); return; break;
    case I2C_TIMEOUT:  LOG_WARN("MS5803: I2C timeout\n"); return; break;
    case I2C_BUF_OVF:  LOG_WARN("MS5803: I2C buffer overflow\n"); return; break;
    default:           LOG_WARN("MS5803: I2C busy\n"); return; break;
  }


  // check crc
  if(!crc4(coefficient)) {
    LOG_WARN("MS5803: initialization error (coefficient error);");
  }

  LOG_INFO("MS5803: initialized I2C;");

  // Fetch value from EEPROM
  LOG_INFO( "MS5803: reading baseline pressure from EEPROM;");
  _baseline_pressure = EEPROM.read(0) | ( EEPROM.read(1) << 8 ) |
                       ( EEPROM.read(2) << 16 ) | ( EEPROM.read(3) << 24 );
  

  char baseline[35];
  sprintf(baseline, "MS5803: baseline = %Lu;", uint64_t(_baseline_pressure) );
  LOG_INFO(baseline);

  samplingTimer.reset();

  status = DEVICE_INITIAZLIED;
  LOG_INFO( "MS5803: setup complete;");
  _errorTimer.reset();
}


void MS5803_14BA::device_loop() {
  if(status != DEVICE_UNINTIALIZED) {
    if(samplingTimer.elapsed(25))
    // set sampling freq of 50Hz
    {
      if(!_isCalibrating) {
        status = DEVICE_RUNNING;
        getMeasurements(ADC_4096);

        #if(ROS_ENABLED)
          _depthMsg.header.stamp = nh.now();
          _depthPub->publish( &_depthMsg );
        #else
          Serial.print(F("abs_pressure:"));
          Serial.print(_depthMsg.abs_pressure);
          Serial.print(F(";"));
          Serial.print(F(" depth(cm):"));
          Serial.print(_depthMsg.depth); // cm
          Serial.println(';');
        #endif
      }
    }
  }

  if(_errorTimer.elapsed(5000)) {
    if(status == DEVICE_RUNNING) {
      LOG_DEBUG("MS5803: online;");
    } else if(status == DEVICE_UNINTIALIZED) {
      LOG_WARN( "MS5803: device not initialized;");
    }
  }

}

void MS5803_14BA::reset(void) {
  sendCommand(CMD_RESET);
  delay(3);
}

void MS5803_14BA::calibrate() {
  if(_isCalibrating) return;
  _isCalibrating = true;
  // Calibrate baseline pressure
  LOG_INFO( "MS5803: calibrating baseline pressure;");
  {
    float total=0;
    for(int i=0; i<100; i++) {
      getMeasurements(ADC_4096);
      total += _pressure_actual;
      // kick dog
      noInterrupts();
      WDOG_REFRESH = 0xA602;
      WDOG_REFRESH = 0xB480;
      interrupts();
    }
    _baseline_pressure = total/100;
  }

  // Save to EEPROM
  EEPROM.write( 0, _baseline_pressure & 0xff );       // lowest byte
  EEPROM.write( 1, _baseline_pressure >> 8 & 0xff );
  EEPROM.write( 2, _baseline_pressure >> 16 & 0xff );
  EEPROM.write( 3, _baseline_pressure >> 24 & 0xff ); // highest byte

  char baseline[35];
  sprintf(baseline, "MS5803: baseline = %Lu;", uint64_t(_baseline_pressure) );
  LOG_INFO(baseline);
  _isCalibrating = false;
}

void MS5803_14BA::getMeasurements(precision _precision)

{
	//Retrieve ADC result
	int32_t temperature_raw = getADCconversion(TEMPERATURE, _precision);
	int32_t pressure_raw = getADCconversion(PRESSURE, _precision);


	//Create Variables for calculations
	int32_t temp_calc;
	int32_t pressure_calc;

	int32_t dT;

	//Now that we have a raw temperature, let's compute our actual.
	dT = temperature_raw - ((int32_t)coefficient[5] << 8);
	temp_calc = (((int64_t)dT * coefficient[6]) >> 23) + 2000;

	//Now we have our first order Temperature, let's calculate the second order.
	int64_t T2, OFF2, SENS2, OFF, SENS; //working variables

	if (temp_calc < 2000)
	// If temp_calc is below 20.0C
	{
		T2 = 3 * (((int64_t)dT * dT) >> 33);
		OFF2 = 3 * ((temp_calc - 2000) * (temp_calc - 2000)) / 2;
		SENS2 = 5 * ((temp_calc - 2000) * (temp_calc - 2000)) / 8;

		if(temp_calc < -1500)
		// If temp_calc is below -15.0C
		{
			OFF2 = OFF2 + 7 * ((temp_calc + 1500) * (temp_calc + 1500));
			SENS2 = SENS2 + 4 * ((temp_calc + 1500) * (temp_calc + 1500));
		}
    }
	else
	// If temp_calc is above 20.0C
	{
		T2 = 7 * ((uint64_t)dT * dT)/pow(2,37);
		OFF2 = ((temp_calc - 2000) * (temp_calc - 2000)) / 16;
		SENS2 = 0;
	}

	// Now bring it all together to apply offsets
	OFF = ((int64_t)coefficient[2] << 16) + (((coefficient[4] * (int64_t)dT)) >> 7);
	SENS = ((int64_t)coefficient[1] << 15) + (((coefficient[3] * (int64_t)dT)) >> 8);

	temp_calc = temp_calc - T2;
	OFF = OFF - OFF2;
	SENS = SENS - SENS2;

	// Now lets calculate the pressure
	pressure_calc = (((SENS * pressure_raw) / 2097152 ) - OFF) / 32768;

	_temperature_actual = temp_calc ;
	_pressure_actual = pressure_calc ; // 10;// pressure_calc;

  _depthMsg.abs_pressure = _pressure_actual / 10;
  _depthMsg.depth = (_pressure_actual - _baseline_pressure) * DENSITY / 10.0;
}

uint32_t MS5803_14BA::getADCconversion(measurement _measurement, precision _precision)
// Retrieve ADC measurement from the device.
// Select measurement type and precision
{
	uint32_t result;
	uint8_t highByte=0, midByte=0, lowByte=0;

	sendCommand(CMD_ADC_CONV + _measurement + _precision);

	// Wait for conversion to complete
	delay(1); //general delay
	switch( _precision )
	{
		case ADC_256 : delay(1); break;
		case ADC_512 : delay(3); break;
		case ADC_1024: delay(4); break;
		case ADC_2048: delay(6); break;
		case ADC_4096: delay(10); break;
	}

	sendCommand(CMD_ADC_READ);
	Wire.requestFrom(MS5803_14BA_I2C_ADDRESS, 3, 100);

	if(Wire.available())
	{
		highByte = Wire.read();
		midByte = Wire.read();
		lowByte = Wire.read();
	}

	result = ((uint32_t)highByte << 16) + ((uint32_t)midByte << 8) + lowByte;

	return result;
}

uint8_t MS5803_14BA::crc4(uint16_t n_prom[]) {
  uint16_t n_rem; // crc reminder
  uint16_t crc_read; // original value of the crc

  n_rem = 0x00;
  crc_read=n_prom[7]; //save read CRC
  n_prom[7]=(0xFF00 & (n_prom[7])); //CRC byte is replaced by 0

  for (uint8_t cnt = 0; cnt < 16; cnt++) {// operation is performed on bytes
    // choose LSB or MSB
    if (cnt % 2 == 1)
      n_rem ^= (unsigned short) ((n_prom[cnt>>1]) & 0x00FF);
    else
      n_rem ^= (unsigned short) (n_prom[cnt>>1]>>8);

    for (uint8_t n_bit = 8; n_bit > 0; n_bit--) {
      if (n_rem & (0x8000))
        n_rem = (n_rem << 1) ^ 0x3000;
      else
        n_rem = (n_rem << 1);
    }
  }

  n_rem= (0x000F & (n_rem >> 12)); // final 4-bit reminder is CRC code
  n_prom[7]=crc_read; // restore the crc_read to its original place
  return (n_rem == crc_read && crc_read != 0);
}


void MS5803_14BA::sendCommand(uint8_t command) {
  Wire.beginTransmission(MS5803_14BA_I2C_ADDRESS);
  Wire.write(command);
  Wire.endTransmission(I2C_NOSTOP, 100);
}

#endif
