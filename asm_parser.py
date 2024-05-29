import re

def convert(file_path):
    extended_asm = []
    registers = set()
    num_inputs = 0
    with open(file_path, 'r') as file:

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
                    num_inputs += 1
                    changed_line += ' %' + str(num_inputs)
                else:
                    # print("normal ", token)
                    changed_line += ' ' + token
            
            extended_asm.append(changed_line)

    # convert the extended assembly to asm volatile block
    asm_volatile = ''
    for i in range(1, num_inputs+1):
        asm_volatile += f'uint32_t arg{i} = {i};\n'

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