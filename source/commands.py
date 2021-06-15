
import tkinter 
from tkinter import * 
from functools import partial
import sqlite3
from fivesix import guestStayInfo
from datetime import *
''' connect to database hotel.db '''
con = sqlite3.connect(database='sql\hotel.db')
cur = con.cursor() 

''' helper functions '''
def clearFrame(frame): #clears the frame
    for i in frame.winfo_children(): 
        i.destroy()

def errorPopUP(message): # pops up error with error message
    popUp = Toplevel()
    popUp.geometry("300x150")
    popUp.title('Error')
    error = Label(popUp,text=message,fg='red',font=('calibre',16,'bold'))
    error.pack()
    popUp.mainloop()

def abrvRm(rm): # changes incoming room string to single char for easier DB read
    if rm == 'King': 
        return 'K'
    elif rm == 'Double Queen':
        return 'DQ'
    elif rm == 'Double Queen w/ Kitchen':
        return 'DQK'
    else: return 'S'

def reAbrvRm(rm):
    if rm == 'K': 
        return 'King'
    elif rm == 'DQ':
        return 'Double Queen'
    elif rm == 'DQK':
        return 'Double Queen w/ Kitchen'
    else: return 'Suite'


def date_handler():
    pass

# checks if there is availiabilty  
def checkResAvail(root,fn,ln,chIn,chOut,rmType):
    rmNum = cur.execute('SELECT rmNum FROM room WHERE type=? AND status = ? ',(abrvRm(rmType.get()),'Available',)).fetchone()
    if not rmNum:
        mesg = 'Room "' + rmType.get() + '" Unavailable' 
        errorPopUP(mesg)
    else: 
        # check if guest is already in database if not place them into database
        checkGuest = cur.execute('SELECT guestID FROM guest WHERE firstName=? AND lastName=?',(fn.get(),ln.get(),)).fetchone()
        if not checkGuest:
            cur.execute('INSERT INTO guest(firstName,lastName) VALUES (?,?)',(fn.get(),ln.get(),)).fetchone()
            con.commit()
            checkGuest = cur.execute('SELECT guestID FROM guest WHERE firstName=? AND lastName=?',(fn.get(),ln.get(),)).fetchone()
        # create reservation
        con.execute('INSERT INTO reservation(guestID,dateMade,checkIN,checkOut,rmNum) VALUES (?,CURRENT_DATE,?,?,?)',(int(checkGuest[0]),chIn.get(),chOut.get(),int(rmNum[0]),))
        # change room availbality to occupied
        # con.execute('UPDATE room SET status = ? WHERE rmNum = ?',('Occupied',int(rmNum[0]),))
        con.commit()

    root.destroy()
#delete reservation for cability 3
def deleteReserv(num,frame):
        con.execute('DELETE FROM reservation WHERE rmNum=?',(num,))
        con.execute('UPDATE room SET status = ? WHERE rmNum=?',('Available',int(num),))
        con.commit()
        disReservations(frame)

# helper for manageRM
def updateRm(root,firstName,lastName,checkIn,checkOut,rmType,rmNum):
    # con.execute('UPDATE reservation SET checkedIn = ? WHERE rmNum=?',(chkdInO.get(),rmNum,))
    # con.commit()
    disReservations(root)
    # this is not complete
    # need to update the rest of the stuff.. 


# manage room for capability 3
#not complete (calls upateRm which is not complete)
def manageRm(rmNum, root):
    #need to call capability 6 instead
    clearFrame(root)
    curRow = 5
    # title
    title = Label(root, text="Manage Room # "+str(rmNum),fg='black',font=('calibre',15,'bold'))
    title.grid(row=curRow,column=1,columnspan=10)
    # creates back button to go back and view all reservation (does not update)
    backB = Button(root,text='back',bg = 'purple',command=partial(disReservations,root))
    backB.grid(row=curRow,column=0)
    curRow+=1
    # sql request
    sqlQuery = 'SELECT firstName, lastName,checkIN,checkOut, type, rm.status,r.checkedIn, r.rmNum FROM guest as g INNER JOIN reservation as r ON g.guestID = r.guestID JOIN room as rm ON r.rmNum = rm.rmNum WHERE r.rmNUM ='+str(rmNum)
    request = cur.execute(sqlQuery).fetchall()[0]
    
    firstName,lastName,checkIn,checkOut,roomType,status = StringVar(value=request[0]),StringVar(value=request[1]),StringVar(value=request[2]),StringVar(value=request[3]),StringVar(value=reAbrvRm(request[4])), StringVar(value=request[5])
    variables = [firstName,lastName,checkIn,checkOut,roomType,status]
    varStr = ['First Name','Last Name','Check in Date','Check Out Date','Room Type', 'Status','Check In/Out']
    for i in range(len(varStr)):
        entryLabel = Label(root,text=varStr[i])
        entryLabel.grid(row=curRow,column=2)
        if varStr[i] == "Check In/Out":
             checkB = Button(root,text='Go to Check In Page',command=partial(guestStayInfo,root,firstName.get(),lastName.get(),rmNum))
             checkB.grid(row=curRow,column=3)
        elif varStr[i] == "Status":
            stLabel = Label(root,text=status.get(), fg='red')
            stLabel.grid(row=curRow,column=3)
        else: 
            entry = Entry(root,textvariable=variables[i])
            entry.grid(row=curRow,column=3,columnspan=3)
        curRow += 1
    # just deletes current reservation and makes new one if update is clicked
    updateB = Button(root, text="update",
                        fg='black',
                        bg='lime',
                        command = partial(updateRm, root,
                        firstName,lastName,checkIn,checkOut,roomType,rmNum))
    updateB.grid(row=curRow+1)
    

