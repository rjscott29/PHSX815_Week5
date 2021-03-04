#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import numpy as np
import matplotlib.pyplot as plt
from random import random

# main function for our coin toss Python code
if __name__ == "__main__":
       
    # default number of points for analysis
    nPoints = 1000
    
    # determines significant digits. This will prove useful for comparing
    # random values with generated points.
    # when we have 2 decimal places, we want 100 x values between 0 and 1
    # 3 decimals takes too long to calculate and search in our tuples
    decimals = 2
    precision = 1*10**decimals
    
    # do not rotate unless commanded
    rotate = 0
    
    # set initial values to 0
    nAccept = 0
    nTotal = 0
    
    # default to 2D plot
    dims = 2
    
    # default shows both accepted and rejected items
    show = 0
        
    # available options for user input
    if '-nPoints' in sys.argv:
        p = sys.argv.index('-nPoints')
        npo = int(sys.argv[p+1])
        if npo >= 0:
            nPoints = npo
    if '-rotate' in sys.argv:
        p = sys.argv.index('-rotate')
        rotate = 1
    if '-ThreeDee' in sys.argv:
        p = sys.argv.index('-ThreeDee')
        dims = 3
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

# bounding lines for data, generate data points at fixed intervals
    x = np.linspace(0,1,precision+1)
    x = np.around(x, decimals)
    y = 1-.5*x**2
    y = np.round(y, decimals)
    z = .2*x**2+y**2
    # turns out this works best as a tuple
    f = list(zip(x,y,z))
      
    xValues = []
    yValues = []
    zValues = []
    for xs in range(0,nPoints):
        xValues.append(random())
    for ys in range(0,nPoints):
        yValues.append(random())
    for zs in range(0,nPoints):
        zValues.append(random())
    
    # rounding values for a direct comparison with the precision of x
    xValues = np.around(xValues, decimals)
    yValues = np.around(yValues, decimals) 
    zValues = np.around(zValues, decimals)
    # another tuple for comparison
    g = list(zip(xValues, yValues, zValues))
    
    yesxValues = []
    yesyValues = []
    yeszValues = []
    noxValues = []
    noyValues = []
    nozValues = []
    
    # These are our for loops determining if we are above or below the curve
    # We take each data point and compare it with the curve equations given
    # Look at the y and z values for any x and calculate the difference.
    # +/- reveals acceptance
    if dims == 2:
        for x_i, y_i, z_i in g:
            for x_j, y_j, z_j in f:
                if x_i == x_j:
                    ydiff = y_j-y_i
                    nTotal += 1
                    if ydiff >= 0:
                        nAccept += 1
                        yesxValues.append(x_i)
                        yesyValues.append(y_i)
                    else:
                        noxValues.append(x_i)
                        noyValues.append(y_i)
    if dims == 3:     
        for x_i, y_i, z_i in g:
            for x_j, y_j, z_j in f:
                if x_i == x_j:
                    nTotal += 1
                    ydiff = y_j-y_i
                    zdiff = z_j-z_i
                    if ydiff >= 0 and zdiff >= 0:
                        nAccept += 1
                        yesxValues.append(x_i)
                        yesyValues.append(y_i)
                        yeszValues.append(z_i)
                    else:
                        noxValues.append(x_i)
                        noyValues.append(y_i)     
                        nozValues.append(z_i)
                    
    print("Accepted points: " + str(nAccept))
    print("Total points: " + str(nTotal))
    area = nAccept/nTotal
                      
# Creating our plot
    title = "Plotting with " + str(nPoints) + " data points. Calculated area = " + str(area) + " per unit area"                

# 2D and 3D plotting based on "ThreeDee" given in argument
    if dims == 2: 
        plt.figure()
        rotate = 0
        plt.plot(x,y, color = 'black')
        if show == 0 or show == 1:
            plt.scatter(yesxValues, yesyValues, color = 'lawngreen')
        if show == 0 or show == 2:
            plt.scatter(noxValues, noyValues, color = 'firebrick')
        
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        
        plt.title(title)
        plt.grid(True)
        
        plt.show()

# 3D plot
    if dims == 3:
        plt.figure()
        ax = plt.axes(projection='3d')
        if show == 0 or show == 1:
            ax.scatter(yesxValues, yesyValues, yeszValues, color = 'lawngreen')
        if show == 0 or show == 2:
            ax.scatter(noxValues, noyValues, nozValues, color = 'firebrick')
     
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_zlim(0, 1)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        
        plt.title(title)
        plt.grid(True)
        
        if rotate == 1:
            for angle in range(0, 360):
                ax.view_init(30, angle)
                plt.draw()
                plt.pause(.1)
        else: plt.show()