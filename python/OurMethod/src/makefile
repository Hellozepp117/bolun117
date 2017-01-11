

all:
	g++ -fPIC -O3 some_class.cpp -c
	swig -c++ -python -o mymodule_wrap.cpp mymodule.i
	gcc -fPIC -c mymodule_wrap.cpp -o mymodule_wrap.o -I/usr/include/python2.7
	g++ -shared mymodule_wrap.o some_class.o -o _mymodule.so
	
	python test.py
