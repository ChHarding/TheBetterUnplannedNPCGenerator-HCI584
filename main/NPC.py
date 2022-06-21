class NPC:
    #name = ("FirstName","LastName")
    #race = ""
    #age = 0 # Age Ranges will Differ Per Race
    #gender = "" # male, female, nonbinary. Expanded gender options can be end-user configured.
    # physicalChars = ("eyeColor", "skinColor", "hairColor", "hairChars", "height", "build")
    # occupation
    # lifestyle # Options: Wretched, Squalid, Poor, Modest, Comfortable, Wealthy, Aristocratic
    # faith
    # alignment # Examples: Chaotic Neutral, Lawful Good, etc. May be informed by faith.

    def __init__(self, race, gender, lifeStage, culture):
        if (race != "Any"):
            self.race = race
        else:
            self.race = generateRace()
        
        if (gender != "Any"):
            self.gender = gender
        else:
            self.gender = generateGender()

        self.lifeStage = "" 
        if (lifeStage == "Any"): # Child, Teenager, Young Adult, Adult, Elder
            self.lifeStage = generateLifeStage()
        else:
            self.lifeStage = lifeStage
        
        self.age = getAge(self.race, self.lifeStage)

        if (culture == "Traditional"):
            self.name = getNameByRaceTradition(self.race)
        elif (culture == "Common"):
            self.name = getCommonName()
        else:
            self.name = getTrueRandomName()
        

def generateRace():
    return "Human" # Implement random race selection

def generateGender():
    return "Male" # Implement random gender selection

def generateLifeStage():
    return "Young Adult" # Implement random life stage selection

def getAge(race, lifeStage):
    return 25
    # Get the race appropriate age range for the provided life stage, then randomly select within that range

def getNameByRaceTradition(race):
    return ("TradFirstName", "TradLastName")

def getCommonName():
    return ("CommonFirstName", "CommonLastName")

def getTrueRandomName():
    return ("Randy","Randington")