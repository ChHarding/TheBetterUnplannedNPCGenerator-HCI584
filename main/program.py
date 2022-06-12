from tkinter import *

win = Tk()
#Set the geometry of frame
#win.geometry("600x400")

#Maximize the window using state property
#win.state('zoomed')

# Set up 3 Column structure
selectPreset = LabelFrame(win, text='Select Preset')
leftColumn = selectPreset
leftColumn.grid(row=0, column=0, rowspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='NWES') 

Label(selectPreset, text='Generic NPC').grid(row=0,column=0)

options = LabelFrame(win, text='Options')
middleColumn = options
middleColumn.grid(row=0, column=1, rowspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='NWES') 

Label(options, text='Choose the options').grid(row=0,column=1)
Button(options, text='Generate NPC').grid(row=1,column=1)

npc = LabelFrame(win, text='NPC')
rightColumnTop = npc
rightColumnTop.grid(row=0,column=2,sticky='NWES') 

Label(npc, text='Your Generated NPC').grid(row=0,column=2)
name = Label(npc, text="Randy Randington",font='Arial 18 bold').grid(row=1,column=2)
race = Label(npc, text="Race: Human").grid(row=2,column=2)
age = Label(npc, text="Age: 28").grid(row=3,column=2)
gender = Label(npc, text="Gender: Male").grid(row=4,column=2)

#Button(npc, text='Export NPC').grid(row=1,column=2)

npcHistory = LabelFrame(win, text='History')
rightColumnBottom = npcHistory
rightColumnBottom.grid(row=2,column=2,sticky='NWES') 

testList = ('NPC1', 'NPC2', 'NPC3', 'NPC4', 'NPC5')

Label(npcHistory, text='Last 5 NPCs Generated').grid(row=3,column=2)
Listbox(npcHistory,listvariable=testList,).grid(row=4,column=2)

win.mainloop()