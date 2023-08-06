#ifndef FRAME_H
#define FRAME_H

static PyObject* get_valuestack_full(PyFrameObject* f);
static PyObject* get_valuestack(PyFrameObject* f, int index);

#endif