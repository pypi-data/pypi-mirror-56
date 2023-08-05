import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms

df = pd.read_csv(filepath_or_buffer = 'data-2.csv', delimiter = ',', header= 0)
#print(df.to_string())
#print(df.columns)
x = df['var1']
y = df['var2']
class1x = []
class1y = []
class2x = []
class2y = []
class3x = []
class3y = []

#if datapoint x, y falls in between 
# 1) x doesnt matter but y < 7.5
# put in class one
#print(len(df))

for i in range(0, len(df)):
    if y[i] < 7.5:
        class1x.append(x[i])
        class1y.append(y[i])
    elif (x[i] < 24.8613 and y[i] > 7.5):
        class2x.append(x[i])
        class2y.append(y[i])
    else:
        class3x.append(x[i])
        class3y.append(y[i])
        
plt.scatter(class1x, class1y)
plt.scatter(class2x, class2y)
plt.scatter(class3x, class3y)
plt.show()
plt.close()    

'''
p_1 = [20, 30]
p_2 = [30.6981, 7.48465]
fig, ax = plt.subplots()
ax.scatter(x, y, c='black')
ax.axhline(7.5, ls='--')
ax.plot(p_1, p_2)
plt.show()
plt.clf()
plt.close()   
'''
