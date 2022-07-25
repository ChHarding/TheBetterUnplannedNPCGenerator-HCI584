import csv
import math
import os
import random
import sys
from tkinter import messagebox


class NPC:
    #name = ("FirstName","LastName")
    #race = ""
    #age = 0 # Age Ranges will Differ Per Race
    #gender = "" # male, female, nonbinary. Expanded gender options can be end-user configured.
    # physicalChars = ("eyeColor", "skinColor", "height", "build", "")
    # occupation

    namesFilePath = "resources\\names\\"

    def __init__(self, options, race, gender, lifeStage, industry, profession, culture):
        self.options = options
        self.npcDisplayText = []

        self.gender = gender
        self.lifeStage = lifeStage
        self.industry = industry
        self.profession = profession
        self.culture = culture

        self.nameDisplay = ""
        self.occupationDisplay = "Occupation: "
        self.raceDisplay = "Race: "
        self.ageDisplay = "Age: "
        self.genderDisplay = "Gender: "
        self.heightDisplay = "Height: "
        self.bodyTypeDisplay = "Body Type: "
        self.eyeColorDisplay = "Eye Color: "
        self.skinDisplay = ""
        self.attribute1Display = ""
        self.attribute2Display = ""
        self.attribute3Display = ""


        # Determine Race and Extract Racial Traits
        if (race == "Any"):
            self.race = self.generateRace()
        else:
            self.race = race

        raceTraits = []

        for raceTraitOption in self.options:
            if (self.race == raceTraitOption[0]):
                raceTraits = raceTraitOption
                break

        if (raceTraits.count == 0):
            errorMessage = "Somehow you have selected a race option that doesn't exist, or I am a bad programmer."
            messagebox.showerror("NPC Generation Error", errorMessage)
            sys.exit(errorMessage)

        
        # Determine Life Stage and Age
        raceLifeStages = [  ("Child",raceTraits[2]),
                            ("Adolescent",raceTraits[3]),
                            ("Young Adult",raceTraits[4]),
                            ("Adult",raceTraits[5]),
                            ("Elder",raceTraits[6]),
                            ("Max",raceTraits[7])   ] # Maximum age possible, not its own lifeStage

        if (lifeStage == "Any"): # Child, Teenager, Young Adult, Adult, Elder
            self.lifeStage = self.generateLifeStage()
        else:
            self.lifeStage = lifeStage

        self.age = str(self.getAge(raceLifeStages, self.lifeStage))


        # Determine Occupation
        if (profession != "Any"):
            if (self.lifeStage != "Child" or (lifeStage != "Any" and self.lifeStage == "Child")):
                self.occupation = (industry, profession)
        else:
            if (self.lifeStage == "Child"):
                self.occupation = ("","None")
            # Introduce a chance for an Adolescent to have a job
            elif (self.lifeStage != "Adolescent" or (self.lifeStage == "Adolescent" and random.randint(1,100) < 50)):
                if (industry == "Any"):
                    self.industry = self.generateIndustry()
                self.occupation = self.generateOccupation(self.industry)
            else:
                self.occupation = ("","None")

            # Chance for Elder to have Retired qualifier
            if (lifeStage == "Elder" and random.randint(1,100) < 25):
                self.occupation = (self.industry, "Retired " + str(self.occupation[1]))
        

        # Determine Gender
        if (self.gender != "Any"):
            self.gender = gender
            self.genderCode = gender[0:1]
        else:
            self.generateGender()


        # Determine Physical Characteristics
        self.eyeColor = self.generateRandomTraitPipeDelimited(raceTraits[10])

        self.skinLabel = raceTraits[11] + " Color: "
        self.skinColor = self.generateRandomTraitPipeDelimited(raceTraits[12])

        self.height = self.generateHeight(raceTraits[19], raceTraits[20], self.genderCode, self.lifeStage)
        self.bodyType = random.choice(["Thin","Lean","Lanky","Slender","Petite","Athletic","Muscular","Heavy","Portly","Plump","Chubby","Big-Boned","Beefy","Well-Built"])
        #TODO: Implement loading body types from file

        if (raceTraits[13] != ""):
            self.att1Label = raceTraits[13] + ": "
            self.att1Property = self.generateRandomTraitPipeDelimited(raceTraits[14])
        else: 
            self.att1Label = ""
            self.att1Property = ""

        if (raceTraits[15] != ""):
            self.att2Label = raceTraits[15] + ": "
            self.att2Property = self.generateRandomTraitPipeDelimited(raceTraits[16])
        else: 
            self.att2Label = ""
            self.att2Property = ""

        if (raceTraits[17] != ""):
            self.att3Label = raceTraits[17] + ": "
            self.att3Property = self.generateRandomTraitPipeDelimited(raceTraits[18])
        else:  
            self.att3Label = ""
            self.att3Property = ""


        # Get Random Name
        if (culture == "Traditional"):
            self.name = self.getNameByRaceTradition(raceTraits[8],raceTraits[9],self.genderCode)
        elif (culture == "Common"):
            self.name = self.getCommonName(self.genderCode)
        else:
            self.name = self.getTrueRandomName(self.genderCode)


        self.buildDisplayText()
    




    # Helper Methods #

    def generateRandomTraitPipeDelimited(self,traitString):
        traits = traitString.split("|")
        return random.choice(traits)

    def generateIndustry(self):
        occupations = []
        occupationsInDir =  os.listdir("resources\\occupations")
        for occupation in occupationsInDir:
            occupations.append(str.removesuffix(occupation,".csv"))
        return random.choice(occupations)

    def generateOccupation(self,industry):
        file = open("resources\\occupations\\"+industry+".csv")
        reader = csv.reader(file)

        professions = []
        for profession in reader:
            professions.append(profession[0])

        file.close()
        return (industry,random.choice(professions))

    def generateRace(self):
        race = random.choice(self.options)
        return race[0]
        #TODO: Implement weighted selection

    def generateGender(self):
        self.gender = random.choice(["Male","Female"])
        self.genderCode = self.gender[0:1]
        #TODO: Load from CSV to allow user to configure custom genders

    def generateLifeStage(self):
        return random.choice(["Child","Adolescent","Young Adult","Adult","Elder"]) 
        #TODO: Implement loading life stage choices

    def generateHeight(self, min, max, gender, lifeStage):
        lowRange = int(min)
        upRange = int(max) + 1

        height = random.randrange(lowRange, upRange)
        randomDeviationValue = random.uniform(0,0.1)
        randomDeviation = int(height*randomDeviationValue)

        if (gender == "M"):
            height = height + randomDeviation
        if (gender == "F"):
            height = height - randomDeviation

        if (lifeStage == "Child"):
            height = height - (height/3)
        
        if (lifeStage == "Adolescent"):
            height = height - (height/5) 

        return self.getHeightString(height)
    
    def getHeightString(self, heightInInches):
        feet = math.trunc(heightInInches / 12)
        inches = int(heightInInches % 12)
        return str(feet) + "'" + str(inches) + "\""

    def getAge(self, raceStages, lifeStage):
        
        lowRange = 0
        upRange = 0

        for index, stage in enumerate(raceStages):
            if (lifeStage == stage[0] and len(raceStages) != index-1):
                lowRange = int(stage[1])
                upRange = int(raceStages[index+1][1])

        if (lowRange == 0 or upRange == 0):
            errorMessage = "Something went wrong determining the age range for a " + lifeStage + " " + self.race + "."
            messagebox.showerror("NPC Generation Error", errorMessage)
            sys.exit(errorMessage)

        return random.randrange(lowRange,upRange)
        #TODO: Need a better way to implement this in general

    def getNameByRaceTradition(self, fnTradition, sTradition, gender):

        if (gender != "M" and gender != "F"):
            gender = "U"

        firstNamesFile = open(self.namesFilePath + fnTradition + " First Names.csv")
        surnamesFile = open(self.namesFilePath + sTradition + " Surnames.csv")

        reader = csv.reader(firstNamesFile)

        firstNames = []
        for name in reader:
            if (gender == "U" or (name[1] == gender or name[1] == "U")):
                firstNames.append(name[0])

        firstNamesFile.close()

        reader = csv.reader(surnamesFile)

        surnames = []
        for surname in reader:
            surnames.append(surname[0])

        surnamesFile.close()

        return (random.choice(firstNames), random.choice(surnames))

    def getCommonName(self, gender):
        return self.getNameByRaceTradition("Common","Common", gender)

    def getTrueRandomName(self, gender):
        fnTrads = ["Common","Draconic","Dwarvish","Elvish","Halfling","Orcish"]
        sTrads = ["Common","Draconic","Dwarvish","Elvish","Halfling"]
        return self.getNameByRaceTradition(random.choice(fnTrads), random.choice(sTrads), gender)

    def buildDisplayText(self):
        self.nameDisplay = self.name[0] + " " + self.name[1]
        self.occupationDisplay = self.occupationDisplay + str(self.occupation[1])
        self.raceDisplay = self.raceDisplay + self.race
        self.ageDisplay = self.ageDisplay + self.age + " (" + self.lifeStage + ")"
        self.genderDisplay = self.genderDisplay + self.gender
        self.heightDisplay = self.heightDisplay + self.height
        self.bodyTypeDisplay = self.bodyTypeDisplay + self.bodyType
        self.eyeColorDisplay = self.eyeColorDisplay + self.eyeColor
        self.skinDisplay = self.skinLabel + self.skinColor
        self.attribute1Display = self.att1Label + self.att1Property
        self.attribute2Display = self.att2Label + self.att2Property
        self.attribute3Display = self.att3Label + self.att3Property

        self.npcDisplayText.append(self.nameDisplay)
        self.npcDisplayText.append(self.occupationDisplay)
        self.npcDisplayText.append(self.raceDisplay)
        self.npcDisplayText.append(self.ageDisplay)
        self.npcDisplayText.append(self.genderDisplay)
        self.npcDisplayText.append(self.heightDisplay)
        self.npcDisplayText.append(self.bodyTypeDisplay)
        self.npcDisplayText.append(self.eyeColorDisplay)
        self.npcDisplayText.append(self.skinDisplay)
        self.npcDisplayText.append(self.attribute1Display)
        self.npcDisplayText.append(self.attribute2Display)
        self.npcDisplayText.append(self.attribute3Display)