# Sonar System

## Compiling
* DTS `dtc -O dtb -o ARVP-PRU-ADC-00A0.dtbo -b 0 -@ ARVP-PRU-ADC.dts`
* PRUClock.p `pasm -b PRUClock.p`
* C Program `gcc PRUADC.c -o PRUADC -lpthread -lprussdrv`

## Running
* Load the device tree overlay
	* `sudo cp ARVP-PRU-ADC-00A0.dtbo /lib/firmware`
	* `sudo sh -c "echo ARVP-PRU-ADC > $SLOTS"`
	* `cat $SLOTS`
* Allocate 2MB of data in Linux Memory
	* `sudo rmmod uio_pruss`
	* `sudo modprobe uio_pruss extram_pool_sz=0x1E8480`
	* `lsmod`
* Run the program `sudo ./PRUADC`
