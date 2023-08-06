/*
 * rubber.cpp
 *
 *  Created on: 14 Nov 2019
 *      Author: julianporter
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <string>
#include <vector>
#include <algorithm>
#include <memory>
#include <sstream>
#include <iostream>
#include <stdexcept>

#define PY_ARRAY_UNIQUE_SYMBOL rubberband_ARRAY_API
#include <arrayobject.h>

#include "stretch.hpp"


static const bool Debug = true;

static PyObject *rubberbandError;

const char* ModuleName="rubberband";
const char* ErrorName="RubberBandError";
static char *Keywords[]={"data","rate","ratio","crispness","formants",NULL};

std::vector<float> numpyToVector(PyObject *obj) {
	if(!PyArray_Check(obj)) throw std::runtime_error("Object is not a Numpy array");
	PyArrayObject *array=(PyArrayObject *)obj;
	if(array==nullptr) throw std::runtime_error("Object is not a Numpy array");

	if(PyArray_NDIM(array)!=1) throw std::runtime_error("Array is not 1 dimensional");
	auto dims=PyArray_DIMS(array);
	if(dims==nullptr) throw std::runtime_error("Array is not 1 dimensional");

	long size = dims[0];

	auto kind=PyArray_TYPE(array);
	if(kind != NPY_FLOAT) throw std::runtime_error("Array is not of type float32");

	float *ptr = static_cast<float *>(PyArray_DATA(array));
	std::vector<float> vec(size,0);
	std::copy(ptr,ptr+size,vec.begin());
	return vec;
}

PyObject *vectorToNumpy(const std::vector<float> &vector) {
	npy_intp dims[] = {(npy_intp)vector.size()};
	PyObject *obj=PyArray_ZEROS(1,dims,NPY_FLOAT,0);
	if(obj==nullptr) throw std::runtime_error("Cannot allocate space for array");
	float *ptr = static_cast<float *>(PyArray_DATA((PyArrayObject *)obj));
	std::copy(vector.begin(),vector.end(),ptr);
	return obj;
}

static PyObject * stretch(PyObject *self, PyObject *args, PyObject *keywds) {

	PyObject *stream;
	long sampleRate=64000;
	double ratio=1.0;
	int crispness=5;
	int formants=0;

	if(!PyArg_ParseTupleAndKeywords(args,keywds,"O|ldip",Keywords,
			&stream,&sampleRate,&ratio,&crispness,&formants)) { return NULL; }

	try {
		auto option=Stretch::makeOptions(crispness,formants!=0);
		std::cout << "Crispness is " << crispness << ", formants is " << formants << std::endl;
		std::cout << "Option is " << std::hex << option << std::dec << std::endl;

		auto values=numpyToVector(stream);
		auto minmax = std::minmax_element(values.begin(),values.end());
		float bound = std::max(abs(*minmax.first),abs(*minmax.second));
		if(bound>1.0) {
			auto factor=1.0/bound;
			std::transform(values.begin(),values.end(),values.begin(),[factor](float x) { return factor*x; });
		}

		if(Debug) std::cout << "Stretching" << std::endl;
		Stretch st(sampleRate,ratio,option);
		std::vector<float> out = st(values);

		PyObject *o = vectorToNumpy(out);
		Py_INCREF(o);
		return (PyObject *)o;
	}
	catch(std::exception &e) {
		PyErr_SetString(rubberbandError,e.what());
		if(Debug) std::cerr << e.what();
		return nullptr;
	}

}

static struct PyMethodDef methods[] = {
		{"stretch",(PyCFunction) stretch, METH_VARARGS | METH_KEYWORDS, "Stretch audio stream"},
		{NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
		PyModuleDef_HEAD_INIT,
		ModuleName,
		"",			/// Documentation string
		-1,			/// Size of state (-1 if in globals)
		methods,
		NULL,		/// Slots
		NULL,		/// traverse
		NULL,		/// clear
		NULL		/// free
};

PyMODINIT_FUNC PyInit_rubberband(void) {
	PyObject *m = PyModule_Create(&module);
	if(m==NULL) return NULL;
	import_array();
	try {
		std::stringstream s;
		s << ModuleName << "." << ErrorName;
		rubberbandError=PyErr_NewException(s.str().c_str(),NULL,NULL);
		if(rubberbandError==NULL) throw std::runtime_error("Cannot allocate RubberbandError");
		Py_INCREF(rubberbandError);
		auto result=PyModule_AddObject(m,ErrorName,rubberbandError);
		if(result<0) throw std::runtime_error("Cannot attach RubberbandError to module");

#ifdef MODULE_VERSION
		PyModule_AddStringConstant(m,"__version__",MODULE_VERSION);
#endif

		return m;
	}
	catch(std::exception &e) {
		PyErr_SetString(PyExc_ImportError,e.what());
		return NULL;
	}
}




