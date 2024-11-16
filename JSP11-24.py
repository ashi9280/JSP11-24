import math
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    @staticmethod
    def midpoint(a, b):
        midx = (a.x + b.x) / 2
        midy = (a.y + b.y) / 2
        return Point(midx, midy)
    
    @staticmethod
    def slope(a, b):
        return (b.y-a.y) / (b.x-a.x)
    
    @staticmethod
    def bisector_xint(a, b):
        mid = Point.midpoint(a, b)
        ab_slope = Point.slope(a, b)
        ab_bisector_slope = -1/ab_slope

        return mid.x - mid.y/ab_bisector_slope
    
    def print(self):
        print(f"({self.x}, {self.y})")

    def reflect_to_bottom_triangle(self):
        x = self.x
        y = self.y

        if x + y > 1:
            x = 1-x
            y = 1-y

        if y > x:
            temp = x
            x = 1-y
            y = temp

        return Point(x, y)
    
    def distance(self, other):
        return math.sqrt((other.y - self.y)**2 + (other.x - self.x)**2)

sim = True # if True, simulate random points and evaluate if in acceptable region. number_of_blue_points must be set to 1.
number_of_blue_points = 1 # number of blue points to sim. If equals 1, plots points.
number_of_red_points = 10000 # number of red points to sim.

# Interactive Desmos Plot: https://www.desmos.com/calculator/9zh8vi8j0t

if sim:
    n_blue = number_of_blue_points
    blue_points = []
    bpx = []
    bpy = []

    print("Creating blue points...")
    for i in range(n_blue):
        x = random.random()
        y = random.random()
        p = Point(x, y)
        p = p.reflect_to_bottom_triangle()
        blue_points.append(p)
        bpx.append(p.x)
        bpy.append(p.y)
    print("Done!\n")

    n_red = number_of_red_points
    red_points = []
    rpx = []
    rpy = []

    print("Creating red points...")
    for i in range(n_red):
        x = random.random()
        y = random.random()
        p = Point(x, y)
        red_points.append(p)
        rpx.append(p.x)
        rpy.append(p.y)
    print("Done!\n")

    def is_between_endpoints(p1: Point, p2: Point):
        xint = Point.bisector_xint(p1, p2)
        return xint >= 0 and xint <= 1

    c = []
    inbound, outbound = 0, 0

    print("Measuring if in endpoint...")
    for bp in blue_points:
        for rp in red_points:
            ibe = is_between_endpoints(bp, rp)
            if ibe:
                c.append('green')
                inbound += 1
            else:
                c.append('red')
                outbound += 1
        
    print("Done!\n")
    print(f"Results: {inbound} inbounds, {outbound} outbounds, with {n_blue} blue points and {n_red} red points")

    if n_blue == 1:
        print("Plotting red points")
        plt.scatter(rpx, rpy, color=c)
        print("Done!\n")

        print("Plotting blue points...")
        plt.scatter(bpx, bpy, color='blue')
        print("Done!\n")

        plt.show()

print(f"Double Integral Calculation...")
f = lambda y, x: math.pi*(x**2+y**2)/4 + math.pi*((1-x)**2+y**2)/4 + y - ((x**2+y**2)*math.atan(y/x) + ((1-x)**2+y**2)*math.atan(y/(1-x)))
p = 8*integrate.dblquad(f, 0, 0.5, 0, lambda x: x)[0]

print(f"p: {p}")
print(f"Done!")