import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from firebase import Firebase
import os
import os.path
from os import path
import json
import tkinter.ttk
from cryptography.fernet import Fernet
from functools import partial
from datetime import datetime
import csv
import traceback
from decouple import config
 
cols = []
for i in range(2):
    cols.append([])

checkVars = []
for i in range(10):
    checkVars.append([None]*80)

locationList = []

dayList = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

importedNames = []
importedLocations = []
importInProgress = False
messageboxChoices = {'option1': 'Names','option2': 'Locations'}

key = b'_oGu0-LyPqlvyff7uv6V-f9whXvz48MGNSEIdTuEFOw='
f = Fernet(key)
settingPath = os.path.join(os.environ['USERPROFILE'],'RBConfig')
settingsData = {}
user = NONE

settingsRunning = False
downloadsRunning = False

def openOrCreateSettingFile():
    global settingsData
    os.chdir(os.environ['USERPROFILE'])
    if path.exists(settingPath) == True:
        with open('RBConfig','rb') as file:
            encryptedData = file.read()
            decryptedData = f.decrypt(encryptedData)
            decodedData = decryptedData.decode()
            settingsData = eval(decodedData)
    else:
        data = str({'Username':'Empty','Password':'Empty','District':'Empty','Route':'Empty'})
        enc_data = data.encode()
        encryptedData = f.encrypt(enc_data)
        with open('RBConfig','wb') as file:
            file.write(encryptedData)

config = {
    'apiKey': config('apikey',default=''),
    'authDomain': config('authDomain',default=''),
    'databaseURL': config('databaseURL',default=''),
    'storageBucket': config('storageBucket',default='')
}

firebase = Firebase(config)
auth = firebase.auth()
db = firebase.database()

def firebasePull():
    try:
        rawLocationList = db.child(settingsData['District']).child(settingsData['Route']).child('Locations').get(user['idToken']).val().split(',')
        locationList = []
        for list in rawLocationList:
            subList = list.split('-')
            locationList.append([subList[0],subList[1]])
        for x in range(80): #Location1
            locationChoice1 = OptionMenu(frame,checkVars[0][x],*locationList)
            locationChoice1.grid(row=3,column=x,padx=2,sticky=EW)
        for x in range(80): #Location2
            locationChoice2 = OptionMenu(frame,checkVars[1][x],*locationList)
            locationChoice2.grid(row=4,column=x,padx=2,sticky=EW)
    except BaseException:
        print('Exception message starts here.')
        traceback.print_exc()
        print('Exception message stops here.')
        locationList = []
    pull = db.child(settingsData['District']).child(settingsData['Route']).child('Passenger Data').get(user['idToken']).val()
    if pull == None:
        messagebox.showerror('Sad Announcement','No data found.\n:(')
    else:
        midPull = pull.split('|')
        column0 = midPull[0].split(',')
        column1 = eval(midPull[1])
        column2 = eval(midPull[2])
        column3 = midPull[3].split(',')
        column4 = midPull[4].split(',')
        column5 = midPull[5].split(',')
        column6 = midPull[6].split(',')
        column7 = midPull[7].split(',')
        column8 = midPull[8].split(',')
        column9 = midPull[9].split(',')
        column10 = midPull[10].split(',')

        for x in range(80): # Display
            cols[0][x].delete(0.0,END)
            cols[0][x].insert(0.0,column0[x])
        for x in range(80): # Location 1
            checkVars[0][x].set(column1[x])
        for x in range(80): # Location 2
            checkVars[1][x].set(column2[x])
        for x in range(80): # Flag
            checkVars[2][x].set(int(column3[x]))
        for x in range(80): # Morning 1
            checkVars[3][x].set(int(column4[x]))
        for x in range(80): # Afternoon 1
            checkVars[4][x].set(int(column5[x]))
        for x in range(80): # Skip 1
            checkVars[5][x].set(int(column6[x]))
        for x in range(80): # Weekday
            if column7[x] == 'None':
                checkVars[6][x].set(column7[x])
            else:
                checkVars[6][x].set(dayList[int(column7[x])-1])
        for x in range(80): # Morning 2
            checkVars[7][x].set(int(column8[x]))
        for x in range(80): # Afternoon 2
            checkVars[8][x].set(int(column9[x]))
        for x in range(80): # Skip 2
            checkVars[9][x].set(int(column10[x]))

