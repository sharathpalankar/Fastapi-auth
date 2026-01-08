from collections import defaultdict,OrderedDict,Counter

s="anagram"
t="nagaram"

def isAnagram(s,t):
    s_count=Counter(s)
    print(s_count)

    for char in t:
        if  char not in s_count:
            return False
        s_count[char]-=1
        if s_count[char]==0:
            del s_count[char]
            
    return len(s_count)==0
    
def groupAnagrams(strs):
    anagram_map = defaultdict(list)   

    for word in strs:
        sorted_word = ''.join(sorted(word))
        anagram_map[sorted_word].append(word)
    return list( anagram_map.values())
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(groupAnagrams(words))
    
res=isAnagram(s,t)
print(res)

class shape:
    def __init__(self, auto_error=True):
        self.auto_error=auto_error

    def __call__(self, *args, **kwds):
        return "shape called from call method"

    def area(self):
        return "the shape of the object figure"
    
class rectangle(shape):
    def __init__(self,width,height):
        self.width=width
        self.height=height

    def area(self):
        return self.width*self.height
    

c=rectangle(10,20)
print(c)

class A:
    def __init__(self):
        self.demo()
        print("init of A")

    def demo(self):
        print("demo of A")  

class B(A):
    def __init__(self):
        super().__init__()
        print("init of B") 

    # def demo(self):
    #     print("demo of B")

b=B()
# b.demo()

# two sum 

marks=[12,20,24,28,30,32]

target = 52
pair=[]

for i in range(len(marks)):
    for j in range(i+1,len(marks)):
        if marks[i] + marks[j] ==target :
            pair.append([i,j])
            
print(pair)

# now with using while loop

a= 0 
b= len(marks)-1

while a < b:
    current_sum = marks[a] + marks[b]
    if current_sum == target:
        pair.append([a,b])
        a += 1
        b -= 1
    elif current_sum < target:
        a += 1
    else:
        b -= 1 

name=' shartah shet '

print(' '.join(name.split()[::-1]))

lastword="   fly me   to   the moon  "

lastword=(lastword.split())

print(len(lastword[-1]))