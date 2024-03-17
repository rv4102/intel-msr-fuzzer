#include <iostream>
#include <fstream>
#include <string>
#include "measure/measure.h"

int main(int argc, char *argv[]) {
    // if(argc < 2) {
    //     std::cout << "Please provide assembly code as input also.\n";
    //     exit(1);
    // }

    // // read assembly file
    // std::ifstream assembly_code(argv[1]);
    // std::string line, asm_temp;

    // if(! assembly_code.is_open()) {
    //     std::cout << "Unable to open file\n";
    //     exit(1);
    // }

    // init the measurement library
    init();

    int num_readings = 1000;
    int num_input_types = 100000;

    for(int i = 0; i < num_input_types; i++) {
        // run the initial assembly code
        asm("nop");
        
        Measurement start = measure();
        for(int j = 0; j < num_readings; j++) {
            // run the target assembly code and measure power
            asm("nop");
        }
        Measurement stop = measure();
        Sample sample = convert(start, stop);

        std::cout << sample.energy << std::endl;
    }
}