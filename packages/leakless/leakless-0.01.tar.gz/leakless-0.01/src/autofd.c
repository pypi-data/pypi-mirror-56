#ifdef __linux__
#include <sys/inotify.h>
#include <sys/eventfd.h>
#include <sys/syscall.h>
#endif
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/socket.h>
#include <stdbool.h>

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

#include "pyposix.inc"

// Convenience functions, for setting a python exception
// from errno and also closing fds & DECREFing

static void *PyErr_SetOSError_DECREF(PyObject *obj) {
  int t = errno;
  Py_DECREF(obj);
  errno = t;
  PyErr_SetFromErrno(PyExc_OSError);
  return NULL;
}

static bool set_cloexec_or_oserror_decref(int fd, PyObject *obj) {
  if(fcntl(fd, F_SETFD, FD_CLOEXEC) != -1)
    return true;
  int t = errno;
  close(fd);
  Py_DECREF(obj);
  errno = t;
  PyErr_SetFromErrno(PyExc_OSError);
  return false;
}

static bool set_cloexec2_or_oserror_decref(int *fds, PyObject *obj) {
  if(
    fcntl(fds[0], F_SETFD, FD_CLOEXEC) != -1 &&
    fcntl(fds[1], F_SETFD, FD_CLOEXEC) != -1
  ) {
    return true;
  }
  int t = errno;
  close(fds[0]);
  close(fds[1]);
  Py_DECREF(obj);
  errno = t;
  PyErr_SetFromErrno(PyExc_OSError);
  return false;
}


// The AutoFD object

typedef struct {
  PyObject_HEAD
  int fd;
} AutoFDObject;

static PyMemberDef AutoFD_members[] = {
    {"fd", T_INT, offsetof(AutoFDObject, fd), READONLY, "The file descriptor. Don't close this or store the int elsewhere; that would defeat the entire point of this library."},
    {NULL}  /* Sentinel */
};

static PyObject *AutoFD_alloc(PyTypeObject *type, Py_ssize_t nitems) {
  PyObject *self = PyType_GenericAlloc(type, nitems);
  if(self)
    ((AutoFDObject*)self)->fd = -1;
  return self;
}

static void AutoFD_dealloc(PyObject *self) {
  int *fd = &((AutoFDObject*)self)->fd;
  if(*fd != -1) {
    close(*fd);
    *fd = -1;
  }
  PyObject_Del(self);
}

static PyObject *AutoFD_repr(PyObject *self) {
  return PyUnicode_FromFormat("<AutoFD %d>", ((AutoFDObject*)self)->fd);
}

static PyObject *
AutoFD_close(PyObject *self, PyObject *Py_UNUSED(ignored)) {
  int *fd = &((AutoFDObject*)self)->fd;
  if(*fd != -1) {
    close(*fd);
    *fd = -1;
  }
  Py_RETURN_NONE;
}

static PyObject *
AutoFD_redup(PyObject *self, PyObject *other) {
  if(!PyLong_Check(other)) {
    PyErr_SetString(PyExc_TypeError, "AutoFD.redup takes an int");
    return NULL;
  }

  long old_fd = PyLong_AsLong(other);
  if(old_fd == -1 || (long)(int)old_fd != old_fd) {
    errno = EBADF;
    return PyErr_SetFromErrno(PyExc_OSError);
  }

  int new_fd = ((AutoFDObject*)self)->fd;

  if(dup2(old_fd, new_fd) == -1)
    return PyErr_SetFromErrno(PyExc_OSError);

  if(fcntl(new_fd, F_SETFD, FD_CLOEXEC) == -1) {
    // Weird case, the old new_fd has been closed so we can't revert.
    // Using dup3() on Linux would fix this. (In general, everywhere
    // we F_SETFD, Linux has a syscall variant that allows us to avoid
    // a separate fcntl; too bad those aren't cross-platform).
    int t = errno;
    AutoFD_close(self, NULL);
    errno = t;
    return PyErr_SetOSError_DECREF(self);
  }

  Py_RETURN_NONE;
}

