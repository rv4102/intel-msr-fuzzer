import sys
import os

if __name__ == "__main__":
    # this function accepts one argument:
    # the first is the path to the assembly input file

    if len(sys.argv) < 2:
        print("Usage: python3 wrapper.py <path to assembly file>")
        sys.exit(1)
    
    # the first path is to run the assembly and try to find violations with revizor script
    asm_file = sys.argv[1]

    if os.fork() == 0:
        print("--- Running revizor script ---")
        os.execve("python3", ["../sca-fuzzer/revizor.py", "-s", "base.json", "-i", asm_file], os.environ)
    else:
        print("--- Monitoring power consumption to find violations ---")
        

