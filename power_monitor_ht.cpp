#include <iostream>
#include <fstream>
#include <string>
#include "measure.h"

int main(int argc, char *argv[]) {
    // init the measurement library
    init();

    int num_input_types = 1000;
    int num_readings = 250000;

    int result;
    for(int i = 0; i < num_input_types; i++) {
        // value1 and value2 are fixed
        volatile int value1 = 3;
        volatile int value2 = 4;

        Measurement start = measure();
        for(int j = 0; j < num_readings; j++) {
            // run the target assembly code and measure power
            asm volatile (
                // "movl %1, %%eax;"   // Move value1 into register %eax
                // "movl %2, %%ebx;"   // Move value2 into register %ebx
                // "addl %%ebx, %%eax;" // Add value2 to value1 (result in %eax)
                // "imull %%ebx, %%eax;" // Multiply value1 by value2 (result in %eax)
                // "movl %%eax, %0;"   // Move the result to the 'result' variable
                : "=r" (result)     // Output operand (result) tied to %0
                : "r" (value1), "r" (value2) // Input operands (value1 and value2) tied to %1 and %2
                : "%eax", "%ebx"    // Clobbered registers
            );
        }
        Measurement stop = measure();
        Sample sample = convert(start, stop);

        std::cout << sample.energy << std::endl;
    }
}