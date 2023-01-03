import tkinter as tk
import webbrowser

root = tk.Tk()


def open_link(event):
    webbrowser.open('http://127.0.0.1:8080/')


label = tk.Label(root, text='Open link', fg='blue', cursor='hand2')
label.pack()
label.bind('<1>', open_link)

root.mainloop()
