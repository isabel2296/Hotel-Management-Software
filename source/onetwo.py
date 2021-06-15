# Marco Botello
# Capability 1: Screen that shows all rooms and their current status.
# Capability 2: Screen showing a list of the rooms and who is staying in the room for each day for the next 7 days. 

import logging
import tkinter as tk
from tkinter import * 
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import sqlite3
import fivesix as fs
import commands as cmd
from functools import partial

headers=['Room','Type', 'Status']
con=sqlite3.connect(database='sql\hotel.db')
cur=con.cursor();

#Placeholder
weekHeaders=['Room #','5/7','5/8','5/9','5/10', '5/11', '5/12', '5/13']

rooms = cur.execute('SELECT rmNum from room')
rooms = cur.fetchall()
roomList = rooms

#Uncomment to reset room statuses
# con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Available', 1))
# con.commit()
# con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Available', 2))
# con.commit()
# con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Dirty', 3))
# con.commit()
# con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Maintenance', 4))
# con.commit()
# con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Available', 5))
# con.commit()
# con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Dirty', 6))
# con.commit()
# con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Maintenance', 7))
# con.commit()
# con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Available', 8))
# con.commit()
# con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Available', 9))
# con.commit()
# con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Available', 10))
# con.commit()



''' helper functions '''
def clearFrame(frame): #clears the frame
    for i in frame.winfo_children(): 
        i.destroy()

def updateList():
    listallrooms = cur.execute('SELECT rmNum, type,status from room')
    listallrooms = cur.fetchall()
    Lists = listallrooms
    return Lists

#Capability #1, Displays list of rooms and status of each
def roomStatus(frame):
    clearFrame(frame)
    name = Label(frame, text="Rooms List\n Click 'Room Statuses' above to refresh.",font=('calibre',12,'bold'))
    name.pack(side=TOP)
    listbox = MultiColumnListbox(frame)
    guestStayInfoButton = Button(frame, text="This Week's Info", fg = 'black', bg='lime', command=thisWeek)
    guestStayInfoButton.pack(side=BOTTOM)

#Capability #2, Display list of rooms and who is staying in them over 7 days
def thisWeek():
    thisWeekWin = Toplevel()
    thisWeekWin.title("Next 7 Days Stay Info")

    weekTree=ttk.Treeview(thisWeekWin)
    weekTree["columns"]=("one","two","three","four","five","six","seven","eight")
    weekTree.column("#0", width=0, stretch=tk.NO)
    weekTree.column("one", width=150, minwidth=150, stretch=tk.NO)
    weekTree.column("two", width=150, minwidth=200, stretch=tk.NO)
    weekTree.column("three", width=150, minwidth=50, stretch=tk.NO)
    weekTree.column("four", width=150, minwidth=150, stretch=tk.NO)
    weekTree.column("five", width=150, minwidth=200, stretch=tk.NO)
    weekTree.column("six", width=150, minwidth=50, stretch=tk.NO)
    weekTree.column("seven", width=150, minwidth=50, stretch=tk.NO)
    weekTree.column("eight", width=150, minwidth=50, stretch=tk.NO)


    weekTree.heading("#0",text="",anchor=tk.W)
    weekTree.heading("one", text="Room #",anchor=tk.W)
    weekTree.heading("two", text="5/7",anchor=tk.W)
    weekTree.heading("three", text="5/8",anchor=tk.W)
    weekTree.heading("four",text="5/9",anchor=tk.W)
    weekTree.heading("five", text="5/10",anchor=tk.W)
    weekTree.heading("six", text="5/11",anchor=tk.W)
    weekTree.heading("seven", text="5/12",anchor=tk.W)
    weekTree.heading("eight", text="5/13",anchor=tk.W)

    for item in rooms:
        weekTree.insert('','end',values=item)
    weekTree.pack(side=tk.TOP,fill=tk.X)
    
    def selectItem(a):
        filledIn= Toplevel()
        filledIn.title("Guest in this room")

        makereserve = Toplevel()
        makereserve.title("Make a Reservation")
        #Focus on currently selected
        curItem = weekTree.focus()
        rmNum = weekTree.item(curItem)['values']

        #Fetch status and names
        status = cur.execute('SELECT status FROM room WHERE rmNum=?',(rmNum))
        status= cur.fetchone()
        fullName = cur.execute('SELECT firstname, lastName FROM guest as g INNER JOIN reservation as r ON g.guestID = r.guestID WHERE r.rmNum = ? ', (rmNum))
        fullName = cur.fetchone()
        fName = fullName[0]
        lName = fullName[1]

        #For testing
        # print(fName)
        # print(lName)

        # If Room is occupied, show guest info (capability 6)
        if status == 'Occupied':
            fs.guestStayInfo(partial(filledIn,fName,lName,rmNum))

        #If Room is available (no reservervation) open capability 3
        if status == 'Available':
            cmd.disReservations(partial(makereserve))

        
    weekTree.bind('<ButtonRelease-1>', selectItem)


