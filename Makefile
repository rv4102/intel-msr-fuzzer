MSR_VAL=0x64E
ASM_PATH=./test_cases/at_t/basic.s

run:
	sudo python3 main.py $(ASM_PATH) $(MSR_VAL)

plot:
	python3 plot.py $(ASM_PATH)

power_monitor: libmeasure.a
	g++ power_monitor.cpp -L./measure -I./measure -l:libmeasure.a -o power_monitor

libmeasure.a: ./measure/measure.cpp ./measure/measure.h
	g++ -c ./measure/measure.cpp -w -DMSR=MSR_VAL -o ./measure/measure.o
	ar rcs ./measure/libmeasure.a ./measure/measure.o

clean:
	-rm ./measure/measure.o ./measure/libmeasure.a power_monitor
