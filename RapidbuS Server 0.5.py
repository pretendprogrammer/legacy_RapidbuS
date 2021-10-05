import tkinter
from tkinter import *
from tkinter import messagebox
from firebase import Firebase
import os
import os.path
from os import path
import json
import tkinter.ttk
from cryptography.fernet import Fernet
from functools import partial
from datetime import datetime
from decouple import config
 
cols = []
for i in range(11):
    cols.append([])

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

config = { #Firebase Configuration Information
    'apiKey': config('apikey',default=''),
    'authDomain': config('authDomain',default=''),
    'databaseURL': config('databaseURL',default=''),
    'storageBucket': config('storageBucket',default='')
}

firebase = Firebase(config)
auth = firebase.auth()
db = firebase.database()

def firebasePull():
    pull = db.child(settingsData['District']).child(settingsData['Route']).child('Driver Data').get(user['idToken']).val()
    if pull == None:
        messagebox.showerror('Sad Announcement','No data found.\n:(')
    else:
        midPull = pull.split('|')
        column1 = midPull[0].split(',')
        column2 = midPull[1].split(',')
        column3 = midPull[2].split(',')
        column4 = midPull[3].split(',')
        column5 = midPull[4].split(',')
        column6 = midPull[5].split(',')

        for x in range(50):
            cols[0][x].delete(0.0,END)
            cols[0][x].insert(0.0,column1[x])
        for x in range(50):
            cols[1][x].delete(0,END)
            cols[1][x].insert(0,column2[x])
        for x in range(50):
            cols[2][x].delete(0,END)
            cols[2][x].insert(0,column3[x])
        for x in range(50):
            cols[3][x].delete(0,END)
            cols[3][x].insert(0,column4[x])
        for x in range(50):
            cols[4][x].delete(0,END)
            cols[4][x].insert(0,column5[x])
        for x in range(50):
            cols[5][x].delete(0,END)
            cols[5][x].insert(0,column6[x])

def populate(frame):
    for x in range(50): #ColNumber
        colLabel = Label(frame, relief = SUNKEN,text=(x))
        colLabel.grid(row=1,column=x,sticky=NSEW)

    for x in range(50): #Display
        display = Text(frame,width=20,height=10)
        display.grid(row=2,column=x)
        cols[0].append(display)
        cols[0][x].insert(END,'Empty')

    for x in range(50): #Flag
        checkFlag = Entry(frame,bg='#FF9AA2',width=20)
        checkFlag.grid(row=3,column=x)
        cols[1].append(checkFlag)
        cols[1][x].insert(END,'Flag')

    for x in range(50): #Condition1
        condition1 = Label(frame,relief=FLAT,background='#808080',text=('Condition 1'))
        condition1.grid(row=4,column=x,sticky=NSEW)

    for x in range(50): #CheckMorning
        checkMorning = Entry(frame,bg='#B5EAD7',width=20)
        checkMorning.grid(row=5,column=x)
        cols[2].append(checkMorning)
        cols[2][x].insert(END,'Morning')

    for x in range(50): #CheckAfternoon
        checkAfternoon = Entry(frame,bg='#FFDAC1',width=20)
        checkAfternoon.grid(row=6,column=x)
        cols[3].append(checkAfternoon)
        cols[3][x].insert(END,'Afternoon')

    for x in range(50): #CheckSkip
        checkSkip = Entry(frame,bg='#80CEE1',width=20)
        checkSkip.grid(row=7,column=x)
        cols[4].append(checkSkip)
        cols[4][x].insert(END,'Skip')
    
    for x in range(50): #AltIndex
        altIndex = Entry(frame,bg='#C7CEEA',width=20)
        altIndex.grid(row=8,column=x)
        cols[5].append(altIndex)
        cols[5][x].insert(END,'Alt Index')

    for x in range(50): #Condition2
        condition2 = Label(frame,relief=FLAT,background='#808080',text=('Condition 2'))
        condition2.grid(row=9,column=x,sticky=NSEW)

    for x in range(50): #CheckDay
        checkDay = Entry(frame,bg='#C7CEEA',width=20)
        checkDay.grid(row=10,column=x)
        cols[6].append(checkDay)
        cols[6][x].insert(END,'Day of Week (1-7)')

    for x in range(50): #CheckMorning2
        checkMorning2 = Entry(frame,bg='#B5EAD7',width=20)
        checkMorning2.grid(row=11,column=x)
        cols[7].append(checkMorning2)
        cols[7][x].insert(END,'Morning')

    for x in range(50): #CheckAfternoon2
        checkAfternoon2 = Entry(frame,bg='#FFDAC1',width=20)
        checkAfternoon2.grid(row=12,column=x)
        cols[8].append(checkAfternoon2)
        cols[8][x].insert(END,'Afternoon')

    for x in range(50): #CheckSkip2
        checkSkip2 = Entry(frame,bg='#80CEE1',width=20)
        checkSkip2.grid(row=13,column=x)
        cols[9].append(checkSkip2)
        cols[9][x].insert(END,'Skip')

    for x in range(50): #AltIndex2
        altIndex2 = Entry(frame,bg='#C7CEEA',width=20)
        altIndex2.grid(row=14,column=x)
        cols[10].append(altIndex2)
        cols[10][x].insert(END,'Alt Index')

