#include "Python.h"
#include "frameobject.h"
#include "frame.h"

static PyObject* get_valuestack(PyFrameObject* f, int index) {
    PyObject* lst = PyList_New(0);
    if (f->f_stacktop != NULL) {
        PyObject** p = f->f_stacktop;
        p--;
        for (p; p >= f->f_valuestack; p--) {
            if (--index < 0) break;
            if (*p != NULL)
                PyList_Append(lst, *p);
            else
                PyList_Append(lst, Py_None);
        }
    }

    PyList_Reverse(lst);
    return lst;
}


static PyObject* get_valuestack_full(PyFrameObject* f) {
    PyObject* lst = PyList_New(0);
    if (f->f_stacktop != NULL) {
        PyObject** p = NULL;
        for (p = f->f_valuestack; p < f->f_stacktop; p++) {
            if (*p != NULL)
                PyList_Append(lst, *p);
            else
                PyList_Append(lst, Py_None);
        }
    }

    return lst;
}
