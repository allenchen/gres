import random

class Enum:
    pass

CARD_TYPES = Enum()
CARD_TYPES.LAND = 0
CARD_TYPES.CREATURE = 1
CARD_TYPES.INSTANT = 2
CARD_TYPES.SORCERY = 3
CARD_TYPES.ENCHANTMENT = 4
CARD_TYPES.PLANESWALKER = 5
CARD_TYPES.ARTIFACT = 6
CARD_TYPES.TRIBAL = 7

COLORS = Enum()
COLORS.WHITE = 0
COLORS.BLUE = 1
COLORS.BLACK = 2
COLORS.RED = 3
COLORS.GREEN = 4
COLORS.COLORLESS = 5

PHASES = Enum()
PHASES.UNTAP = 0
PHASES.UPKEEP = 1
PHASES.DRAW = 2
PHASES.MAIN1 = 3
PHASES.BEGIN_COMBAT = 4
PHASES.DECLARE_ATTACKERS = 5
PHASES.DECLARE_BLOCKERS = 6
PHASES.FIRST_STRIKE_COMBAT_DAMAGE = 7
PHASES.COMBAT_DAMAGE = 8
PHASES.END_COMBAT = 9
PHASES.MAIN2 = 10
PHASES.END = 11
PHASES.CLEANUP = 12

EFFECT_ID = 0
CARD_ID = 0
PERMANENT_ID = 0
SPELL_ID = 0

class ManaCost(object):
    def __init__(self):
        self.white = 0
        self.blue = 0
        self.black = 0
        self.red = 0
        self.green = 0
        self.colorless = 0

class ManaRepository(object):
    def __init__(self):
        self.white = 0
        self.blue = 0
        self.black = 0
        self.red = 0
        self.green = 0
        self.colorless = 0

    def canPay(self, cost):
        return (self.white >= cost.white and
            self.blue >= cost.blue and
            self.black >= cost.black and
            self.red >= cost.red and
            self.green >= cost.green and
            self.colorless >= cost.colorless)

    def spendMana(self, cost):
        if not self.canPay(cost):
            return False
        self.white -= cost.white
        self.blue -= cost.blue
        self.black -= cost.black
        self.red -= cost.red
        self.green -= cost.green
        self.colorless -= cost.colorless

class CardAttributes(object):
    def __init__(self,
                 colors=list(),
                 types=list(),
                 costs=list(),
                 subtypes=list(),
                 power=None,
                 toughness=None,
                 owner=None):
        self.colors = colors
        self.types = types
        self.costs = costs
        self.subtypes = subtypes
        self.power = power
        self.toughness = toughness
        self.owner = owner

    def isPermanentCard(self):
        return any(
            map(lambda type: type in [CARD_TYPES.LAND,
                                CARD_TYPES.CREATURE,
                                CARD_TYPES.ENCHANTMENT,
                                CARD_TYPES.PLANESWALKER,
                                CARD_TYPES.ARTIFACT],
                self.types))

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

    def applyEffect(self, effect):
        effect(self)

    def shuffleDeck(self, player):
        random.shuffle(self.libraries[player])

    def getOpponent(self, player):
        if player == 1:
            return 2
        elif player == 2:
            return 1
        return 0

    def putPermanentIntoGraveyard(self, permanent):
        pass

    def checkStateBasedActions(self):
        # Put all creatures that have lethal damage marked on them into graveyards
        pass

class Effect(object):
    def __init__(self):
        self.actions = []
        self.id = EFFECT_ID
        EFFECT_ID += 1

    def addAction(self, action):
        self.actions += [action]

class Permanent(object):
    def __init__(self, attributes):
        self.attributes = attributes
        self.controller = 0
        self.damage = 0
        self.id = EFFECT_ID
        EFFECT_ID += 1

    def isType(self, type):
        return type in self.types

    def isColor(self, color):
        if color == COLORS.COLORLESS and len(self.colors) is 0:
            return True
        return color in self.colors

class Spell(object):
    def __init__(self, attributes):
        self.attributes = attributes
        self.id = SPELL_ID
        SPELL_ID += 1

    def permanentize(self):
        if not self.isPermanentCard:
            return None

class Card(object):
    def __init__(self, attributes):
        self.attributes = attributes
        self.id = CARD_ID
        CARD_ID += 1

class DelayedEffect(object):
    def __init__(self):
        self.triggerCondition = lambda state: False
        self.effect = lambda state: state
