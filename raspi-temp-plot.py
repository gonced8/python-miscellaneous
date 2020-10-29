from sys import argv
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

def parse_file(filename, time=[], temp=[]):
    date = Path(filename).stem
    print(date)

    with open(filename, 'r') as f:
        for line in f.readlines():
            time_i, temp_i = line.split('\t')

            time_i = datetime.strptime(date+' '+time_i, "%Y-%m-%d %H:%M")
            temp_i = float(temp_i)

            time.append(time_i)
            temp.append(temp_i)

    return time, temp


def plot_temp(time, temp):
    plt.plot(time, temp)

    plt.title("Temperature throughout the day")
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

        plot_temp(time, temp)
