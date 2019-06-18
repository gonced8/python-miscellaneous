from sys import argv

def frequency_analysis(filename, options=[1]):

    file = open(filename, 'r')
    n_letters = int(options[0])

    text = file.read()
    text = ''.join(filter(str.isalpha, text))
    text = text.upper()

    for n in range (n_letters):
        info = {}

        for step in range (2):  # first read then count

            for i in range(len(text)-n): # cycle text

                word = text[i:i+1+n]

                if step==0:
                    info[word]=0
                else:
                    info[word]+=1

        print("Frequency analysis for %d letter(s):" %(n+1))

        maximum = max(info, key=info.get)
        ref = info[maximum]
        total = sum(info.values())
        count = 1

        while info[maximum]!=0:

            number = info[maximum]
            percentage = 100.0*number/total
            stars = "*" * int(round(10.*number/ref))

            print("%d\t\"%s\"\t%d\t%.3f%%\t%s" %(count, maximum, number, percentage, stars))
            info[maximum]=0
            maximum = max(info, key=info.get)
            count+=1

        print('')
        #input("Press ENTER to continue")

    file.close()

    return

################################################################################

words = len(argv)

if words>=2:
    if words>=3:
        frequency_analysis(argv[1], argv[2:])
    else:
        frequency_analysis(argv[2])
else:
    print("\nFrequency Analysis")
    print("Use this program as:\npython <program_name> <file> <#letters=1>")
