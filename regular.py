import re 

import string

text = "My phone number is 9876543210 and my zip code is 560001"

numbers=re.findall(r"\d+", text)

print(numbers)

re.findall(r'[A-Za-z]+', text)

mystr = 'sha@18kohli1998'

my=re.findall(r'[^A-Za-z0-9]', mystr)

print(my)