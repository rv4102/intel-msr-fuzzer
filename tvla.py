import numpy as np 
from scipy import stats
import argparse

def main():
    # read input file1 and file2 from command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("file1", help="input file1")
    parser.add_argument("file2", help="input file2")

    args = parser.parse_args()
    file1 = args.file1
    file2 = args.file2

    # read data from file1 and file2
    with open(file1, 'r') as file1:
        data1 = np.array([float(line.strip()) for line in file1])
    with open(file2, 'r') as file2:
        data2 = np.array([float(line.strip()) for line in file2])

    t_stat, p_val = stats.ttest_ind(data1, data2, equal_var=False)
    alpha = 0.05

    df = len(data1) + len(data2) - 1
    critical_value = stats.t.ppf(1 - alpha / 2, df)

    # # output the results
    # print("t-statistic: ", t_stat)
    # print("p-value: ", p_val)
    # print("critical value: ", critical_value)

    if abs(t_stat) > critical_value:
        # print("Reject Null Hypothesis: Significant side-channel leakage detected")
        return 1
    else:
        # print("Accept Null Hypothesis: No significant side-channel leakage detected")
        return 0
    
if __name__ == "__main__":
    print(main())