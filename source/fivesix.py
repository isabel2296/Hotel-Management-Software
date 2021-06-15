# Bryan Monh
#Capability 5: A guest profile screen to show guest information
#   This screen will show the guest profile information.  It will include the following information: First Name, Last Name, Phone, Address, E-mail,  
#   ID Info (State, ID#), Vehicle License Plate
#   If using a GUI, a photo of the guest or photo of ID.
#Capability 6: Current stay screen showing a guest’s information for their current stay.
#   This screen will show the room/guest current stay information.  It will contain the following information:  
#   Guest Name, Check In Date and Time, Expected Check Out Date and Time,  
#   Room Type, Room Number, Room Rate ($/Day), Total Charge, Payments Made, Balance
#

from commands import *
import sqlite3
#from PIL import Image,ImageTk #for PNG/JPG

''' connect to database hotel.db '''
con = sqlite3.connect(database='sql\hotel.db')
cur = con.cursor() 

def clearFrame(frame): #clears the frame
    for i in frame.winfo_children(): 
        i.destroy()

class labeling:
    def __init__(self,frame1,frame2,message, textVar):
        label = Label(frame1, text=message, fg='white',bg='black',font=('calibre',12))
        label.pack(expand=True,fill=BOTH, side=TOP)
        label2 = Label(frame2, textvariable=textVar, font =('calibre',12),bg='yellow' )
        label2.pack(side=TOP)

class label_button: #Special Variant with clickable "text"
    def __init__(self,frame1,frame2,message, textVar, first,last):
        label = Label(frame1, text=message, fg='white',bg='black',font=('calibre',12))
        label.pack(expand=True,fill=BOTH, side=TOP)
        # Calls new window
        action_with_arg = partial(pullGuestInfo,first,last)
        button = Button(frame2, textvariable=textVar, font =('calibre',12),bg='yellow', command=action_with_arg)
        button.pack(side=TOP)

class label_entry: #Variant with entry after label
    def __init__(self,frame1,frame2, message, textVar):
        if (str(type(textVar))!="<class 'tkinter.StringVar'>"):
            textVar = StringVar(value=textVar)
        label = Label(frame1, text=message, fg='white',bg='black',font=('calibre',12))
        label.pack(expand=True,fill=BOTH, side=TOP)
        entry = Entry(frame2, textvariable=textVar, font =('calibre',13),bg='yellow' )
        entry.pack(side=TOP)

class Guest: #placeholder
    def __init__(self,guestID, first, last, phone=None, address=None, email=None, ID=None, vehicle=None,totalCharge = None, balance = None,  photo="none"):
        self.guestid = guestID
        self.firstName = first
        self.lastName = last
        self.phoneNumber = phone
        self.address = address
        self.email = email
        self.id = ID
        self.vehicle = vehicle
        self.totalCharge = totalCharge
        self.balance = balance
        
        self.photo = photo
        self.fullName = (f"{str(first)} {str(last)}")


class Reservation:
    def __init__(self, reservID, guestID,dateMade, checkIN, checkOut, rmNum, checkedIn):
        self.reservID = reservID
        self.guestID = guestID
        self.dateMade = dateMade
        self.checkIN = checkIN
        self.checkOut = checkOut
        self.rmNum = rmNum
        self.checkedIn = checkedIn


#Returns a list with (Guest, Reservation, rmType, rmRate)
def sql_pull_GuestReserve(firstName, lastName):
    #Pull DB for room info using firstname+lastname to grab the guestID
    #Then pull the reservation info using the guestID.
    uniqueID = 0
    for x in cur.execute(f"SELECT guestID FROM guest WHERE firstName = '{firstName}' AND lastname = '{lastName}'"):
        uniqueID = x[0]

    tempList = []
    #Initialize Guest class for easier usage later (not saved to db)
    for x in cur.execute(f"SELECT * FROM guest WHERE guestID = '{uniqueID}' "):
        tempList.append(Guest(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9]))

    #Initialize Reservation Class for easier usage (not saved to db)
    for x in cur.execute(f"SELECT * FROM reservation WHERE guestID = '{uniqueID}' "):
        tempList.append(Reservation(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))

    for x in cur.execute(f"SELECT type FROM room WHERE rmNum = '{tempList[1].rmNum}' "):
        tempList.append(x[0])

    for x in cur.execute(f"SELECT rate FROM room where rmNum = '{tempList[1].rmNum}' "):
        tempList.append(x[0])

    return tempList

