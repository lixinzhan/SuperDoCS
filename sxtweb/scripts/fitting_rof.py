import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

x = [22.75, 16.93, 14, 13, 12, 10, 8, 6, 5.25, 4.25, 2.25]
y = [1, 1, 0.992, 0.9884, 0.9853, 0.9798, 0.9747, 0.964, 0.9603, 0.9523, 0.9314]

print('The length of x, y: ',len(x), len(y))

def fit_func(x,P,S,U,L,N):
    return P*x**N / (L**N+x**N) + S*(1.0-np.exp(-U*x)) # Hill-Exponential
def fit_hill_func(x,P,S,U,L,N):
    S=0.0
    U=0.0
    return P*x**N / (L**N+x**N) # Hill-Exponential
def fit_exp_func(x,P,S,U,L,N):
    P=0.0
    N=0.0
    L=1.0
    return S*(1.0-np.exp(-U*x)) # Hill-Exponential

[P,S,U,L,N],params_covariance = optimize.curve_fit(fit_func,x,y)
[P1,S1,U1,L1,N1],params_covariance = optimize.curve_fit(fit_hill_func,x,y)
#[P2,S2,U2,L2,N2],params_covariance = optimize.curve_fit(fit_exp_func,x,y)

print('\nRED - Hill-Exponential Fitting Parameters P,S,U,L,N: ')
print(P,S,U,L,N)
print('\nBLUE - Hill Fitting Parameters P,S,U,L,N: ')
print(P1,S1,U1,L1,N1)
#print('\nGREEN - Exponential Fitting Parameters P,S,U,L,N: ')
#print(P2,S2,U2,L2,N2)
print('\n')
print('x\t y\t yfit\t\t diff%')
for n in range(len(x)):
    yfit=fit_func(x[n],P,S,U,L,N)
    print(x[n], '\t', y[n], '\t', yfit, '\t', 100*(yfit-y[n])/y[n])

plt.figure()
xcurve=np.linspace(23,2,num=20)
plt.plot(xcurve,fit_func(xcurve,P,S,U,L,N),'r-',x,y,'*',
         xcurve,fit_hill_func(xcurve,P1,S1,U1,L1,N1),'b-',
#         xcurve,fit_exp_func(xcurve,P2,S2,U2,L2,N2),'g-',
)
plt.show()


