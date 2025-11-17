
# class Father:
#     def __init__(self):
#         pass
#     def demo(self):
#        print("parent method")
   

# class Son(Father):
#     def __init__(self):
#         pass

#     # def demo(self):
#     #   print("called from child metod")


# s=Son()
# s.demo()

# numbers=[5,2,8,13,10,20,22]

# max_sum = 0  # to store maximum sum

# for i in range(len(numbers) - 2):
#     total = 0
#     # manually calculate sum of 3 consecutive numbers
#     for j in range(3):
#         total = total + numbers[i + j]
#     # manually check if this is the largest so far
#     if i == 0 or total > max_sum:
#         max_sum = total

# print("Maximum sum of 3 consecutive numbers:", max_sum)


a={"name":"sharu",
    "gender":"boy",
    "class":"fifteen",
    "city":"pune"
}
#output={}

inputkey=4
print(a.items())

outputdetails=[]

for k ,v in a.items():
    # print(k,v)
    if inputkey==len(k):

        print(k)
        outputdetails.append({k:v})

print(outputdetails)
        # output[k]=v


#find ist occurence

haystack = "hellohello"
needle = "lo"

for i in range(len(haystack) - len(needle) + 1):
    print(i)
    if haystack[i:i+len(needle)] == needle:
        print(f"Needle found at index: {i}")
        break