class MultiColumnListbox(object):
    #use a ttk.TreeView as a multicolumn ListBox
    
    def __init__(self,master):
        self.tree = None
        self.master = master
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="green", background="white")


        msg = ttk.Label(self.master, wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6))
        msg.pack(fill='x')
        global container 
        container = ttk.Frame(self.master)
        container.pack(fill='both', expand=True)
        
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(self.master, columns=headers, show="headings")
        vsb = ttk.Scrollbar(self.master, orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(self.master, orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        #click on item to recieve all values in row
        def selectItem(a):
            curItem = self.tree.focus()
            print('This room is ' + self.tree.item(curItem)['values'][2])
            rmNum = self.tree.item(curItem)['values'][0]
            rmType = self.tree.item(curItem)['values'][1]
            rmStatus = self.tree.item(curItem)['values'][2]
            if rmStatus == 'Dirty' or rmStatus=='Maintenance':
                unavailableRoomClicked(rmNum,rmStatus)

            if rmStatus == 'Available':
                window = Toplevel()
                window.title("Guest Stay Info")
                fs.guestStayInfo(window, rmNum)
                con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Occupied', rmNum))
                con.commit()

            if rmStatus == 'Occupied':
                newWindow = Toplevel()
                newWindow.title("Guest Stay Info")
                fs.guestStayInfo(newWindow,rmNum)
                con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Dirty', rmNum))
                con.commit()

        self.tree.bind('<ButtonRelease-1>', selectItem)
      

    def _build_tree(self):
        Lists = updateList()
        for col in headers:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in Lists:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(headers[ix],width=None)<col_w:
                    self.tree.column(headers[ix], width=col_w)

           

def sortby(tree, col, descending):
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    # data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))


def changetoAvailable(rmNum):
    con.execute('UPDATE room SET status = ? WHERE rmNum = ?', ('Available', rmNum))
    con.commit()

def unavailableRoomClicked(rmNum,rmStatus):
    unavailableRoom = tk.Toplevel()
    unavailableRoom.wm_title('Warning!')
    unavailableRoom.geometry('450x100')

    #Dirty -> Available or stays as is
    if rmStatus == 'Dirty':
        header = tk.Label(unavailableRoom, text="Room #" + str(rmNum) + " is Dirty. Would you like to set it as available?\n You may close this window after you've made a choice.",fg='red',font=('calibre',12,'bold'))
        header.grid(row=0,column=0)
        yesBtn = tk.Button(unavailableRoom,text="Yes",command= partial(changetoAvailable,rmNum), bg='lightgreen', width=20)
        yesBtn.place(x=45,y=50)
        noBtn = tk.Button(unavailableRoom,text="No", command= unavailableRoom.destroy, bg='red', width=20)
        noBtn.place(x=245,y=50)

    #Maintenance -> Available or stays as is
    if rmStatus == 'Maintenance':
        unavailableRoom.geometry('550x100')
        header = tk.Label(unavailableRoom, text="Room #" + str(rmNum) + " is under Maintenance. Would you like to set it as available?\n You may close this window after you've made a choice.",fg='red',font=('calibre',12,'bold'))
        header.grid(row=0,column=0)
        yesBtn = tk.Button(unavailableRoom,text="Yes",command= partial(changetoAvailable,rmNum), bg='lightgreen', width=20)
        yesBtn.place(x=45,y=50)
        noBtn = tk.Button(unavailableRoom,text="No", command= unavailableRoom.destroy, bg='red', width=20)
        noBtn.place(x=300,y=50)
    

    
   