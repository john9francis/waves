import numpy as np
import os
import time
from matplotlib import pyplot as plt

from my_wave import Wave

def main():
  w = Wave(15)
  w.set_clamp(right_clamp=False)
  #w.animated_plot(100)

  # TODO: perform a spectrum analysis
  w.plot_left_right_pos_over_time(.5)




if __name__ == "__main__":
  main()