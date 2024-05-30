#include <ctime>
#include <stdio.h>
#include <cstdlib>
#include "./measure/measure.h"

#define NUM_RUNS 250000
#define NUM_READINGS 1000

void basic_inst() {

}

void measurement_inst() {

}

int main(int argc, char *argv[]) {
    // init the measurement library
    init();

    srand(time(NULL));

    for(int i = 0; i < NUM_READINGS; i++) {
        basic_inst();

        Measurement start = measure();
        for(int j = 0; j < NUM_RUNS; j++) {
            measurement_inst();
        }
        Measurement stop = measure();
        Sample sample = convert(start, stop);

        printf("%lf\n", sample.energy);
    }
}