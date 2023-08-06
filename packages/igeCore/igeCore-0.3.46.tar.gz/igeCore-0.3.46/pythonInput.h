///////////////////////////////////////////////////////////////
//Pyxie game engine
//
//  Copyright Kiharu Shishikura 2019. All rights reserved.
///////////////////////////////////////////////////////////////
#pragma once

#include <Python.h>

#include "pyxieTypes.h"

#include "input/pyxieEvent.h"
#include "input/pyxieKeyboard.h"
#include "input/pyxieTouch.h"
#include "input/pyxieInputHandler.h"

#include "pyxieApplication.h"
extern std::shared_ptr<pyxie::pyxieApplication> gApp;

namespace pyxie
{    
	extern void pyxieRegisterEventListener(int eventType, int eventCode, const void* handler);

    static PyObject* pyxie_registerEventListener(PyObject* self, PyObject* args) {
		int event_type;
		int event_code;
		PyObject* event_callback_fn;

		if (!PyArg_ParseTuple(args, "iiO", &event_type, &event_code, &event_callback_fn))
			return NULL;

		if (!PyCallable_Check(event_callback_fn)) {
			PyErr_SetString(PyExc_TypeError, "Callback function must be a callable object!");
			return NULL;
		}
		Py_XINCREF(event_callback_fn);

		// Call to pyxie module
		pyxieRegisterEventListener(event_type, event_code, (const void*)event_callback_fn);

		Py_INCREF(Py_None);
		return Py_None;
	}

	static PyObject* pyxie_isKeyPressed(PyObject* self, PyObject* args) {
		int keyCode;
		if (!PyArg_ParseTuple(args, "i", &keyCode))
			return NULL;			
		return PyBool_FromLong(gApp->getInputHandler()->getKeyboard()->isKeyDown(static_cast<KeyCode>(keyCode)));
	}	

	static PyObject* pyxie_isKeyReleased(PyObject* self, PyObject* args) {
		int keyCode;
		if (!PyArg_ParseTuple(args, "i", &keyCode))
			return NULL;	
		return PyBool_FromLong(gApp->getInputHandler()->getKeyboard()->isKeyUp(static_cast<KeyCode>(keyCode)));
	}

	static PyObject* pyxie_isKeyHold(PyObject* self, PyObject* args) {
		int keyCode;
		if (!PyArg_ParseTuple(args, "i", &keyCode))
			return NULL;		
		return PyBool_FromLong(gApp->getInputHandler()->getKeyboard()->isKeyHold(static_cast<KeyCode>(keyCode)));
	}

	static PyObject* pyxie_getKeyChar(PyObject* self, PyObject* args) {
		int keyCode;
		if (!PyArg_ParseTuple(args, "i", &keyCode))
			return NULL;
		auto ch = gApp->getInputHandler()->getKeyboard()->getChar(static_cast<KeyCode>(keyCode));
		return PyUnicode_FromUnicode((const Py_UNICODE*)&ch, 1);
	}

	static PyObject* pyxie_getKeyModifier(PyObject* self, PyObject* args) {		
		return PyLong_FromLong(gApp->getInputHandler()->getKeyboard()->getKeyModifier());
	}

	static PyObject* pyxie_getFingerPosition(PyObject* self, PyObject* args) {
		uint32_t fingerId;
		if (!PyArg_ParseTuple(args, "i", &fingerId))
			return NULL;
		float posX, posY;
		gApp->getInputHandler()->getTouchDevice()->getFingerPosition(fingerId, posX, posY);		
		PyObject *tuple = PyTuple_New(2);
		PyTuple_SET_ITEM(tuple, 0, PyLong_FromLong((int)posX));
		PyTuple_SET_ITEM(tuple, 1, PyLong_FromLong((int)posY));
		return tuple;
	}

	static PyObject* pyxie_getFingerPressure(PyObject* self, PyObject* args) {
		uint32_t fingerId;
		if (!PyArg_ParseTuple(args, "i", &fingerId))
			return NULL;	
		return PyBool_FromLong(gApp->getInputHandler()->getTouchDevice()->getFingerPressure(fingerId));
	}

	static PyObject* pyxie_isFingerPressed(PyObject* self, PyObject* args) {
		uint32_t fingerId;
		if (!PyArg_ParseTuple(args, "i", &fingerId))
			return NULL;	
		return PyBool_FromLong(gApp->getInputHandler()->getTouchDevice()->isFingerPressed(fingerId));
	}

	static PyObject* pyxie_isFingerMoved(PyObject* self, PyObject* args) {
		uint32_t fingerId;
		if (!PyArg_ParseTuple(args, "i", &fingerId))
			return NULL;	
		return PyBool_FromLong(gApp->getInputHandler()->getTouchDevice()->isFingerMoved(fingerId));
	}

	static PyObject* pyxie_isFingerReleased(PyObject* self, PyObject* args) {
		uint32_t fingerId;
		if (!PyArg_ParseTuple(args, "i", &fingerId))
			return NULL;	
		return PyBool_FromLong(gApp->getInputHandler()->getTouchDevice()->isFingerReleased(fingerId));
	}

	static PyObject* pyxie_isFingerScrolled(PyObject* self, PyObject* args) {
		uint32_t fingerId;
		if (!PyArg_ParseTuple(args, "i", &fingerId))
			return NULL;	
		return PyBool_FromLong(gApp->getInputHandler()->getTouchDevice()->isFingerScrolled(fingerId));
	}

	static PyObject* pyxie_getFingerScrolledData(PyObject* self, PyObject* args) {
		uint32_t fingerId;
		if (!PyArg_ParseTuple(args, "i", &fingerId))
			return NULL;
		float scroll_x, scroll_y;
		bool isInverse;
		gApp->getInputHandler()->getTouchDevice()->getFingerScrolledData(fingerId, scroll_x, scroll_y, isInverse);

		PyObject *tuple = PyTuple_New(3);
		PyTuple_SET_ITEM(tuple, 0, PyFloat_FromDouble(scroll_x));
		PyTuple_SET_ITEM(tuple, 1, PyFloat_FromDouble(scroll_y));
		PyTuple_SET_ITEM(tuple, 2, PyBool_FromLong(isInverse));
		return tuple;		
	}

	static PyObject* pyxie_getFingersCount(PyObject* self, PyObject* args) {		
		return PyLong_FromLong(gApp->getInputHandler()->getTouchDevice()->getFingersCount());
	}

	static PyObject* pyxie_getAllFingers(PyObject* self, PyObject* args) {
		PyObject* list = PyList_New(0);

		auto fingers = gApp->getInputHandler()->getTouchDevice()->getAllFingers();
		for(int i = 0; i < fingers.size(); i++)
		{
			auto finger = fingers[i];
			PyObject* fingerObject = Py_BuildValue(
						"{s:i, s:d, s:d, s:d, s:b, s:b, s:b, s:b, s:d, s:d, s:b}",						
						"id", finger->getFingerId(),						
						"cur_x", finger->getCurrentPosX(),
						"cur_y", finger->getCurrentPosY(),
						"force", finger->getPressure(),					
						"is_pressed", finger->isPressed() ? 1 : 0,
						"is_moved", finger->isMoved() ? 1 : 0,
						"is_released", finger->isReleased() ? 1 : 0,
						"is_scrolled", finger->isScrolled() ? 1 : 0,
						"scroll_x", finger->getScrollX(),
						"scroll_y", finger->getScrollY(),
						"is_flipped", finger->isScrollFlipped() ? 1 : 0
					);
			PyList_Append(list, fingerObject);
		}
		return list;
	}
}
