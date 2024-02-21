import numpy as np
import os
import time

def main():
  print("Hello World")
  # Let's get a simple wave going

  # start our wave arrays for time -1, 0 and 1
  wave_time_array1 = np.array([0 for _ in range(10)])
  wave_time_array2 = np.array([0 for _ in range(10)])
  wave_time_array3 = np.array([0 for _ in range(10)])

  # set initial conditions
  wave_time_array1[3] = 1
  wave_time_array2[4] = 1
  wave_time_array3[5] = 1

  # create a loop to do a simple animation
  l = [wave_time_array1, wave_time_array2, wave_time_array3]
  for _ in range(10):
    for i in l:
      print(i)
      time.sleep(.2)
      clear_console()

  


def clear_console():
  os.system('cls' if os.name == 'nt' else 'clear')




if __name__ == "__main__":
  main()