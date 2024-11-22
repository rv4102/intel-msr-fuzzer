import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import re


def read_file(file_path):
    with open(file_path, "r") as file:
        data = np.array([float(line.strip()) for line in file])
    return data


def convert(file, randomize=False, is_measurement_inst=False):
    extended_asm = []
    registers = set()
    num_inputs = 0
    # with open(file_path, 'r') as file:

    for line in file:
        line = line.strip()  # remove leading and trailing whitespaces
        # add spaces before comma, after comma and before semi colon
        line = line.replace(",", " , ").replace(";", " ; ")
        tokens = line.split()  # split the line into tokens

        changed_line = ""
        for token in tokens:
            # check if the token is a register
            if re.match(r"%[a-z]+", token):
                # print("register ", token)
                if len(token) > 4:
                    token = token[0:4]
                if token != "%rsp":
                    registers.add(token)
                changed_line += " %" + token

            # if the token is a number (argument or immediate value)
            elif re.match(r"\$[0-9]+", token):
                # print("number ", token)
                changed_line += " %" + str(num_inputs)
                num_inputs += 1
            else:
                # print("normal ", token)
                changed_line += " " + token

        extended_asm.append(changed_line)

    # convert the extended assembly to asm volatile block
    asm_volatile = ""
    if not is_measurement_inst:
        if not randomize:
            for i in range(1, num_inputs + 1):
                asm_volatile += f"\tvolatile uint32_t arg{i} = {i};\n"
        else:
            for i in range(1, num_inputs + 1):
                asm_volatile += f"\tvolatile uint32_t arg{i} = distribution(rng);\n"

    asm_volatile += "\tasm volatile(\n"
    for line in extended_asm:
        asm_volatile += '\t\t"' + line + '"\n'

    # get the list of input registers and output values
    asm_volatile += "\t\t:\n\t\t:"  # no outputs

    for i in range(1, num_inputs):
        asm_volatile += '"r" ' + f"(arg{i}), "

    if num_inputs > 0:
        asm_volatile += '"r" ' + f"(arg{num_inputs})"

    # get the list of clobbered registers
    asm_volatile += "\n\t\t: "
    for idx, register in enumerate(registers):
        if idx == len(registers) - 1:
            asm_volatile += '"' + register + '"'
        else:
            asm_volatile += '"' + register + '", '
    asm_volatile += "\n\t);"

    return asm_volatile, num_inputs


def create_temp_assembly(asm_code, line_num):
    basic_inst_code = ""
    measurement_inst_code = ""
    lines = asm_code.split("\n")
    for i, line in enumerate(lines):
        if i < line_num:
            basic_inst_code += line + "\n"
        elif i == line_num:
            measurement_inst_code += line + "\n"
        else:
            break

    return basic_inst_code, measurement_inst_code
    # return "", asm_code


def replace_func_body(
    file_path,
    basic_inst,
    measurement_inst,
    measurement_inst_num_inputs,
    randomize=False,
):
    output = ""
    with open(file_path, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if re.match(
            r"\s*void basic_inst\(std::mt19937\& rng, std::uniform_int_distribution<std::mt19937::result_type>\& distribution\) {",
            line,
        ):
            output += line
            output += basic_inst
        elif re.match(r"\s*void measurement_inst\(\) {", line):
            output += "void measurement_inst("
            for j in range(1, measurement_inst_num_inputs):
                output += f"uint32_t arg{j}, "

            if measurement_inst_num_inputs > 0:
                output += "uint32_t arg" + str(measurement_inst_num_inputs) + ") {\n"
            else:
                output += ") {\n"

            output += measurement_inst
        elif re.match(r"\s*Measurement start = measure\(\);", line):
            if measurement_inst_num_inputs > 0:
                output += "\t\tvolatile uint32_t "
                if not randomize:
                    for j in range(1, measurement_inst_num_inputs):
                        output += f"arg{j} = {j}, "
                    output += (
                        "arg"
                        + str(measurement_inst_num_inputs)
                        + " = "
                        + str(measurement_inst_num_inputs)
                        + ";\n"
                    )
                else:
                    for j in range(1, measurement_inst_num_inputs):
                        output += f"arg{j} = distribution(rng), "
                    output += (
                        "arg"
                        + str(measurement_inst_num_inputs)
                        + " = distribution(rng);\n"
                    )
            output += line
        elif re.match(r"\s*measurement_inst\(\);", line):
            output += "\t\t\tmeasurement_inst("
            for j in range(1, measurement_inst_num_inputs):
                output += f"arg{j}, "

            if measurement_inst_num_inputs > 0:
                output += f"arg{measurement_inst_num_inputs});\n"
            else:
                output += ");\n"
        else:
            output += line
    return output


def tvla(data1, data2, alpha=4.5):
    t_stat, p_val = stats.ttest_ind(data1, data2, equal_var=False)
    print("T-Statisitc: ", t_stat, "; P-Value: ", p_val)

    if abs(t_stat) > alpha:
        # print("Reject Null Hypothesis: Significant side-channel leakage detected")
        return 1
    else:
        # print("Accept Null Hypothesis: No significant side-channel leakage detected")
        return 0


def make_plot(data1, data2, instruction_num, instruction, tvla_result, folder_name):
    # plot each instruction in a separate plot
    plt.figure()

    plt.plot(data1, label="HT")
    plt.plot(data2, label="CT")
    plt.title(f"Instruction {instruction_num}: {instruction}")
    # plt.title('edx set to 1')
    plt.xlabel("Reading")
    plt.ylabel("MSR 0x64E: Productive Performance Count")

    if tvla_result == 1:
        plt.plot([], [], " ", label="t-stat > 4.5, Violation")
    else:
        plt.plot([], [], " ", label="t-stat <= 4.5, No Violation")

    plt.legend()

    plt.savefig(f"./plots/at_t/{folder_name}/inst_{instruction_num}.png")
    plt.close()
    return
