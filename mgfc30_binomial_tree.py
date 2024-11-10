# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 20:58:29 2024

@author: 21085
"""

import numpy as np
def binomial_tree(S,X,r,sigma,total_time,step,option_type,exercise_type):
    dt = total_time/step
    u = np.exp(sigma*np.sqrt(dt))
    d = 1/u
    p = (np.exp(r * dt) - d) / (u - d)
    print(f'here is the probability of goes up: {p}')
#try to assign stock price
    stock_price_tree = []
    for i in range(step+1):
        level = []
        for j in range(i+1):
            price = S*(u**(i-j))*d**j
            level.append(price) 
        stock_price_tree.append(level)
    print(f'this is stock price tree: {stock_price_tree}') 
# build the option tree
# when i = 1 [[0],[0,0]]
# when i = 2 [[0],[0,0],[0,0,0]]
# we need to creat the empty list first
# otherwise, you will have the index error
    option_tree = []
    for i in range(len(stock_price_tree)):
        option_tree.append([0] * len(stock_price_tree[i]))
#for example, you will have [[0],[0,0],[0,0,0],[0,0,0,0]]
#how many elements inside the stock price tree[i]
    for i in range(len(stock_price_tree)):
        option_tree[i] = [0] * len(stock_price_tree[i])  
        if option_type == "call":
            for idx in range(len(stock_price_tree[-1])):      
                price = stock_price_tree[-1][idx]             
                option_tree[-1][idx] = max(0, price - X)      
        elif option_type == "put":
            for idx in range(len(stock_price_tree[-1])):     
                price = stock_price_tree[-1][idx]             
                option_tree[-1][idx] = max(0, X - price)
    #print(f'this is option tree: {option_tree}')
    for i in range(step -1, -1,-1):     # so from the second from the bottom to the original point, but we have to include it, so we have to go until -1
        for j in range(i+1):
            possible_value = np.exp(-r * dt) *(p * option_tree[i + 1][j] + (1 - p) * option_tree[i + 1][j + 1])
            if exercise_type == 'american':
                if option_type == 'call':
                    exercise_value = max(0, (stock_price_tree[i][j] -X))
                if option_type == 'put':
                    exercise_value = max(0, (X - stock_price_tree[i][j]))
                option_tree[i][j] = max(possible_value, exercise_value)
            else:
                option_tree[i][j] = possible_value
   # print(f'this is the final answer {option_tree}')
    return option_tree[0][0]
                