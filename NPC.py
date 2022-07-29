import csv
import math
import os
import os.path
import random
import sys

from tkinter import messagebox


class NPC:
    
    namesFilePath = "generation-criteria\\names\\"

    def __init__(self, options, race, raceWeights, gender, lifeStage, industry, profession, culture):
        
        self.options = options
        # TODO: Make each option an object with easily referenceable variables
        # Currently large maintenance problem with relying on index numbers to get the right values
        # May also change the main Races file into a JSON file instead to simplify it further

        self.raceWeights = raceWeights
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
        raceLifeStages = [  ("Child",raceTraits[1]),
                            ("Adolescent",raceTraits[2]),
                            ("Young Adult",raceTraits[3]),
                            ("Adult",raceTraits[4]),
                            ("Elder",raceTraits[5]),
                            ("Max",raceTraits[6])   ] # Maximum age possible, not its own lifeStage

        if (lifeStage == "Any"): # Child, Teenager, Young Adult, Adult, Elder
            self.lifeStage = self.generateLifeStage()
        else:
            self.lifeStage = lifeStage

        self.age = str(self.getAge(raceLifeStages, self.lifeStage))


        # Determine Occupation

        # If industry and profession were both set manually
        if (profession != "Any"):
            # If generated life stage is not Child, or it was manually set to Child
            # Assign the chosen occupation
            if (self.lifeStage != "Child" or (lifeStage != "Any" and self.lifeStage == "Child")):
                self.occupation = (industry, profession)
        else:
            if (self.lifeStage == "Child"):
                self.occupation = ("","None")
            # Chance for an Adolescent to have a job
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
        self.eyeColor = self.generateRandomTraitPipeDelimited(raceTraits[9])

        self.skinLabel = raceTraits[10] + " Color: "
        self.skinColor = self.generateRandomTraitPipeDelimited(raceTraits[11])

        self.height = self.generateHeight(raceTraits[18], raceTraits[19], self.genderCode, self.lifeStage)
        self.bodyType = random.choice(["Thin","Lean","Lanky","Slender","Petite","Athletic","Muscular","Heavy","Portly","Plump","Chubby","Big-Boned","Beefy","Well-Built"])
        #TODO: Implement loading body types from file

        if (raceTraits[12] != ""):
            self.att1Label = raceTraits[12] + ": "
            self.att1Property = self.generateRandomTraitPipeDelimited(raceTraits[13])
        else: 
            self.att1Label = ""
            self.att1Property = ""

        if (raceTraits[14] != ""):
            self.att2Label = raceTraits[14] + ": "
            self.att2Property = self.generateRandomTraitPipeDelimited(raceTraits[15])
        else: 
            self.att2Label = ""
            self.att2Property = ""

        if (raceTraits[16] != ""):
            self.att3Label = raceTraits[16] + ": "
            self.att3Property = self.generateRandomTraitPipeDelimited(raceTraits[17])
        else:  
            self.att3Label = ""
            self.att3Property = ""


        # Get Random Name
        if (culture == "Traditional"):
            self.name = self.getNameByRaceTradition(raceTraits[7],raceTraits[8],self.genderCode)
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
        occupationsInDir =  os.listdir("generation-criteria\\occupations")
        for occupation in occupationsInDir:
            occupations.append(str.removesuffix(occupation,".csv"))
        return random.choice(occupations)

    def generateOccupation(self,industry):
        file = open("generation-criteria\\occupations\\"+industry+".csv")
        reader = csv.reader(file)

        professions = []
        for profession in reader:
            professions.append(profession[0])

        file.close()
        return (industry,random.choice(professions))

    def generateRace(self):
        if (self.raceWeights[0] == ""):
            randomRace = random.choice(self.options)
            return randomRace[0]
        else:
            randomRace = random.choices(self.options,self.raceWeights,k=1)
            return randomRace[0][0]
        #TODO: Implement weighted selection

    def generateGender(self):
        self.gender = random.choice(["Male","Female"])
        self.genderCode = self.gender[0:1]
        #TODO: Load from CSV to allow user to configure custom genders
        #TODO: Make the gender code its own column so custom genders can be coded masculine 
        #      or feminine, rather than all of them being considered unisex

    def generateLifeStage(self):
        return random.choice(["Child","Adolescent","Young Adult","Adult","Elder"]) 
        #TODO: Implement loading life stage choices from a file

    def getAge(self, raceStages, lifeStage):
        
        lowRange = 0
        upRange = 0

        # The next life stage above the chosen one determines the upper bound of the age range
        # Elder is a special case where the next stage up is defined as "Max Age", not its own life stage
        for index, stage in enumerate(raceStages):
            if (lifeStage == stage[0] and len(raceStages) != index-1):
                lowRange = int(stage[1])
                upRange = int(raceStages[index+1][1])

        if (lowRange == 0 or upRange == 0):
            errorMessage = "Something went wrong determining the age range for a " + lifeStage + " " + self.race + "."
            messagebox.showerror("NPC Generation Error", errorMessage)
            sys.exit(errorMessage)

        return random.randrange(lowRange,upRange)

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


    # Name Generation #
    def getNameByRaceTradition(self, fnTradition, sTradition, gender):

        if (gender != "M" and gender != "F"):
            gender = "U"

        if (os.path.exists(self.namesFilePath + fnTradition + " First Names.csv")):
            firstNamesFile = open(self.namesFilePath + fnTradition + " First Names.csv")
        else:
            print("The selected first name tradition does not have a corresponding file. Defaulting to Common.")
            firstNamesFile = open(self.namesFilePath + "Common" + " First Names.csv")

        if (os.path.exists(self.namesFilePath + sTradition + " Surnames.csv")):
            surnamesFile = open(self.namesFilePath + sTradition + " Surnames.csv")
        else:
            print("The selected surname tradition does not have a corresponding file. Defaulting to Common.")
            surnamesFile = open(self.namesFilePath + "Common" + " Surnames.csv")

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
        namesInDir =  os.listdir("generation-criteria\\names")

        fnTrads = []
        sTrads = []

        for nameFile in namesInDir:
            if ("First Names" in nameFile):
                fnTrads.append(nameFile.removesuffix(" First Names.csv"))
            elif ("Surnames" in nameFile):
                sTrads.append(nameFile.removesuffix(" Surnames.csv"))

        return self.getNameByRaceTradition(random.choice(fnTrads), random.choice(sTrads), gender)

    # Create a standard display text array out of generated values
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