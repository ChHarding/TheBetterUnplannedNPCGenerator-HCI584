import os
import csv

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

from NPC import NPC

class BetterNPCGenerator():

    presetsFilePath = "resources\\presets\\"
    occupationTypesFilePath = "resources\\occupations"
    namesFilePath = "resources\\names"

    leftStartColumn = 0
    middleStartColumn = 1
    rightStartColumn = 4



    def __init__(self):
        self.root = Tk()
        self.root.title("The Better Unplanned NPC Generator")

        defaultOptionsFileName = "Default.csv"
        self.raceTraitsOptions = self.loadOptionsFromCsv(self.presetsFilePath + defaultOptionsFileName, TRUE)
        self.raceTraitsOptions.sort()

        self.npcHistoryList = []
    
        # Primary Colors
        inkBlack = "#27221f"
        veryLightParchment = "#fefdfb"
        lightParchment = "#f5f0e5"
        parchment = "#f0e6d1"
        darkParchment = "#efdfbb"

        # Accent Colors
        lycheeRed = "#bb2f43"
        ashGray = "#6f7678"

        # Assigned Colors
        self.defaultTextColor = inkBlack
        self.defaultBackgroundColor = lightParchment

        self.buttonColor = lycheeRed
        self.buttonTextColor = veryLightParchment

        self.presetButtonColor = darkParchment
        self.presetButtonTextColor = inkBlack
        self.presetButtonSelectedColor = veryLightParchment
        self.presetButtonHoverColor = parchment

        self.dropDownColor = darkParchment
        self.dropDownHoverColor = parchment
        self.dropDownTextColor = inkBlack
        self.dropDownExpandedHoverColor = ashGray
        self.dropDownExpandedHoverTextColor = veryLightParchment

        self.npcNameColor = lycheeRed

        self.npcHistoryColor = veryLightParchment
        self.npcHistorySelectColor = ashGray
        self.npcHistorySelectTextColor = veryLightParchment

        #########
        # Fonts #
        #########

        self.headerFont = font.Font(family="Century Schoolbook", size=10, weight="bold")
        self.buttonFont = font.Font(family="Century Schoolbook", size=10, weight="bold")

        self.generateButtonFont = font.Font(family="Century Schoolbook", size=12, weight="bold")

        self.presetsFont = font.Font(family="Century Gothic",size=11)

        self.optionsLabelFont = font.Font(family="Century Schoolbook", size=10, weight="bold")
        self.optionsMenuFont = font.Font(family="Century Gothic", size=9, weight="bold")
        self.optionsTextFont = font.Font(family="Century Gothic", size=11)
        
        self.npcNameFont = font.Font(family="Century Schoolbook", size=15, weight="bold")
        self.npcDisplayFont = font.Font(family="Century Gothic", size=9)

        self.historyTextFont = font.Font(family="Century Gothic", size=9)

        self.root.configure(bg=self.defaultBackgroundColor)

        # ==================== #
        # Left Column: Presets #
        # ==================== #

        # Set up 3 Column structure
        self.selectPreset = LabelFrame(self.root, text="Presets", font=self.headerFont,background=self.defaultBackgroundColor, foreground=self.defaultTextColor)
        leftColumn = self.selectPreset
        leftColumn.grid(row=0, column=self.leftStartColumn, rowspan=50, padx=5, pady=5, ipady=5, sticky='NWES') 


        presets = os.listdir(self.presetsFilePath)
        presets.sort()
        presets.remove(defaultOptionsFileName)
        presets.insert(0,defaultOptionsFileName)
        self.selectedPreset = StringVar()
        self.buildPresetsMenu(presets, defaultOptionsFileName)

        # On Click of another preset in list: reload options
        # File name will be [ OptionName + ".csv" ] in resources>presets



        # ====================== #
        # Middle Column: Options #
        # ====================== #

        self.optionsRowCounter = 0

        self.options = LabelFrame(self.root, text="Options", font=self.headerFont,background=self.defaultBackgroundColor, foreground=self.defaultTextColor)
        middleColumn = self.options
        middleColumn.grid(row=0, column=self.middleStartColumn, rowspan=50, columnspan=3, padx=5, pady=5, sticky="NWES") 

        optionsInstructions = Label(self.options, text='Choose your options, then click "Generate NPC"', font=self.optionsTextFont, background=self.defaultBackgroundColor, foreground=self.defaultTextColor)
        optionsInstructions.grid(row=self.optionsRowCounter,column=self.middleStartColumn,columnspan=3, pady=(10,5))

        self.optionsRowCounter += 1

        # Race
        self.raceOptions = ["Any"]
        self.raceWeights = []
        for race in self.raceTraitsOptions:
            self.raceOptions.append(race[0])
            weight = 0
            try:
                weight = float(race[1])
            except:
                weight = ""
            self.raceWeights.append(weight)
        

        self.raceChoice = StringVar()
        self.raceChoice.set("Any")

        self.raceDropDown = self.configureOptionsDropDownMenu("Race", self.raceChoice, self.raceOptions)

        # Gender
        self.genderOptions = ["Any","Male","Female","Nonbinary"]
        #TODO: Load from CSV to allow user to configure custom genders
        self.genderChoice = StringVar()
        self.genderChoice.set("Any")

        self.genderDropDown = self.configureOptionsDropDownMenu("Gender", self.genderChoice, self.genderOptions)

        # Life Stage 
        self.lifeStageOptions = ["Any","Child","Adolescent","Young Adult","Adult","Elder"] 
        #TODO: Load from the preset header label
        self.lifeStageChoice = StringVar()
        self.lifeStageChoice.set("Any")

        self.lifeStageDropDown = self.configureOptionsDropDownMenu("Life Stage", self.lifeStageChoice, self.lifeStageOptions)


        # Occupation
        occupations =  os.listdir(self.occupationTypesFilePath)
        self.occupationTypeOptions = ["Any"]
        for occupation in occupations:
            self.occupationTypeOptions.append(str.removesuffix(occupation,".csv"))
        self.occupationTypeChoice = StringVar()
        self.occupationTypeChoice.set("Any")

        self.occupationTypeDropDown = self.configureOptionsDropDownMenu("Occupation Type", self.occupationTypeChoice, self.occupationTypeOptions, self.updateProfessions)

        # Profession
        self.professionTypeOptions = ["Any"]
        self.professionTypeChoice = StringVar()
        self.professionTypeChoice.set("Any")

        self.professionTypeDropDown = self.configureOptionsDropDownMenu("Profession", self.professionTypeChoice, self.professionTypeOptions)
        self.professionTypeDropDown.configure(state=DISABLED)


        # Culture
        self.cultureChoice = StringVar()
        self.cultureChoice.set("Any")

        self.configureOptionsLabel("Name Culture",padding=(5,(5,0),2,2))
        self.optionsRowCounter += 1

        self.cultureChoicesFrame = Frame(self.options)
        self.cultureChoicesFrame.grid(row=self.optionsRowCounter,column=self.middleStartColumn,columnspan=3)
        self.configureRadioOptions(self.cultureChoicesFrame, self.cultureChoice, ["Any","Common","Traditional"])
        self.optionsRowCounter += 1


        # Buttons
        generateNPCButton = Button(self.options, text='Generate NPC',command=self.generateNPC,width=15,font=self.generateButtonFont, background=self.buttonColor, foreground=self.buttonTextColor)
        generateNPCButton.grid(row=self.optionsRowCounter,column=self.middleStartColumn,columnspan=3, padx=5, pady=5, ipadx=5, ipady=5)



        # ========================= #
        # Right Column: NPC Display #
        # ========================= #

        self.npcDisplayRowCount = 0

        self.npcFrame = LabelFrame(self.root, text='NPC', font=self.headerFont, background=self.defaultBackgroundColor, foreground=self.defaultTextColor)
        rightColumnTop = self.npcFrame
        rightColumnTop.grid(row=self.npcDisplayRowCount,column=self.rightStartColumn, sticky='NWES', padx=5, pady=5) 

        self.nameLabel = self.configureNPCDisplayField()
        self.nameLabel.configure(text='Click "Generate NPC"')
        self.nameLabel.configure(foreground=self.npcNameColor)
        self.nameLabel.configure(font=self.npcNameFont)

        self.occupationLabel = self.configureNPCDisplayField()
        self.raceLabel = self.configureNPCDisplayField()
        self.ageLabel = self.configureNPCDisplayField()
        self.genderLabel = self.configureNPCDisplayField()
        self.heightLabel = self.configureNPCDisplayField()
        self.bodyTypeLabel = self.configureNPCDisplayField()
        self.eyeColorLabel = self.configureNPCDisplayField()
        self.skinLabel = self.configureNPCDisplayField()
        self.attribute1Label = self.configureNPCDisplayField()
        self.attribute2Label = self.configureNPCDisplayField()
        self.attribute3Label = self.configureNPCDisplayField()

        exportNPCButton = Button(self.npcFrame, text='Export to File', command=self.saveNPC, width=15, font=self.buttonFont, background=self.buttonColor, foreground=self.buttonTextColor)
        exportNPCButton.grid(row=self.npcDisplayRowCount,column=self.rightStartColumn,padx=5, pady=5, ipadx=5, ipady=5)

        copyNPCButton = Button(self.npcFrame, text='Copy to Clipboard', command=self.copyNPC, width=15, font=self.buttonFont, background=self.buttonColor, foreground=self.buttonTextColor)
        copyNPCButton.grid(row=self.npcDisplayRowCount,column=self.rightStartColumn+1, padx=(0,5), pady=5, ipadx=5, ipady=5)


        # NPC History Panel
        npcHistory = LabelFrame(self.root, text='History', font=self.headerFont, background=self.defaultBackgroundColor, foreground=self.defaultTextColor)
        rightColumnBottom = npcHistory
        rightColumnBottom.grid(row=2,column=self.rightStartColumn,sticky='NWES', padx=5, pady=5) 

        Label(npcHistory, text='Last 10 NPCs Generated', font=self.historyTextFont, background=self.defaultBackgroundColor).grid(row=4,column=self.rightStartColumn,pady=(5,0))
        self.npcHistoryBox = Listbox(npcHistory,activestyle="none",font=('Courier New',10),width=38,height=10,borderwidth=0,background=self.npcHistoryColor,foreground=self.defaultTextColor,selectbackground=self.npcHistorySelectColor,selectforeground=self.npcHistorySelectTextColor)
        self.npcHistoryBox.grid(column=self.rightStartColumn, columnspan=3,sticky="ew", pady=5, padx=5, ipadx=5, ipady=5)
        self.npcHistoryBox.bind("<<ListboxSelect>>", self.recallNPC)

        self.root.mainloop()




     # Helper Methods #   

    def configureOptionsLabel(self, labelText, padding=(5,5,2,2)):
        label = Label(self.options, text=labelText, justify="left", anchor="w", font=self.optionsLabelFont, background=self.defaultBackgroundColor, foreground=self.defaultTextColor)
        label.grid(row=self.optionsRowCounter, column=self.middleStartColumn, sticky="w", padx=padding[0], pady=padding[1], ipadx=padding[2], ipady=padding[3])

    def configureOptionsDropDownMenu(self, labelText, variable, menuOptions, command=""):
        self.configureOptionsLabel(labelText)
        menu = OptionMenu(self.options, variable, *menuOptions, command=command)
        menu.configure(font=self.optionsMenuFont)
        menu.configure(width=30)
        menu.configure(background=self.dropDownColor)
        menu.configure(foreground=self.dropDownTextColor)
        menu.configure(borderwidth=0)
        menu.configure(activebackground=self.dropDownHoverColor)
        ddMenu = self.root.nametowidget(menu.menuname)
        ddMenu.config(font=self.optionsMenuFont)
        ddMenu.config(background=self.dropDownHoverColor)
        ddMenu.config(activebackground=self.dropDownExpandedHoverColor)
        menu.grid(row=self.optionsRowCounter, column=self.middleStartColumn+1, columnspan=2, sticky="ew", padx=5, pady=5, ipadx=2, ipady=2)
        self.optionsRowCounter += 1
        return menu

    def configureRadioOption(self, radioFrame, text, variable, value):
        radio = Radiobutton(radioFrame, text=text, variable=variable, value=value, font=self.optionsTextFont, background=self.defaultBackgroundColor)
        radio.pack(side="left",anchor="w")

    def configureRadioOptions(self, frame, variable, options):
        if (options[0] is tuple):
            for option in options:
                self.configureRadioOption(frame, option[0], variable, option[1])
        else:
            for option in options:
                self.configureRadioOption(frame, option, variable, option)

    def configureNPCDisplayField(self):
        label = Label(self.npcFrame, background=self.defaultBackgroundColor, font=self.npcDisplayFont, foreground=self.defaultTextColor)
        label.grid(row=self.npcDisplayRowCount,column=self.rightStartColumn,columnspan=2)
        self.npcDisplayRowCount += 1
        return label

    def buildPresetsMenu(self, values, select):
        for item in self.selectPreset.winfo_children():
            item.destroy()
        displayRow = 0
        for text in values:
            radio = Radiobutton(self.selectPreset, text = str.removesuffix(text,".csv"), variable = self.selectedPreset,
                value = text, indicator = 0,
                background = self.presetButtonColor,
                foreground = self.presetButtonTextColor,
                activebackground = self.presetButtonSelectedColor,
                borderwidth=0,
                relief=FLAT,
                font=self.presetsFont)
            radio.grid(row=displayRow,column=self.leftStartColumn,sticky="ew", padx=5, pady=2, ipadx=7, ipady=2)
            radio.configure(command=lambda: self.refreshOptions(self.selectedPreset.get()))
            displayRow += 1
        self.selectedPreset.set(select)

    def loadOptionsFromCsv(self, filePath, skipHeader=FALSE):
        
        file = open(filePath)
        reader = csv.reader(file)

        if (skipHeader):
            next(reader)

        items = []
        for item in reader:
            items.append(item)

        items.sort()

        file.close()

        return items


    def updateProfessions(self, selection):
        if (selection != "Any"):
            self.professionTypeOptions = self.loadOptionsFromCsv(self.occupationTypesFilePath + "\\" + selection + ".csv")
            self.updateOptionsMenu(self.professionTypeDropDown, self.professionTypeChoice, self.professionTypeOptions)            
            self.professionTypeDropDown.configure(state=ACTIVE)
        else:
            self.professionTypeDropDown.configure(state=DISABLED)
        self.professionTypeChoice.set("Any")

    def updateOptionsMenu(self, optionMenu, variable, newOptions):
        menu = optionMenu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="Any", 
                             command=lambda value="Any": variable.set(value))
        for string in newOptions:
            menu.add_command(label=string[0], 
                             command=lambda value=string[0]: variable.set(value))

    def generateNPC(self):

        npc = NPC(  self.raceTraitsOptions,
                    self.raceChoice.get(),
                    self.raceWeights,
                    self.genderChoice.get(),
                    self.lifeStageChoice.get(),
                    self.occupationTypeChoice.get(),
                    self.professionTypeChoice.get(),
                    self.cultureChoice.get()    )

        self.updateNPCUI(npc)

    def updateNPCUI(self, npc):

        self.currentNPC = npc

        self.nameLabel.configure(text=npc.nameDisplay)
        self.occupationLabel.configure(text=npc.occupationDisplay)
        self.raceLabel.configure(text=npc.raceDisplay)
        self.ageLabel.configure(text=npc.ageDisplay)
        self.genderLabel.configure(text=npc.genderDisplay)
        self.heightLabel.configure(text=npc.heightDisplay)
        self.bodyTypeLabel.configure(text=npc.bodyTypeDisplay)
        self.eyeColorLabel.configure(text=npc.eyeColorDisplay)
        self.skinLabel.configure(text=npc.skinDisplay)
        self.attribute1Label.configure(text=npc.attribute1Display)
        self.attribute2Label.configure(text=npc.attribute2Display)
        self.attribute3Label.configure(text=npc.attribute3Display)

        self.updateNPCHistory(npc)

    def updateNPCHistory(self, npc):
        if (npc not in self.npcHistoryList):
            if (len(self.npcHistoryList) >= 10):
                self.npcHistoryList.pop()
        else:
            self.npcHistoryList.remove(npc)

        self.npcHistoryList.insert(0,npc)

        # Clear and repopulate box
        self.npcHistoryBox.delete(0,END)
        for x, n in enumerate(self.npcHistoryList):
            name = " " + n.nameDisplay[0:20] + self.spacer(n.nameDisplay, 20) + " | " + n.race + " " + n.gender
            self.npcHistoryBox.insert(x, name)
        self.npcHistoryBox.select_set(0)

    def recallNPC(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            npc = self.npcHistoryList[index]
            self.updateNPCUI(npc)
        self.npcHistoryBox.select_set(0)

    def saveNPC(self):
        npc = self.getCurrentNPC()
        if (npc == NONE):
            return

        file = filedialog.asksaveasfilename(filetypes=[("txt file", ".txt")],defaultextension=".txt", initialfile=npc.nameDisplay)
        if file:
            fob = open(file, 'w')
            for line in npc.npcDisplayText:
                fob.write(line + '\n')
            fob.close()

    def copyNPC(self):
        npc = self.getCurrentNPC()
        if (npc == NONE):
            return

        self.root.clipboard_clear
        for line in npc.npcDisplayText:
            self.root.clipboard_append(line + "\n")
        
        messagebox.showinfo("NPC Copied", npc.nameDisplay + " has been copied to the clipboard.")


    def getCurrentNPC(self):
        if (len(self.npcHistoryList) == 0):
            errorMessage = "No NPCs currently loaded."
            messagebox.showerror("NPC Save Error", errorMessage)
            return NONE
        else:
            return self.npcHistoryList[0]
    
    

            
    
    def refreshOptions(self, presetName):
        self.raceTraitsOptions = self.loadOptionsFromCsv(self.presetsFilePath + presetName, TRUE)
        self.raceTraitsOptions.sort()

        self.raceOptions.clear()
        self.raceWeights.clear()

        for race in self.raceTraitsOptions:
            self.raceOptions.append(race)
            self.raceWeights.append(float(race[1]))

        self.updateOptionsMenu(self.raceDropDown, self.raceChoice, self.raceOptions)


    def spacer(self, text, width):
        spaces = ""
        num = width - len(text)

        for _ in range(num):
            spaces = spaces + " "

        return spaces

