# This is an external mod script!
class Entity:
    def __init__(self):
        self.name = "Berserker Bot"
        self.aggression = 100

    def update(self):
        # Custom logic written by the modder
        if self.aggression > 50:
            return "ATTACK_NEAREST"
        else:
            return "PATROL"
