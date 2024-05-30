from utils import tvla, read_file
import matplotlib.pyplot as plt
import argparse
import os

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
    
    
        
