#include <random>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <assert.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#define MSR 0x611
#define NUM_RUNS 1000000
#define NUM_READINGS 10000

static int fd;

void init() {
    fd = open("/dev/cpu/1/msr", O_RDONLY);
    assert(fd > 0);
}

uint64_t read() {
    uint64_t value;
    ssize_t n = pread(fd, &value, 8, MSR);
    assert(n == 8);
    return value;
}

uint64_t convert(uint64_t start, uint64_t stop) {
    return stop - start;
}

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

        uint64_t start = read();
        for(int j = 0; j < NUM_RUNS; j++) {
            measurement_inst();
        }
        uint64_t stop = read();
        uint64_t sample = convert(start, stop);

        printf("%lu\n", sample);
    }
}