static PyObject *
AutoFD_dup(PyObject *cls, PyObject *other) {
  if(!PyLong_Check(other)) {
    PyErr_SetString(PyExc_TypeError, "AutoFD.dup takes an int");
    return NULL;
  }

  long old_fd = PyLong_AsLong(other);
  if(old_fd == -1 || (long)(int)old_fd != old_fd) {
    errno = EBADF;
    return PyErr_SetFromErrno(PyExc_OSError);
  }

  PyObject *self = PyObject_CallObject(cls, NULL);
  if(!self)
    return NULL;

  int new_fd = fcntl((int)old_fd, F_DUPFD_CLOEXEC, 0);
  if(new_fd == -1) {
    return PyErr_SetOSError_DECREF(self);
  }
  ((AutoFDObject*)self)->fd = new_fd;
  return self;
}


static PyObject *
AutoFD_open(PyObject *cls, PyObject *args) {
  PyObject *pathobj;
  int flags = O_RDONLY;
  int mode = 0777;
  if(!PyArg_ParseTuple(args, "O|ii", &pathobj, &flags, &mode))
    return NULL;

  char *path;
  PyObject *pathtmp = PyOS_FSPath(pathobj);
  if(!pathtmp)
    return NULL;
  int fsconv = fsconvert_strdup(pathtmp, &path);
  Py_DECREF(pathtmp);
  if(!fsconv) {
    if(path)
      PyMem_Free(path);
    return NULL;
  }

  PyObject *self = PyObject_CallObject(cls, NULL);
  if(!self) {
    PyMem_Free(path);
    return NULL;
  }

  int fd = open(path, flags|O_CLOEXEC, mode);
  PyMem_Free(path);
  if(fd == -1) {
    return PyErr_SetOSError_DECREF(self);
  }

  ((AutoFDObject*)self)->fd = fd;
  return self;
}

static PyObject *
AutoFD_openat(PyObject *cls, PyObject *args) {
  PyObject *pathobj;
  int dirfd;
  int flags = O_RDONLY;
  int mode = 0777;
  if(!PyArg_ParseTuple(args, "iO|ii", &dirfd, &pathobj, &flags, &mode))
    return NULL;

  char *path;
  PyObject *pathtmp = PyOS_FSPath(pathobj);
  if(!pathtmp)
    return NULL;
  int fsconv = fsconvert_strdup(pathtmp, &path);
  Py_DECREF(pathtmp);
  if(!fsconv) {
    if(path)
      PyMem_Free(path);
    return NULL;
  }

  PyObject *self = PyObject_CallObject(cls, NULL);
  if(!self) {
    PyMem_Free(path);
    return NULL;
  }

  int fd = openat(dirfd, path, flags|O_CLOEXEC, mode);
  PyMem_Free(path);
  if(fd == -1) {
    return PyErr_SetOSError_DECREF(self);
  }

  ((AutoFDObject*)self)->fd = fd;
  return self;
}

static PyObject *
AutoFD_pipe(PyObject *cls, PyObject *Py_UNUSED(ignored)) {
  PyObject *fst = PyObject_CallObject(cls, NULL);
  if(!fst)
    return NULL;

  PyObject *snd = PyObject_CallObject(cls, NULL);
  if(!snd) {
    Py_DECREF(fst);
    return NULL;
  }

  PyObject *ret = PyTuple_Pack(2, fst, snd);
  Py_DECREF(fst);
  Py_DECREF(snd);
  if(!ret) {
    return NULL;
  }

  int fds[2];
  if(pipe(fds) != 0)
    return PyErr_SetOSError_DECREF(ret);


  if(!set_cloexec2_or_oserror_decref(fds, ret))
    return NULL;

  ((AutoFDObject*)fst)->fd = fds[0];
  ((AutoFDObject*)snd)->fd = fds[1];
  return ret;
}

static PyObject *
AutoFD_socket(PyObject *cls, PyObject *args) {
  int domain, type, protocol;
  if(!PyArg_ParseTuple(args, "iii", &domain, &type, &protocol))
    return NULL;

  PyObject *self = PyObject_CallObject(cls, NULL);
  if(!self)
    return NULL;

  int fd = socket(domain, type, protocol);
  if(fd == -1)
    return PyErr_SetOSError_DECREF(self);

  if(!set_cloexec_or_oserror_decref(fd, self))
    return NULL;

  ((AutoFDObject*)self)->fd = fd;
  return self;
}

