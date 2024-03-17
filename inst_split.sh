#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_file.asm> <i>"
    exit 1
fi

input_file="$1"
i="$2"

# Create a file with the first i-1 instructions
head -n $((i-1)) "$input_file" > "${input_file%.asm}_first_instructions.asm"

# Create a file with only the ith instruction
sed -n "${i}p" "$input_file" > "${input_file%.asm}_ith_instruction.asm"

echo "Resulting files created:"
echo "${input_file%.asm}_first_instructions.asm"
echo "${input_file%.asm}_ith_instruction.asm"