def nameTextClear(event):
    if event.widget.get("1.0",'end-1c') == 'Empty':
        event.widget.delete(0.0,END)

def nameTextReset(event):
    if len(event.widget.get("1.0",'end-1c')) < 1:
        event.widget.insert(0.0,'Empty')

def populate(frame):
    for x in range(80): #ColNumber
        colLabel = Label(frame,relief = SUNKEN,text=(x))
        colLabel.grid(row=1,column=x,sticky=NSEW)

    for x in range(80): #Name
        display = Text(frame,width=20,height=5)
        display.grid(row=2,column=x)
        cols[0].append(display)
        display.insert(END,'Empty')
        cols[0][x].bind("<FocusIn>",nameTextClear)
        cols[0][x].bind("<FocusOut>",nameTextReset)

    for x in range(80): #Location1
        checkVars[0][x] = StringVar()
        locationChoice1 = OptionMenu(frame,checkVars[0][x],*locationList)
        checkVars[0][x].set(None)
        locationChoice1.grid(row=3,column=x,padx=2,sticky=EW)

    for x in range(80): #Location2
        checkVars[1][x] = StringVar()
        locationChoice1 = OptionMenu(frame,checkVars[1][x],*locationList)
        checkVars[1][x].set(None)
        locationChoice1.grid(row=4,column=x,padx=2,sticky=EW)

    for x in range(80): #Flag
        checkVars[2][x] = IntVar()
        checkFlag = Checkbutton(frame,bg='#FF9AA2',width=18,text='Flag',var=checkVars[2][x],relief=GROOVE,anchor=W)
        checkFlag.grid(row=5,column=x)

    for x in range(80): #Condition1
        condition1 = Label(frame,relief=FLAT,background='#808080',text=('Condition 1'))
        condition1.grid(row=6,column=x,sticky=NSEW)

    for x in range(80): #CheckMorning
        checkVars[3][x] = IntVar()
        checkMorning = Checkbutton(frame,bg='#B5EAD7',width=18,text='Morning',var=checkVars[3][x],relief=GROOVE,anchor=W)
        checkMorning.grid(row=7,column=x)

    for x in range(80): #CheckAfternoon
        checkVars[4][x] = IntVar()
        checkMorning = Checkbutton(frame,bg='#FFDAC1',width=18,text='Afternoon',var=checkVars[4][x],relief=GROOVE,anchor=W)
        checkMorning.grid(row=8,column=x)

    for x in range(80): #CheckSkip
        checkVars[5][x] = IntVar()
        checkSkip = Checkbutton(frame,bg='#80CEE1',width=18,text='Skip',var=checkVars[5][x],relief=GROOVE,anchor=W)
        checkSkip.grid(row=9,column=x)

    for x in range(80): #Condition2
        condition2 = Label(frame,relief=FLAT,background='#808080',text=('Condition 2'))
        condition2.grid(row=10,column=x,sticky=NSEW)

    for x in range(80): #CheckDay
        checkVars[6][x] = StringVar()
        checkDay = OptionMenu(frame,checkVars[6][x],*dayList)
        checkVars[6][x].set(None)
        checkDay.grid(row=11,column=x,sticky='ew',padx=5)

    for x in range(80): #CheckMorning2
        checkVars[7][x] = IntVar()
        checkMorning2 = Checkbutton(frame,bg='#B5EAD7',width=18,text='Morning',var=checkVars[7][x],relief=GROOVE,anchor=W)
        checkMorning2.grid(row=12,column=x)

    for x in range(80): #CheckAfternoon2
        checkVars[8][x] = IntVar()
        checkAfternoon2 = Checkbutton(frame,bg='#FFDAC1',width=18,text='Afternoon',var=checkVars[8][x],relief=GROOVE,anchor=W)
        checkAfternoon2.grid(row=13,column=x)

    for x in range(80): #CheckSkip2
        checkVars[9][x] = IntVar()
        checkSkip2 = Checkbutton(frame,bg='#80CEE1',width=18,text='Skip',var=checkVars[9][x],relief=GROOVE,anchor=W)
        checkSkip2.grid(row=14,column=x)

