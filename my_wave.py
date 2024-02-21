import numpy as np
from matplotlib import pyplot as plt

class Wave():
  def __init__(self, velocity) -> None:
    self.dx = .001
    
    # cdt/dx = 1
    # dt = dx/c
    self.dt = self.dx / velocity

    self.wave_array = np.arange(0, 1, self.dx)
    self.time_range = 0
    pass


  def initial_conditions(self):
    k = 1000
    x0 = .6
    y_array = np.exp(-k * (self.wave_array - x0)**2)

    # take a single step to get our 3 arrays, old, current, and new.
    return self.step(y_array, y_array)


  def step(self, old, current):
    '''
    takes in n-1 and n wave_arrays and returns 
    n-1, n, and n+1 arrays. uses this formula:
    y(i,n+1) = 2[1-r^2]y(i,n)-y(i,n-1)+r^2[y(i+1,n)+y(i-1,n)]
    note that r = 1
    '''
    new = - old[1:-1] + current[2:] + current[:-2]

    # enforce boundary conditions, for now clamp both ends.
    new = np.append(new, 0)
    new = np.insert(new, 0, 0)
    return old, current, new


  def animated_plot(self, seconds):
    old, current, new = self.initial_conditions()

    for i in range(round(seconds/self.dt)):
      old, current, new = self.step(current, new)

      # plot one frame
      plt.plot(self.wave_array, current)
      plt.draw()
      plt.pause(self.dt)
      plt.cla()
    pass