def photoLabel():
    newWin = Toplevel()
    newWin.title("Picture")
    img = "guest.gif" #placeholder
    photo = PhotoImage(file=img)
    photo_label = Label(newWin, image=photo)
    photo_label.image = photo #to reference the image so it doesn't get garbage collected.
    photo_label.pack()


def profileUpdateButton(frame, stringVarList, guest):
    values = []
    getValue = lambda variableX : variableX.get()

    for x in stringVarList:
        values.append(getValue(x))

    guestid = guest[0].guestid
    firstName = guest[0].firstName
    lastName = guest[0].lastName
    phone = values[1]
    address = values[2]
    email = values[3]
    ID = values[4]
    vehicle = values[5]

    cur.execute(f"UPDATE guest SET phone = '{phone}' WHERE firstName = '{firstName}' AND lastName = '{lastName}'")
    cur.execute(f"UPDATE guest SET addr = '{address}' WHERE firstName = '{firstName}' AND lastName = '{lastName}'")
    cur.execute(f"UPDATE guest SET email = '{email}' WHERE firstName = '{firstName}' AND lastName = '{lastName}'")
    cur.execute(f"UPDATE guest SET id = '{ID}' WHERE firstName = '{firstName}' AND lastName = '{lastName}'")
    cur.execute(f"UPDATE guest SET vehicle = '{vehicle}' WHERE firstName = '{firstName}' AND lastName = '{lastName}'")
    con.commit()

    print("Updated")
    #tempA = []
    #tempA.append(Guest(guestid, firstName, lastName, phone, address, email, ID, vehicle))

#Capability 6 (Submit button for Scenario 1)
def checkInButton(frame, stringVarList):
    print(len(stringVarList))
    #Grab New Variables from stringVarList
    values = []
    getValue = lambda variableX : variableX.get()

    for x in range(len(stringVarList)):
        values.append(getValue(stringVarList[x]))

    # Split fullname into two
    # nameList = values[0].split(' ')
    # firstName = nameList[0]
    # lastName = nameList[1]
    # checkIn = values[1]
    # checkOut = values[2]
    # roomType = values[3]
    # roomNum = values[4]
    # roomRate = values[5]
    # totalCharge = values[6]
    #paymentsMade = values[7]
    #balance = values[7]
    # redo 
    firstName = values[0]
    lastName = values[1]
    checkIn = values[2]
    checkOut = values[3]
    roomType = values[4]
    roomNum = values[5]
    roomRate = values[6]
    totalCharge = values[7]
    #paymentsMade = values[7]
    balance = values[8]
    #Update DB

    #Create New Entry
    cur.execute('INSERT INTO guest(firstName,lastName,totalCharge, balance) VALUES (?,?,?,?)',(firstName,lastName,totalCharge,balance)).fetchone()
    con.commit()
    checkGuest = cur.execute('SELECT guestID FROM guest WHERE firstName=? AND lastName=?',(firstName,lastName,)).fetchone()
    # create reservation
    con.execute('INSERT INTO reservation(guestID,dateMade,checkIN,checkOut,rmNum) VALUES (?,CURRENT_DATE,?,?,?)',(int(checkGuest[0]),checkIn, checkOut,roomNum,))
    # change room availbality to occupied
    con.execute('UPDATE room SET status = ? WHERE rmNum = ?',('Occupied', roomNum,))
    con.commit()

    for x in cur.execute("SELECT * FROM guest WHERE firstName = '{firstName}' AND lastName = '{lastName}' "):
        print(x)
    #"Refresh" window (by recalling)
    guestStayInfo(frame, firstName, lastName)

def checkOutButton(frame, variableList):
    nameList = variableList[0].split(" ")
    firstName = nameList[0]
    lastName = nameList[1]

    guestID = cur.execute(f"SELECT guestID FROM guest WHERE firstName = '{firstName} AND lastname = '{lastName}' ")
    roomNumber = cur.execute(f"SELECT rmNum FROM reservation WHERE guestID = '{guestID}' ")

    cur.execute(f"DELETE FROM guest WHERE guestID = '{guestID}' ")
    cur.execute(f"DELETE FROM reservation WHERE guestID = '{guestID}'")

    cur.execute('UPDATE room SET status = ? WHERE rmNum=?',('Dirty',int(roomNumber),))
    con.commit()

    guestStayInfo(frame)


#Capability 6 -> Clicking name calls Capability 5
def pullGuestInfo(firstName, lastName):
    guestList = []
    for x in cur.execute(f"SELECT * FROM guest WHERE firstName = '{firstName}' AND lastname = '{lastName}'"):
        guestList.append(Guest(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]))

    newWin = Toplevel()
    newWin.title(f"{firstName} {lastName}")
    
    guestInfo(newWin, guestList)


