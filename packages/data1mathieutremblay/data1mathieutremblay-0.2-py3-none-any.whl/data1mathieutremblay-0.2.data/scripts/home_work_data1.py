#!python
import pandas as pd 
from numpy import zeros
import os
data_path=os.path.join(os.path.dirname(__file__),"..","data-1.csv")
df = pd.read_csv(data_path)
# classes = pd.read_csv("/Users/mathieutremblay/Desktop/python homework/class work 9/data-1.csv")
from matplotlib import pyplot as plt 
# plt.scatter(df['var1'],df['var2'])
# print (df.head())
# print (classes.head())

# plt.show()
A =(-11,-2.5)
B = (-6,-7.5)
C = (-1,-5,)
var1 = df['var1']
var2 = df['var2']
n= len(var1)
classes=zeros(n)
for i in range(n):
   da=(var1[i]-A[0])**2+(var2[i]-A[1])**2
   db=(var1[i]-B[0])**2+(var2[i]-B[1])**2
   dc=(var1[i]-C[0])**2+(var2[i]-C[1])**2
   if da<= db and da<= dc:
       classes[i]=0
   if db<= da and db<= dc:
       classes[i]=1    
   if dc<= db and dc<= da:
       classes[i]=2
plt.scatter(df["var1"], df["var2"], c=classes)
plt.show()

