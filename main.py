from utils import convert, replace_func_body, create_temp_assembly, read_file, tvla, make_plot
import subprocess
import argparse
import re
import os

def create_contract_trace(asm_code, power_monitor_code_path, line_num):
    basic_inst_code, measurement_inst_code = create_temp_assembly(asm_code, line_num)
    basic_inst_code, measurement_inst_code = basic_inst_code.split('\n'), measurement_inst_code.split('\n')
    basic_inst, _ = convert(basic_inst_code, randomize = True)
    measurement_inst, measurement_inst_num_inputs = convert(measurement_inst_code, is_measurement_inst = True, randomize = True)

    # replace basic_inst() and measurement_inst() in power_monitor.c
    if line_num == 0:
        basic_inst = ""
    
    power_monitor_code = replace_func_body(power_monitor_code_path, basic_inst, measurement_inst, measurement_inst_num_inputs, randomize = True)
    with open('temp.cpp', 'w') as f:
        f.write(power_monitor_code)
    
    # compile temp file in a separate process
    result = subprocess.run(['g++', 'temp.cpp', '-L./measure', '-I.', '-l:libmeasure.a', '-o', 'temp'])

    if os.path.exists(f'./outputs/inst_{line_num+1}_ct.txt'):
        os.remove(f'./outputs/inst_{line_num+1}_ct.txt')

    # run temp file and store its output
    with open(f'./outputs/inst_{line_num+1}_ct.txt', 'a') as f:
        result = subprocess.run(['sudo',  'taskset', '-c', '1', './temp'], stdout=subprocess.PIPE)
        f.write(result.stdout.decode('utf-8'))

    os.remove('temp')
    os.remove('temp.cpp')


def create_hardware_trace(asm_code, power_monitor_code_path, line_num):
    basic_inst_code, measurement_inst_code = create_temp_assembly(asm_code, line_num)
    basic_inst_code, measurement_inst_code = basic_inst_code.split('\n'), measurement_inst_code.split('\n')
    basic_inst, _ = convert(basic_inst_code)
    measurement_inst, measurement_inst_num_inputs = convert(measurement_inst_code, is_measurement_inst = True)

    # replace basic_inst() and measurement_inst() in power_monitor.c
    if line_num == 0:
        basic_inst = ""
    
    power_monitor_code = replace_func_body(power_monitor_code_path, basic_inst, measurement_inst, measurement_inst_num_inputs)
    with open('temp.cpp', 'w') as f:
        f.write(power_monitor_code)
    
    # compile temp file in a separate process
    result = subprocess.run(['g++', 'temp.cpp', '-L./measure', '-I.', '-l:libmeasure.a', '-o', 'temp'])

    if os.path.exists(f'./outputs/inst_{line_num+1}_ht.txt'):
        os.remove(f'./outputs/inst_{line_num+1}_ht.txt')

    # run temp file num_readings times
    with open(f'./outputs/inst_{line_num+1}_ht.txt', 'a') as f:
        result = subprocess.run(['sudo',  'taskset', '-c', '1', './temp'], stdout=subprocess.PIPE)
        f.write(result.stdout.decode('utf-8'))
        
    os.remove('temp')
    os.remove('temp.cpp')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Hardware/Contract Trace')
    parser.add_argument('ASM_Code_Path', type=str, help='Path to assembly code')
    parser.add_argument('MSR_Value', type=str, help='MSR Value')
    args = parser.parse_args()
    
    # compile libmeasure.a
    result = subprocess.run(['make', 'libmeasure.a'])

    # read assembly code
    with open(args.ASM_Code_Path, 'r') as f:
        asm_code = f.read()
    
    num_instructions = 0
    instructions = []
    for line in asm_code.split('\n'):
        instructions.append(line)
        if line.strip() != "":
            num_instructions += 1
    
    # if outputs folder doesnt exist then create it
    if not os.path.exists('./outputs'):
        os.makedirs('./outputs')
    
    # num_readings = 1000 
    print(f'Number of instructions: {num_instructions}')

    print('###### Building Hardware Trace ######')
    for i in range(num_instructions):
        print("Building trace for instruction: ", instructions[i])
        create_hardware_trace(asm_code, './power_monitor.cpp', i)
    print('###### Hardware Trace Built ######')

    print('###### Building Contract Trace ######')
    for i in range(num_instructions):
        print("Building trace for instruction: ", instructions[i])
        create_contract_trace(asm_code, './power_monitor.cpp', i)
    print('###### Contract Trace Built ######')

    # if outputs folder doesnt exist then create it
    if not os.path.exists('./plots'):
        os.makedirs('./plots')
    
    print('####### Generating Plots ######')
    for i in range(num_instructions):
        data1 = read_file(f'./outputs/inst_{i+1}_ht.txt')
        data2 = read_file(f'./outputs/inst_{i+1}_ct.txt')
        
        # show on the plot that TVLA detected a violation
        result = tvla(data1, data2)

        # make plot
        make_plot(data1, data2, i+1, instructions[i], result)
    print('###### Plots Generated ######')

    exit(0)