#Capability 5
def guestInfo(frame, guest=None):
    clearFrame(frame)
    frameTop = Frame(master=frame, width=350, height =240, bg='white')
    frameTop.pack(side=TOP)
    frameBot = Frame(master=frame, width=350, height=240, bg='white')
    frameBot.pack(side=BOTTOM)
    frame1 = Frame(master=frameTop, width=50, height = 120, bg='white')
    frame1.pack(side=LEFT)
    frame2= Frame(master=frameTop, width=50, height= 120, bg='yellow')
    frame2.pack(side=RIGHT)
    
    # variables taken in (current placeholders)
    fullName = StringVar()
    phone = StringVar()
    address = StringVar()
    email = StringVar()
    ID = StringVar()
    vehicle = StringVar()

    variableList = [fullName, phone, address, email, ID, vehicle]
    messageList = ["Full Name", "Phone Number", "Address", "Email" , "ID", "License Plate"]

    if guest: # Fills in with info if available
        fullName.set(guest[0].fullName)
        phone.set(guest[0].phoneNumber)
        address.set(guest[0].address)
        email.set(guest[0].email)
        ID.set(guest[0].id)
        vehicle.set(guest[0].vehicle)

        entryList = []
        entryLam = lambda message, variable : label_entry(frame1, frame2, message, variable)
        for x in range(len(messageList)):
            entryList.append(entryLam(messageList[x],variableList[x]))

        action_with_arg = partial(profileUpdateButton, frame, variableList, guest)
        button = Button(frameBot, text="Update", font =('calibre',12),bg='yellow', command=action_with_arg)
        button.pack(side=TOP)
    else:
        fullName_label = labeling(frame1,frame2,"Full Name", fullName)
        phone_label = labeling(frame1,frame2,"Phone Number", phone)
        address_label = labeling(frame1,frame2,"Address",address)
        email_label = labeling(frame1,frame2,"Email", email)
        ID_label = labeling(frame1,frame2,"ID", ID)
        vehicle_label = labeling(frame1,frame2,"License Plate", vehicle)
    
    B = Button(frameBot, text="Click for Picture", font=('calibre',12), command=photoLabel)
    B.pack(side=TOP)


