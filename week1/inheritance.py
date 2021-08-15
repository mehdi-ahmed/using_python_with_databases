class PartyAnimal:
    x = 0
    name = ""

    def __init__(self, name):
        self.name = name
        print(self.name, 'I am constructed')

    def party(self):
        self.x = self.x + 1
        print(self.name, 'party count', self.x)


class FootballFan(PartyAnimal):  # Extends PartyAnimal
    points = 0

    def touch_down(self):
        self.points = self.points + 7
        self.party()
        print(self.name, 'points', self.points)


s = PartyAnimal('Sally')
s.party()
# Sally I am constructed
# Sally party count 1


j = FootballFan('Jim')  # This will call Parent's constructor
j.party()

# Jim I am constructed
# Jim party count 1


j.touch_down()
# Jim party count 2
# Jim points 7

print(dir(s))