static PyObject *
AutoFD_socketpair(PyObject *cls, PyObject *args) {
  int domain, type, protocol;
  if(!PyArg_ParseTuple(args, "iii", &domain, &type, &protocol))
    return NULL;

  PyObject *fst = PyObject_CallObject(cls, NULL);
  if(!fst)
    return NULL;

  PyObject *snd = PyObject_CallObject(cls, NULL);
  if(!snd) {
    Py_DECREF(fst);
    return NULL;
  }

  PyObject *ret = PyTuple_Pack(2, fst, snd);
  Py_DECREF(fst);
  Py_DECREF(snd);
  if(!ret) {
    return NULL;
  }

  int fds[2];
  if(socketpair(domain, type, protocol, fds) != 0) {
    return PyErr_SetOSError_DECREF(ret);
  }

  if(!set_cloexec2_or_oserror_decref(fds, ret))
    return NULL;

  ((AutoFDObject*)fst)->fd = fds[0];
  ((AutoFDObject*)snd)->fd = fds[1];
  return ret;
}

static PyObject *
AutoFD_accept(PyObject *cls, PyObject *args) {
  int sockfd;
  struct sockaddr *restrict addr;
  int addrlen_i;
  if(!PyArg_ParseTuple(args, "iy#", &sockfd, &addr, &addrlen_i))
    return NULL;

  socklen_t addrlen = addrlen_i;

  PyObject *self = PyObject_CallObject(cls, NULL);
  if(!self)
    return NULL;

  int fd = accept(sockfd, addr, &addrlen);
  if(fd == -1) {
    return PyErr_SetOSError_DECREF(self);
  }

  if(!set_cloexec_or_oserror_decref(fd, self))
    return NULL;

  ((AutoFDObject*)self)->fd = fd;
  return self;
}

#ifdef __linux__
static PyObject *
AutoFD_inotify(PyObject *cls, PyObject *Py_UNUSED(ignored)) {
  PyObject *self = PyObject_CallObject(cls, NULL);
  if(!self)
    return NULL;

  int fd = inotify_init1(IN_CLOEXEC);
  if(fd == -1)
    return PyErr_SetOSError_DECREF(self);

  ((AutoFDObject*)self)->fd = fd;
  return self;
}


static PyObject *
AutoFD_memfd(PyObject *cls, PyObject *Py_UNUSED(ignored)) {
  PyObject *self = PyObject_CallObject(cls, NULL);
  if(!self)
    return NULL;

  char buf[40];
  snprintf(buf, sizeof buf, "leakless.autofd.%p", self);
#ifdef SYS_memfd_create
  int fd = syscall(SYS_memfd_create, buf, 1); // MFD_CLOEXEC
#else
  int fd = -1;
  errno = ENOSYS;
#endif
  if(fd == -1)
    return PyErr_SetOSError_DECREF(self);

  ((AutoFDObject*)self)->fd = fd;
  return self;
}

static PyObject *
_autoFD_eventfd(int flags, PyObject *cls, PyObject *other) {
  if(!PyLong_Check(other)) {
    PyErr_SetString(PyExc_TypeError, "AutoFD.eventfd takes an int");
    return NULL;
  }

  PyObject *self = PyObject_CallObject(cls, NULL);
  if(!self)
    return NULL;

  int fd = eventfd(PyLong_AsLong(other), flags);
  if(fd == -1)
    return PyErr_SetOSError_DECREF(self);

  ((AutoFDObject*)self)->fd = fd;
  return self;
}

static PyObject *
AutoFD_eventfd(PyObject *cls, PyObject *other) {
  return _autoFD_eventfd(EFD_CLOEXEC, cls, other);
}
static PyObject *
AutoFD_eventfd_semaphore(PyObject *cls, PyObject *other) {
  return _autoFD_eventfd(EFD_CLOEXEC|EFD_SEMAPHORE, cls, other);
}
#endif

static PyObject *
AutoFD_acquire(PyObject *cls, PyObject *other) {
  if(!PyLong_Check(other)) {
    PyErr_SetString(PyExc_TypeError, "AutoFD.unsafe_acquire takes an int");
    return NULL;
  }

  long fd = PyLong_AsLong(other);
  if(fd == -1 || (long)(int)fd != fd) {
    errno = EBADF;
    return PyErr_SetFromErrno(PyExc_OSError);
  }

  PyObject *self = PyObject_CallObject(cls, NULL);
  if(!self)
    return NULL;

  if(fcntl((int)fd, F_SETFD, FD_CLOEXEC) == -1) {
    return PyErr_SetOSError_DECREF(self);
  }

  ((AutoFDObject*)self)->fd = fd;
  return self;
}

