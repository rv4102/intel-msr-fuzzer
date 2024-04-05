#include <iostream>
#include <fstream>
#include <string>
#include "measure.h"

void basic_inst() {

}

void measurement_inst() {

}

int main(int argc, char *argv[]) {
    // init the measurement library
    init();

    int num_readings = 250000;
    basic_inst();

    Measurement start = measure();
    for(int j = 0; j < num_readings; j++) {
        measurement_inst();
    }
    Measurement stop = measure();
    Sample sample = convert(start, stop);

    std::cout << sample.energy << std::endl;
}