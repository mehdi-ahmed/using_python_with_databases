# Week 1 - OOP

# self is similar to 'this' in Java
class PartyAnimal:
    x = 0
    name = ""

    # Optional - usually used to set up variables
    def __init__(self, z):
        self.name = z
        print(self.name, 'I am constructed')

    # Optional - seldom used
    def __del__(self):
        print('I am destructed', self.x)

    def party(self):
        self.x = self.x + 1
        print(self.name, 'party count', self.x)


an = PartyAnimal('test')
an.party()  # So far 1
an.party()  # So far 2
an.party()  # So far 3

an = 42
print('an contains', an)

s = PartyAnimal("Sally")
j = PartyAnimal("Jimmy")

s.party()
j.party()
