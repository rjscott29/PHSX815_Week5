#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import numpy as np
import matplotlib.pyplot as plt
import math


# main function for our coin toss Python code
if __name__ == "__main__":
       
    # default number of points for analysis
    nOrder = 2
       
    # available options for user input
    if '-nOrder' in sys.argv:
        p = sys.argv.index('-nPoints')
        nord = int(sys.argv[p+1])
        if nord >= 1 and nord <= 3:
            nOrder = nord
    if '-show' in sys.argv:
        p = sys.argv.index('-show')
        sh = int(sys.argv[p+1])
        if sh >= 0 and sh <= 2:
            show = sh
        else:
            show == 0
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [options]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)             print options")
        print ("   -nPoints [number]      number of data points to find volume")
        print ("   -ThreeDee              show a 3D plot")
        print ("   -rotate                rotates 3D plot (Use at own risk!)")
        print ("   -show [number 0,1,2]   determines what data is visualized")
        sys.exit(1)

    # a, b are limits for integration
    a = -1
    b = 6
    
    # deg for gaussian quadrature, defines highest degree of poly in function
    deg = 4
    
    # gives number of data points per digit of range of data
    precision = 10**nOrder
    datapoints = (b-a)*precision
    
    t_value = .5*(b+a+1*(b-a)) - .5*(b+a-1*(b-a))
    t_datapoints = int(t_value*precision)
    
    # defines our space of data
    x = np.linspace(a,b,datapoints)
    x = np.around(x,nOrder)
    t = np.linspace(-1,1,datapoints)
    # t = np.linspace(-1,1,t_datapoints)
    # t = np.around(t,nOrder)
    
    # gives nearest value in array to given value
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]
    
    # takes three arrays as inputs. v maps onto x, and then each x value
    # correlating with v will give a list of y values.
    def correlated_index(v,x,y):
        nearestxvalues = []
        yvalues = []
        for v_i in v:
            nearestx = find_nearest(x,v_i)
            nearestxvalues.append(nearestx)
        for x_i in nearestxvalues:
            i = nearestxvalues.index(x_i)
            y_i = y[i]
            yvalues.append(y_i)
        return yvalues
    
    # gives the product of two lists
    def productlists(list1,list2):
        products = []
        for num1, num2 in zip(list1, list2):
            products.append(num1 * num2)
        return products
    
    # defines our function.
    def Function(x):
        y = 4*x**4+3
        y = np.around(y,nOrder)
        return x,y
    
    # Trapezoidal method of integration    
    # f is Function returning tuples, a and b are start end points, N is bins
    def Trapezoidal(f,a,b,Bins):
        # get x and y components of f
        f_x = f[0]
        f_y = f[1]
        # prefactor of the trapezoidal method uses x values and number of bins
        T_prefactor = (f_x[precision-1]-f_x[0])/(2*Bins)
        # sum all y values of g, and get f(a) + 2*f(a+1)... + 2*f(b-1) + f(b)
        T_sum = sum(f_y)
        T_sum = 2*T_sum - f_y[precision-1] - f_y[0]
        # multiply to get trapezoidal equation for uniform grid
        # this will be exact for linear equations of y and x
        T = round(T_prefactor*T_sum, nOrder)
        return T
    
    # Returns tuple of [sample points, weights]
    def GaussLegendre(deg):
        GL = np.polynomial.legendre.leggauss(deg)
        return GL
    
    def Gaussian(a,b,n,deg):
        # reference: https://homepage.divms.uiowa.edu/~atkinson/ftp/ENA_Materials/Overheads/sec_5-3.pdf
        # convert bounds [a,b] to [-1,1] with change of basis x->t
        xprime = .5*(b+a+t*(b-a))
        # call our new function F(x) on [a,b] to F(xprime) on [-1,1]
        f = Function(xprime)
        # get x and y components of f
        f_x = f[0]
        f_y = .5*(b-a)*f[1]
        # we can now "integrate" f over -1 to 1 with gaussian quadrature
        # int(-1,1){f(x)dx} = sum(i=1,n) w_i*f(x_i)
        g = GaussLegendre(deg)
        g_x = g[0]
        w = g[1]
        # now we can solve w_1*f_1+...w_n*f_n at the points g_x
        G_a = correlated_index(g_x,f_x,f_y)
        G_a = [element ** deg for element in G_a]
        G = productlists(G_a, w)
        G = .5*(b-a)*sum(G)
        return G
                
    trapezoidal = Trapezoidal(Function(x),a,b,precision)
    print(trapezoidal)
    
    gaussian = Gaussian(a,b,precision,deg)
    print(gaussian)