import numpy as np
from matplotlib import pyplot as plt
import datetime

class Wave():
  def __init__(self, velocity, clamp_right=True, clamp_left=True) -> None:
    self.dx = .01
    
    # cdt/dx = 1
    # dt = dx/c
    self.dt = self.dx / velocity

    self.wave_array = np.arange(0, 1, self.dx)
    self.time_range = 0

    # some bool flags
    self.right_clamped = clamp_right
    self.left_clamped = clamp_left
    pass


  def set_clamp(self, right_clamp: bool =True, left_clamp: bool =True):
    '''
    Clamp one or both ends of the string so they can't move
    '''
    self.right_clamped = right_clamp
    self.left_clamped = left_clamp


  def initial_conditions(self):
    k = 100
    x0 = .6

    # gaussian wavepacket 60% into the wave
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

    # enforce boundary conditions
    # note: depends on free or clamped ends
    if self.left_clamped:
      new = np.insert(new, 0, 0)
    else:
      new = np.insert(new, 0, new[0])

    if self.right_clamped:
      new = np.append(new, 0)
    else:
      new = np.append(new, new[-1])

    return old, current, new


  def animated_plot(self, _seconds):
    old, current, new = self.initial_conditions()

    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=_seconds)

    ymin = -max(current)
    ymax = max(current)

    while True:
      old, current, new = self.step(current, new)

      # plot one frame
      # enforce axes
      plt.ylim(ymin, ymax)

      plt.plot(self.wave_array, current)
      plt.draw()
      plt.pause(self.dt)
      plt.cla()

      # stop if we're out of time
      if datetime.datetime.now() > end_time:
        break
    pass