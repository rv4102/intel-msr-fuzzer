.intel_syntax noprefix
mfence
.test_case_enter:
.function_main:
.bb_main.entry:
jmp .bb_main.0
.bb_main.0:
mov eax, 1
mov ebx, 2
add eax, ebx
imul eax, ebx
.bb_main.exit:
.test_case_exit:
mfence