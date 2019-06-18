import numpy as np
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
import sys
import subprocess

if len(sys.argv)>1:

    delimiter=None
    skiprows=0
    ls='.'

    for elem in sys.argv[1:]:
        if elem.find('delimiter=')!=-1:
            delimiter=elem[elem.find('=')+1:]
        elif elem.find('skiprows=')!=-1:
            skiprows=int(elem[elem.find('=')+1:])
        elif elem.find('ls=')!=-1:
            ls=elem[elem.find('=')+1:]
        elif elem.find('=')==-1:
            filepath = elem
            
    data = np.loadtxt(filepath, delimiter=delimiter, skiprows=skiprows)
    data = np.transpose(data)

    for i in range(1, data.shape[0]):
            plt.figure()
            plt.plot(data[0], data[i], ls, markersize=1., linewidth=1.)
            #filename = "fig_temp%d.png" %i
            #plt.savefig(filename, bbox_inches='tight')

    plt.show()
    
    '''
    for i in range(1, data.shape[0]):
        bashCommand = "open fig_temp%d.png" %i
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    for i in range(1, data.shape[0]):
            bashCommand = "rm fig_temp%d.png" %i
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
    '''

else:
    print("graph <filename> <delimiter=> <skiprows=> <ls=>")
