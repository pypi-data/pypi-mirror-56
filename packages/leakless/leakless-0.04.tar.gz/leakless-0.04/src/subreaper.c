//
// A wrapper process that catches stray children from its process tree,
// and kills them all when the first process exits.
//

// Note that most of this code is intended to be invoked in a CLONE_VM
// context. So basically, it can't use global memory, and needs to be
// careful even about which libc functions it calls.
// TODO: Reduce use of fopen and *printf calls. This is to remove doubts
// about memory allocation, threading, and stack size that come from
// using the host libc.

#ifndef __linux__
#error "Subreaper is necessarily linux-only"
#endif

#define _GNU_SOURCE
#include <sched.h>

#include <stdlib.h>
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <signal.h>
#include <sys/prctl.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <sys/syscall.h>

struct globals {
  //
  // These MUST be set up before entering doit()
  //
  const char *path; // path to exec
  char **argv; // argv to exec with
  char **envp; // envp to execve with, or null for execv
  int errfd; // fd for subreaper internal errors. May be zero.
  void (*post_fork)(void*);
  void *post_fork_arg;

  pid_t pid; // Avoid getpid() to be sure we don't hit glibc caching.
  void *sighandler;

  

#ifndef STANDALONE
  void *free_me; // munmap this on termination, if not null.
  size_t free_len;
#endif

  //
  // Leave these uninitialized before doit()
  //
  pid_t child_pid;
  bool got_sigterm;
};


//
// Convenience functions, macros, and compile-time settings.
//

static void dperror(int fd, const char *s, int errnum) {
  //char buf[100];
  //strerror_r(errnum, buf, sizeof buf);
  //fprintf(fp, "%s: %s\n", s, buf);
  char buf[100];
  size_t slen = strlen(s);
  if(slen > 64)
    slen = 64;
  memcpy(buf, s, slen);
  char *gnu = strerror_r(errnum, &buf[slen], sizeof buf - slen - 1);
  if(gnu != &buf[slen])
    strncpy(&buf[slen], gnu, sizeof buf - slen - 1);
  buf[sizeof buf - 1] = 0;
  size_t len = strlen(buf);
  buf[len] = '\n';
  write(fd, buf, len+1);
}

static int writes(int fd, const char *s) {
  return write(fd, s, strlen(s));
}

#define perror dont use me
#ifdef SILENT
static const bool show_reaped_procs = false;
static const bool show_killed_procs = false;
#define eperror(x) ((void)0)
#define eprintf(...) ((int)0)
#define eputs(s) ((int)0)
#else
#define STRINGIFY_(x) #x
#define STRINGIFY(x) STRINGIFY_(x)

static const bool show_reaped_procs = false; // Just for testing, no one actually cares.
static const bool show_killed_procs = true;
#define eperror(s) (globals->errfd >= 0 ? dperror(globals->errfd, (STRINGIFY(__LINE__) " " s ": "), errno) : (void)0)
#define eprintf(...) (globals->errfd >= 0 ? dprintf(globals->errfd, __VA_ARGS__) : 0)
#define eputs(s) (globals->errfd >= 0 ? writes(globals->errfd, (s)) : 0)
#endif

#ifndef STANDALONE
extern void __attribute__((__noreturn__)) unmap_stack_and_exit(void *page, size_t len, int status);
extern void __attribute__((__noreturn__)) unmap_stack_and_signal(void *page, size_t len, pid_t pid, int sig);
extern char trampoline;
extern char trampoline_entry;
extern void *trampoline_data;
extern void *trampoline_target;
extern char trampoline_end;
#endif

//
// printing helper functions
//

// Mini show, used for show_reaped_procs
static void _show_reaped_proc(int fd, pid_t pid, int wstatus) {
  dprintf(fd, "$!=%d $?=%d\n", pid, WIFEXITED(wstatus) ? WEXITSTATUS(wstatus) : -WTERMSIG(wstatus));
}

#define show_reaped_proc(pid, wstatus) (show_reaped_procs && globals->errfd >= 0 ? _show_reaped_proc(globals->errfd, (pid), (wstatus)) : (void)0)

