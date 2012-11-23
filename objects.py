CARD_TYPES = {
    LAND: 0,
    CREATURE: 1,
    INSTANT: 2,
    SORCERY: 3,
    ENCHANTMENT: 4,
    PLANESWALKER: 5,
    ARTIFACT: 6,
    TRIBAL: 7
}

COLORS = {
    WHITE: 0,
    BLUE: 1,
    BLACK: 2,
    RED: 3,
    GREEN: 4,
    COLORLESS: 5
}

class ManaRepository(object):
    def __init__(object):
        self.white = 0
        self.blue = 0

class GameState(object):
    def __init__(self):
        self.permanents = {
            0: [],
            1: [],
            2: []
            }
        self.hands = {
            0: [],
            1: [],
            2: []
            }
        self.graveyards = {
            0: [],
            1: [],
            2: []
            }
        self.libraries = {
            0: [],
            1: [],
            2: []
            }
        self.exiled = {
            0: [],
            1: [],
            2: []
            }
        self.mana = {
            0: ManaRepository(),
            1: ManaRepository(),
            2: ManaRepository()
            }
        self.delayedEffects = []

    def addPermanent(self, permanent):
        self.permanents[permanent.controller] += [permanent]

    def drawCard(self, player):
        if len(self.libraries[player]) == 0:
            self.loseGame(player)
            return

        card = self.libraries[player].pop()
        self.hands[player] += [card]
        return card

    def addCard(self, card, player):
        self.hands[player] += [card]

    def playCard(self, card):
        

class Effect(object):
    def __init__(self):
        self.actions = []

    def addAction(self, action):
        self.actions += [action]

class Permanent(object):
    def __init__(self):
        self.controller = 0
        self.owner = 0
        self.colors = []
        self.types = []

    def isType(self, type):
        return type in self.types

    def isColor(self, color):
        if color == COLORS.COLORLESS and len(self.colors) is 0:
            return True
        return color in self.colors

class DelayedEffect(object):
    pass
