s1 = 'a' * 2
s2 = 'a' * 2
s = 2
s3 = 'a' * s
s4 = 'a' * s
print(id(s1))
print(id(s2))
print(id(s3))
print(id(s4))
print(s1 == s4)