#manage house keeping for capability 4
def updateStatus(rmNum,chckB,amenities,master):
    for i in range(len(chckB)): 
        if (amenities[i]== 'Need Maintenance?'):
            val = 'status'
        else: 
            val = amenities[i]
        query = 'UPDATE room SET ' + val + '= ? WHERE rmNum=' + str(rmNum)
        if amenities[i] == 'Need Maintenance?':
            con.execute(query,('Maintenance',))
        elif chckB[i].get() == 1: 
            con.execute(query,(1,))
        else: 
            con.execute(query,(0,))
        con.commit()
    sqlquery = 'SELECT bathroom, towels,bedSheets,vacum, dusting, electronics FROM room WHERE rmNum='+str(rmNum)
    if all(cur.execute(sqlquery).fetchall()[0]) == 1:
        con.execute('UPDATE room SET status = ? WHERE rmNum = ?',('Available',int(rmNum),))
        con.commit()
    master.destroy()

def manageHouseKeep(rmNum,root):
    popUp = Toplevel()
    popUp.title('Manage Room '+str(rmNum))
    title = Label(popUp, text="Room:"+str(rmNum),fg='black',font=('calibre',15,'bold'))
    title.grid(row=4,columnspan=10)
    amenities = ['bathroom','towels','bedSheets','vacum','dusting','electronics','Need Maintenance?'] 
    checkedB = []
    rrow = 5
    sqlquery = 'SELECT bathroom, towels,bedSheets,vacum, dusting, electronics, status FROM room WHERE rmNum='+str(rmNum)
    amenitiesValues = cur.execute(sqlquery).fetchall()[0]
    for i in range(len(amenities)):
        cVar = IntVar()
        chkb = Checkbutton(popUp,text=amenities[i],variable=cVar,justify=LEFT)
        chkb.grid(row=rrow)
        rrow+=1
        if(amenitiesValues[i]==None or amenitiesValues[i]==0):
            chkb.deselect()
        else: 
            chkb.select()
        checkedB.append(cVar)
    updateB = Button(popUp,text='Update Room',command=partial(updateStatus,rmNum,checkedB,amenities,popUp))
    updateB.grid(row=rrow+1)
        
# table creator for both capability 3&4
def create_table(names,title,root,sqlQuery,commands,deleteButton=False):
    clearFrame(root)  
    title = Label(root, text=title,fg='black',font=('calibre',15,'bold'))
    title.grid(row=4,columnspan=10)
    # displays the top row of table
    for num in range(len(names)+1):
        try: 
            na = Label(root, text =names[num],fg='blue')
            na.grid(row=6,column=num+1, sticky=W)
            if num == len(names)-1: 
                refreshB = Button(root,text="refresh",bg='orange',
                command=partial(commands[1],root))
                refreshB.grid(row=6,column=num+2)
        except Exception:
            pass
    counter = 7
     # displays the results of sql query
    for row in cur.execute(sqlQuery):
        for l in range(len(row)+1): 
            try: 
                label = Label(root,text=row[l])
                label.grid(row=counter,column=l+1,sticky=W)
                if deleteButton:
                    deleteB = Button(root,text='Delete', fg="white", bg='blue',
                    command=partial(deleteReserv,int(row[0]),root) ) 
                    deleteB.grid(row=counter,column=0)
                elif l == len(row)-1 and deleteButton==False:
                    manageB = Button(root,text="manage", bg='light green',
                        command=partial(commands[0],int(row[0]),root))
                    manageB.grid(row=counter,column=len(names)+1)
            except Exception:
                pass 
        counter += 1
    return counter # to get the last position for delete/add reservation buttons

