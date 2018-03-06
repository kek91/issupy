import json
import os
import sys
from time import sleep
from pprint import pprint #debug
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, RAISED, W, S, E
from tkinter.ttk import Frame, Button, Label, Entry, Style

# https://api.github.com/user/repos?access_token=token
# https://api.github.com/repos/:user/:repo/issues?access_token=token

'''
API = {
    "repos":"https://api.github.com/user/repos?access_token=token",
    "issues":"https://api.github.com/user/repos?access_token=token"
}
'''

def center(win, width, height):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    # width = 600
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    # height = 400
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()






class Root(tk.Tk):
    """Container for all frames within the application"""
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.winfo_toplevel().title("Issupy")
        # self.geometry("400x300+800+800")
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        # self.geometry("400x300+%s+%s")
        # toplevel.winfo_screenwidth()
        center(self, 1024, 640)

        self.status = StatusBar(self)
        self.status.pack(side='bottom', fill='x')
        self.status.set('Issupy initialized.')
        
        self.config(menu=MenuBar(self, self.status))

        self.appFrame = Application(self, self.status)
        self.appFrame.pack(side='top', fill='both', expand='True')

        # Application.getIssues(self, self.status)

        




class MenuBar(tk.Menu):
    def __init__(self, parent, statusbar):
        tk.Menu.__init__(self, parent)

        filemenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=filemenu)
        filemenu.add_command(label="New", command=self.callback)
        filemenu.add_command(label="Reload config", command=lambda:self.reloadConfig(statusbar))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", underline=1, command=self.quit)

        helpmenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self.openAboutWindow)
        helpmenu.add_command(label="Debug info", command=self.openDebugWindow)

    def quit(self):
        sys.exit(0)
    
    def callback(self):
        print("called the callback!")

    def reloadConfig(self, statusbar):
        statusbar.set('Reloading config file...')
        Application.getConfig(self, statusbar)

    def openAboutWindow(self):
        aboutWin = AboutWindow()
        aboutWin.mainloop()
        # aboutWin = ExampleWindow()

    def openDebugWindow(self):
        debugWin = DebugWindow()
        debugWin.mainloop()





class StatusBar(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.label = ttk.Label(self, relief='sunken', anchor='w')
        self.label.pack(fill='x')

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()






class Application(ttk.Notebook):
    def __init__(self, root, statusbar):
        ttk.Notebook.__init__(self, root)

        tab1 = ttk.Frame(self)
        tab2 = ttk.Frame(self)
        tab3 = ttk.Frame(self)
        
        self.add(tab1, text = "Open")
        self.add(tab2, text = "Closed")
        self.add(tab3, text = "Labels")

        # tab1.pack(fill=BOTH, expand=False)
        # tab1.columnconfigure(1, weight=1)
        # tab1.columnconfigure(3, pad=7)
        # tab1.rowconfigure(3, weight=1)
        # tab1.rowconfigure(5, pad=7)
        
        lbl = Label(tab1, text="Issues...")
        lbl.grid(sticky=W, pady=4, padx=5)
        # area = Text(tab1)
        # area.grid(row=1, column=0, columnspan=2, rowspan=4, 
        #     padx=5, sticky=E+W+S+N)
        # abtn = Button(tab1, text="Activate")
        # abtn.grid(row=1, column=3)
        # hbtn = Button(tab1, text="Help")
        # hbtn.grid(row=5, column=0, padx=5)
        # obtn = Button(tab1, text="OK")
        # obtn.grid(row=5, column=3)

        self.getIssues(statusbar, lbl)

    def getConfig(self, statusbar):
        data = json.load(open('config.json'))
        pprint(data)
        user = data["user"]
        repo = data["repo"]
        token = data["token"]
        statusbar.set("Config reloaded. User: "+user+", Repo: "+repo+", Token: "+token+"")
        # tk.messagebox.showinfo("Configuration", "Config file successfully reloaded.\n\nUser:\n"+user+"\n\nRepository:\n"+repo+"\n\nPersonal Access Token:\n"+token)

    def getIssues(self, statusbar, label):
        label.labelText = 'Please wait, fetching issues...'
        data = json.load(open('test_issues.json'))
        i = 0
        for issue in data:
            print(issue["title"])
            statusbar.set('Fetching "'+str(issue["title"])+'"...')
            label.config(text = label.cget("text") + '\n' + str(issue["title"]))
            sleep(0.02)
        statusbar.set('Finish.')
        sleep(0.5)
        statusbar.set('Idle.')
        # label.config(text='change the value')
        self.update_idletasks()
        # pprint(data)
        # statusbar.set("Loading issues from Github, please wait...")






class AboutFrame(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root)
        self.pack(fill=BOTH, expand=True)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        lbl = Label(self, text="Windows")
        lbl.grid(sticky=W, pady=4, padx=5)
        area = Text(self)
        area.grid(row=1, column=0, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)
        abtn = Button(self, text="Activate")
        abtn.grid(row=1, column=3)
        cbtn = Button(self, text="Close", command = root.closeButton)
        cbtn.grid(row=2, column=3, pady=4)
        hbtn = Button(self, text="Help")
        hbtn.grid(row=5, column=0, padx=5)
        obtn = Button(self, text="OK")
        obtn.grid(row=5, column=3)

    

class AboutWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("About Issupy")
        center(self, 500, 250)
        self.frame = AboutFrame(self)
    def closeButton(self):
        self.destroy()




class DebugWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("Debug info")
        center(self, 400, 400)
        
        





root = Root()
root.mainloop()