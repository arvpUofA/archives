/* This program loads the PRU clock program into the PRU-ICSS, transfers the configuration
 * into the PRU memory spaces and starts execution.
 */

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <prussdrv.h>
#include <pruss_intc_mapping.h>
#include <time.h>

#define CLK_PRU_NUM		0	// Using PRU0 for the sample clock
#define ADC_PRU_NUM		1	// Using PRU1 for the ADC

#define MMAP0_LOC		"/sys/class/uio/uio0/maps/map0/"
#define MMAP1_LOC		"/sys/class/uio/uio0/maps/map1/"

enum FREQUENCY {
	FREQ_500kHz =  95,
	FREQ_250kHz = 196,
	FREQ_200kHz = 245,
	FREQ_100kHz = 495,
	FREQ_25kHz = 1995,
	FREQ_10kHz = 4995,
	FREQ_5kHz =  9995,
	FREQ_2kHz = 24995,
	FREQ_1kHz = 49995
};

enum CONTROL {
	PAUSED = 0,
	RUNNING = 1,
	UPDATE = 3
};

// Short function to load a single unsigned int from a sysfs entry
unsigned int readFileValue( char filename[] ){
	FILE* fp;
	unsigned int value = 0;
	fp = fopen( filename, "rt" );
	fscanf( fp, "%x", &value );
	fclose( fp );
	return value;
}

clock_t prev;

void *halfThreadFunction( void *arg ) {
	unsigned int* mem_loc = (unsigned int*) arg;
	while(1) {
		int notimes = prussdrv_pru_wait_event( PRU_EVTOUT_0 );
		double time_spent = (double)(clock() - prev) / CLOCKS_PER_SEC;
		printf( "1st: Reading from 0x%x every %.3f\n", *mem_loc, time_spent );
		prussdrv_pru_clear_event( PRU_EVTOUT_0, PRU0_ARM_INTERRUPT );
		prev = clock();
	}
	return NULL;
}

clock_t prev2;

void *fullThreadFunction( void *arg ) {
	unsigned int* mem_loc = (unsigned int*) arg;
	while(1) {
		int notimes = prussdrv_pru_wait_event( PRU_EVTOUT_1 );
		double time_spent = (double) (clock() - prev2) / CLOCKS_PER_SEC;
		printf( "2nd: Reading from 0x%x every %.3f\n", *mem_loc, time_spent );
		prussdrv_pru_clear_event( PRU_EVTOUT_1, PRU1_ARM_INTERRUPT );
		prev2 = clock();
	}
	return NULL;
}

int main(void) {
	if( getuid() != 0 ) {
		printf( "You must run this program as root. Exiting.\n" );
		exit( EXIT_FAILURE );
	}
	
	// Initailize structre used by prussdrv_pruintc_intc
	tpruss_intc_initdata pruss_intc_initdata = PRUSS_INTC_INITDATA;

	// PRU sample clock data
	unsigned int timerData[2];
	timerData[0] = FREQ_250kHz;
	timerData[1] = RUNNING;
	printf( "The PRU clock state is set as period %d and state %d\n", timerData[0], timerData[1] );

	// PRU adc data
	unsigned int adcData[2];
	adcData[0] = readFileValue( MMAP1_LOC "addr" );
	adcData[1] = readFileValue( MMAP1_LOC "size" );
	printf( "The DDR External Memory pool has location: 0x%x and size: 0x%x bytes\n", adcData[0], adcData[1] );
	int numberSamples = adcData[1] / 2;
	printf( "-> this space has capacity to store %d 16-bit samples (max)\n", numberSamples );

	// Allocate and initialize memory
	prussdrv_init();
	prussdrv_open( PRU_EVTOUT_0 );
	prussdrv_open( PRU_EVTOUT_1 );

	// write the freq and state to PRU0 dataram
	prussdrv_pru_write_memory( PRUSS0_PRU0_DATARAM, 0, timerData, 8 );
	// write ddr memory location and size to PRU1 dataram
	prussdrv_pru_write_memory( PRUSS0_PRU1_DATARAM, 0, adcData, 8 );

	// Map the PRU's interrupts
	prussdrv_pruintc_init( &pruss_intc_initdata );

	// load and execute the PRU programs on the PRU
	prussdrv_exec_program( CLK_PRU_NUM, "./PRUClock.bin" );
	printf( "Sampling clock is running (%d)\n", timerData[0] );
	prussdrv_exec_program( ADC_PRU_NUM, "./PRUADC.bin" );
	printf( "Sampling ...\n" );
	
	// create threads
	// send starting size
	unsigned int size = adcData[0];
	pthread_t half_thread;
	if( pthread_create( &half_thread, NULL, halfThreadFunction, &size ) ) {
		printf( "Failed to create thread." );
		return( EXIT_FAILURE );
	}
	// send size for second half
	unsigned int second_size = adcData[0] + ( adcData[1] / 2 );
	pthread_t full_thread;
	if( pthread_create( &full_thread, NULL, fullThreadFunction, &second_size ) ) { 
		printf( "Failed to create thread." );
		return( EXIT_FAILURE );
	}

	// wait here forever
	while(1);

	// Disable the PRU and close memory mappings
	prussdrv_pru_disable( CLK_PRU_NUM );
	prussdrv_pru_disable( ADC_PRU_NUM );

	// join threads
	//pthread_join( half_thread, NULL );
	//pthread_join( full_thread, NULL );

	prussdrv_exit();

	return EXIT_SUCCESS;
}
