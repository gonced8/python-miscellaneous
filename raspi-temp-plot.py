import matplotlib.pyplot as plt
from sys import argv

def parse_file(filename):
    with open(filename, 'r') as f:
        time = []
        temp = []

        for line in f.readlines():
            time_i, temp_i = line.split('\t')

            time_i = time_i.split(':')
            time_i = float(time_i[0]) + float(time_i[1])/60
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
        time,  temp = parse_file(argv[1])
        plot_temp(time, temp)
