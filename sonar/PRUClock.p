// PRU0 program to provide a variable frequency clock on P9_31 (pru0_pru_r30_0)
// that is controlled from Linux userspace by setting the PRU memory state. 
// The program is memory controlled using the first two 4-byte numbers in PRU 
// memory space:
// - The delay is set in memory address 0x00000000 (4 bytes long)
// - The counter is turned on and off by setting the LSB of 0x00000004 (4 bytes)
//   to 1 (on) or 0 (off)
// - The delay value can be updated by setting the second most LSB to 1 (it will return
//   to 0 to indicate that update has been performed.

// Register map
// r0 | temp register (indexing)
// r1 | base address (0x00000000) 
// r2 | clock period
// r3 | state of counter
// r4 | PRU shared memory address (0x00010000)
// r5 | state of clock (HIGH/LOW)

.origin 0
.entrypoint START

#define     CLK_OUT     r30.t0

START:                          // aims to load the clock period into r2
    MOV     r1, 0x00000000      // load the base address into r1
    LBBO    r2, r1, 0, 4        // load clock delay from mem into r2 (4 bytes)
    MOV     r4, 0x00010000      // use the PRU shared memory to share the state changed
    MOV     r5, r1              // r5 is going to store the state of clock i.e. high/low
    QBA     ENDOFLOOP           // move to comparison

MAINLOOP:
    CLR     CLK_OUT             // set the clock signal to low
    CLR     r5.t00              // update state register
    SBBO    r5, r4, 0, 4        // store the clock state in shared memory
    MOV     r0, r2              // load the delay r2 into temp r0 (50% duty cycle)
    ADD     r0, r0, 1           // balance the duty cycle by looping 1 extra time on low

DELAYOFF:
    SUB     r0, r0, 1           // decrement the counter by 1
    QBNE    DELAYOFF, r0, 0     // loop until the delay has expired  ( ==0 )

    MOV     r0, r2              // reload the delay r2 into r0
    SET     CLK_OUT             // set the clock signal to high
    SET     r5.t00              // update state register
    SBBO    r5, r4, 0, 4        // store the clock state in PRU shared memory

DELAYON:
    SUB     r0, r0, 1           // decrement the counter by 1
    QBNE    DELAYON, r0, 0      // loop until delay has expired ( ==0 )

ENDOFLOOP:                      // is the clock running?
    LBBO    r3, r1, 4, 4        // loaded the state into r3 -- is running? ( bytes)
    QBBS    RESETCLK, r3.t1     // if r3 bit 1 is high then reload the clock period
    QBBS    MAINLOOP, r3.t0     // if r3 bit 0 is high then clock is running
    QBA     ENDOFLOOP

RESETCLK:                       // clear the r3.t1 bit and write back to memory
                                // indicating that the clock frequency has been updated
    CLR     r3, r3.t1           // clear the reload clock flag
    SBBO    r3, r1, 4, 4        // write the value back into memory
    QBA     START               // go back to start of program

END:
    HALT                        // program never ends (never reached)
    
