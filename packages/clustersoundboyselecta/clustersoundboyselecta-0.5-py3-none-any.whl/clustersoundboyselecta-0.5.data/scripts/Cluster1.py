import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv(filepath_or_buffer = 'data-1.csv', delimiter = ',', header= 0)
#print(df.to_string())
#print(df.columns)
var1 = df['var1']
var2 = df['var2']


class1x = []
class1y = []
class2x = []
class2y = []
class3x = []
class3y = []
for i in range(0, len(var1)):
    if var1[i] > -4:
        class1x.append(var1[i])
        class1y.append(var2[i])
    elif ((var1[i] < -4) and (var1[i] > -8)):
        class2x.append(var1[i])
        class2y.append(var2[i])
    else:
        class3x.append(var1[i])
        class3y.append(var2[i])
        
plt.scatter(class1x, class1y)
plt.scatter(class2x, class2y)
plt.scatter(class3x, class3y)
plt.show()
plt.close()    

