#include <Python.h>
#include <windows.h>

static PyObject *method_pwmCycle(PyObject *self, PyObject *args)
{
    const PyObject *pwm_cycle;
    /*const PyObject *pwm_object;
	const PyObject *dlllocation
	const PyObject *portregister
	const PyObject *bitindex*/
    int sts;
	
	if (!PyArg_ParseTuple(args, "O", &pwm_cycle))
        return NULL;
	
	PyObject* shouldStop = PyObject_GetAttrString(pwm_cycle,(char*)"shouldStop");
	PyObject* args = PyTuple_Pack(1,pwm_cycle);

    PyObject* pwm_object = PyObject_GetAttrString(pwm_cycle,(char*)"_pwm_object");
    PyObject* gpio_port = PyObject_GetAttrString(pwm_object,(char*)"_port");
    PyObject* portregister = PyObject_GetAttrString(pwm_object,(char*)"register");
    PyObject* bitindex = PyObject_GetAttrString(pwm_object,(char*)"bit_index");
    PyObject* dllloc = PyObject_GetAttrString(pwm_object,(char*)"_windll_location");
	
	int shouldBreak = 0
	
	while (shouldBreak == 0)
	{
		
		
		
		PyObject* myResult = PyObject_CallObject(shouldStop, args);
		int result = PyFloat_AsDouble(myResult);
	}
};