count={
    set:['apple','banana','mango'],
    dict:['green','head','david']

}

for d in count:
    print(d)

name='swiss'
keyvalue={}
for n in name:
    keyvalue[n]=keyvalue.get(n,0)+1

print(keyvalue)

def first_one(s):
    for i in keyvalue:
        if keyvalue[i]==1:
            return i

a=first_one(name)
print(a,'first')

def first_non_repeating(s):
    count = {}
    for char in s:
        count[char] = count.get(char, 0) + 1

    for char in s:
        if count[char] == 1:
            return char
    return None

print(first_non_repeating("swiss"))