# add reservation
def makeReservPopUp():
    frame = Toplevel()
    title = Label(frame, text="Management: Make Reservation",font=('calibre',12,'bold'))
    title.grid(row=4,columnspan=10)
    curRow = 5
  
    fName,lName,checkIn,checkOut,roomType = StringVar(), StringVar(),StringVar(),StringVar(),StringVar(frame)
    varList = [fName,lName,checkIn,checkOut,roomType]
    varListStr = ["First Name","Last Name","Check In M/D/Y","Check Out M/D/Y","Room Type"]
    # list of rooms
    roomTypeL= ['King','Double Queen','Double Queen w/ Kitchen','Suite']
    roomType.set(roomTypeL[0]) #set the variable to King
    # date option menu
    days = [i+1 for i in range(31)]
    years = [i+2021 for i in range(5)]
    months = ["January","Febuary","March","April","May","June","July","August","September","October","November","December"] # reservation up to 5 years from 2020
    inDay,outDay,inMonth,outMonth,inYear,outYear = StringVar(value=days[0]),StringVar(value=days[0]),StringVar(value=months[0]),StringVar(value=months[0]),StringVar(value=years[0]),StringVar(value=years[0])
    # show labels and Entry for taking in guest information
    for i in range(len(varList)):
        label = Label(frame,text=varListStr[i])
        label.grid(row=curRow,column=0)
        if varListStr[i] == "Room Type": 
            rmType_entry = OptionMenu(frame,roomType,*roomTypeL)
            rmType_entry.grid(row=curRow,column=1)
        elif varListStr[i] == "Check In M/D/Y":
            dayEntry=OptionMenu(frame,inDay,*days)
            dayEntry.grid(row=curRow,column=1, sticky='e')
            monthEntry=OptionMenu(frame,inMonth,*months)
            monthEntry.grid(row=curRow,column=1,sticky='w')
            yearEntry=OptionMenu(frame,inYear,*years)
            yearEntry.grid(row=curRow,column=2,sticky='e')
            checkIn.set( datetime.strptime((inDay.get()+" "+inMonth.get()+" "+inYear.get()), "%d %B %Y").date())
        elif varListStr[i] == "Check Out M/D/Y" :
            dayOutEntry=OptionMenu(frame,outDay,*days)
            dayOutEntry.grid(row=curRow,column=1,sticky='e')
            monthOutEntry=OptionMenu(frame,outMonth,*months)
            monthOutEntry.grid(row=curRow,column=1,sticky='w')
            yearOutEntry=OptionMenu(frame,outYear,*years)
            yearOutEntry.grid(row=curRow,column=2,sticky='e')
            checkOut.set( datetime.strptime((outDay.get()+" "+outMonth.get()+" "+outYear.get()), "%d %B %Y").date())
        else:
            entry = Entry(frame,textvariable=varList[i], font=('calibre',12,'bold'))
            entry.grid(row=curRow,column=1)
        curRow+=1
    # button to check room availability
    checkAvaliabilty = Button(frame, text="Check Avaliability",
                        fg='black',
                        bg='lime',
                        command = partial(checkResAvail, frame,
                        fName,lName,checkIn,checkOut,roomType))
    checkAvaliabilty.grid(row=curRow, column=1)

'''Command Functions'''
# Capability 3 & 4 assigned to Isabel Silva
# capability 3
def disReservations(frame):
    clearFrame(frame)
    title = "Managment: Reservation List"
    titles = ['Room Number','First Name', 'Last Name', 'Date Made','Check In','Check Out', 'Room Type', 'Rate','Total']
    sqlQuery = 'SELECT r.rmNum, firstName, lastName,dateMade,checkIN,checkOut, type FROM guest as g INNER JOIN reservation as r ON g.guestID = r.guestID JOIN room as rm ON r.rmNum = rm.rmNum '
    last_Rposition = create_table(titles,title,frame,sqlQuery,[manageRm,disReservations])

    addResrvButten = Button(frame, text='Make Reservation', command=makeReservPopUp,bg='yellow')
    addResrvButten.grid(row=last_Rposition+3,column=0,columnspan=5)
    deleteRservB = Button(frame, text='Delete Reservation',command=partial(
                                    create_table,titles,"Managment: Delete Reservation",frame,sqlQuery,[manageRm,disReservations],True),
                                    fg='white',bg='red')
    deleteRservB.grid(row=last_Rposition+3,column=3,columnspan=5)

# capability 4 : display a list of dirty rooms and gives options to edit aviability
def disDirtyRoom(root):
    clearFrame(root)
    title= "Managment: Dirty Room List"
    names=['Room Number', 'Type', 'Status'] 
    sql_request = 'SELECT rmNum, type,status from room WHERE status IS NOT \'Available\''
    create_table(names,title,root,sql_request,[manageHouseKeep,disDirtyRoom]) # calls helper function to create table