static PyObject *
AutoFD_release(PyObject *self, PyObject *Py_UNUSED(ignored)) {
  int *fd = &((AutoFDObject*)self)->fd;
  PyObject *ret = PyLong_FromLong(*fd);
  if(!ret)
    return NULL;
  *fd = -1;
  return ret;
}

static PyMethodDef AutoFD_methods[] = {
  {"close", AutoFD_close, METH_NOARGS, "close() the AutoFD"},
  {"dup", AutoFD_dup, METH_O|METH_CLASS, "New AutoFD from dup() (actually F_DUPFD_CLOEXEC)"},
  {"open", AutoFD_open, METH_VARARGS|METH_CLASS, "New AutoFD from open()"},
  {"openat", AutoFD_openat, METH_VARARGS|METH_CLASS, "New AutoFD from openat()"},
  {"pipe", AutoFD_pipe, METH_NOARGS|METH_CLASS, "New AutoFD pair from pipe()"},
  {"socket", AutoFD_socket, METH_VARARGS|METH_CLASS, "New AutoFD from socket()"},
  {"socketpair", AutoFD_socketpair, METH_VARARGS|METH_CLASS, "New AutoFD pair from socketpair()"},
  {"accept", AutoFD_accept, METH_VARARGS|METH_CLASS, "New AutoFD from accept()"},
#ifdef __linux__
  {"inotify", AutoFD_inotify, METH_NOARGS|METH_CLASS, "New AutoFD from inotify_init()"},
  {"memfd", AutoFD_memfd, METH_NOARGS|METH_CLASS, "New AutoFD from memfd_create()"},
  {"eventfd", AutoFD_eventfd, METH_O|METH_CLASS, "New AutoFD from eventfd()"},
  {"eventfd_semaphore", AutoFD_eventfd_semaphore, METH_O|METH_CLASS, "New AutoFD from eventfd(EFD_SEMAPHORE)"},
#endif
  {"unsafe_acquire", AutoFD_acquire, METH_NOARGS|METH_CLASS, "New AutoFD from an int. Sets CLOEXEC.\nThis method is unsafe because there's no atomic way to transfer 'ownership' of who should close the descriptor."},
  {"unsafe_release", AutoFD_release, METH_NOARGS, "Returns the file descriptor, which will no longer be auto-closed.\nThis method is unsafe because there's no atomic way to transfer 'ownership' of who should close the descriptor."},
  {"redup", AutoFD_redup, METH_O, "Runs dup2(arg, self.fd). That is, the current wrapped fd is closed, 're-opened' with dup2. The integer value of the wrapped fd does not change.\nIf you'd like to create a new AutoFD with dup2(), use `fd = AutoFD.unsafe_acquire(new_fd); fd.redup(old_fd)`."},
  {NULL}
};

static PyTypeObject AutoFDType = {
  PyObject_HEAD_INIT(NULL)
  .tp_name = "leakless.AutoFD",
  .tp_doc = "Wrapper for a file descriptor integer that closes when GCed.\nAll new AutoFDs start with CLOEXEC set.",
  .tp_basicsize = sizeof(AutoFDObject),
  .tp_itemsize = 0,
  .tp_flags = Py_TPFLAGS_DEFAULT,
  .tp_new = PyType_GenericNew,
  .tp_alloc = AutoFD_alloc,
  .tp_dealloc = AutoFD_dealloc,
  .tp_members = AutoFD_members,
  .tp_methods = AutoFD_methods,
  .tp_repr = AutoFD_repr,
};

static PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  .m_name = "leakless._autofd",
  .m_doc = "Module that helps avoid leaking file descriptors.",
  .m_size = -1,
};

PyMODINIT_FUNC
PyInit__autofd() {
  if(PyType_Ready(&AutoFDType) < 0)
    return NULL;

  PyObject *m = PyModule_Create(&module);
  if(!m)
    return NULL;

  Py_INCREF(&AutoFDType);
  if(PyModule_AddObject(m, "AutoFD", (PyObject *) &AutoFDType) < 0) {
    Py_DECREF(&AutoFDType);
    Py_DECREF(m);
    return NULL;
  }

  return m;
}
