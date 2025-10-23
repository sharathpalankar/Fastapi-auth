class person:
    def __init__(self, name, age):
        self.__name = name  # private attribute
        self.__age = age    # private attribute

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_age(self):
        return self.__age

    def set_age(self, age):
        if age >= 0:
            self.__age = age
        else:
            print("Age cannot be negative")

p = person("Alice", 30)
print(p.get_name()) 

p.set_name("Andrew")
print(p.get_name()) # Accessing private attribute via getter


data={"sub": ["email"]}
print(data)