def updatePush():
    displayContent = ''
    location1Content = []
    location2Content = []
    checkFlagContent = ''
    checkMorningContent = ''
    checkAfternoonContent = ''
    checkSkipContent = ''
    checkDayContent = ''
    checkMorning2Content = ''
    checkAfternoon2Content = ''
    checkSkip2Content = ''
    passengerToStop = [[None] for _ in range(80)]
    passengerToStopContent = ''

    for y in range(80):
        z = cols[0][y].get("1.0",'end-1c')
        if y == 0:
            displayContent += z
        else:
            displayContent += (',' + z)
    for y in range(80):
        z = checkVars[0][y].get()
        location1Content.append(z)
    for y in range(80):
        z = checkVars[1][y].get()
        location2Content.append(z)
    for y in range(80):
        z1 = location1Content[y]
        z2 = location2Content[y]
        if z1 != 'None':
            if passengerToStop[int(eval(z1)[0])][0] == None:
                passengerToStop[int(eval(z1)[0])][0] = y
            else:
                passengerToStop[int(eval(z1)[0])].append(y)
        if z2 != 'None':
            if passengerToStop[int(eval(z2)[0])][0] == None:
                passengerToStop[int(eval(z2)[0])][0] = y
            else:
                passengerToStop[int(eval(z2)[0])].append(y)
    for y in range(80):
        z = str(checkVars[2][y].get())
        if y == 0:
            checkFlagContent += z
        else:
            checkFlagContent += (','+z)
    for y in range(80):
        z = str(checkVars[3][y].get())
        if y == 0:
            checkMorningContent += z
        else:
            checkMorningContent += (','+z)
    for y in range(80):
        z = str(checkVars[4][y].get())
        if y == 0:
            checkAfternoonContent += z
        else:
            checkAfternoonContent += (','+z)
    for y in range(80):
        z = str(checkVars[5][y].get())
        if y == 0:
            checkSkipContent += z
        else:
            checkSkipContent += (','+z)
    for y in range(80):
        z = checkVars[6][y].get()
        if z != 'None':
            z = str(dayList.index(z) + 1)
        if y == 0:
            checkDayContent += z
        else:
            checkDayContent += (','+z)
    for y in range(80):
        z = str(checkVars[7][y].get())
        if y == 0:
            checkMorning2Content += z
        else:
            checkMorning2Content += (','+z)
    for y in range(80):
        z = str(checkVars[8][y].get())
        if y == 0:
            checkAfternoon2Content += z
        else:
            checkAfternoon2Content += (','+z)
    for y in range(80):
        z = str(checkVars[9][y].get())
        if y == 0:
            checkSkip2Content += z
        else:
            checkSkip2Content += (','+z)
    db.child(settingsData['District']).child(settingsData['Route']).child('Passenger Data').set(displayContent+\
        '|'+str(location1Content)+\
            '|'+str(location2Content)+\
                '|'+checkFlagContent+\
                    '|'+checkMorningContent+\
                        '|'+checkAfternoonContent+\
                            '|'+checkSkipContent+\
                                    '|'+checkDayContent+\
                                        '|'+checkMorning2Content+\
                                            '|'+checkAfternoon2Content+\
                                                '|'+checkSkip2Content,user['idToken'])

    for y in range(80):
        if y == 0:
            if passengerToStop[y] != [None]:
                if len(passengerToStop[y]) == 1:
                    passengerToStopContent += str(passengerToStop[y][0])
                else:
                    tempIndex = 0
                    for x in passengerToStop[y]:
                        if tempIndex != 0:
                            passengerToStopContent += '-'
                        passengerToStopContent += str(x)
                        tempIndex += 1
        else:
            if passengerToStop[y] == [None]:
                passengerToStopContent += ','
            else:
                if len(passengerToStop[y]) == 1:
                    passengerToStopContent += ','+str(passengerToStop[y][0])
                else:
                    tempIndex = 0
                    for x in passengerToStop[y]:
                        if tempIndex == 0:
                            passengerToStopContent += ','+str(x)
                            tempIndex += 1
                        else:
                            passengerToStopContent += '-'+str(x)
                            tempIndex += 1

    db.child(settingsData['District']).child(settingsData['Route']).child('Passengers per Stop').set(passengerToStopContent,user['idToken'])

