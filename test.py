import random


class a:
    a = random.randint(0, 5) / 10

b = a()
print(b.a)

c = a()
print(b.a)
print(c.a)

d = a()
d.a = 10/10
print(b.a)
print(c.a)
print(d.a)
a.a = 15
print(d.a, a().a)