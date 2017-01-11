



all:
	swig -python -c++ example.i
	c++ -c -fPIC example.cpp example_wrap.c   -I/usr/include/python2.7
	c++ -shared -fPIC example_wrap.o -o _example.so
	python test.py
        
        
