from tkinter import *
from NPC import NPC

class BetterNPCGenerator():

    def __init__(self):
        self.root = Tk()

        # Set up 3 Column structure
        selectPreset = LabelFrame(self.root, text='Select Preset')
        leftColumn = selectPreset
        leftColumn.grid(row=0, column=0, rowspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='NWES') 

        Label(selectPreset, text='Generic NPC').grid(row=0,column=0)

        options = LabelFrame(self.root, text='Options')
        middleColumn = options
        middleColumn.grid(row=0, column=1, rowspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='NWES') 

        optionsInstructions = Label(options, text='Choose the options')
        optionsInstructions.grid(row=0,column=1)
        # Race
        # Gender
        # Life Stage
        # Culture
        generateNPCButton = Button(options, text='Generate NPC',command=self.generateNPC)
        generateNPCButton.grid(row=1,column=1)

        npcFrame = LabelFrame(self.root, text='NPC')
        rightColumnTop = npcFrame
        rightColumnTop.grid(row=0,column=2,sticky='NWES') 

        self.nameLabel = Label(npcFrame, text='Click "Generate NPC"',font='Arial 18 bold')
        self.nameLabel.grid(row=0,column=2)
        self.raceLabel = Label(npcFrame, text="Race: ")
        self.raceLabel.grid(row=1,column=2)
        self.ageLabel = Label(npcFrame, text="Age: ")
        self.ageLabel.grid(row=2,column=2)
        self.genderLabel = Label(npcFrame, text="Gender: ")
        self.genderLabel.grid(row=3,column=2)

        Button(npcFrame, text='Export NPC').grid(row=4,column=2)

        npcHistory = LabelFrame(self.root, text='History')
        rightColumnBottom = npcHistory
        rightColumnBottom.grid(row=2,column=2,sticky='NWES') 

        testList = ('NPC1', 'NPC2', 'NPC3', 'NPC4', 'NPC5')

        Label(npcHistory, text='Last 5 NPCs Generated').grid(row=4,column=2)
        Listbox(npcHistory,listvariable=testList).grid(row=5,column=2)

        self.root.mainloop()

    def generateNPC(self):
        # Figure out how to clear the existing content in the frame
        npc = NPC("Any","Any","Any","Any")

        self.nameLabel.configure(text=npc.name[0] + " " + npc.name[1])
        self.raceLabel.configure(text="Race: " + npc.race)
        self.ageLabel.configure(text="Age: " + npc.age)
        self.genderLabel.configure(text="Gender: " + npc.gender)

        #updateNPCHistory(npc)

    def updateNPCHistory(npc):
        # Update the NPC History
        return None

app = BetterNPCGenerator()