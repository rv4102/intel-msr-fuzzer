all:
	g++ power_monitor.cpp -L./measure -I./measure -l:libmeasure.a -o power_monitor