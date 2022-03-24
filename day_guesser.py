from ast import Try
import random
from datetime import timedelta, date
import tkinter as tk
import time
import os

class RandomDate:
    '''creates a random date between some limits, and also determinates the day of the week for the date.''' 
    def __init__(self):
        #difference between lowest date and today is the same as distance between oday and highest date
        self.lowest_date = date(1582, 10, 15) #before this date the Julian calender was used instead of the Gregorian
        self.current_date = date.today()
        self.highest_date = self.current_date+timedelta(days=(self.current_date-self.lowest_date).days)

        self.create_random_date()

    def create_random_date(self):
        #creates an random date between lowest_date and highest_date
        self.random_date = self.lowest_date+timedelta(days=random.randint(0, (self.highest_date-self.lowest_date).days))
        self.date_string = self.random_date.strftime("%d - %m - %Y")
        self.day_of_week = self.random_date.isoweekday()%7 # 0=Sunday, 1=Monday, ... 

class Timer():
    '''Simple timer, starts when first called and returns the time passed in seconds since the last call.'''
    def __init__(self):
        self.start_time = time.time()
    
    def total_time(self):
        self.end_time = time.time()
        self.time_difference = round(self.end_time-self.start_time, 4)
        self.start_time = time.time()
        return self.time_difference

class ResultSaver():
    '''Creates an .csv file if not existent, and saves results from the gusss to the file'''
    def __init__(self):

        self.session = 1
        self.index = 0

        self.filename = "Doomsday.csv"
        file_exists = os.path.exists(self.filename)
        if not file_exists:
            with open(self.filename, 'w') as file:
                file.write('index,session,date_of_session,date_to_guess,day_of_week,guess,time\n') #adding header
        else:
            try:
                # creates an error if programm is opend on the secound time,
                # when it was closed on the first time without a first guess.
                with open(self.filename, 'r') as file:
                    last_line = file.readlines()[-1]
                values = last_line.split(sep=',')
                self.session = int(values[1])+1
                self.index = int(values[0])+1
            except ValueError:
                pass

    def add_result(self, date_of_session, date_to_guess, day_of_week, guess, time):
        with open(self.filename, 'a') as file:
            file.write(f'{self.index},{self.session},{date_of_session},{date_to_guess},{day_of_week},{guess},{time}\n')
        self.index += 1

class ShowText():
    '''Creates two text boxes beneath each other. The lower one shows static text, the upper one dynamic text.'''
  
    def __init__(self, root, string1, string2, fontsize, pos_x, pos_y):
        # testbox with static text 
        self.text = tk.Label(root, text=string1)
        self.text.config(font=("Arial", fontsize-6))
        self.text.place(relx=pos_x, y=pos_y+20, anchor=tk.CENTER)

        # text which changes during running
        self.dynamic_text_var = tk.StringVar()
        self.dynamic_text_var.set(string2)

        # textbox with dynamic text
        self.dynamic_text = tk.Label(root, textvariable=self.dynamic_text_var)
        self.dynamic_text.config(font=("Arial", fontsize))
        self.dynamic_text.place(relx=pos_x, y=pos_y, anchor=tk.CENTER)

    def update_text(self, new_text):
        self.dynamic_text_var.set(new_text)

class DoomsdayAlgorithm():
    '''GUI for traning the doomsday alghorithm.
    Shows date, session counter, and buttons to select the day of the week.'''
    def __init__(self):
        # window size
        x_size = 700
        y_size = 350

        # general settings of the window
        self.root = tk.Tk()
        self.root.geometry(str(x_size)+'x'+str(y_size))
        self.root.resizable(False, False)
        self.root.title('Doomsday Algorithm')

        # create random date
        self.date_to_guess = RandomDate()

        # timer to stop time in ms
        self.timer = Timer() 
        
        # saves the results
        self.saver = ResultSaver() 
        
        # shows text with objective
        task = "What's the day of the week for the following date?"
        self.date_text = ShowText(self.root, '', task, 14, 0.5, 45)

        # shows date to guess
        self.date_text = ShowText(self.root, "day - month - year", self.date_to_guess.date_string, 15, 0.5, 150)

        # shows guesses per session
        self.guess_count = 0
        self.counter_text = ShowText(self.root, "guesses", self.guess_count, 15, 0.92, 40)

        # list for labeling buttons
        days_of_week=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        #fake imagae to enable size by pixel
        pixelVirtual = tk.PhotoImage(width=1, height=1)

        #buttons
        y=300
        button_width = 85
        # caculates the x position of the first button so all buttons are centered
        x=(x_size-7*button_width)/2+button_width/2
        
        day_number = 0 # value of each day needed for buttons 

        self.list_of_buttons = [] # list to store buttons
        for day in days_of_week:
            # add buttons to list 
            self.list_of_buttons.append(tk.Button(self.root, text=day, image=pixelVirtual, width=button_width-10, height=30, compound="c", bg='#d9d9d9', command=lambda i=day_number: self.button_hit(i)))

            # specifies the position of the buttons
            self.list_of_buttons[day_number].place(x=x, y=y, anchor=tk.CENTER)

            x+=85 # shift x position for next button
            day_number+=1
        self.root.mainloop()

    def button_hit(self, guess):
        # color of button indicates result
        self.button_coloring(guess)

        # gets the time it took for the user to make the guess
        self.time = self.timer.total_time() 
        
        # saves results to file 
        self.saver.add_result(self.date_to_guess.current_date, self.date_to_guess.random_date, self.date_to_guess.day_of_week, guess, self.time)

        # increase and update guess counter
        self.guess_count+=1
        self.counter_text.update_text(self.guess_count)

        # creates new date an updates display
        self.date_to_guess.create_random_date()
        self.date_text.update_text(self.date_to_guess.date_string)

    def button_coloring(self, guess):
        # coulering buttons based on results
        for button in self.list_of_buttons:
            button.configure(bg='#d9d9d9') # gray for all buttons
        self.list_of_buttons[guess].configure(bg='#ff4d4d') # red for wrong button
        self.list_of_buttons[self.date_to_guess.day_of_week].configure(bg='#99ff66') # green for correct button

if __name__=='__main__':
    app = DoomsdayAlgorithm()