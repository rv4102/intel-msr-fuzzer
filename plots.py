import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

def read_file(file_path):
    with open(file_path, 'r') as file:
        data = np.array([float(line.strip()) for line in file])
    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot TVLA Results')
    parser.add_argument('asm_code_path', type=str, help='Path to assembly code')
    args = parser.parse_args()
        
    with open(args.asm_code_path, 'r') as f:
        asm_code = f.read()
    
    num_instructions = 0
    instructions = []
    for line in asm_code.split('\n'):
        instructions.append(line)
        if line.strip() != "":
            num_instructions += 1
    
    # if outputs folder doesnt exist then create it
    if not os.path.exists('./plots'):
        os.makedirs('./plots')
    
    for i in range(num_instructions):
        data1 = read_file(f'./outputs/inst_{i+1}.txt')
        data2 = read_file(f'./outputs/inst_{i+1}_ct.txt')
        
        # plot each instruction in a separate plot
        plt.figure()

        plt.plot(data1, label='HT')
        plt.plot(data2, label='CT')
        plt.title(f'Instruction {i+1}')
        plt.xlabel('Frequency')
        plt.ylabel('Power')

        plt.legend()

        plt.savefig(f'./plots/inst_{i+1}.png')
