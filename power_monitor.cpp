#include <random>
#include <cstdlib>
#include "./measure/measure.h"

#define NUM_RUNS 1000000
#define NUM_READINGS 10000

void basic_inst(std::mt19937& rng, std::uniform_int_distribution<std::mt19937::result_type>& distribution) {

}

void measurement_inst() {

}

int main(int argc, char *argv[]) {
    // init the measurement library
    init();
    std::random_device dev;
    std::mt19937 rng(dev());
    std::uniform_int_distribution<std::mt19937::result_type> distribution(1,1000000);

    for(int i = 0; i < NUM_READINGS; i++) {
        basic_inst(rng, distribution);

        Measurement start = measure();
        for(int j = 0; j < NUM_RUNS; j++) {
            measurement_inst();
        }
        Measurement stop = measure();
        Sample sample = convert(start, stop);

        printf("%lf\n", sample.energy);
    }
}