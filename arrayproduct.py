import requests
import math

data=requests.get('https://dummyjson.com/posts/')

# print(data.json())

res=data.json()
titles=[]

for i in res['posts']:
    if i['views']>1000:
        #print(i['title'])
        titles.append(i['title'])
    
print(sorted(titles))
no=[1,2,4,6,10]

op=[480,240,120,80,48]
totalsum=1

product=math.prod(no)

print(product)
sq=[]
for i in no: 
    sqlist=product//i
    sq.append(sqlist)

print(sq)

product=1
for p in no:
    product*=p 

print(product)



an=["listen", "silent","ate","eat"]

opp=[["listen", "silent"],["ate","eat"]]


class MyClass:
    "to instansiate all classes"
    def mtd1(self):
        pass

print(MyClass.mtd1.__reduce__)


#missing number in array

nums=[3,0,1,5,2]

current_sum=sum(nums)

n=len(nums)
expected_sum=n*(n+1)//2
missing_number=expected_sum-current_sum
print(missing_number)