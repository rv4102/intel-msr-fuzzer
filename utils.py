import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import re

def read_file(file_path):
    with open(file_path, 'r') as file:
        data = np.array([float(line.strip()) for line in file])
    return data


def convert(file, randomize = False):
    extended_asm = []
    registers = set()
    num_inputs = 0
    # with open(file_path, 'r') as file:

    for line in file:
        line = line.strip() # remove leading and trailing whitespaces  
        # add spaces before comma, after comma and before semi colon          
        line = line.replace(',', ' , ').replace(';', ' ; ')
        tokens = line.split() # split the line into tokens

        changed_line = ''
        for token in tokens:
            # check if the token is a register
            if re.match(r'%[a-z]+', token):
                # print("register ", token)
                if len(token) > 4:
                    token = token[0:4]
                registers.add(token)
                changed_line += ' %' + token
            # if the token is a number (argument or immediate value)
            elif re.match(r'\$[0-9]+', token):
                # print("number ", token)
                changed_line += ' %' + str(num_inputs)
                num_inputs += 1
            else:
                # print("normal ", token)
                changed_line += ' ' + token
        
        extended_asm.append(changed_line)

    # convert the extended assembly to asm volatile block
    asm_volatile = ''
    if not randomize:
        for i in range(1, num_inputs+1):
            asm_volatile += f'uint32_t arg{i} = {i};\n'
    else:
        for i in range(1, num_inputs+1):
            asm_volatile += f'uint32_t arg{i} = rand();\n'

    asm_volatile += 'asm volatile(\n'
    for line in extended_asm:
        asm_volatile += '\t"' + line + '"\n'

    # get the list of input registers and output values
    asm_volatile += '\t:\n\t:' # no outputs
    
    for i in range(1, num_inputs+1):
        if i == num_inputs:
            asm_volatile += '"r" ' + f'(arg{i})\n'
        else:
            asm_volatile += '"r" ' + f'(arg{i}), '
    
    # get the list of clobbered registers
    asm_volatile += '\t: '
    for idx, register in enumerate(registers):
        if idx == len(registers) - 1:
            asm_volatile +=  '"' + register + '"\n'
        else:
            asm_volatile +=  '"' + register + '", '
    asm_volatile += ');'

    return asm_volatile


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
    
    # with open('basic_inst.s', 'w') as f:
    #     f.write(basic_inst_code)
    
    # with open('measurement_inst.s', 'w') as f:
    #     f.write(measurement_inst_code)
    return basic_inst_code, measurement_inst_code


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


def tvla(data1, data2, alpha = 0.05):
    t_stat, p_val = stats.ttest_ind(data1, data2, equal_var=False)

    if p_val < alpha:
        # print("Reject Null Hypothesis: Significant side-channel leakage detected")
        return 1
    else:
        # print("Accept Null Hypothesis: No significant side-channel leakage detected")
        return 0
    

def make_plot(data1, data2, instruction_num, instruction, tvla_result):
    # plot each instruction in a separate plot
    plt.figure()

    plt.plot(data1, label='HT')
    plt.plot(data2, label='CT')
    plt.title(f'Instruction {instruction_num}: {instruction}')
    plt.xlabel('Reading')
    plt.ylabel('MSR 0x64E Productive Performance Count')

    if tvla_result == 1:
        plt.plot([], [], ' ', label='p-value < 0.05, Violation')
    else:
        plt.plot([], [], ' ', label='p-value >= 0.05, No Violation')

    plt.legend()

    plt.savefig(f'./plots/inst_{instruction_num}.png')
    plt.close()
    return