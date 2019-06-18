import math
import time


def show_primes(n1):
    print('start')

    count=0

    n1=n1+1

    start_time = time.time()

    for i in range (2, n1, 1):

        t=False

        #n2=i/2
        n3=int(math.sqrt(i))+1
        
        for j in range (2, n3, 1):

            if(i%j==0):
                
                t=True
                
                break


        if(not t):
            
            count=count+1
            
            #print (i)

            #input()

    end_time = time.time()

    print("number of primes", count)

    elapsed_time = end_time - start_time

    print ('time', elapsed_time)



def is_prime(number):
    
    start_time = time.time()

    t=False

    #n2=i/2
    n3=int(math.sqrt(number))+1
        
    for j in range (2, n3, 1):

        if(number%j==0):
                
            t=True
                
            break

    #input()     

    if not t:
        print(number, 'is prime')
    else:
        print(number, 'is NOT prime')

    elapsed_time = time.time() - start_time

    print ('time', elapsed_time)


#is_prime(2017)
#input()
show_primes(1000000)

input()
