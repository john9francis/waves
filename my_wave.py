import numpy as np
from matplotlib import pyplot as plt
import datetime

class Wave():

  # static variable to control if it's running
  # so all instances of the class share this one value
  running = True

  def __init__(self, velocity, clamp_right=True, clamp_left=True) -> None:
    self.dx = .01
    
    # cdt/dx = 1
    # dt = dx/c
    self.dt = self.dx / velocity

    # create y positional array for the wave
    self.wave_array = np.arange(0, 1, self.dx)
    self.time_range = 0

    # define arrays of position of ends over time
    self.left_over_time = []
    self.right_over_time = []
    self.time_array = []

    # some bool flags
    self.right_clamped = clamp_right
    self.left_clamped = clamp_left
    self.save = False

    # hook up plot to a close event, so we can quit the animation
    # by closing the animation window. otherwise the animation is
    # impossible to stop.
    self.fig = plt.figure()
    self.fig.canvas.mpl_connect('close_event', self.on_close)
    pass


  def set_clamp(self, right_clamp: bool =True, left_clamp: bool =True):
    '''
    Clamp one or both ends of the string so they can't move
    '''
    self.right_clamped = right_clamp
    self.left_clamped = left_clamp


  def initial_conditions(self):
    '''
    Creates a gaussian pluck of the string
    note: this function could be improved if 
    we want custom initial conditions, but for now it's
    hardcoded to create a gaussian pluck 40% from the end.
    '''
    k = 1000
    x0 = .6

    # gaussian wavepacket 40% away from the end of the wave
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
    '''
    Opens a window that animates a wave on a string moving
    '''
    # get our basic graph from initial conditions
    old, current, new = self.initial_conditions()

    # get start and end time based on the _seconds parameter
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=_seconds)

    # bounds for our graph
    ymin = -max(current)
    ymax = max(current)

    while True:
      # quit if running flag is false
      # note: self.running is false when the user closes a window
      if not self.running:
        return
      
      # update our wave to the next position
      old, current, new = self.step(current, new)

      # enforce axes
      plt.ylim(ymin, ymax)

      # plot one frame
      plt.plot(self.wave_array, current)
      plt.draw()
      plt.pause(self.dt)
      plt.cla()

      # stop if we're out of time
      if datetime.datetime.now() > end_time:
        break
    pass

  @classmethod
  def set_running(cls, value:bool):
    '''Static method that sets the running parameter'''
    cls.running = value

  def on_close(self, event):
    '''Method that is called when user closes the window'''
    self.set_running(False)
    pass


  def generate_pos_over_time_data(self, amount_of_time: int):
    '''
    Fills the self.left_over_time and self.right_over_time graphs.
    These are the two ends of the string's y displacement over time.
    by the 'two ends' I mean 5% away from the ends.

    note: this method is similar to animated_plot but this does the 
    whole thing fast and just generates a final plot. 
    '''

    old, current, new = self.initial_conditions()

    # loop over our time period
    for i in range(round(amount_of_time / self.dt)):

      # update our wave
      old, current, new = self.step(current, new)

      # save to our lists
      left_indx = round(len(current) * .05)
      right_indx = round(len(current) * .95)

      self.left_over_time.append(current[left_indx])
      self.right_over_time.append(current[right_indx])

      self.time_array.append(i * self.dt)
    


  
  def plot_pos_over_time(self):
    '''
    Plots the pos over time data with accurate labels
    '''
    left_free_label = "fixed"
    right_free_label = "fixed"
    # fix plot labels
    if not self.left_clamped:
      left_free_label = "free"
    if not self.right_clamped:
      right_free_label = "free"
    
    # now plot the data
    fig = plt.figure()
    fig, ax = plt.subplots()
    ax.plot(self.time_array, self.left_over_time, label=f"Left end ({left_free_label})")
    ax.plot(self.time_array, self.right_over_time, label=f"Right end ({right_free_label})")
    ax.legend()
    fig.savefig("outputs/pos_over_time.png")
    pass


  def DFT(self, samples):
    '''
    Takes in a list of samples, and 
    returns gamma values of a discrete fourier transform
    '''
    N = len(samples)
    gamma = []
    kvalues = []
    for k in range(N//2+1):
        gammaK = 0
        for n,yn in enumerate(samples):
            gammaK += yn * np.exp(-2j * np.pi * k * n/N )
        gamma.append(gammaK/N) # square for absolute value
        kvalues.append(k)

    return kvalues, gamma
  

  def plot_dfts(self, graph_portion=3):
    '''
    plots frequency vs. power, and calculates fundamental frequencies.
    parameter is graph_portion, the higher the value the less
    of the graph we generate. 

    Note: this function does a lot, and it probably should
    be split up into different functions. 
    '''
    # first create our frequency axis
    
    x, y = self.DFT(self.left_over_time)
    y = [abs(i) for i in y]

    x1, y1 = self.DFT(self.right_over_time)
    y1 = [abs(i) for i in y1]

    # get plot labels
    left_free_label = "fixed"
    right_free_label = "fixed"
    # fix plot labels
    if not self.left_clamped:
      left_free_label = "free"
    if not self.right_clamped:
      right_free_label = "free"

    
    fig, ax = plt.subplots()
    ax.plot(
      x[:int(len(x)//graph_portion)], 
      y[:int(len(y)//graph_portion)],
      label=f"Left side ({left_free_label})")
    
    ax.plot(
      x1[:int(len(x1)//graph_portion)], 
      y1[:int(len(y1)//graph_portion)],
      label=f"Right side ({right_free_label})")
    
    fig.legend()
    fig.savefig("outputs/dft_plots.png")

    # print out the fundamental frequencies

    # first get the correct frequencies
    y_frequencies = self.get_values_of_indices(x, self.find_indices_of_maxima(y))
    y1_frequencies = self.get_values_of_indices(x1, self.find_indices_of_maxima(y1))
    
    print(f"The fundamental frequencies (left) are: {y_frequencies}")
    print(f"The fundamental frequencies (right) are: {y1_frequencies}")




  # some helper functions for self.plot_dfts

  def find_indices_of_maxima(self, _array:list):
    '''returns a list of indices where we are at maxima'''
    i_list = []

    for i in range(len(_array)):
      if _array[i-1] < _array[i] and _array[i+1] < _array[i]:
        i_list.append(i)

    return i_list


  def get_values_of_indices(self, value_list:list, indice_list:list):
    '''
    Goes through the indices list (ints) and returns all 
    the values from value_list at those indices.
    '''
    final_values = []

    for i in indice_list:
      final_values.append(round(value_list[i]))

    return final_values