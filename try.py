asd = "woman's"
hash = 0
for i in range(len(asd)):
    if asd[i] >= 'a' and asd[i] <= 'z':
        hash += (ord(asd[i]) - ord('a'))* 30**i
print(hash%41)