def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def checkSettingsRunning():
    global settingsRunning
    if settingsRunning == True:
        pass
    else:
        settingsWindow()

def settingsWindow():
    global settingsRunning
    settingsRunning = True
    top = Toplevel()
    top.focus_force()
    top.title('Settings')
    top.geometry('+'+str(int((width/3)*2))+'+'+str(int(height/10)))
    routeVar = StringVar(top)
    try:
        routes = list(dict(db.child(settingsData['District']).get(user['idToken']).val()))
        routeVar.set(settingsData['Route'])
    except:
        routes = ['None Found']

    def exitNoSave():
        global settingsRunning
        settingsRunning = False
        checkLogin()
        top.destroy()

    top.protocol('WM_DELETE_WINDOW', exitNoSave)

    def saveSettings(username,password,district,route):
        global settingsRunning
        os.chdir(os.environ['USERPROFILE'])
        settingsData = {'Username':username,'Password':password,'District':district,'Route':route}
        enc_Data = str(settingsData).encode()
        encryptedData = f.encrypt(enc_Data)
        with open('RBConfig','wb') as file:
            file.write(encryptedData)
        settingsRunning = False
        checkLogin()
        top.destroy()

    def getEntries():
        global username
        global password
        global district
        global route
        username = usernameEntry.get()
        password = passwordEntry.get()
        district = districtEntry.get()
        route = routeVar.get()
        saveSettings(username,password,district,route)

    usernameLabel = Label(top,text=('Enter username below'))
    passwordLabel = Label(top,text=('Enter password below'))
    districtLabel = Label(top,text=('Enter district (path) below'))
    routeLabel = Label(top,text=('Enter route title (path) below'))
    usernameEntry = Entry(top)
    passwordEntry = Entry(top,show='*')
    districtEntry = Entry(top)
    routeEntry = OptionMenu(top,routeVar,*routes)

    save = Button(top,text='Save and close',command=getEntries)
    usernameLabel.grid(row=0)
    usernameEntry.grid(row=1,columnspan=2,sticky=EW,padx=5)
    passwordLabel.grid(row=2)
    passwordEntry.grid(row=3,columnspan=2,sticky=EW,padx=5)
    districtLabel.grid(row=5,column=0)
    districtEntry.grid(row=6,column=0)
    routeLabel.grid(row=5,column=1)
    routeEntry.grid(row=6,column=1)
    save.grid(row=7,column=2)
    username = ''
    password = ''
    district = ''
    route = ''

    usernameEntry.insert(0,settingsData['Username'])
    passwordEntry.insert(0,settingsData['Password'])
    districtEntry.insert(0,settingsData['District'])

    top.mainloop()

def checkDownloadsRunning():
    global downloadsRunning
    if downloadsRunning == True:
        pass
    else:
        downloadsWindow()