// Full show, used for show_killed_procs
static void show_proc(struct globals *globals, pid_t pid) {
  char buf[500];
  if(snprintf(buf, sizeof buf, "/proc/%u/cmdline", pid) >= sizeof buf) {
    eprintf("snprintf: truncated %s\n", buf);
    return;
  }

  FILE *cmdline = fopen(buf, "r");
  if(!cmdline) {
    switch(errno) {
      case ENOENT:
        // Don't care if processes disappear on us. This might never actually
        // happen, since show_proc is only called on direct children (which
        // stick around until we reap them).
        break;
      case EACCES:
        // Assumedly this is a permissions error; we're already going to perror
        // for kill() later, so messages now would be redundant.
        break;
      default:
        eperror("fopen");
        break;
    }
    return;
  }

  // Print out cmdline, replacing nulls with spaces.
  size_t size = fread(buf, 1, sizeof buf - 1, cmdline);
  if(size <= 0) {
    if(ferror(cmdline)) {
      eperror("fread");
      fclose(cmdline);
      return;
    }
    size = 0;
  }
  fclose(cmdline);

  for(int i = 0; i < size; i++) {
    if(buf[i] == 0)
      buf[i] = ' ';
    else if(buf[i] < 32 || buf[i] >= 127)
      buf[i] = '.';
  }
  buf[size] = 0;

  if(eprintf("$!=%d $*=%s\n", pid, buf) <= 0) {
    eperror("fwrite"); // probably fails too but whatever
    return;
  }
}


//
// 
//

static void kill_children(struct globals *globals, int sig) {
  char buf[40];
  if(snprintf(buf, sizeof buf, "/proc/self/task/%u/children", globals->pid) >= sizeof buf) {
    eprintf("snprintf: truncated %s\n", buf);
    return;
  }

  FILE *children = fopen(buf, "r");
  if(!children) {
    eperror("fopen");
    eputs("Can't kill children due to inaccessible /proc/self/task/tid/children\n");
    return;
  }

  while(1) {
    pid_t pid;
    int ret = fscanf(children, " %u", &pid);
    if(ret == EOF || ret < 0) {
      if(ferror(children))
        eperror("fscanf");
      break;
    }

    if(ret != 1) {
      eputs("fscanf: match failure\n");
      break;
    }

    if(show_killed_procs)
      show_proc(globals, pid);
    if(kill(pid, sig) < 0)
      eperror("kill");
  }

  fclose(children);
}

// Reap without blocking, returns true iff no remaining children.
static bool wait_for_children(struct globals *globals, unsigned long timeout_millis) {
  pid_t pid;
  int stat;
  struct timespec start_time;

  if(timeout_millis > 0) {
    clock_gettime(CLOCK_MONOTONIC_RAW, &start_time);
  }

again:
  while(1) {
    pid = waitpid(-1, &stat, WNOHANG);
    if(pid < 0) {
      if(errno == ECHILD)
        return true;
      eperror("wait");
      return false; // Shouldn't be possible.
    }

    if(pid == 0) {
      break;
    } else {
      show_reaped_proc(pid, stat);
    }
  }

  if(timeout_millis > 0) {
    struct timespec tv;
    clock_gettime(CLOCK_MONOTONIC_RAW, &tv);
    unsigned long millis = (tv.tv_sec - start_time.tv_sec)*1000 + (tv.tv_nsec - start_time.tv_nsec) / 1000000;
    if(millis < timeout_millis) {
      unsigned long to_sleep = timeout_millis / 4;
      if(to_sleep > 2000) to_sleep = 2000;
      else if(to_sleep < 2) to_sleep = 2;
      usleep(to_sleep * 1000);
      goto again;
    }
  }

  return false;
}

static void my_sighandler(struct globals *globals, int sig) {
  if(sig == SIGTERM) {
    if(!globals->got_sigterm) {
      globals->got_sigterm = true;
    } else {
      // Second SIGTERM, upgrade to killing the child.
      sig = SIGKILL;
    }
  }

  if(globals->child_pid > 0)
    kill(globals->child_pid, sig);
}

#ifdef STANDALONE
struct globals *global_globals_ref;
static void standalone_sighandler(int sig) {
  my_sighandler(sig, global_globals_ref);
}
#endif

