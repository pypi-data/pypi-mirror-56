#include <sys/syscall.h>

.text
// void unmap_stack_and_exit(void *page, size_t len, int status)
.global unmap_stack_and_exit
// void unmap_stack_and_signal(void *page, size_t len, pid_t pid, int sig)
.global unmap_stack_and_signal

.global trampoline
.global trampoline_target
.global trampoline_data
.global trampoline_entry
.global trampoline_end

#if defined(__i386__)
.intel_syntax noprefix
.align 4
unmap_stack_and_exit:
  pop ebp
  pop ebx
  pop ecx
  pop esi

  mov eax, SYS_munmap
  int 0x80

  mov eax, SYS_exit
  mov ebx, esi
  int 0x80
  ud2

.align 4
unmap_stack_and_signal:
  pop ebp
  pop ebx
  pop ecx
  pop esi
  pop edi

  mov eax, SYS_munmap
  int 0x80

  mov eax, SYS_kill
  mov ebx, esi
  mov ecx, edi
  int 0x80

  mov eax, SYS_exit
  mov ebx, edi
  add ebx, 128
  int 0x80
  ud2

.align 4
trampoline:
trampoline_target:
  .byte 0,0,0,0
trampoline_data:
  .byte 0,0,0,0
trampoline_entry:
  pop ecx
  call $+5
0:
  pop eax
  push [eax - (0b - trampoline_data)]
  push ecx
  jmp [eax - (0b - trampoline_target)]
trampoline_end:
  nop

#elif defined(__x86_64__)
.intel_syntax noprefix
.align 4
unmap_stack_and_exit:
  mov eax, SYS_munmap
  syscall

  mov eax, SYS_exit
  mov edi, edx
  syscall
  ud2

.align 4
unmap_stack_and_signal:
  mov ebx, ecx

  mov eax, SYS_munmap
  syscall

  mov eax, SYS_kill
  mov edi, edx
  mov esi, ebx
  syscall

  mov eax, SYS_exit
  mov edi, ebx
  add edi, 128
  syscall
  ud2

.align 4
trampoline:
trampoline_target:
  .byte 0,0,0,0, 0,0,0,0
trampoline_data:
  .byte 0,0,0,0, 0,0,0,0
trampoline_entry:
  pop rax
  push [rip + trampoline_data]
  push rax
  jmp [rip + trampoline_target]
trampoline_end:
  nop

#elif defined(__arm__)
unmap_stack_and_exit:
  mov r7, # SYS_munmap
  swi #0

  mov r7, # SYS_exit
  mov r0, r2
  swi #0
  .inst 0xe7f000f0

unmap_stack_and_signal:
  mov r7, # SYS_munmap
  swi #0

  mov r7, # SYS_kill
  mov r0, r2
  mov r1, r3
  swi #0

  mov r7, # SYS_exit
  mov r0, r3
  add r0, #128
  swi #0
  .inst 0xe7f000f0

.align 4
trampoline:
trampoline_target:
  .byte 0,0,0,0
trampoline_data:
  .byte 0,0,0,0
trampoline_entry:
  mov r1, r0
  ldr r0, trampoline_data
  ldr pc, trampoline_target
trampoline_end:
  nop

#elif defined(__aarch64__)
unmap_stack_and_exit:
  mov x8, # SYS_munmap
  svc #0
  mov x8, # SYS_exit
  mov x0, x2
  svc #0
  hlt #0

unmap_stack_and_signal:
  mov x8, # SYS_munmap
  svc #0

  mov x8, # SYS_kill
  mov x0, x2
  mov x1, x3
  svc #0

  mov x8, # SYS_exit
  add x0, x3, #128
  svc #0
  hlt #0

.align 4
trampoline:
trampoline_target:
  .byte 0,0,0,0, 0,0,0,0
trampoline_data:
  .byte 0,0,0,0, 0,0,0,0
trampoline_entry:
  mov x1, x0
  ldr x0, trampoline_data
  ldr x2, trampoline_target
  br x2
trampoline_end:
  nop

#else
#error "unsupported arch"
#endif
