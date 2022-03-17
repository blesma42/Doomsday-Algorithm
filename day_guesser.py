import random
from datetime import timedelta, date
import tkinter as tk
import time
import os

class RandomDate:
    # creates a random date between some limits 
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
        self.day_of_week = self.random_date.weekday() #0=Monday, 1=Tuesday, ..., 6=Sunday 

class Timer():
    def __init__(self):
        self.start_time = time.time()
    
    def total_time(self):
        self.end_time = time.time()
        self.time_difference = round(self.end_time-self.start_time, 4)
        self.start_time = time.time()
        return self.time_difference

class ResultSaver():
    def __init__(self):

        self.filename = "Doomsday.csv"
        file_exists = os.path.exists(self.filename)
        if not file_exists:
            with open(self.filename, 'w') as file:
                file.write('index, session, date, day_of_week, guess, time\n') #adding header
            self.session = 1
            self.index = 0
        else:
            with open(self.filename, 'r') as file:
                last_line = file.readlines()[-1]
            values = last_line.split(sep=', ')
            self.session = int(values[0])+1
            self.index = int(values[1])+1

    def add_result(self, date, day_of_week, guess, time):
        with open(self.filename, 'a') as file:
            file.write(f'{self.index}, {self.session}, {date}, {day_of_week}, {guess}, {time}\n')
        self.index += 1

class DoomsdayAlgorithm():
    def __init__(self):
        # window settings
        x_size = 700
        y_size = 350

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
        
        # text box with objective
        self.task_text = tk.Label(self.root, text="What's the day of the week for the following date?")
        self.task_text.config(font=("Arial", 12))
        self.task_text.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # textbox to display date
        self.index_text = tk.Label(self.root, text="day - month - year")
        self.index_text.config(font=("Arial", 10))
        self.index_text.place(relx=0.5, y=180, anchor=tk.CENTER)
        # variable field for updating when new date is created
        self.date = tk.StringVar()
        self.date.set(self.date_to_guess.date_string)

        # textbox with labaling for date
        self.date_text = tk.Label(self.root, textvariable=self.date)
        self.date_text.config(font=("Arial", 15))
        self.date_text.place(relx=0.5, y=150, anchor=tk.CENTER)

        # list for labeling buttons
        days_of_week=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        #fake imagae to enable size by pixel
        pixelVirtual = tk.PhotoImage(width=1, height=1)

        #buttons
        y=300
        button_width = 85
        x=(x_size-7*button_width)/2+button_width/2
        
        day_number=0

        self.list_of_buttons = [] # list to store buttons
        for day in days_of_week:
            self.list_of_buttons.append(tk.Button(self.root, text=day, image=pixelVirtual, width=button_width-10, height=30, compound="c", bg='#d9d9d9', command=lambda i=day_number: self.button_hit(i)))

            self.list_of_buttons[day_number].place(x=x, y=y, anchor=tk.CENTER)

            x+=85
            day_number+=1
        self.root.mainloop()

    def button_hit(self, guess):
        # color of button indicates result
        self.button_coloring(guess)
        
        self.time = self.timer.total_time()
        
        self.saver.add_result(self.date_to_guess.random_date, self.date_to_guess.day_of_week, guess, self.time)

        # new date
        self.date_to_guess.create_random_date()
        self.date.set(self.date_to_guess.date_string)

    def button_coloring(self, guess):
        # coulering buttons based on results
        for button in self.list_of_buttons:
            button.configure(bg='#d9d9d9') # gray for all buttons
        self.list_of_buttons[guess].configure(bg='#ff4d4d') # red for wrong button
        self.list_of_buttons[self.date_to_guess.day_of_week].configure(bg='#99ff66') # green for correct button
    

app = DoomsdayAlgorithm()