#Capability 6
def guestStayInfo(frame, firstName=None, lastName=None, rmNum=None):
    clearFrame(frame)
    frameTop = Frame(master=frame, width=350, height =240, bg='white')
    frameTop.pack(side=TOP)

    frameBot = Frame(master=frame, width=350, height=240, bg='white')
    frameBot.pack(side=BOTTOM)

    frame1 = Frame(master=frameTop, width=50, height = 120, bg='white')
    frame1.pack(side=LEFT)
    frame2= Frame(master=frameTop, width=50, height= 120, bg='yellow')
    frame2.pack(side=RIGHT)

    frame3 = Frame(master=frameBot)
    frame3.pack(side=TOP)

    # # variables taken in (current placeholders)
    firstName = StringVar()
    lastName = StringVar()
    checkIn = StringVar()
    #checkInTime = StringVar()
    checkOut = StringVar()
    #checkOutTime = StringVar()
    roomType = StringVar()
    roomNum = StringVar()
    roomRate = StringVar()
    totalCharge = StringVar()
    #paymentsMade = StringVar()
    balance = StringVar()
    
    stringVarList = [firstName,lastName, checkIn, checkOut, roomType, roomNum, roomRate, totalCharge, balance]
    variableList =[]
    sqlQuery = 'SELECT firstName, lastName,checkIN,checkOut, type, r.rmNum ,rm.rate, totalCharge, balance FROM guest as g INNER JOIN reservation as r ON g.guestID = r.guestID JOIN room as rm ON r.rmNum = rm.rmNum WHERE r.rmNUM ='+str(rmNum)
    '''changed this'''
    flag = 0

    if rmNum != None:
        variableList = cur.execute(sqlQuery).fetchall()[0]
        flag = 1

    messageList = ["First Name","Last Name", "Check In ", "Check Out", "Room Type", "Room Number", "Room Rate", "Total Charge", "Balance"]


    # Figure out if empty - partial - full \
    # Empty - 0, partial - 1, full - 2
    #firstName = 'Ax'
    #lastName = 'Bx'
    # tempList = []
    # if lastName != None and rmNum==None : # added this to rule out the rmnum input
    #     flag = 2
    #     #tempList = sql_pull_GuestReserve(firstName, lastName)
    #     print(tempList[0])
    #     print(tempList[1].checkedIn)
    #     x = cur.execute('') 
    #     print(x)
    #     for y in cur.execute(f"SELECT status FROM room WHERE rmNum = '{x}' "):
    #         print(y)
    #     if y[0] == "Available":
    #         flag = 1
    if lastName == None and rmNum != None: 
        flag = 2

    entryList = []
    #Scenario 1: Worst Case (fill out everything) + Check in option 
    if flag == 0 and rmNum ==None: #done
        print("FLAG 0")
        '''added an empty variable list'''
        #variableList = ["" for i in range(len(messageList))] #IS added this 
        entryLam = lambda message, variable : label_entry(frame1, frame2, message, variable)
        for x in range(len(messageList)):
            entryList.append(entryLam(messageList[x],stringVarList[x])) # string var to fill out empty

        action_with_arg = partial(checkInButton, frame, stringVarList)
        button = Button(frame3, text="Check In", font =('calibre',12),bg='yellow', command=action_with_arg)
        button.pack(side=TOP)

        
    #Scenario 3: Reservation, some info available + checkin option
    if flag == 1:
        print("FLAG 1")
        # listA = tempList[0].fullname().split(" ")
        # firstName = listA[0]
        # lastName = listA[1]
        # guestID = cur.execute(f"SELECT guestID FROM guest WHERE firstname = '{firstName}'AND lastName = '{lastName}'")
        # checkInV = cur.execute(f"SELECT checkIN FROM reservation WHERE guestID = '{guestID}' ")
        # checkOutV = cur.execute(f"SELECT checkOut FROM reservation where guestID = '{guestID}' ")

        ''' this is the same as variable list '''
        #valueList = [tempList[0].fullName, checkInV, checkOutV, tempList[2], tempList[1].rmNum, tempList[3], tempList[0].totalCharge, tempList[0].balance]
        # valueList = cur.execute(sqlQuery).fetchall()[0]
        SetValue = lambda VariableX, Value : VariableX.set(Value)
        
        for x in range(len(variableList)):
            SetValue(stringVarList[x], variableList[x])
       
        entryLam = lambda message, variable : label_entry(frame1, frame2, message, variable)
        for x in range(len(messageList)):
            entryList.append(entryLam(messageList[x],stringVarList[x]))

        action_with_arg = partial(checkInButton, frame, stringVarList)
        button = Button(frame3, text="Check In", font =('calibre',12),bg='yellow', command=action_with_arg)
        button.pack(side=TOP)

    # if flag == 2:
    #     print("FLAGG TWO")
    #     ''' this is when no info is available ''' 
    #     #Scenario 2: Already checked in, all info available +  checkout option
    #     #Current Is fine. Needs to add checkout button
    #     tempList = []
    #     tempList = sql_pull_GuestReserve(firstName, lastName)
    #     valueList = [tempList[0].fullName, tempList[1].checkIN, tempList[1].checkOut, tempList[2], tempList[1].rmNum, tempList[3], tempList[0].totalCharge, tempList[0].balance]
    #     SetValue = lambda VariableX, Value : VariableX.set(Value)

    #     for x in range(len(variableList)):
    #         SetValue(variableList[x], valueList[x])
    
    #     #ALL Scenarios - Create button to edit and save (See capability 1)

    #     fullName_label = label_button(frame1,frame2,"Full Name", fullName, firstName, lastName)
    #     checkIn_label = labeling(frame1,frame2,"Check In Date", checkIn)
    #     #checkInTime_label = labeling(frame1,frame2,"Check In Time", checkInTime)
    #     checkOut_label = labeling(frame1,frame2,"Check Out Date", checkOut)
    #     #checkOutTime_label = labeling(frame1,frame2,"Check Out Time", checkOutTime)
    #     roomType_label = labeling(frame1,frame2,"Room Type", roomType)
    #     roomNum_label = labeling(frame1,frame2,"Room Number", roomNum)
    #     roomRate_label = labeling(frame1,frame2,"Room Rate", roomRate)
    #     totalCharge_label = labeling(frame1,frame2,"Total Charge", totalCharge)
    #     #paymentsMade_label = labeling(frame1,frame2,"Payments Made", paymentsMade)
    #     balance_label = labeling(frame1,frame2,"Balance", balance)
        
    #     action_with_arg = partial(checkOutButton, frame, variableList)
    #     button = Button(frame3, text="Check Out", font =('calibre',12),bg='yellow', command=action_with_arg)
    #     button.pack(side=TOP)