def updatePush():
    displayContent = ''
    checkFlagContent = ''
    checkMorningContent = ''
    checkAfternoonContent = ''
    checkSkipContent = ''
    altIndexContent = ''
    checkDayContent = ''
    checkMorning2Content = ''
    checkAfternoon2Content = ''
    checkSkip2Content = ''
    altIndex2Content = ''

    for y in range(50):
        z = cols[0][y].get("1.0",'end-1c')
        if y == 0:
            displayContent += z
        else:
            displayContent += (',' + z)
    for y in range(50):
        z = cols[1][y].get()
        if y == 0:
            checkFlagContent += z
        else:
            checkFlagContent += (','+z)
    for y in range(50):
        z = cols[2][y].get()
        if y == 0:
            checkMorningContent += z
        else:
            checkMorningContent += (','+z)
    for y in range(50):
        z = cols[3][y].get()
        if y == 0:
            checkAfternoonContent += z
        else:
            checkAfternoonContent += (','+z)
    for y in range(50):
        z = cols[4][y].get()
        if y == 0:
            checkSkipContent += z
        else:
            checkSkipContent += (','+z)
    for y in range(50):
        z = cols[5][y].get()
        if y == 0:
            altIndexContent += z
        else:
            altIndexContent += (','+z)
    for y in range(50):
        z = cols[6][y].get()
        if y == 0:
            checkDayContent += z
        else:
            checkDayContent += (','+z)
    for y in range(50):
        z = cols[7][y].get()
        if y == 0:
            checkMorning2Content += z
        else:
            checkMorning2Content += (','+z)
    for y in range(50):
        z = cols[8][y].get()
        if y == 0:
            checkAfternoon2Content += z
        else:
            checkAfternoon2Content += (','+z)
    for y in range(50):
        z = cols[9][y].get()
        if y == 0:
            checkSkip2Content += z
        else:
            checkSkip2Content += (','+z)
    for y in range(50):
        z = cols[10][y].get()
        if y == 0:
            altIndex2Content += z
        else:
            altIndex2Content += (','+z)
    db.child(settingsData['District']).child(settingsData['Route']).child('Driver Data').set(displayContent+\
        '|'+checkFlagContent+\
            '|'+checkMorningContent+\
                '|'+checkAfternoonContent+\
                    '|'+checkSkipContent+\
                        '|'+altIndexContent+\
                            '|'+checkDayContent+\
                                '|'+checkMorning2Content+\
                                    '|'+checkAfternoon2Content+\
                                        '|'+checkSkip2Content+\
                                            '|'+altIndex2Content,user['idToken'])

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
    top.title('Settings')
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
    top = Toplevel()
    top.title('Downloads')
    downloadFromPath = db.child(settingsData['District']).child(settingsData['Route']).child('Log Data')
    rowPosition = 0

    def downloadOne(position):
        download = db.child(settingsData['District']).child(settingsData['Route']).child('Log Data').child(logListPull[position]).get(user['idToken']).val()
        with open('RB Log'+logListPull[position]+'.csv','w') as file:
            file.write(download)
    
    def deleteOne(position):
        db.child(settingsData['District']).child(settingsData['Route']).child('Log Data').child(logListPull[position]).remove(user['idToken'])
        top.destroy()
        downloadsWindow()

    def exitNoSave():
        global downloadsRunning
        downloadsRunning = False
        top.destroy()

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
        top.destroy()

    top.protocol('WM_DELETE_WINDOW', exitNoSave)

    try:
        logListPull = list(dict(downloadFromPath.get(user['idToken']).val()))
        for i in logListPull:
            currentRowPosition = rowPosition
            logSelect = Label(top,text=(str(i)),pady=5)
            logDownload = Button(top,text='↓',command=partial(downloadOne,currentRowPosition))
            logDelete = Button(top,text='Delete',command=partial(deleteOne,currentRowPosition))
            logSelect.grid(row=rowPosition,column=0,ipadx=5)
            logDownload.grid(row=rowPosition,column=1,padx=10)
            logDelete.grid(row=rowPosition,column=2,padx=10)
            rowPosition += 1
        allDownload = Button(top,text='Download All',font=('Helvetica','15'),bg='#B5EAD7',command=downloadAll)
        allDelete = Button(top,text='Delete All',font=('Helvetica','15'),bg='#FF9AA2',command=deleteAll)
        allDownload.grid(row=rowPosition,column=0,columnspan=2)
        allDelete.grid(row=rowPosition,column=2)
    except:
        downloadsRunning = False
        top.destroy()
        messagebox.showerror('Sad Announcement','No data found.\n:(')