static void __attribute__((__noreturn__)) doit(struct globals *globals) {
  if(prctl(PR_SET_CHILD_SUBREAPER, 1) < 0) {
    eperror("prctl");
    goto abort;
  }

  sigset_t allset, oset;
  sigfillset(&allset);
  sigprocmask(SIG_SETMASK, &allset, &oset);

  pid_t child_pid = fork();
  if(child_pid < 0) {
    eperror("fork");
    goto abort;
  }
  if(child_pid == 0) {
    sigprocmask(SIG_SETMASK, &oset, NULL);
    if(globals->post_fork)
      globals->post_fork(globals->post_fork_arg);
    if(globals->envp)
      execve(globals->path, globals->argv, globals->envp);
    else
      execv(globals->path, globals->argv);
    eperror("execve");
    goto abort;
  }

  globals->child_pid = child_pid;
  globals->got_sigterm = false;

  {
    // We could do better by looking at siginfo source pid to forward all
    // foriegn signals, but meh, this seems like enough.
    struct sigaction act;
    memset(&act, 0, sizeof(act));
    act.sa_handler = globals->sighandler;
    act.sa_flags = SA_RESTART;
    sigaction(SIGHUP, &act, 0);
    sigaction(SIGINT, &act, 0);
    sigaction(SIGQUIT, &act, 0);
    sigaction(SIGALRM, &act, 0);
    sigaction(SIGTERM, &act, 0);
    sigaction(SIGUSR1, &act, 0);
    sigaction(SIGUSR2, &act, 0);

    act.sa_handler = SIG_IGN;
    sigaction(SIGTTOU, &act, 0);
    sigaction(SIGPIPE, &act, 0);

    act.sa_handler = SIG_DFL;
    act.sa_flags = SA_NOCLDSTOP;
    sigaction(SIGCHLD, &act, 0);
  }
  sigprocmask(SIG_SETMASK, &oset, NULL);

  int status;

  // reap until child exits.
  while(1) {
    eprintf("waiting...\n");
    pid_t pid = wait(&status);
    eprintf("got %d\n", pid);

    if(pid < 0) {
      if(errno == EINTR)
        continue;
      // Really shouldn't be possible...
      eperror("wait");
      goto abort;
    }

    if(pid == child_pid) {
      child_pid = -1; // Make sure no one tries to use this.
      break;
    }

    show_reaped_proc(pid, status);
  }

  // We're going down, mask out everything.
  // (Any signals we got, we'd be forwarding to an already-reaped child process.)
  sigprocmask(SIG_SETMASK, &allset, NULL);

  show_reaped_proc(0, status); // Show main proc as pid 0 to distinguish it.

  do {
    // Silently reap everything that's already exited or exits before a grace period.
    if(wait_for_children(globals, 1000))
      break;

    // Kill & complain about remaining children.
    kill_children(globals, SIGTERM);
    if(wait_for_children(globals, 3000))
      break;

    // Really kill children now. Let init do the reaping.
    kill_children(globals, SIGKILL);
  } while(0);

  if(WIFEXITED(status)) {
#ifndef STANDALONE
    if(globals->free_me)
      unmap_stack_and_exit(globals->free_me, globals->free_len, WEXITSTATUS(status));
#endif
    _exit(WEXITSTATUS(status));
  } else {
    // Try to imitate the signal death.
    int sig = WTERMSIG(status);
    signal(sig, SIG_DFL);
#ifndef STANDALONE
    if(globals->free_me)
      unmap_stack_and_signal(globals->free_me, globals->free_len, globals->pid, sig);
#endif
    kill(globals->pid, sig);
    _exit(128 + sig);
  }

  // Note that this abort stub is also used for the fork() child,
  // in which case it does more cleanup than necessary but that's fine.
abort:
  signal(SIGABRT, SIG_DFL);
  if(globals->free_me)
    unmap_stack_and_signal(globals->free_me, globals->free_len, globals->pid, SIGABRT);
  kill(globals->pid, SIGABRT);
  _exit(128 + SIGABRT);
  __builtin_trap();
}

//
// Entry points
//

#ifdef STANDALONE
int main(int argc, char *argv[]) {
  if(argc <= 1)
    return 127;
  struct globals globals = {
    .path = argv[1],
    .argv = &argv[1],
    .envp = NULL,
    .errfd = STDERR_FILENO,
    .pid = getpid(),
    .sighandler = standalone_sighandler
    .post_fork = NULL;
  };
  global_globals_ref = &globals;
  doit(&globals);
  return -1;
}
#endif // ifdef STANDALONE

