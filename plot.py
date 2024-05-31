from utils import read_file, tvla, make_plot
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Hardware/Contract Trace')
    parser.add_argument('ASM_Code_Path', type=str, help='Path to assembly code')
    args = parser.parse_args()

    # get folder name from args.ASM_Code_Path
    folder_name = args.ASM_Code_Path.split('/')[-1].split('.')[0]

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
    if not os.path.exists('./plots/at_t'):
        os.makedirs('./plots/at_t')
    
    print('####### Generating Plots ######')
    for i in range(num_instructions):
        data1 = read_file(f'./outputs/at_t/{folder_name}/inst_{i+1}_ht.txt')
        print(f'./outputs/at_t/{folder_name}/inst_{i+1}_ht.txt')
        data2 = read_file(f'./outputs/at_t/{folder_name}/inst_{i+1}_ct.txt')
        
        # show on the plot that TVLA detected a violation
        result = tvla(data1, data2)

        # make plot
        make_plot(data1, data2, i+1, instructions[i], result, folder_name)
    print('###### Plots Generated ######')