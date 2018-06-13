// A sample of python embedding (calling python classes from within C++ code)
//
// To run:
// 1) setenv PYTHONPATH ${PYTHONPATH}:./
// 2) call_class py_source Multiply multiply 
// 3) call_class py_source Multiply multiply 9 8 
//

#include <Python.h>

int main(int argc, char *argv[])
{
    PyObject *pName, *pModule, *pDict, *pClass, *pInstance, *pValue;
    int i, arg[8];

    if (argc < 4) 
    {
        fprintf(stderr,"Usage: call python_filename class_name function_name\n");
        return 1;
    }

    Py_Initialize();
    pName = PyString_FromString(argv[1]);
    pModule = PyImport_Import(pName);
	pDict = PyModule_GetDict(pModule);
   
    // Build the name of a callable class 
    pClass = PyDict_GetItemString(pDict, argv[2]);

    // Create an instance of the class
    if (PyCallable_Check(pClass))
    {
		pInstance = PyObject_CallObject(pClass, NULL); 
    }

    // Build parameter list
    if( argc > 4 )
    {
    	for (i = 0; i < argc - 4; i++)
    	{
        	arg[i] = atoi(argv[i + 4]);
    	}
        if( i>1 )   //assume 2, todo
		    // Call a method of the class with two parameters
    	    pValue = PyObject_CallMethod(pInstance, argv[3], "(ii)", arg[0], arg[1]);
        else
            pValue = PyObject_CallMethod(pInstance, argv[3], "(i)", arg[0]);

    } else
    {
		// Call a method of the class with no parameters
    	pValue = PyObject_CallMethod(pInstance, argv[3], NULL);
    }
   
	if (pValue != NULL) 
    {
		if( PyDict_Check(pValue) ) {
    			PyObject *pVal, *pKeys;
			unsigned int sz;

			pKeys = PyDict_Keys(pValue);
			sz = PyList_Size(pKeys);

			printf("Return a dictionary w/ %d elements\n", sz);
			for( int i=0; i<sz; ++i ) {
				PyObject *pThisKey = PyList_GetItem(pKeys, i);
				const char *str;
				if( !pThisKey ) {
					printf("null key\n");
					continue;
				}
				if( !PyString_Check(pThisKey) ) {
					printf("not a string key\n");
					continue;
				}
				str = PyString_AsString(pThisKey);
				pVal = PyDict_GetItem(pValue, pThisKey);
				if ( pVal ) {
					if( PyInt_Check(pVal) ) {
						printf("(int) %s =%d\n", str, PyInt_AsLong(pVal) );
						Py_DECREF(pVal);
					} else if( PyDict_Check(pVal) ) {
						printf("(dict) %s \n", str );
					} else if( PyList_Check(pVal) ) {
						printf("(list) %s \n", str );
					} else if( PyTuple_Check(pVal) ) {
						printf("(tuple) %s \n", str );
					} else if( PyString_Check(pVal) ) {
						printf("(string) %s = %s\n", str, PyString_AsString(pVal) );
					}
				} else printf("missing key %s\n", str);
			}
			Py_DECREF(pKeys);
		} else {
			printf("Return of call : %d\n", PyInt_AsLong(pValue));
		}
		Py_DECREF(pValue);
    }
    else 
    {
		PyErr_Print();
    }
    
    // Clean up
    Py_DECREF(pModule);
    Py_DECREF(pName);
    Py_Finalize();
    
    return 0;
}
