
import numpy as np 
import array,string
import unittest
import pandas as pd


# data={
#     'name':"sharu"
# }

# res=pandas.DataFrame(data=data,index=[98])
#Sha@18kohli
# print(res)

n=np.array([1,2,3,4,5])

print(n)
print(n.ndim)

print(type(n))

arr=np.array([2,4,6,8,10])

print(arr[3])

a=[1,7,2]
res=pd.Series(a,index=['x','y','z'])

print(res['y'])

data = {
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}

dicseries=pd.Series(data)
print(dicseries)

# df=pd.DataFrame(data)
# print(df)

df=pd.read_csv('fitness.csv')

res=df.dropna()

print(res)
