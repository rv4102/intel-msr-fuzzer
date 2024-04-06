MSR_VAL=0x00000611

all: libmeasure.a

libmeasure.a: measure.cpp measure.h
	g++ -c measure.cpp -DMSR=MSR_VAL -o measure.o
	ar rcs libmeasure.a measure.o

clean:
	-rm measure.o libmeasure.a