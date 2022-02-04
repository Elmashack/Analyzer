import re


num = input()
res = 0
gener = (int(n) for n in num)
for n in gener:
    res = res + n
print(res)


