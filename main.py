import sys
import re
import os
import subprocess
import argparse
import random
from tvla import tvla
from asm_parser import convert

def replace_func_body(file_path, basic_inst, measurement_inst):
    output = ""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        output += line
        if re.match(r'\s*void basic_inst\(\) {', line):
            output += basic_inst
        if re.match(r'\s*void measurement_inst\(\) {', line):
            output += measurement_inst
    return output

def create_temp_assembly(asm_code, line_num):
    basic_inst_code = ""
    measurement_inst_code = ""
    lines = asm_code.split('\n')
    for i, line in enumerate(lines):
        if i < line_num:
            basic_inst_code += line + '\n'
        elif i == line_num:
            measurement_inst_code += line + '\n'
        else:
            break
    
    with open('basic_inst.s', 'w') as f:
        f.write(basic_inst_code)
    
    with open('measurement_inst.s', 'w') as f:
        f.write(measurement_inst_code)
    
def create_hardware_trace(asm_code, power_monitor_code_path, line_num):
    create_temp_assembly(asm_code, line_num)
    basic_inst = convert('basic_inst.s')
    measurement_inst = convert('measurement_inst.s')

    # replace basic_inst() and measurement_inst() in power_monitor.c
    if line_num == 0:
        basic_inst = ""

    power_monitor_code = replace_func_body(power_monitor_code_path, basic_inst, measurement_inst)

    # write to temp file
    with open('temp.cpp', 'w') as f:
        f.write(power_monitor_code)
        
    # compile temp file in a separate process
    result = subprocess.run(['g++', 'temp.cpp', '-L./measure', '-I./measure', '-l:libmeasure.a', '-o', 'temp'])

    # run temp file num_readings times
    with open(f'./outputs/inst_{line_num+1}_ht.txt', 'a') as f:
        for j in range(num_readings):
            if j/num_readings == 0.50:
                print("50% done")
            result = subprocess.run(['./temp'], stdout=subprocess.PIPE)
            f.write(result.stdout.decode('utf-8'))
    print("100% done")
        
    # delete temp, temp.cpp, basic_inst.s, measurement_inst.s
    os.remove('temp')
    os.remove('temp.cpp')
    os.remove('basic_inst.s')
    os.remove('measurement_inst.s')

def create_contract_trace(asm_code, power_monitor_code_path, line_num):
    # run temp file num_readings times
    for j in range(num_readings):
        # replace the locations with $num values present in the assembly code with random values
        lines = asm_code.split('\n')
        for i, line in enumerate(lines):
            lines[i] = re.sub(r'\$[0-9]+', f'${str(random.randint(0, 10000))}', line)
        asm_code = '\n'.join(lines)

        create_temp_assembly(asm_code, line_num)
        basic_inst = convert('basic_inst.s')
        measurement_inst = convert('measurement_inst.s')

        # replace basic_inst() and measurement_inst() in power_monitor.c
        if line_num == 0:
            basic_inst = ""
        power_monitor_code = replace_func_body(power_monitor_code_path, basic_inst, measurement_inst)

        # write to temp file
        with open('temp.cpp', 'w') as f:
            f.write(power_monitor_code)
            
        # compile temp file in a separate process
        result = subprocess.run(['g++', 'temp.cpp', '-L./measure', '-I./measure', '-l:libmeasure.a', '-o', 'temp'])
        result = subprocess.run(['./temp'], stdout=subprocess.PIPE)

        with open(f'./outputs/inst_{line_num+1}_ct.txt', 'a') as f:
            f.write(result.stdout.decode('utf-8'))
        
        if j/num_readings == 0.50:
            print("50% done")
    
    print("100% done")

    # delete temp, temp.cpp, basic_inst.s, measurement_inst.s
    os.remove('temp')
    os.remove('temp.cpp')
    os.remove('basic_inst.s')
    os.remove('measurement_inst.s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Hardware/Contract Trace')
    parser.add_argument('asm_code_path', type=str, help='Path to assembly code')
    parser.add_argument('MSR_value', type=str, help='MSR Value')
    args = parser.parse_args()

    # change the value of Makefile argument to MSR_value
    with open('Makefile', 'r') as f:
        makefile = f.read()
        makefile = re.sub(r'MSR_VAL=0x[0-9A-Z]+', f'MSR_VAL={args.MSR_value}', makefile)
    with open('Makefile', 'w') as f:
        f.write(makefile)
    
    # compile libmeasure.a
    result = subprocess.run(['make', 'libmeasure.a'])

    # read assembly code
    with open(args.asm_code_path, 'r') as f:
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
    
    num_readings = 1000 
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

    exit(0)
