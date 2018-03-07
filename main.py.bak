import json
import os
from pprint import pprint #debug
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


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

        #initialize menu
        self.config(menu=MenuBar(self))
        
        self.appFrame = Application(self)
        self.appFrame.pack(side='top', fill='both', expand='True')
        
        self.status = StatusBar(self)
        self.status.pack(side='bottom', fill='x')
        self.status.set('Issupy initialized.')
        



class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        filemenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=filemenu)
        filemenu.add_command(label="New", command=self.callback)
        filemenu.add_command(label="Reload config", command=self.reloadConfig)
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

    def reloadConfig(self):
        Application.getConfig(self)

    def openAboutWindow(self):
        aboutWin = AboutWindow()
        aboutWin.mainloop()

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
    def __init__(self, root):
        ttk.Notebook.__init__(self, root)
        
        tab1 = ttk.Frame(self)
        tab2 = ttk.Frame(self)
        tab3 = ttk.Frame(self)
        
        self.add(tab1, text = "Open")
        self.add(tab2, text = "Closed")
        self.add(tab3, text = "Labels")

    def getConfig(self):
        data = json.load(open('config.json'))
        pprint(data)
        user = data["user"]
        repo = data["repo"]
        token = data["token"]
        tk.messagebox.showinfo("Configuration", "Config file successfully reloaded.\n\nUser:\n"+user+"\n\nRepository:\n"+repo+"\n\nPersonal Access Token:\n"+token)
        
        # StatusBar.set(root, 'Config file successfully reloaded.')

        self.status = StatusBar(self)
        self.status.pack(side='bottom', fill='x')
        self.status.set("Config file successfully reloaded.")






class AboutWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("About Issupy")
        center(self, 300, 100)
        # self.appFrame = Application(self)
        # self.appFrame.pack(side='top', fill='both', expand='True')
        



class DebugWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("Debug info")
        center(self, 400, 400)
        
        





root = Root()
root.mainloop()