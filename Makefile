MSR_VAL=0x00000611

all: libmeasure.a
	g++ power_monitor.cpp -L./measure -I./measure -l:libmeasure.a -o power_monitor

libmeasure.a: ./measure/measure.cpp ./measure/measure.h
	g++ -c ./measure/measure.cpp -w -DMSR=MSR_VAL -o ./measure/measure.o
	ar rcs ./measure/libmeasure.a ./measure/measure.o

clean:
	-rm ./measure/measure.o ./measure/libmeasure.a power_monitor
