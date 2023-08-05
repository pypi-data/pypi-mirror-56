#!python

import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv("data-1.csv")

n_centers = 3

centers = [(-10, -3), (-7, -7.5), (-1, 5)]

for i in range(n_centers):
    data[str(i)] = (data['var1'] - centers[i][0])**2 + (data['var2'] - centers[i][1])**2
data['class'] = data[[ str(x) for x in range(n_centers)]].idxmin(axis=1)    

data.to_csv("classes-1.csv", index=False)
classes = pd.read_csv("classes-1.csv")

plt.scatter(data["var1"], data["var2"], c=classes["class"])
plt.savefig("classes.png")
