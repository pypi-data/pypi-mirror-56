#include <Python.h>

static PyObject* print_message(PyObject* self, PyObject* args)
{
    const char* str_arg;
    if(!PyArg_ParseTuple(args, "s", &str_arg)) {
        puts("Could not parse the python arg!");
        return NULL;
    }
#ifdef USE_PRINTER
    printf("royal %s\n", str_arg);
#else
    printf("royal %s\n", str_arg);
#endif
    // This can also be done with Py_RETURN_NONE
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef myMethods[] = {
    { "print_message", print_message, METH_VARARGS, "Prints a called string" },
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef myModule = {
    PyModuleDef_HEAD_INIT,
    "_royal",
    "An economic market modeling library",
    -1,
    myMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit__royal(void)
{
    return PyModule_Create(&myModule);
}