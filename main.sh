#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <asm_file.asm> <input.cpp>"
    exit 1
fi

asm_file="$1"
input_file="$2"

# # Compile the C code without any changes
# gcc -o output "$input_file"

# Loop over each instruction in the asm file
num_instructions=$(wc -l < "$asm_file")
for ((i=1; i<=num_instructions; i++)); do
    # Create asm files for each i
    ./inst_split.sh "$asm_file" "$i"

    # Replace two "nop"s with the contents of the asm files
    sed -i "0,/nop/s//$(cat ${asm_file%.asm}_first_instructions.asm | tr -d '\n')/" "$input_file"
    sed -i "0,/nop/s//$(cat ${asm_file%.asm}_ith_instruction.asm | tr -d '\n')/" "$input_file"

    # Compile the modified C code
    gcc -o output "$input_file"

    # Clean up the asm files
    rm "${input_file%.c}_first_instructions.asm" "${input_file%.c}_ith_instruction.asm"
done

echo "Compilation completed"
