#ifdef STANDALONE
#undef STANDALONE
#endif
#include "subreaper.c"

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "pyposix.inc"

static void post_fork_wrapper(void *obj) {
  PyObject_CallObject(obj, NULL);
  // No need to decref or anything, execve() is gonna happen next.
}

static PyObject *
py_subreaper_spawn(PyObject *module, PyObject *args) {
  PyObject *path, *argv, *envp, *post_fork = NULL;
  int errfd = -1;
  if(!PyArg_ParseTuple(args, "OOO|iO:spawn", &path, &argv, &envp, &errfd, &post_fork))
    return NULL;

  char *pathchars = NULL;
  char **argvlist = NULL;
  char **envlist = NULL;
  Py_ssize_t argc, envc;

  PyObject *pathobj = PyOS_FSPath(path);
  if(!pathobj)
    goto error;
  int fsconv = fsconvert_strdup(pathobj, &pathchars);
  Py_DECREF(pathobj);
  if(!fsconv)
    goto error;

  if(argv != Py_None) {
    if(!PyList_Check(argv) && !PyTuple_Check(argv)) {
      PyErr_SetString(PyExc_TypeError, "spawn: argv must be a tuple or list");
      goto error;
    }
  }

  if(envp != Py_None && !PyMapping_Check(envp)) {
    PyErr_SetString(PyExc_TypeError, "spawn: environment must be a mapping object");
    goto error;
  }

  if(post_fork) {
    if(post_fork == Py_None) {
      post_fork = NULL;
    } else {
      if(!PyCallable_Check(post_fork)) {
        PyErr_SetString(PyExc_TypeError, "spawn: post-fork callback must be callable");
        goto error;
      }
    }
  }

  if(argv == Py_None) {
    argc = 0;
    argvlist = PyMem_NEW(char *, 2);
    if(!argvlist) {
      PyErr_NoMemory();
      goto error;
    }
    size_t len = strlen(pathchars);
    void *buf = PyMem_Malloc(len+1);
    if(!buf) {
      PyErr_NoMemory();
      goto error;
    }
    memcpy(buf, pathchars, len);
    argc = 1;
    argvlist[0] = buf;
    argvlist[1] = NULL;
  } else {
    argc = PySequence_Size(argv);
    argvlist = parse_arglist(argv, &argc);
  }
  if(!argvlist)
    goto error;

  if(envp != Py_None) {
    envlist = parse_envlist(envp, &envc);
    if(!envlist)
      goto error;
  }

  pid_t ret = subreaper_spawn(pathchars, argvlist, envlist, errfd, post_fork ? post_fork_wrapper : NULL, post_fork);
  if(ret == -1) {
    PyErr_SetFromErrno(PyExc_OSError);
    goto error;
  }

  PyMem_Free(pathchars);
  if(envlist)
    free_string_array(envlist, envc);
  free_string_array(argvlist, argc);
  return PyLong_FromLong(ret);

error:
  if(pathchars)
    PyMem_Free(pathchars);
  if(argvlist)
    free_string_array(argvlist, argc);
  if(envlist)
    free_string_array(envlist, argc);
  return NULL;
}

static PyMethodDef methods[] = {
    {"spawn", py_subreaper_spawn, METH_VARARGS, "fork & exec, but kill whole process tree once the primary child process exits or dies.\nNote that the subprocess tree is NOT killed when Python exits."},
    {NULL, NULL, 0, NULL}
};

static PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  .m_name = "leakless._subreaper",
  .m_doc = "Module with an wrapped execve that will kill stray processes.",
  .m_size = -1,
  methods
};

PyMODINIT_FUNC
PyInit__subreaper() {
  PyObject *m = PyModule_Create(&module);
  if(!m)
    return NULL;
  return m;
}
