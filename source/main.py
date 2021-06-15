# Hotel Project CPSC 463Members: 
#   Isabel Silva
#   Bryan Monh
#   Marco Botello

import commands as c
import fivesix as d
import onetwo as e
from commands import *
import random 
'''
following button menu got the idea from 
https://www.python-course.eu/tkinter_layout_management.php
'''
def buttomMenu(window): 
    
    frame = Frame(window) #frame to hold buttons
    frame.pack(side=TOP)

    #frame2 = Frame(window,width=700,height=480,
    #    bg='white',borderwidth=2,relief='sunken') #frame to hold views
    frame2 = Frame(window,width=700,height=480)
    frame2.pack(side = TOP)
    
    '''
    The following is to add your button to the button menu
    '''
    #place name of command here, this will show on the button 
    languages = ['Reservations','Dirty Room List', "Guest Info", "Guest Stay Info", "Room Statuses"]
    #place name of function for the command; this will call the function 
    #when our button is pressed
    comName = ['c.disReservations','c.disDirtyRoom', 'd.guestInfo', 'd.guestStayInfo', 'e.roomStatus']

    for i in range(len(languages)):
        buttons = Button(frame, 
                        text=languages[i], 
                        fg='black' , 
                        bg='light blue',
                        command = partial(eval(comName[i]),frame2))
        buttons.pack(expand= True, fill=BOTH, side = LEFT)
        #buttons.place(x = 20, y = 30 + i*30, width=120, height=25)
    
            
# shows the main screen able to switch between capability
class mainScreen(Tk):
    def __init__(self):
        Tk.__init__(self) #creates a window
        # name of window
        self.title("Hotel")
        self.geometry("700x500") # size of screen
        buttomMenu(self)


'''
need to create a grid that will allow us to view the 
results to the right of the buttons; look up frames, grid, for tkinter
'''
    

if __name__ == '__main__':
    app = mainScreen()
    app.mainloop()
    