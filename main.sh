#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <asm_file.asm> <input.cpp>"
    exit 1
fi

asm_file="$1"
input_file="$2"
output_file="${input_file%.cpp}_modified.cpp"

# Loop over each instruction in the asm file
num_instructions=$(wc -l < "$asm_file")
for ((i=1; i<=num_instructions; i++)); do
    # Create asm files for each i
    ./inst_split.sh "$asm_file" "$i"

    if [ -s "${asm_file%.asm}_first_instructions.asm" ]; then
        echo
    else
        echo "nop" > "${asm_file%.asm}_first_instructions.asm"
    fi
    # Read lines from the replacement file and enclose them in double quotes
    while IFS= read -r line; do
        replacement_lines+="\"$line;\"\n"
    done < "${asm_file%.asm}_first_instructions.asm"

    
    # Replace "nop" with the lines from the replacement file in the input file
    sed "0,/\"nop\"/s//${replacement_lines}/" "$input_file" > "$output_file"

    sed -i "0,/nop/s//$(cat ${asm_file%.asm}_ith_instruction.asm)/" "$output_file"

    # Compile the modified C code
    g++ -o output "$output_file" -L./measure -I./measure -l:libmeasure.a

    # Run the code
    sudo taskset -c 1 ./output > "${i}_output.txt"

    # Clean up the asm files
    rm "${asm_file%.asm}_first_instructions.asm" "${asm_file%.asm}_ith_instruction.asm" "$output_file"
done

echo "Compilation completed"
