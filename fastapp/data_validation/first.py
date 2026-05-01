from pydantic import BaseModel ,validate_email ,EmailStr,model_serializer , ValidationError, Field , SecretStr , HttpUrl,field_validator
from functools import partial
from typing import Literal,Annotated
from uuid import UUID,uuid4

class User(BaseModel):
    uid:UUID =Field(default_factory=uuid4)
    name:str=Field(max_length=6)
    age:int
    password:SecretStr
    fullname:str | None = None
    website:str |None =None

    @field_validator("name")
    def validate_name(cls,value:str):
        if not value.isalpha():
            raise ValueError("name can't contain numbers ")
        return value
    
    @field_validator("website",mode="before")
    def validate_website(cls,value:str):
        if not value :
            return ValueError("please pass value for website")
        return value


u =User(name="abcd" ,age="98",password="sha@18klrahul",website="ab")
print(u.password.get_secret_value())
print(u.name)
print(u.model_dump_json(indent=2))



d={}

if "A" not in d:
    d["a" ] =1

print(d)

from collections import Counter , defaultdict ,ChainMap
d1 =defaultdict(list)

print(d1)

s ="sharath n shet"

print(s.split(' '))
j="".join(s)
print(j)


def group_anagrams(strs):
    anagramlist=defaultdict(list)
    for i in strs:
        key="".join(sorted(s))
        anagramlist[key].append(i)

    return list(anagramlist.values())

print(group_anagrams(strs=""))

# sliding window pattern max sub array  and  

no = [2,1,4,5,6,3,1]

k =3 

currentwindowsum = sum(no[:k])
max_sum =currentwindowsum

sub_array = 0

for i in range(k,len(no)):
    currentwindowsum= currentwindowsum - no[i-k] + no[i]
    if currentwindowsum > max_sum:
        max_sum = currentwindowsum
        sub_array = i-k+1 

    
print("max sub array elements are", no[sub_array:sub_array+k])
    #max_sum = max(max_sum, currentwindowsum) 

print(max_sum)


#sliding window longest subsequence

s1="abcabcbb"

output = 0
l =0 
seen =set()
for r in range(len(s1)):
    while s1[r] in seen:
        seen.remove(s1[l])
        l+=1 
    seen.add(s1[r])
    output=max(output, r-l+1)

print(output)


#string compression problem 

s2 ="abbccc"

strresult = ""

count =1 

for i in range(1,len(s2)):
    if s2[i] == s2[i-1]:
        count +=1 
    else:
        strresult +=  s2[i-1]+str(count)
        count =1 

strresult += s2[-1]+str(count)
print(strresult)

indict = {'apple':5 , 'cat':3, 'bat':3, 'grapes':6,'bikini':6}

res_dict = {} 

# {3:['cat' , 'bat'], 6:'grapes' , 5:'apple' }

for k, v in indict.items():
    if v not in res_dict:
        res_dict[v]= k 
    else:
        res_dict[v]=[res_dict[v] , k]

print(res_dict)

#2 sum 
