#!python
import pandas as pd
from matplotlib import pyplot as plt


df = pd.read_csv(filepath_or_buffer = './data-3.csv', delimiter = ',', header= 0)

x = df['var1']
y = df['var2']

class1x = []
class1y = []
class2x = []
class2y = []
class3x = []
class3y = []



for i in range(0, len(df)):
    if x[i] < 113.258:
        class1x.append(x[i])
        class1y.append(y[i])
    elif (x[i] > 113.258 and x[i] < 162):
        class2x.append(x[i])
        class2y.append(y[i])
    else:
        class3x.append(x[i])
        class3y.append(y[i])
        
plt.scatter(class1x, class1y, c = 'blue')
plt.scatter(class2x, class2y, c = 'red')
plt.scatter(class3x, class3y, c = 'green')
plt.show()
plt.close()    
'''
# PRE CLASS VISUALs
#p_1 = [20, 30]
#p_2 = [30.6981, 7.48465]
fig, ax = plt.subplots()
ax.scatter(x, y, c='black')
ax.axvline(113.258, ls='--')
ax.axvline(162, ls='--')
#ax.plot(p_1, p_2)
plt.show()
plt.clf()
plt.close()   
'''