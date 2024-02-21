import numpy as np
from matplotlib import pyplot as plt
import datetime

class Wave():

  # static variable to control if it's running
  running = True

  def __init__(self, velocity, clamp_right=True, clamp_left=True) -> None:
    self.dx = .01
    
    # cdt/dx = 1
    # dt = dx/c
    self.dt = self.dx / velocity

    self.wave_array = np.arange(0, 1, self.dx)
    self.time_range = 0

    # define arrays of position of ends over time
    self.left_over_time = []
    self.right_over_time = []
    self.time_array = []

    # some bool flags
    self.right_clamped = clamp_right
    self.left_clamped = clamp_left

    # hook up plot to a close event, so we can quit the animation
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
    '''
    k = 1000
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
      # quit if running flag is false
      if not self.running:
        return
      
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

  @classmethod
  def set_running(cls, value:bool):
    cls.running = value

  def on_close(self, event):
    self.set_running(False)
    pass


  def DFT(self, samples):
    '''
    Takes in a list of samples
    '''
    N = len(samples)
    gamma = []
    for k in range(N//2 + 1):
      gammaK = 0
      for n,yn in enumerate(samples):
        gammaK += yn * np.exp(-2 * np.pi * k * n/N)
      gamma.append(gammaK/N)

    return gamma
  


  # TODO: create plots of the position over time 95% from the end
  def generate_pos_over_time_data(self, amount_of_time: int):

    old, current, new = self.initial_conditions()

    for i in range(round(amount_of_time / self.dt)):
      old, current, new = self.step(current, new)

      # save to our lists
      left_indx = round(len(current) * .05)
      right_indx = round(len(current) * .95)

      self.left_over_time.append(current[left_indx])
      self.right_over_time.append(current[right_indx])

      self.time_array.append(i * self.dt)
    


  
  def plot_pos_over_time(self):
    left_free_label = "fixed"
    right_free_label = "fixed"
    # fix plot labels
    if not self.left_clamped:
      left_free_label = "free"
    if not self.right_clamped:
      right_free_label = "free"
    
    # now plot the data
    plt.plot(self.time_array, self.left_over_time, label=f"Left end ({left_free_label})")
    plt.plot(self.time_array, self.right_over_time, label=f"Right end ({right_free_label})")
    plt.legend()
    plt.show()
    pass


  def DFT(self, samples):
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
  

  def plot_dfts(self):
    '''
    plot frequency vs. power
    '''
    # first create our frequency axis
    
    x, y = self.DFT(self.left_over_time)
    y = [abs(i) for i in y]

    x1, y1 = self.DFT(self.right_over_time)
    y1 = [abs(i) for i in y1]
    plt.plot(x, y)
    plt.plot(x1, y1)
    plt.show()