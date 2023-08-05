import pandas as pd

df = pd.read_csv("data-1.csv")
df.head()

from matplotlib import pyplot as plt
plt.scatter(df['var1'], df['var2'])
plt.show()
var1=df['var1']
var2=df['var2']
a = (-11,-5)
b = (-7, -9)
c = (-1,5)
classes = [0,1,2]
n = len(df['var1'])
from numpy import zeros
label = zeros(n)
for i in range(n):
    d1 = (var1[i]-a[0])**2 + (var2[i]-a[1])**2
    d2 = (var1[i]-b[0])**2 + (var2[i]-b[1])**2
    d3 = (var1[i]-c[0])**2 + (var2[i]-c[1])**2

    if d1 <= d2 and d1 <= d3:
        label[i] = classes[0]
    if d2 <= d1 and d2 <= d3:
        label[i] = classes[1]
    if d3 <= d1 and d3 <= d2:
        label[i] = classes[2]
plt.scatter(df['var1'], df['var2'], c = label)
plt.show()