//
// Launch path with argv. Errors from subreaper itself will print to errfd,
// as will notifications about killed stray processes.
//
// errfd can be -1, to not print anywhere. errfd can be closed as soon as
// subreaper_spawn returns; we effectivley duplicate the descriptor. errfd
// should have CLOEXEC set if you do not want it to be open in the child process.
//
// DO NOT SIGKILL THE RETURNED PID, that would defeat the entire point of
// using subreaper and allow processes to escape.
// Instead, sigterm it twice, and the underlying child process will be sigkilled
// on your behalf. There's a hard-coded shutdown procedure that occurs whenever
// the child process exits (via signal or naturally), that takes a few seconds
// and sigterm & sigkills any stray processes.
//
#ifndef STANDALONE
pid_t subreaper_spawn(const char *path, char *const argv[], char *const envp[], int errfd, void (*post_fork)(void *), void *post_fork_arg) {
  // The problem with fork() is that the subreaper process does not go on to exec.
  // This means that we'd be maintaining a copy of the heap at the time of the
  // subreaper_spawn() call, which kinda sucks for our usecase of long-running
  // Python processes.
  // So, we're gonna use clone() to essentially fork, but keep the same address space.
  // This of course requires extreme care.
#ifdef SUBREAPER_USE_FORK
  pid_t subreaper_pid = fork();
  if(subreaper_pid < 0) {
    int t = errno;
    if(errfd > 0)
      dperror(errfd, "fork: ", errno);
    errno = t;
    return -1;
  }
  if(subreaper_pid == 0) {
    struct globals globals = {
      .path = path,
      .argv = argv,
      .errfd = errfd,
      .pid = getpid(),
      .free_me = NULL,
      .free_len = 0,
      .post_fork = post_fork,
      .post_fork_arg = post_fork_arg,
    };
    doit(&globals);
    __builtin_trap();
  }
#else
  //
  // Allocate stack. A struct globals & deep copies of path/argv/envp will
  // sit on top of the stack.
  //
  long page_size = sysconf(_SC_PAGESIZE);

  // First, determine how much non-stack space we'll need.
  size_t strings_len = strlen(path) + 1;
  int argv_len = 0;
  int envp_len = 0;
  for(; argv[argv_len]; argv_len++)
    strings_len += strlen(argv[argv_len])+1;
  if(envp) {
    for(; envp[envp_len]; envp_len++)
      strings_len += strlen(envp[envp_len])+1;
  }

  // 64k stack, plus the argument space we need, plus the trampoline space, plus extra pages for rounding reasons.
  size_t stack_size = (64<<10) + sizeof(struct globals) + strings_len + (argv_len + envp_len + 2) + (&trampoline_end - &trampoline) + 3*page_size;
  stack_size = stack_size / page_size * page_size;

  // allocate the stack.
  char *stack_bottom = mmap(NULL, stack_size, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS|MAP_STACK, -1, 0);
  char *stack_top = &stack_bottom[stack_size];
  if(stack_bottom == MAP_FAILED) {
    int t = errno;
    if(errfd > 0)
      dperror(errfd, "mmap: ", errno);
    errno = t;
    return -1;
  }

  // Initialize globals at top of stack.
  stack_top -= sizeof(struct globals);
  struct globals *globals = (void*)stack_top;
  globals->free_me = stack_bottom;
  globals->free_len = stack_size;
  globals->errfd = errfd;
  globals->post_fork = post_fork;
  globals->post_fork_arg = post_fork_arg;

  // Initialize trampoline at bottom of the stack
  memcpy(stack_bottom, &trampoline, &trampoline_end - &trampoline);
  *(void**)((char*)&trampoline_target - &trampoline + stack_bottom) = &my_sighandler;
  *(void**)((char*)&trampoline_data - &trampoline + stack_bottom) = globals;
  globals->sighandler = stack_bottom + (&trampoline_entry - &trampoline);

  // We picked the bottom of stack to store the executable trampoline,
  // so it can also serve as a small guard page.
  if(mprotect(stack_bottom, ((&trampoline_end - &trampoline) + page_size - 1) / page_size * page_size, PROT_READ|PROT_EXEC) == -1) {
    int t = errno;
    if(errfd > 0)
      dperror(errfd, "mprotect: ", errno);
    munmap(stack_bottom, stack_size);
    errno = t;
    return -1;
  }

  //
  // Copy path & argv & envnp to top of stack.
  //
  stack_top -= (argv_len+1) * sizeof(char*);
  globals->argv = (char**)stack_top;
  globals->argv[argv_len] = NULL;
  if(envp) {
    stack_top -= (envp_len+1) * sizeof(char*);
    globals->envp = (char**)stack_top;
    globals->envp[envp_len] = NULL;
  } else {
    globals->envp = NULL;
  }

  stack_top -= strings_len;
  char *p = stack_top;
  globals->path = p;
  p = stpcpy(p, path)+1;
  for(int i = 0; i < argv_len; i++) {
    globals->argv[i] = p;
    p = stpcpy(p, argv[i])+1;
  }
  for(int i = 0; i < envp_len; i++) {
    globals->envp[i] = p;
    p = stpcpy(p, envp[i])+1;
  }
  assert(p == stack_top + strings_len);

  stack_top = (char*)((uintptr_t)stack_top & ~(uintptr_t)0x3F);
  pid_t subreaper_pid = clone((int(*)(void*))doit, stack_top, CLONE_VM|SIGCHLD|CLONE_CHILD_SETTID, globals, NULL, NULL, &globals->pid);
  if(subreaper_pid < 0) {
    int t = errno;
    if(errfd > 0)
      dperror(errfd, "clone: ", errno);
    errno = t;
    return -1;
  }
#endif

  return subreaper_pid;
}
#endif // ifndef STANDALONE
