class Family:
    lastname = "박"

a = Family()
b = Family()
c = Family()

b.lastname = "조"

print(a.lastname)
print(b.lastname)
print(c.lastname)