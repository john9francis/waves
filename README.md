# waves
A python simulation of waves on a string

From the giordano and nakanishi book

**6.9**

Perform a spectrum analysis of waves on a string in which one end is free to move while the other is held fixed. Assume an initial Gaussian wavepacket located 40% from one end. Explain the peaks in the spectrum in terms of the allowed standing waves. Note that because the ends are free, these standing waves will be different from those found with fixed ends. (Fig 6.8)

# General wave equation

$$\frac{\partial^2y}{\partial t^2} = c^2\frac{\partial^2y}{\partial x^2}$$

This turns into: 

$$y(i,n+1) = 2[1-r^2]y(i,n)-y(i,n-1)+r^2[y(i+1,n)+y(i-1,n)]$$
$$r = \frac{c\Delta t}{\Delta x} \approx 1$$

Note: n has to do with time and i has to do with position