def downloadsWindow():
    global downloadsRunning
    downloadsRunning = True
    downloadPath = os.path.join(os.environ['USERPROFILE'], 'Desktop/')
    os.chdir(downloadPath)
    downloadTop = Toplevel()
    downloadTop.focus_force()
    downloadTop.title('Downloads')
    downloadTop.geometry('+'+str(int((width/3)*2))+'+'+str(int(height/10)))
    downloadFromPath = db.child(settingsData['District']).child(settingsData['Route']).child('Log Data')
    logListPull = []

    def populateLogs(downloadFrame):
        try:
            global logListPull
            rowPosition = 0
            logListPull = list(dict(downloadFromPath.get(user['idToken']).val()))
            for i in logListPull:
                currentRowPosition = rowPosition
                logSelect = Label(downloadFrame,text=(str(i)),pady=5)
                logDownload = Button(downloadFrame,text='↓',command=partial(downloadOne,currentRowPosition))
                logDelete = Button(downloadFrame,text='Delete',command=partial(deleteOne,currentRowPosition))
                logSelect.grid(row=rowPosition,column=0,ipadx=5)
                logDownload.grid(row=rowPosition,column=1,padx=10)
                logDelete.grid(row=rowPosition,column=2,padx=10)
                rowPosition += 1
            allDownload = Button(downloadFrame,text='Download All',font=('Helvetica','15'),bg='#B5EAD7',command=downloadAll)
            allDelete = Button(downloadFrame,text='Delete All',font=('Helvetica','15'),bg='#FF9AA2',command=deleteAll)
            allDownload.grid(row=rowPosition,column=0,columnspan=2)
            allDelete.grid(row=rowPosition,column=2)
        except BaseException :
            global downloadsRunning
            downloadsRunning = False
            traceback.print_exc()
            downloadTop.destroy()
            messagebox.showerror('Sad Announcement','No data found.\n:(')

    def downloadOne(position):
        global logListPull
        download = db.child(settingsData['District']).child(settingsData['Route']).child('Log Data').child(logListPull[position]).get(user['idToken']).val()
        with open('RB Log'+logListPull[position]+'.csv','w') as file:
            file.write(download)
    
    def deleteOne(position):
        db.child(settingsData['District']).child(settingsData['Route']).child('Log Data').child(logListPull[position]).remove(user['idToken'])
        downloadTop.destroy()
        downloadsWindow()

    def exitNoSave():
        global downloadsRunning
        downloadsRunning = False
        downloadTop.destroy()

    def downloadAll():
        foldername = 'RB Download '+(str(datetime.now().time())[:-7].replace(':','-'))
        os.mkdir(foldername)
        os.chdir(foldername)
        downloadIndex = 0
        for i in logListPull:
            download = db.child(settingsData['District']).child(settingsData['Route']).child('Log Data').child(logListPull[downloadIndex]).get(user['idToken']).val()
            with open('RB Log'+logListPull[downloadIndex]+'.csv','w') as file:
                file.write(download)
            downloadIndex += 1
        os.chdir(downloadPath)

    def deleteAll():
        global downloadsRunning
        deleteIndex = 0
        for i in logListPull:
            db.child(settingsData['District']).child(settingsData['Route']).child('Log Data').child(logListPull[deleteIndex]).remove(user['idToken'])
            deleteIndex += 1
        downloadsRunning = False
        downloadTop.destroy()

    downloadTop.protocol('WM_DELETE_WINDOW', exitNoSave)

    downloadCanvas = Canvas(downloadTop,width=(width/7),height=(height/2),bd=2,bg='#D3D3D3')
    downloadFrame = Frame(downloadTop)
    downloadScroll_y = Scrollbar(downloadTop,orient="vertical",width=25,command=(downloadCanvas.yview))
    downloadCanvas.create_window(0,0,anchor=NW,window=downloadFrame)
    downloadCanvas.configure(yscrollcommand=downloadScroll_y.set)

    downloadCanvas.grid(row=3,column=0,columnspan=5,sticky=EW)
    downloadScroll_y.grid(row=3,column=5,rowspan=5,sticky=NS,ipady=10)
    downloadFrame.bind("<Configure>",lambda event,canvas=downloadCanvas:onFrameConfigure(downloadCanvas))

    populateLogs(downloadFrame)
    downloadTop.mainloop()

def checkLogin():
    openOrCreateSettingFile()
    global user
    try:
        user = auth.sign_in_with_email_and_password(settingsData['Username'],settingsData['Password'])
        firebasePull()
    except BaseException:
        print('Exception message starts here.')
        traceback.print_exc()
        print('Exception message stops here.')
        messagebox.showerror('Connection to database failed!','Please go to settings and review your current configuration.')

