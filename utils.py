from objects import ManaCost

def stringToManaCost(manaString):
    cost = ManaCost()
    manaSymbols = "WUBRGwubrg"
    integers = "0123456789"
    integerBuffer = ""
    for c in manaString:
        if c in manaSymbols:
            # clear integerbuffer
            if len(integerBuffer) > 0:
                cost.colorless += int(integerBuffer)
                integerBuffer = ""

            c = c.upper()
            if c == "W":
                cost.white += 1
            elif c == "U":
                cost.blue += 1
            elif c == "B":
                cost.black += 1
            elif c == "R":
                cost.red += 1
            elif c == "G":
                cost.green += 1
        elif c in integers:
            integerBuffer += [c]
    # clear integerbuffer
    if len(integerBuffer) > 0:
        cost.colorless += int(integerBuffer)

    return cost
