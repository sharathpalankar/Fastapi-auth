class shape:
    def area(self):
        return "the shape of the object figure"
    
class rectangle(shape):
    def __init__(self,width,height):
        self.width=width
        self.height=height

    def area(self):
        return self.width*self.height
    

class  circle(shape):
    def __init__(self,radius):
        self.radius=radius

    def area(self):
        return 3.14*self.radius*self.radius
    

def print_area(obj):
    print(obj.area())

r=rectangle(10,20)
c=circle(7)

print_area(c)


class Person:
    def __init__(self,name,age):
        self._name=name
        self.age=age

class Employee(Person):
    def __init__(self,name,age,salary):
        super().__init__(name,age)
        self.salary=salary

    # def getName(self):
    #     return self._name

p=Person("sharu",24)
print(dir(p))
# print(p._Person__name)

e=Employee("bharu",24,10000)
print(e._name)
# print(e.getName())

class parent:
    def __init__(self,name):
        self.name=name
        self.count=0
    def __call__(self):
        self.count+=1 
        print(f"parent class called{self.count} times")
        
class smallparent:
    def __init__(self ,name):
        self.name=name
        
