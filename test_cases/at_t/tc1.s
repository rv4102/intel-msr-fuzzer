xor %edx, %edx;
cmp $1, %edx;
cmovz 0( %rsp ), %rax;