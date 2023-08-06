#include <Python.h>
#include "scrypt.h"

#if PY_MAJOR_VERSION >= 3
#define PY_STRING_FORMAT "y#"
#else
#define PY_STRING_FORMAT "s#"
#endif

static PyObject *scrypt_getpowhash(PyObject *self, PyObject *args, PyObject* kwargs) {
    char *input;
    int inputlen;

    char *outbuf;

    static char *g2_kwlist[] = {"input", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, PY_STRING_FORMAT, g2_kwlist,
                                     &input, &inputlen)) {
        return NULL;
    }

    outbuf = PyMem_Malloc(32);

    Py_BEGIN_ALLOW_THREADS;
    
    scrypt_1024_1_1_256(input, outbuf);

    Py_END_ALLOW_THREADS;

    PyObject *value = NULL;
    
    value = Py_BuildValue(PY_STRING_FORMAT, outbuf, 32);
    
    PyMem_Free(outbuf);
    return value;
}

static PyMethodDef ScryptMethods[] = {
    { "getPoWHash", (PyCFunction) scrypt_getpowhash, METH_VARARGS | METH_KEYWORDS, "Returns the proof of work hash using scrypt" },
    { NULL, NULL, 0, NULL }
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef scryptmodule = {
    PyModuleDef_HEAD_INIT,
    "scrypt",
    NULL,
    -1,
    ScryptMethods
};

PyMODINIT_FUNC PyInit_scrypt(void) {
    PyObject *m = PyModule_Create(&scryptmodule);

    if (m == NULL) {
        return NULL;
    }

    return m;
}
#else
PyMODINIT_FUNC init_scrypt(void) {
    Py_InitModule("scrypt", ScryptMethods);
}
#endif

