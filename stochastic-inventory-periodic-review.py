###### Stochastic Inventory Models: Periodic Review

###### Periodic Review with Non-Zero Fixed Costs: (s,S) Policies
import pandas as pd
import numpy as np
from scipy.stats import poisson

# Input 
h = int(input('Holding cost = ')) # Holding cost
p = int(input('Stockout cost = ')) # Stockout cost
K = int(input('Fixed cost = ')) # Fixed cost
muu = int(input('Standard deviation = ')) # Standard deviation

# Calculate probability
def f(d):
    f = poisson.pmf(k=d, mu=muu)
    return f

def m(r):
    if r == 0:
        ans = 1 / (1 - f(0))
    else:
        d = 1
        a = 0
        for jj in range(d, r + 1):
            a += f(jj) * m(r-jj)
            ans = a / (1 - f(0))
    return ans

def M(j):
    if j == 0:
        ans = 0
    elif j == 1:
        ans = 1 / (1 - f(0))
    else:
        #
        ans = M(j-1) + m(j-1)
        #
    return ans

def n(i):
    n = 0
    for xx in range(i, 100):
        n += (xx - i)*f(xx)
    return(n)

def nh(i):
    n = 0
    for xx in range(0, i + 1):
        n += (i - xx)*f(xx)
    return n

def g(S):
    ans = h * nh(S) + p * n(S)
    return ans

def G(s, S):
    ans = 0
    for d in range(0, S-s):
        ans += m(d) * g(S-d)
    answer = (K + ans)/ M(S-s)
    return answer

def solve():
    min_value = g(20)
    min_index = 0
    for i in range(0, 20):
        if g(i) < min_value:
            min_value = g(i)
            min_index = i
    g_p = 0
    c = 0
    for i in range(0, min_index): 
        c += 1
        if G(min_index-c, min_index) < g(min_index-c):
            s_p = min_index-c
            S_p = min_index
            g_p = G(s_p, S_p)
            break
    S = S_p
    s = s_p
    
    while g(S) <= g_p:
        if G(s_p, S) < g_p:
            S_p = S
            while G(s, S_p) <= g(s + 1):
                s = s + 1

                break
            s_p = s
            g_p = G(s_p, S_p)
        S = S + 1

    return s_p, S_p

# print('Quantity: ', G(4,10))
print('Optimal parameters: ',solve())
print('Cost: ', G(solve()[0], solve()[1]))