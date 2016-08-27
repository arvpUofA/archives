// PRU program to communicate to the ADS7861 SPI ADC ICs. To use this program,
// use the following wiring configuration:
// - Chip Select (CS): P8_27    pru1_pru_r30_8
// - CLK             : P8_28    pru1_pru_r30_10
// - CONVST          : P8_29    pru1_pru_r30_9
// - SER1A           : P8_39    pru1_pru_r31_6
// - SER1B           : P8_40    pru1_pru_r31_7

// Register map
// r0  | temp (indexing)
// r1  | base address (0x00000000)
// r3  | response from SER_A
// r4  | counter to read 16 bits (loaded with 16)
// r5  | address of shared memory (0x00010000)
// r6  | sampling clock flag (LSB)
// r7  | bit mask for output (0x00000FFF)
// r8  | linux memory address to store output
// r9  | size of linux memory available
// r10 | current memory address for output
// r11 | current memory size
// r12 | half of memory size

.setcallreg r29.w2
.origin     0
.entrypoint START

#define PRU0_R31_VEC_VALID  32
#define PRU_EVTOUT_0        3   // interrupt for half full
#define PRU_EVTOUT_1        4   // interrupt for memory full

#define CS      r30.t8
#define CLK     r30.t10
#define CONVST  r30.t9
#define SER1A   r31.t6

#define TIME_CLOCK  7   // t_h1 + t_lo = 125ns (manually calibrated)

START:
    // Enable the OCP master port
    LBCO    r0, C4, 4, 4            // load SYSCFG reg into r0
    CLR     r0, r0, 4               // clear bit 4 (STANDBY_INIT)
    SBCO    r0, C4, 4, 4            // write modified reg back

    MOV     r1, 0x00000000          // load base address in r1

    MOV     r7, 0x00000FFF          // bit mask on returned data (only keep 12 bits)
    LBBO    r8, r1, 0, 4            // load linux address to store values
    LBBO    r9, r1, 4, 4            // load size of memory space (noOfSamples = r9/2)

    LSR     r12, r9, 1              // half of memory size 
    
    MOV     r3, 0x00000000          // r3 will recieve response from SER_A
    CLR     CLK                     // pull clock low

START_CYCLE:
    MOV     r10, r8                 // load ddr memory address to r10
    MOV     r11, r9                 // load ddr memory size to r11

GET_SAMPLE:
    MOV     r5, 0x00010000          // stores base address of shared mem (stores sampling clock bit)

SAMPLE_WAIT_HIGH:                   // wait until PRU0 sampling clock goes high
    LBBO    r6, r5, 0, 4            // load sampling clock flag
    QBNE    SAMPLE_WAIT_HIGH, r6, 1 // wait until sampling clock goes high

    CLR     CS                      // pull CS low
    SET     CONVST                  // pull conversion start line high
    MOV     r4, 16                  // goes to read 16 bits

SPICLK_BIT:
    SUB     r4, r4, 1               // count down through the bits
    QBNE    SKIP_CLR, r4, 13        // if 13th bit clear consvt
    CLR     CONVST                  // pull convst low
SKIP_CLR:
    CALL    SPICLK
    QBNE    SPICLK_BIT, r4, 0       // performed 16 cycles?

    LSR     r3, r3, 2               // Shift right twice ( last two bits are useless (datasheet) ) 
    AND     r3, r3, r7              // AND the data with mask to get 12 LSBs

    MOV     r0, 3
WAIT_LOOP:
    SUB     r0, r0, 1
    QBNE    WAIT_LOOP, r0, 0
    SET     CS                      // pull CS high (end of sample)

STORE_DATA:
    SUB     r11, r11, 2             // reduce number of samples (2 bytes per sample)
    SBBO    r3.w0, r10, 0, 2        // store value of r3 in memory
    ADD     r10, r10, 2             // increment memory address
    QBNE    CYCLE_CONT, r11, r12    // branch if current mem size != half memory size
                                    // generate interrupt for memory half full
    MOV     r31.b0, PRU0_R31_VEC_VALID | PRU_EVTOUT_0
CYCLE_CONT:
    QBEQ    END_CYCLE, r11, 0       // memory full, create interrupt

SAMPLE_WAIT_LOW:                    // wait here if sample line is still high
    LBBO    r6, r5, 0, 4            // load sampling flag
    QBNE    SAMPLE_WAIT_LOW, r6, 0  // wait until sampling flag goes low
    QBA     GET_SAMPLE

END_CYCLE:
    // generate interrupt for memory full
    MOV     r31.b0, PRU0_R31_VEC_VALID | PRU_EVTOUT_1
    QBA     START_CYCLE

END:
    HALT    // end of program

// This procedure applies an SPI clock cycle to the SPI clock.
// The clock cycle is determined by TIME_CLOCK (time that the clock must remain
// high and remain low with 50% duty cycle)

SPICLK:
    LSL     r3, r3, 1               // shift captured data left by 1 position
    MOV     r0, TIME_CLOCK          // time for clock low -- CPOL = 0
CLKLOW:
    SUB     r0, r0, 1               // decrement the counter by 1 and loop
    QBNE    CLKLOW, r0, 0           // check if the clock is still low

    SET     CLK                     // set clock high
    MOV     r0, TIME_CLOCK          // time for clock high
CLKHIGH:
    SUB     r0, r0, 1
    QBNE    CLKHIGH, r0, 0
    CLR     CLK                     // set clock low
    // read data
    QBBC    DATAINLOW, SER1A        // if bit is low, jump
    OR      r3, r3, 0x00000001      // otherwise, set LSB bit to 1
DATAINLOW:
    RET
