import random
from datetime import datetime
random.seed(datetime.now().timestamp())

###########################################################
# Main functions
###########################################################

def main():

    strategems = []

    # 0: support
    # 1: offense
    # 2: vehicle
    # 3: defensive
    category_prob = [.25, .25, .25, .25]
    category_limits = [4, 4, 2, 4]

    # 0: WeaponWPack
    # 1: WeaponWoPack
    # 2: Backpack
    support_prob = [.33, .33, .33]
    support_limits = [1, 2, 2]
    # 0: Orbitals
    # 1: Eagles
    offensive_prob = [.5, .5]
    offensive_limits = [2, 2]
    # 0: Emplacements
    # 1: Sentries
    # 2: Mines
    defensive_prob = [.4, .4, .2]
    defensive_limits = [1, 4, 2]
    fully_random_supports = False
    mech_selected = False

    armor_passives = csvToRandomizerData("ArmorPassives.csv")[0]
    primary_weapons = csvToRandomizerData("Primaries.csv")[0]
    secondary_weapons = csvToRandomizerData("Secondaries.csv")[0]
    grenades = csvToRandomizerData("Grenades.csv")[0]
    support_weapons_with_backpack = csvToRandomizerData("SupportWeaponsWithBackpacks.csv")[0]
    support_weapons = csvToRandomizerData("SupportWeapons.csv")[0]
    support_backpack = csvToRandomizerData("Backpacks.csv")[0]
    vehicles = csvToRandomizerData("Vehicles.csv")[0]
    orbitals = csvToRandomizerData("Orbitals.csv")[0]
    eagles = csvToRandomizerData("Eagles.csv")[0]
    emplacements = csvToRandomizerData("Fortifications.csv")[0]
    sentries = csvToRandomizerData("Sentries.csv")[0]
    mines = csvToRandomizerData("Mines.csv")[0]

    # Generating weights from probability tables
    category_weights = generateWeightsFromProbabilities(category_prob)
    support_weights = generateWeightsFromProbabilities(support_prob)
    offensive_weights = generateWeightsFromProbabilities(offensive_prob)
    defensive_weights = generateWeightsFromProbabilities(defensive_prob)

    print("Armor passive: ", armor_passives[selector(armor_passives, False)])
    print("Primary weapon: ", primary_weapons[selector(primary_weapons, False)])
    print("Secondary weapon: ", secondary_weapons[selector(secondary_weapons, False)])
    print("Grenade: ", grenades[selector(grenades, False)])

    for iter in range(4):
        category = selectCategory(category_weights, category_limits)
        strategem = ""
        if category == 0:
            support_category = selectCategory(support_weights, support_limits)
            if not fully_random_supports:
                if support_category == 0:
                    support_limits[1] = 0
                    support_limits[2] = 0
                    category_limits[0] = 0
                else:
                    support_limits[0] = 0
            while (strategem in strategems or strategem == ""):
                if support_category == 0:
                    strategem = support_weapons_with_backpack[selector(support_weapons_with_backpack, False)]
                elif support_category == 1:
                    strategem = support_weapons[selector(support_weapons, False)]
                elif support_category == 2:
                    strategem = support_backpack[selector(support_backpack, False)]
        elif category == 1:
            offensive_category = selectCategory(offensive_weights, offensive_limits)
            while (strategem in strategems or strategem == ""):
                if offensive_category == 0:
                    strategem = orbitals[selector(orbitals, False)]
                elif offensive_category == 1:
                    strategem = eagles[selector(eagles, False)]
        elif category == 2:
            while (strategem in strategems or strategem == "" or (mech_selected and "Exo" in strategem)):
                strategem = vehicles[selector(vehicles, False)]
            if "Exo" in strategem:
                mech_selected = True
        elif category == 3:
            defensive_category = selectCategory(defensive_weights,defensive_limits)
            while (strategem in strategems or strategem == ""):
                if defensive_category == 0:
                    strategem = emplacements[selector(emplacements, False)]
                elif defensive_category == 1:
                    strategem = sentries[selector(sentries, False)]
                elif defensive_category == 2:
                    strategem = mines[selector(mines, False)]
        print("Strategem {}: {}".format(iter, strategem))
        strategems.append(strategem)


###########################################################
# Selection functions
###########################################################
# Functions for selecting strategems


def selectCategory(weights, limits, retries=20):
    while retries:
        category = selector(weights)
        if (limits[category] > 0):
            limits[category] -= 1
            return category
        retries -= 1
    return None

# Selects an index from a weighted list
# Completely random if weighted is false


def selector(weights, weighted=True):
    if weighted:
        t = random.random()
        for index in range(len(weights)):
            if (weights[index]-t > -1E-1):
                return index
        return None
    else:
        return random.randint(0, len(weights) - 1)

###########################################################
# Helper functions
###########################################################


def csvToRandomizerData(filename, hasHeader=True):
    lines = []
    headers = []
    with open(filename, 'r') as file:
        if hasHeader:
            headers = file.readline().strip().split(",")
        line = file.readline()
        while line:
            columns = line.strip().split(",")
            lines.append(columns[0])
            line = file.readline()
    return lines, headers


def generateWeightsFromProbabilities(prob_table):
    prob_table_sum = sum(prob_table)
    weight_table = []
    for index in range(len(prob_table)):
        value = prob_table[index] / prob_table_sum
        if index != 0:
            value += weight_table[index-1]
        weight_table.append(value)
    return weight_table


if __name__ == "__main__":
    main()
