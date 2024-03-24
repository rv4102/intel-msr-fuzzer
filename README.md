# Setup instructions

1. Install Intel RAPL interface using:
    ```
    sudo apt update
    sudo apt install powercap-utils 
    ```
2. Install scipy and numpy using pip

# Run instructions

```main.sh``` contains all the code needed to first create a contract trace for 1000 different input values (contract traces) and then to create 1000 readings for a fixed input value (hardware traces).

1. ```chmod +x main.sh```
2. ```./main.sh```

# Other

All outputs are created and stored in ```./outputs```

```i_output.txt``` files contain the cumulative power reading upto ith instruction pertaining to the contract traces.

```i_output_ht.txt``` contains the cumulative power reading upto ith instruction pertaining to the hardware traces.

```inst_i.txt``` contains the power reading due to ith instruction whereas ```inst_i_ht.txt``` contains the power reading due to ith instruction in case of hardware traces.

The TVLA code looks uses ```inst_i.txt``` and ```inst_i_ht.txt``` and finds violations.