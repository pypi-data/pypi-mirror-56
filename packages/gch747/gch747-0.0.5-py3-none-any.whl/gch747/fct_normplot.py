# -*- coding: utf-8 -*-
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
    
def normplt(x):

    x = np.squeeze(x)
    
    # Calculate quantiles and least-square-fit curve
    (quantiles, values), (slope, intercept, r) = stats.probplot(x, dist='norm')
    
      
    plt.plot(values, quantiles,'ob')
    
    #Label points
    o = 2.5*np.ones([x.shape[0],1])
    point_labels = list(range(1, max(x.shape)+1))
    for i, label in enumerate(point_labels): 
        plt.text (x[i], o[i], label, fontsize=15).set_color('red')

     
    plt.plot(quantiles * slope + intercept, quantiles, 'r')
    
    #define ticks
    ticks_perc=[1, 5, 10, 20, 50, 80, 90, 95, 99]
    
    #transfrom them from precentile to cumulative density
    ticks_quan=[stats.norm.ppf(i/100.) for i in ticks_perc]
    
    #assign new ticks
    plt.yticks(ticks_quan,ticks_perc)

    #show plot
    plt.show()
