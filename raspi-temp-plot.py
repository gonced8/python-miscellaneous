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


def smooth_data(time, data, N=5):
    time = np.array(time)
    data = np.array(data)

    begin = N//2
    end = time.size-N+begin+1
    time = time[begin:end]

    data = np.convolve(data, np.ones((N,))/N, mode='valid')

    return time, data


def polynomial_regression(x, y, deg=1):
    z = np.polyfit(x, y, deg)
    return np.poly1d(z)


def plot_temp(time, temp, fit_line=False):
    plt.plot(time, temp, label='measurement')

    if fit_line:
        x = range(0, len(temp))
        p = polynomial_regression(x, temp, 1)
        plt.plot(time, p(x), '--', label='linear regression')

        plt.legend()

    plt.title("Raspberry Pi CPU Temperature")
    plt.xlabel("days")
    plt.ylabel("temperature [ºC]")
    plt.grid()

    plt.tight_layout()
    plt.savefig("temp.png")
    plt.show()


if __name__=="__main__":
    if len(argv)<2:
        print(f"{argv[0]} <log filename>")
    else:
        time, temp = [], []

        for filename in argv[1:]:
            time,  temp = parse_file(filename, time, temp)

        time, temp = smooth_data(time, temp)
        plot_temp(time, temp, True) 