def locationsWindow():
    locationsTop = Toplevel()
    locationsTop.focus_force()
    locationsTop.title('Locations')
    locationsTop.geometry('+'+str(int((width/3)*2))+'+'+str(int(height/5)))
    locationList = []
    locationButtonList = []
    try:
        if importInProgress:
            locationList = importedLocations
        else:
            locationListRawPull = db.child(settingsData['District']).child(settingsData['Route']).child('Locations').get(user['idToken']).val()
            locationListSubPull = locationListRawPull.split(',')
            for x in locationListSubPull:
                locationList.append(x.split('-'))

    except BaseException:
        print('Exception message starts here.')
        traceback.print_exc()
        print('Exception message stops here.')
        messagebox.showwarning('No Data Found','No locations found.')

    addressVar = StringVar()
    labelVar = StringVar()
    orderVar = IntVar()
    addressVar.set('Enter Address Here')
    labelVar.set('Enter Label Here')
    availableOrderPositions = []

    def fillPositionList():
        availableOrderPositions.clear()
        for x in range(len(locationList)+1):
            availableOrderPositions.append(x)
        orderDefinition = OptionMenu(locationsTop,orderVar,*availableOrderPositions)
        orderDefinition.grid(row=1,column=1,sticky=NSEW,padx=5,pady=3)
        orderVar.set(len(availableOrderPositions)-1)

    def buildLocationList(locationFrame):
        rowIndex = 1
        for location in locationList:
            locationButton = Button(locationFrame,text=location,width=60,command=lambda index=int(location[0]): locationButtonClick(index))
            deleteLocation = Button(locationFrame,text='Delete',command=lambda index=int(location[0]): locationDelete(index))
            locationButton.grid(row=rowIndex,column=0,sticky=W)
            deleteLocation.grid(row=rowIndex,column=1)
            locationButtonList.append(locationButton)
            rowIndex += 1

    def locationDelete(index):
        del locationList[index]
        widgetList = locationFrame.grid_slaves()
        for button in widgetList:
            button.destroy()
        if index < (len(availableOrderPositions)-1):
                for location in locationList:
                    if int(location[0]) >= index:
                        location[0] = int(location[0]) -1
        buildLocationList(locationFrame)
        fillPositionList()
        orderDefinition = OptionMenu(locationsTop,orderVar,*availableOrderPositions)
        orderDefinition.grid(row=1,column=1,sticky=NSEW,padx=5,pady=3)
        orderVar.set(availableOrderPositions[len(availableOrderPositions)-1])

    def locationButtonClick(index):
        addressVar.set(locationList[index][2])
        labelVar.set(locationList[index][1])
        orderVar.set(locationList[index][0])

    def saveLocation():
        value = [orderVar.get(),labelVar.get(),addressVar.get()]
        if value[2] == 'Enter Address Here':
            messagebox.showerror('Insufficient Information','Address field must not be empty! Please enter an address and try again.')
        else:
            if value[1] == 'Enter Label Here':
                value[1] = value[2]
            for location in locationList:
                if int(location[0]) >= value[0]:
                    location[0] = int(location[0]) + 1
            locationList.insert(value[0],value)
            buildLocationList(locationFrame)
            fillPositionList()
            orderDefinition = OptionMenu(locationsTop,orderVar,*availableOrderPositions)
            orderDefinition.grid(row=1,column=1,sticky=NSEW,padx=5,pady=3)
            orderVar.set(availableOrderPositions[len(availableOrderPositions)-1])
            addressVar.set('Enter Address Here')
            labelVar.set('Enter Label Here')

    def editLocation():
        value = [orderVar.get(),labelVar.get(),addressVar.get()]
        if value[2] == 'Enter Address Here':
            messagebox.showerror('Insufficient Information','Address field must not be empty! Please enter an address and try again.')
        else:
            if value[1] == 'Enter Label Here':
                value[1] = value[2]
            if value[0] > (len(locationList)-1):
                messagebox.showerror('Invalid Request','Location placeholder does not exist. Choose a different order number or create a new location.')
            else:
                locationList[value[0]] = value
                buildLocationList(locationFrame)
                fillPositionList()
                orderDefinition = OptionMenu(locationsTop,orderVar,*availableOrderPositions)
                orderDefinition.grid(row=1,column=1,sticky=NSEW,padx=5,pady=3)
                orderVar.set(availableOrderPositions[len(availableOrderPositions)-1])
                addressVar.set('Enter Address Here')
                labelVar.set('Enter Label Here')

    def addressEntryClear():
        if addressVar.get() == 'Enter Address Here':
            addressVar.set('')

    def addressLabelEntryClear():
        if labelVar.get() == 'Enter Label Here':
            labelVar.set('')

    def addressEntryReset():
        if len(addressVar.get()) < 1:
            addressVar.set('Enter Address Here')

    def addressLabelEntryReset():
        if len(labelVar.get()) < 1:
            labelVar.set('Enter Label Here')

    def saveCheck():
        answer = messagebox.askyesno('Close Without Saving?','Your changes have not been saved.\nTo save your changes, select \'No\'. To close without saving, select \'Yes\'.',default='no')
        if answer == True:
            locationsTop.destroy()
        else:
            saveAndClose()

    def saveAndClose():
        locationListContent = ''

        for y in range(len(locationList)):
            tempIndex = 0
            if y != 0:
                locationListContent += ','
            for x in locationList[y]:
                if tempIndex != 0:
                    locationListContent += '-'
                locationListContent += str(x)
                tempIndex += 1

        db.child(settingsData['District']).child(settingsData['Route']).child('Locations').set(locationListContent,user['idToken'])
        locationsTop.destroy()
        checkLogin()

    locationsTop.protocol('WM_DELETE_WINDOW', saveCheck)

    addressEntry = Entry(locationsTop,textvariable=addressVar,width=70,font=('Helvetica','11'))
    addressLabelEntry = Entry(locationsTop,textvariable=labelVar,width=50,font=('Helvetica','11'))
    saveLocation = Button(locationsTop,text='Save New Location',command=saveLocation,padx=5)
    editLocation = Button(locationsTop,text='Save Changes',command=editLocation,padx=5)
    orderDefinition = OptionMenu(locationsTop,orderVar,*availableOrderPositions)
    saveToFirebase = Button(locationsTop,text='Save and Close',command=saveAndClose,font=('Helvetica','11'))

    locationCanvas = Canvas(locationsTop,width=(width/4),height=(height/2),bd=2,bg='#D3D3D3')
    locationFrame = Frame(locationCanvas)
    locationScroll_y = Scrollbar(locationsTop,orient="vertical",width=25,command=(locationCanvas.yview))
    locationCanvas.create_window(0,0,anchor=NW,window=locationFrame)
    locationCanvas.configure(yscrollcommand=locationScroll_y.set)

    locationCanvas.grid(row=3,column=0,columnspan=5,sticky=EW)
    locationScroll_y.grid(row=3,column=5,rowspan=5,sticky=NS,ipady=10)
    addressEntry.grid(row=0,column=0,columnspan=2)
    saveLocation.grid(row=2,column=0,sticky=EW)
    editLocation.grid(row=2,column=1,sticky=EW)
    addressLabelEntry.grid(row=1,column=0)
    orderDefinition.grid(row=1,column=1,sticky=NSEW,padx=5,pady=3)
    saveToFirebase.grid(row=4,column=0,columnspan=2)

    addressEntry.bind("<FocusOut>",lambda event:addressEntryReset())
    addressLabelEntry.bind("<FocusOut>",lambda event:addressLabelEntryReset())
    addressEntry.bind("<FocusIn>",lambda event:addressEntryClear())
    addressLabelEntry.bind("<FocusIn>",lambda event:addressLabelEntryClear())
    locationFrame.bind("<Configure>",lambda event,canvas=locationCanvas:onFrameConfigure(locationCanvas))

    buildLocationList(locationFrame)
    fillPositionList()
    locationsTop.mainloop()

