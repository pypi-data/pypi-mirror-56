#ifndef WASI_PREAMBLE
#define WASI_PREAMBLE 1

#include <unistd.h>
#include <sys/types.h>
#include <limits.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/stat.h>
#include <wasi/core.h>
#include <errno.h>
#include <utime.h>

// char *realpath(const char *path, char *resolved_path);
// uid_t getuid(void);
// int getpagesize(void);

__attribute__((weak)) uid_t getuid(void) { return 0; }
__attribute__((weak)) char *realpath(const char *path,   char *resolved_path) { return 0; }
// int chdir(const char *path);


///
#define PAGESIZE (0x10000)
#define PAGE_SIZE PAGESIZE
#define SIG_IGN 0
#define SIG_ERR 1
#define F_DUPFD 0
#define SIG_DFL 0
#define ESHUTDOWN 1
#define MAX_GROUPS 1
#define GRND_NONBLOCK 0

__attribute__((weak)) int getpagesize(void) { printf("getpagesize\n"); return PAGE_SIZE; }

__attribute__((weak)) int mprotect(void *addr, size_t len, int prot) { printf("mprotect\n"); return 0; }

__attribute__((weak)) int sysctlbyname(const char *name, void *oldp,	size_t *oldlenp, const void *newp, size_t newlen) { printf("sysctlbyname\n"); return 0; }

__attribute__((weak)) pid_t getpid(void) { printf("getpid\n"); return 0; }

__attribute__((weak)) uid_t geteuid(void) { printf("geteuid\n"); return 0; }

__attribute__((weak)) gid_t getgid(void) { printf("getgid\n"); return 0; }

__attribute__((weak)) gid_t getegid(void) { printf("getegid\n"); return 0; }

__attribute__((weak)) int chmod(const char *pathname, mode_t mode) { printf("chmod\n"); return 0; }
__attribute__((weak)) int chdir(const char *path) { printf("chdir\n"); return 0; }

__attribute__((weak)) int signal(int signum, int handler) { printf("signal\n"); return 0; }

__attribute__((weak)) int sigaction(int signum, const struct sigaction *act,
                     struct sigaction *oldact) { printf("sigaction\n"); return 0; }


// FILE *popen(const char *cmd, const char *mode);
// int pclose(FILE *f);
// mode_t umask(mode_t mode);
// int utime (const char *a, const struct utimbuf *b);

__attribute__((weak)) FILE *popen(const char *cmd, const char *mode) { printf("popen\n"); return 0; }
__attribute__((weak)) int pclose(FILE *f) { printf("pclose\n"); return 0; }
__attribute__((weak)) mode_t umask(mode_t mode) { printf("umask\n"); return 0; }
// __attribute__((weak)) int utime (const char *a, const struct utimbuf *b) { printf("utime\n"); return 0; }
__attribute__((weak)) int grantpt(int fd) { printf("grantpt\n"); return 0; }
__attribute__((weak)) int unlockpt(int fd) { printf("unlockpt\n"); return 0; }
// __attribute__((weak)) char *ptsname(int fd) { return 0; }
__attribute__((weak)) char *ptsname(int fd) { printf("ptsname\n"); return 0; }
__attribute__((weak)) int dup(int fd) { printf("dup\n"); return 0; }
__attribute__((weak)) struct passwd *getpwuid(uid_t uid) { printf("getpwuid\n"); return 0; }
__attribute__((weak)) struct passwd *getpwnam(const char *name) { printf("getpwnam\n"); return 0; }

__attribute__((weak)) void *dlopen(const char *filename, int flag)  { printf("dlopen\n"); return 0; }
__attribute__((weak)) char *dlerror(void) { printf("dlerror\n"); return 0; }
__attribute__((weak)) void *dlsym(void *handle, const char *symbol) { printf("dlsym\n"); return 0; }
__attribute__((weak)) int dlclose(void *handle) { printf("dlclose\n"); return 0; }

__attribute__((weak)) char *getcwd(char *buf, size_t size) {return 0;}
__attribute__((weak)) int clock_settime(clockid_t clk_id, const struct timespec *tp) {return 0;}
__attribute__((weak)) int utime(const char *filename, const struct utimbuf *times) {return 0;}
__attribute__((weak)) int raise(int sig) {return 0;}
__attribute__((weak)) ssize_t getrandom(void *buf, size_t buflen, unsigned int flags) {
    if (buflen > 256) {
        errno = EIO;
        return -1;
    }
    int r = __wasi_random_get(buf, buflen);
    if (r != 0) {
        errno = r;
        return -1;
    }
    return buflen;
}

// getcwd
// clock_settime
// ttyname
// system
// kill
// pipe
// raise
#endif