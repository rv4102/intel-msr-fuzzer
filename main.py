import sys
import re
import os
import subprocess

def convert(file_path):
    extended_asm = []
    with open(file_path, 'r') as file:
        registers = set()
        for line in file:
            line = line.strip() # remove leading and trailing whitespaces  
            # add spaces before comma, after comma and before semi colon          
            line = line.replace(',', ' , ').replace(';', ' ; ')
            tokens = line.split() # split the line into tokens

            changed_line = ''
            for token in tokens:
                # check if the token is a register
                if re.match(r'%[a-z]+', token):
                    if len(token) > 4:
                        token = token[0:4]
                    registers.add(token)
                    changed_line += ' %' + token
                else:
                    changed_line += ' ' + token
            
            extended_asm.append(changed_line)

    # convert the extended assembly to asm volatile block
    asm_volatile = 'asm volatile(\n'
    for line in extended_asm:
        asm_volatile += '\t"' + line + '"\n'

    # get the list of input registers and output values
    asm_volatile += '\t:\n\t:\n'
    
    # get the list of clobbered registers
    asm_volatile += '\t: '
    for idx, register in enumerate(registers):
        if idx == len(registers) - 1:
            asm_volatile +=  '"' + register + '"\n'
        else:
            asm_volatile +=  '"' + register + '", '
    asm_volatile += ');'

    return asm_volatile

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
        else:
            measurement_inst_code += line + '\n'
    
    with open('basic_inst.s', 'w') as f:
        f.write(basic_inst_code)
    
    with open('measurement_inst.s', 'w') as f:
        f.write(measurement_inst_code)
    
def create_hw_trace(asm_code, power_monitor_code_path, line_num):
    create_temp_assembly(asm_code, i)
    basic_inst = convert('basic_inst.s')
    measurement_inst = convert('measurement_inst.s')

    # replace basic_inst() and measurement_inst() in power_monitor.c
    power_monitor_code = replace_func_body(power_monitor_code_path, basic_inst, measurement_inst)

    # write to temp file
    with open('temp.cpp', 'w') as f:
        f.write(power_monitor_code)
        
    # compile temp file in a separate process
    result = subprocess.run(['g++', 'temp.cpp', '-L./measure', '-I./measure', '-l:libmeasure.a', '-o', 'temp'])

    # if outputs folder doesnt exist then create it
    if not os.path.exists('./outputs'):
        os.makedirs('./outputs')

    # run temp file num_readings times
    for j in range(num_readings):
        result = subprocess.run(['./temp'], stdout=subprocess.PIPE)

        with open(f'./outputs/inst_{i}.txt', 'a') as f:
            f.write(result.stdout.decode('utf-8'))
        
    # delete temp, temp.cpp, basic_inst.s, measurement_inst.s
    os.remove('temp')
    os.remove('temp.cpp')
    os.remove('basic_inst.s')
    os.remove('measurement_inst.s')

if __name__ == '__main__':
    # read assembly code
    with open(sys.argv[1], 'r') as f:
        asm_code = f.read()
    
    # read power_monitor
    power_monitor_code_path = sys.argv[2]
    
    num_instructions = 0
    for line in asm_code.split('\n'):
        # get instruction 
        if line.strip() != "":
            num_instructions += 1
    
    print(f'Number of instructions: {num_instructions}')
    print('###### Building Hardware Trace ######')
    
    num_readings = 1000
    
    for i in range(1, num_instructions):
        print("Building trace for instruction: ")
        create_hw_trace(asm_code, power_monitor_code_path, i)
    
    print('###### Hardware Trace Built ######')

    # run TVLA and print results

