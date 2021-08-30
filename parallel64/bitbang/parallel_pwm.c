#include <Python.h>
#include <windows.h>
    
    typedef short _stdcall (*ifuncPntr(short portRegister)
    typedef void _stdcall (*ofuncPntr(short portRegister, short valueToWrite)

static PyObject *method_pwmCycle(PyObject *self, PyObject *args)
{
    const PyObject *pwm_cycle;
	
	if (!PyArg_ParseTuple(args, "O", &pwm_cycle))
        return NULL;
	
	PyObject* shouldStop = PyObject_GetAttrString(pwm_cycle,(char*)"shouldStop");
	PyObject* args = PyTuple_Pack(1,pwm_cycle);

    PyObject* pwm_object = PyObject_GetAttrString(pwm_cycle,(char*)"_pwm_object");
    PyObject* gpio_port = PyObject_GetAttrString(pwm_object,(char*)"_port");
    PyObject* gpio_pin = PyObject_GetAttrString(gpio_port,(char*)"pin");
    short portregister = PyLong_AsLong(PyObject_GetAttrString(gpio_pin,(char*)"register"));
    unsigned int bitindex = PyLong_AsLong(PyObject_GetAttrString(gpio_pin,(char*)"bit_index"));
    int onvalue = PyLong_AsLong(PyObject_GetAttrString(pwm_object,(char*)"_on_value"));
    PyObject* dllloc = PyObject_GetAttrString(gpio_port,(char*)"_windll_location");
	sleep(
    double dutycycle = PyFloat_AsDouble(PyObject_GetAttrString(pwm_object,(char*)"duty_cycle"));
    double cycletime = PyFloat_AsDouble(PyObject_GetAttrString(pwm_object,(char*)"cycle_time"));
    
    HISTNACE iolib = LoadLibrary(dllloc);
    portInput = (ifuncPntr) GetProcAddress(iolib, "Inp32");
    portOutput = (ofuncPntr) GetProcAddress(iolib, "Out32");
	
	int shouldBreak = 0
	short current_byte;
	short bit_mask;
	short byte_result;
	unsigned double ontime = dutycycle*cycletime
	unsigned double offtime = cycletime-ontime
	
	while (shouldBreak == 0)
	{
		register_byte = portInput(portregister);
		bit_mask = onvalue << bit_index
		byte_result = bit_mask ^ register_byte
		portOutput(portregister, byte_result);
		sleep(ontime)
		
		register_byte = portInput(portregister);
		bit_mask = onvalue << bit_index
		byte_result = bit_mask ^ register_byte
		portOutput(portregister, byte_result);
		sleep(offtime)
		
		shouldBreak = PyLong_AsLong(PyObject_CallObject(shouldStop, args));
	}
	return 1
};
static PyMethodDef ParallelPWMMethods[] = {
    ...
    {"pwmCycle",  method_pwmCycle, METH_VARARGS,
     "Begin PWM cycle"},
    ...
    {NULL, NULL, 0, NULL}        /* Sentinel */
};
static struct PyModuleDef parallel_pwm = {
    PyModuleDef_HEAD_INIT,
    "parallel_pwm",
    "Python interface for the pwmCycle C library function",
    -1,
    ParallelPWMMethods
};