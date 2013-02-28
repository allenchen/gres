import random

# TODO(allenchen): [organization] These enums belong in a
# separate file.

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

# TODO(allenchen): Subtype enum.  ie. Goblin, Merfolk, Elf, ...
# [organization] obviously move that to another file. subtypes.py

# TODO(allenchen): Counter type. (eg. +1/+1 counters, Poison counters,
# -1/-1 counters, feather counters, etc.)

# TODO(allenchen): Special static effects. (eg. static effects from
# Olivia that makes things into vampires not expressed through counters)

EFFECT_ID = 0
CARD_ID = 0
PERMANENT_ID = 0
SPELL_ID = 0

class Cost(object):
    pass

class ManaCost(Cost):
    def __init__(self):
        self.white = 0
        self.blue = 0
        self.black = 0
        self.red = 0
        self.green = 0
        self.colorless = 0

class SpecialCost(Cost):
    def __init__(self):
        # TODO(allenchen): Abstraction for "special" cost?
        # This includes things like additional costs, optional
        # effects, etc.
        pass

class ManaRepository(object):
    def __init__(self):
        # all: integers
        self.white = 0
        self.blue = 0
        self.black = 0
        self.red = 0
        self.green = 0
        self.colorless = 0

    def canPay(self, cost):
        # cost: ManaCost()
        return (self.white >= cost.white and
            self.blue >= cost.blue and
            self.black >= cost.black and
            self.red >= cost.red and
            self.green >= cost.green and
            self.colorless >= cost.colorless)

    def spendMana(self, cost):
        # cost: ManaCost()
        if not self.canPay(cost):
            return False
        self.white -= cost.white
        self.blue -= cost.blue
        self.black -= cost.black
        self.red -= cost.red
        self.green -= cost.green
        self.colorless -= cost.colorless

class CardAttributes(object):
    # TODO(allenchen): Make subclasses:
    # PermanentAttributes(), SpellAttributes(), etc.
    def __init__(self,
                 colors=list(),
                 types=list(),
                 costs=list(),
                 subtypes=list(),
                 power=None,
                 toughness=None,
                 owner=None,
                 special=list()):
        # colors: list of [E]COLOR : integer
        # types: list of [E]CARD_TYPES : integer
        # costs: list of Cost() - both Mana and Special costs
        # subtypes: list of [E]SUBTYPES : integer
        # power: integer (?? - do I care about unhinged)
        # toughness: integer (?? - do I care about unhinged)
        # owner: Player()
        self.colors = colors
        self.types = types
        self.costs = costs
        self.subtypes = subtypes
        self.power = power
        self.toughness = toughness
        self.owner = owner
        # Cards in graveyards and exile can have counters on them.
        # fuck you whoever made that idea.
        # fuck you whoever let that idea through.
        self.special = list()

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
        self.stack = []
        self.priority = 0

    def addPermanent(self, permanent):
        # permanent: Permanent()
        self.permanents[permanent.controller] += [permanent]

    def drawCard(self, player):
        # player: Player()
        if len(self.libraries[player]) == 0:
            # TODO(allenchen): This isn't right since there should be a special event
            # for drawing from an empty library.  You don't necessarily lose the game
            # because of things like Laboratory Manic or anything that prevents you
            # from dying due to an empty library. (Platinum Angel should override
            # loseGame())
            self.loseGame(player)
            return

        card = self.libraries[player].pop()
        self.hands[player] += [card]
        return card

    def addCard(self, card, player):
        # card: Card()
        # player: Player()
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
        controller = permanent.controller
        # TODO(allenchen): Progress and put stuff into graveyards, trigger effects.
        # Need a hook into "graveyard trigger".

    def progressPriorityOrPhase(self):
        # TODO(allenchen): Finish this.
        # Progress to the next priority; if both players pass priority with the
        # stack empty we progress into the next phase.
        pass

    def checkStateBasedActions(self):
        # TODO(allenchen): Do a lot of maintenance here.
        # Put all creatures that have lethal damage marked on them into graveyards
        # Put creatures with 0 or less toughness into graveyards
        # Check static effects
        # Check legend rule
        # Read the comprehensive rules to find out wtf goes on here.
        pass

class Stack(object):
    # This represents the game stack (ie. the thing spells/effects go on)
    def __init__(self):
        self.stack = []

    def push(self, entity):
        self.stack.append(entity)

    def pop(self):
        if len(self.stack) is 0:
            # TODO(allenchen): This really shouldn't return None; I'd like to reduce
            # the usage of None as much as possible.
            return None
        return self.stack.pop()

class Effect(object):
    def __init__(self):
        self.actions = []
        self.id = EFFECT_ID
        EFFECT_ID += 1

    def addAction(self, action):
        # Actions ARE order sensitive; they should be added with care.
        self.actions += [action]

    def apply(self, gamestate):
        for action in self.actions:
            action(gamestate)

class Permanent(object):
    def __init__(self, attributes):
        self.attributes = attributes
        self.controller = 0
        self.damage = 0
        self.id = PERMANENT_ID
        PERMANENT_ID += 1

    def isType(self, type):
        return type in self.types

    def isColor(self, color):
        if color == COLORS.COLORLESS and len(self.attributes.colors) is 0:
            return True
        return color in self.colors

class Spell(object):
    def __init__(self, attributes):
        # attributes: CardAttributes()
        # id: integer
        # TODO(allenchen): attributes should be SpellAttributes() <= CardAttributes()
        self.attributes = attributes
        self.id = SPELL_ID
        SPELL_ID += 1

    def permanentize(self, player):
        # player: Player()
        # TODO(allenchen): Make Player() class.
        # Turns the spell into a permanent under the player's control.
        if not self.isPermanentCard:
            return None
        # TODO(allenchen): Create a permanent under PLAYER's control.

class Card(object):
    # TODO(allenchen): This needs to split.  There should be TWO kinds of cards:
    # actual Card information (which are singletons) and Card as in cards in library
    # that will be played. [urgent]
    def __init__(self, attributes):
        # attributes: CardAttributes()
        # id: integer
        self.attributes = attributes
        self.id = CARD_ID
        CARD_ID += 1

class DelayedEffect(object):
    def __init__(self, triggerCondition, effect):
        # triggerCondition: lambda gamestate: [[returns true|false]]
        # effect: lambda gamestate: [[void]]
        self.triggerCondition = triggerCondition
        self.effect = effect

    def trigger(self, gamestate):
        # gamestate: GameState()
        # TODO(allenchen): How do we represent the global gamestate?
        self.effect(gamestate)

    def test(self, gamestate):
        return self.triggerCondition(gamestate)
