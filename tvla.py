from scipy import stats
import numpy as np 
import argparse

def tvla(file1_path, file2_path):
    # read data from file1 and file2
    with open(file1_path, 'r') as file1:
        data1 = np.array([float(line.strip()) for line in file1])
    with open(file2_path, 'r') as file2:
        data2 = np.array([float(line.strip()) for line in file2])

    t_stat, p_val = stats.ttest_ind(data1, data2, equal_var=False)
    alpha = 0.05

    # # output the results
    # print("t-statistic: ", t_stat)
    # print("p-value: ", p_val)
    # print("critical value: ", critical_value)

    if p_val < alpha:
        # print("Reject Null Hypothesis: Significant side-channel leakage detected")
        return 1
    else:
        # print("Accept Null Hypothesis: No significant side-channel leakage detected")
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TVLA')
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

    # run TVLA and print results
    print('###### Running TVLA ######')
    for i in range(num_instructions):
        print("Running TVLA for instruction: ", instructions[i])
        result = tvla(f'./outputs/inst_{i+1}_ht.txt', f'./outputs/inst_{i+1}_ct.txt')
        if result == 1:
            print("Violation Detected, significant leakage found")
            # exit(0)
    
    print('No violation detected, no significant leakage found')
    exit(0)