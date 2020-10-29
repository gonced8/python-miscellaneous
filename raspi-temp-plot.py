from sys import argv
from pathlib import Path
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt


def parse_file(filename, time=[], temp=[]):
    date = Path(filename).stem

    with open(filename, 'r') as f:
        for line in f.readlines():
            time_i, temp_i = line.split('\t')

            time_i = datetime.strptime(date+' '+time_i, "%Y-%m-%d %H:%M")
            temp_i = float(temp_i)

            time.append(time_i)
            temp.append(temp_i)

    return time, temp


def smooth_data(time, data, N=8):
    time = np.array(time)
    data = np.array(data)

    begin = N//2
    end = time.size-N+begin+1
    time = time[begin:end]

    data = np.convolve(data, np.ones((N,))/N, mode='valid')

    return time, data

def plot_temp(time, temp):
    plt.plot(time, temp)

    plt.title("Raspberry Pi Temperature")
    plt.xlabel("time [h]")
    plt.ylabel("temperature [ºC]")
    plt.grid()

    plt.tight_layout()
    plt.show()


if __name__=="__main__":
    if len(argv)<2:
        print(f"{argv[0]} <log filename>")
    else:
        time, temp = [], []

        for filename in argv[1:]:
            time,  temp = parse_file(filename, time, temp)

        time, temp = smooth_data(time, temp)
        plot_temp(time, temp)
