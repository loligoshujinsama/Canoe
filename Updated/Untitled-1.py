#!usr/bin/env/python
#To use lambda later
import sys

def double(x):
    return x*2

def square(x):
    return x**2

def cube(x):
    return x**3

def doTwice(func, x):
    return func(x)
        

if __name__ == "__main__":
    try:
        number = int(sys.argv[1]) #Number input
        mode = int(sys.argv[2]) #Mode selector
        out = 0
        if mode == 1:
            out = doTwice(double,double(number))
        elif mode == 2:
            out = doTwice(square,square(number))
        elif mode == 3:
            out = doTwice(cube,cube(number))
        else:
            raise Exception
        print(out)
    except Exception as e:
        print("It cannot be supported!")
