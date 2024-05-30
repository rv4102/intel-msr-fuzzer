# Setup instructions

1. Load MSR module using
    ```
    sudo modprobe msr
    ```
2. Install Intel RAPL interface using:
    ```
    sudo apt update
    sudo apt install powercap-utils 
    ```
3. Install scipy and numpy using pip
4. Disable Intel SGX extensions to stop RAPL Filtering (go to BIOS -> Security -> Intel SGX)

# Explanation of setup

The file ```main.py``` contains all the code needed to compile and measure the energy consumption for different instructions. Our methodology is simple: for a given ```instruction.s``` file containing assembly code, we measure energy for each instruction by first changing the input operand values and obtaining a set of 1000 readings and then fix the input operand values and measure energy again 1000 times for each instruction. Then we run a TVLA analysis to check if there is a significant leakage.

The motivation behind this attack lies in the Platypus paper and we aim to support multiple MSRs with different kinds of physical measurements to be used for creating the profile of each instruction.

# Run instructions

```main.py``` contains all the code needed to first create a contract trace for 1000 different input values (contract traces) and then to create 1000 readings for a fixed input value (hardware traces).

1. ```make run``` (sudo is needed in order to read the MSR values)
2. ```make plot```

# Other

All outputs are created and stored in ```./outputs```

```inst_i.txt``` contains the power reading due to ith instruction whereas ```inst_i_ct.txt``` contains the power reading due to ith instruction in case of contract traces.

The TVLA code looks uses ```inst_i.txt``` and ```inst_i_ct.txt``` and finds violations.