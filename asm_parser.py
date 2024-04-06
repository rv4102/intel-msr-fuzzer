import re

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