def locationsPull():
    try:
        global locationList
        locationList = eval(db.child(settingsData['District']).child(settingsData['Route']).child('Locations').get(user['idToken']).val())
    except BaseException:
        print('Exception message starts here.')
        traceback.print_exc()
        print('Exception message stops here.')
        locationList = []

def importData():
    try:
        choice = None
        file_path = filedialog.askopenfilename()
        with open(file_path,'r') as file:
            csvFile = file.read()
            csvList = csvFile.split('\n')
            listConversion = []
            for sublist in csvList:
                listConversion.append(sublist.split(','))
            numOfColumns = len(listConversion[0])
            if numOfColumns < 5:
                global importInProgress
                importInProgress = True
                if numOfColumns == 1:
                    choice = messagebox.askquestion('Uneven number of columns!','One column was detected. Is this a column of names or a column of locations?',**messageboxChoices)
                    if choice == messageboxChoices['option1']:
                        for row in listConversion:
                            importedNames.append(row[0])
                    else:
                        for row in listConversion:
                            importedLocations.append(row[0])
                elif numOfColumns == 2:
                    for row in csvFile:
                        importedNames.append(row[0])
                        importedLocations.append(row[1])
                elif numOfColumns == 3:
                    choice = messagebox.askquestion('Uneven number of columns!','Three columns were detected. Are there two columns of names or two columns of locations?',**messageboxChoices)
                    if choice == messageboxChoices['option1']:
                        for row in listConversion:
                            importedNames.append(row[0]+' '+row[1])
                            importedLocations.append(row[2])
                    else:
                        for row in listConversion:
                            importedNames.append(row[0])
                            importedLocations.append(row[1]+' '+row[2])
                elif numOfColumns == 4:
                    for row in csvFile:
                        importedNames.append(row[0]+' '+row[1])
                        importedLocations.append(row[2]+' '+row[3])
            else:
                messagebox.showerror('Incorrect Formatting','A maximum of four columns is accepted. Two of names, and two of locations.')
    except BaseException:
        print('Exception message starts here.')
        traceback.print_exc()
        print('Exception message stops here.')