def checkLogin():
    openOrCreateSettingFile()
    global user
    try:
        user = auth.sign_in_with_email_and_password(settingsData['Username'],settingsData['Password'])
        firebasePull()
    except:
        messagebox.showerror('Connection to database failed!','Please go to settings and review your current configuration.')


root = Tk(screenName='Rapidbus Server')
root.title('Rapidbus Server')
root.configure(background='#ffffff')
width  = root.winfo_screenwidth()
height = root.winfo_screenheight()

canvas = Canvas(root,width=width/2,height=(height/5)*2,borderwidth=0,background='#ffffff')
frame = Frame(canvas,width=width/2,height=(height/2)-50,background="#ffffff")
vsb = Scrollbar(root,orient="horizontal",width=25,troughcolor='#a9a9a9',command=(canvas.xview))
updatePush = Button(root,text=('Save Changes'),command=(updatePush),fg="#000000",bg='#fdfd96',font=('Helvetica','25'))
pullData = Button(root,text=('Refresh'),command=(checkLogin),fg="#000000",bg='#fed8b1',font=('Helvetica','15'))
settingWindow = Button(root,text=('Settings'),command=(checkSettingsRunning),font=('Helvetica','15'))
downloadWindow = Button(root,text=('↓'),command=(checkDownloadsRunning),font=('Helvetica','18'))
canvas.configure(xscrollcommand=vsb.set)

vsb.grid(row=1,column=1,columnspan=3,sticky=S,pady=10,ipadx=width/5)
updatePush.grid(row=2,column=1,columnspan=3,ipadx=width/6)
pullData.grid(row=3,column=1,columnspan=2,pady=5,padx=2,ipadx=width/6)
settingWindow.grid(row=3,column=3,padx=2)
downloadWindow.grid(row=3,column=4,padx=1)
canvas.grid(row=0,column=0,columnspan=5,sticky=W)
canvas.create_window((0,0),window=frame,anchor="nw")

frame.bind("<Configure>",lambda event,canvas=canvas:onFrameConfigure(canvas))

populate(frame)
openOrCreateSettingFile()
checkLogin()

root.mainloop()