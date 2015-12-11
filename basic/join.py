list1 = ['1', '2', '3']
string1 = ''.join(list1)
print(string1)
#123

list2 = ["1", "2", "3"]
string2 = "-*-".join(list2)
print(string2)
#1-*-2-*-3

list3 = [1, 2, 3]       
string3 = "".join(str(x) for x in list3)
print(string3)
#123

list4 = list(list1)
print(list4)
#['1', '2', '3']

list5 = list(list2)
print(list5)
#['1', '2', '3']

list6 = list(list3)
print(list6)
#[1, 2, 3]