root = Tk(screenName='Rapidbus Server')
root.title('Rapidbus Server')
root.configure(background='#ffffff')
root.resizable(width=False,height=False)
width  = root.winfo_screenwidth()
height = root.winfo_screenheight()

canvas = Canvas(root,width=width/2,height=(height/2),borderwidth=0,background='#ffffff')
frame = Frame(canvas,background="#ffffff")
vsb = Scrollbar(root,orient="horizontal",width=25,troughcolor='#a9a9a9',command=(canvas.xview))
updatePush = Button(root,text=('Save Changes'),command=(updatePush),fg="#000000",bg='#fdfd96',font=('Helvetica','25'))
pullData = Button(root,text=('Refresh'),command=(checkLogin),fg="#000000",bg='#fed8b1',font=('Helvetica','15'),width=20)
settingWindow = Button(root,text=('Settings'),command=(checkSettingsRunning),font=('Helvetica','15'))
downloadWindow = Button(root,text=('↓'),command=(checkDownloadsRunning),font=('Helvetica','18'))
locationsWindow = Button(root,text=('Locations'),command=(locationsWindow),font=('Helvetica','15'))
importButton = Button(root,text=('Import Data'),command=(importData),font=('Helvetica','15'))
canvas.configure(xscrollcommand=vsb.set)

vsb.grid(row=1,column=1,columnspan=3,sticky=S,pady=10,ipadx=width/5)
updatePush.grid(row=2,column=1,columnspan=3,ipadx=width/6)
pullData.grid(row=3,column=1,pady=5,padx=2,sticky=W)
settingWindow.grid(row=3,column=3,padx=2,sticky=W)
downloadWindow.grid(row=3,column=4,padx=1)
importButton.grid(row=3,column=2,sticky=W)
canvas.grid(row=0,column=0,columnspan=5,sticky=W)
locationsWindow.grid(row=3,column=2,sticky=E)
canvas.create_window((0,0),window=frame,anchor=NW)

frame.bind("<Configure>",lambda event,canvas=canvas:onFrameConfigure(canvas))

populate(frame)
openOrCreateSettingFile()
checkLogin()

root.mainloop()