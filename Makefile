MSR_VAL=0x64E
ASM_PATH=./test_cases/at_t/basic.s

run:
	sudo python3 main.py $(ASM_PATH) $(MSR_VAL)

plot:
	python3 plot.py $(ASM_PATH)

power_monitor:
	g++ power_monitor.cpp -DMSR=MSR_VAL -o power_monitor

clean:
	-rm power_monitor
