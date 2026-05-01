
score = [4,8 ,12,15,22,28]
target = 20 

a = 0 
b =len(score)-1 
pair= []

while a<b:
    target_sum = score[a]+score[b]

    if target_sum < target:
        a+=1        
         
    elif target_sum > target:
        b-=1

    else:
        pair.append((score[a],score[b]))
        break

print(pair)  

instr = "a,b&c"
outstr ="a&b,c"

inlist=list(instr)
print(inlist)

l =0 
r= len(inlist)-1 

while l<r:
    if not instr[l].isalpha() :
        l+=1
    elif not instr[r].isalpha():
        r-=1 
    else:
        inlist[l] ,inlist[r] = inlist[r] ,inlist[l]
        l+=1
        r-=1

print("".join(inlist))

spec= [ch for ch in instr if not ch.isalpha()]
print(spec)
spec.reverse()
print(spec)

result = []
j=0
for k in instr:
    if k.isalpha():
        result.append(k)
    else:
        result.append(spec[j])
        j+=1 

print(''.join(result))


name="shrath shet"

vowels=['a','e','i','o','u']


namevowel=[n for n in name if n in vowels]

print(namevowel) 

vowelsresult =[]
v =len(namevowel)-1
for nm in name:
    if nm not in vowels:
        vowelsresult.append(nm)
    else:
        vowelsresult.append(namevowel[v])
        v-=1 

print(''.join(vowelsresult))  


# 2 pointers remove element

val =[2,4,5,4,6,7,8,9]

rem =4 

i = 0 

for v in val:
    if v!=rem :
        val[i] = v 
        i+=1

print(val[:i]) 

# nested 

flat_list = [10,20,30,40,50,60]

size = 2 

nested_list = []

for i in range(0,len(flat_list),size):
    nested_list.append(flat_list[i:i+size])

print(nested_list)

vars()

class order:
    def __init__(self, order_id ,amount):
        self.order_id = order_id
        self.amount = amount

order_obj =order(1,1000)
print((order_obj.__dict__))

        
