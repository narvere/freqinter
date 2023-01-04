# Import Required Library
from tkinter import *
from tkcalendar import Calendar

# Create Object
root = Tk()

# Set geometry
root.geometry("400x400")

# Add Calendar
cal = Calendar(root, selectmode='day', year=2022, month=1, day=1)

cal.pack(pady=20)


def grad_date():
    user_date = cal.get_date().split('/')
    if int(user_date[0]) >= 10:
        date1 = '20' + user_date[2] + user_date[1] + user_date[0]
    else:
        date1 = '20' + user_date[2] + user_date[1] + '0' + user_date[0]
    print(date1)
    return date1

    # date.config(text="Selected Date is: " + date1)


# Add Button and Label
Button(root, text="Get Date",
       command=grad_date).pack(pady=20)

date = Label(root, text="")
date.pack(pady=20)

# Execute Tkinter
root.mainloop()
