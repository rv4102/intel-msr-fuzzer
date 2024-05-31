xor %edx, %edx;
cmp $0x0, %edx;
cmovz 0(%rsp), %rax;