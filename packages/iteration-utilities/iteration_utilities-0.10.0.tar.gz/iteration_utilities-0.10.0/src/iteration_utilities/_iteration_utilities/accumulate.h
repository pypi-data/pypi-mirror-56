#ifndef PYIU_ACCUMULATE_H
#define PYIU_ACCUMULATE_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "helpercompat.h"

typedef struct {
    PyObject_HEAD
    PyObject *iterator;
    PyObject *binop;
    PyObject *total;
} PyIUObject_Accumulate;

extern PyTypeObject PyIUType_Accumulate;

#endif
