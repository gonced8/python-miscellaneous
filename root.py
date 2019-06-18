i=2     # radicando
n=2    # numero

x=1.0*n
y=0

while x-y!=0:
    y=x
    x=((n/x**(i-1))+(2**(i-1)-1)*x)/(2**(i-1))
    print(x)
