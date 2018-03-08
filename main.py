# -*- coding: utf-8 -*-

import json
import os
import sys
from time import sleep
from pprint import pprint #debug
from tkinter import font
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, RAISED, W, S, E, END
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
        # self.wm_iconbitmap(bitmap = "@list.XBM")
        img = tk.PhotoImage(file='./issupy.gif')
        self.tk.call('wm', 'iconphoto', self._w, img)

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

        self.style = ttk.Style()
        self.style_bg = ''
        self.style_fg = ''
        data = json.load(open('config.json', encoding='utf-8'))
        self.loadSettings(data, self.status)

        self.appFrame = Application(self, self.status, self.style_bg, self.style_fg)
        self.appFrame.pack(side='top', fill='both', expand='True')
        
    def loadSettings(root, jsondata, statusbar):
        root.default_font = font.nametofont("TkDefaultFont")
        root.default_font.configure(size=int(jsondata["fontsize"]))
        root.winfo_toplevel().title("Issupy - "+str(jsondata["user"]))
        root.style = ttk.Style()
        root.style.configure('Issupy.TFrame', background=str(jsondata["background"]))
        statusbar.set("Settings loaded. User: "+jsondata["user"]+", Repo: "+jsondata["repo"]+", Token: "+jsondata["token"]+"")
        root.style_bg = jsondata["background"]
        root.style_fg = jsondata["foreground"]
        # Application.listboxIssues.config('bg='+str(jsondata["background"]))
        # Application.listboxIssues.config('fg='+str(jsondata["foreground"]))
        sleep(0.5)
        statusbar.set("Idle.")

    




class MenuBar(tk.Menu):
    def __init__(self, parent, statusbar):
        tk.Menu.__init__(self, parent)

        filemenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=filemenu)
        filemenu.add_command(label="New", command=self.openNewIssueWindow, accelerator="Ctrl+N")
        filemenu.add_separator()
        filemenu.add_command(label="Reload Config", command=lambda:self.reloadConfig(parent, statusbar), accelerator="Ctrl+R")
        filemenu.add_command(label="Settings", command=self.openSettingsWindow, accelerator="Ctrl+O")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", underline=1, command=self.quit, accelerator="Ctrl+Q")

        helpmenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self.openAboutWindow)
        helpmenu.add_command(label="License", command=self.openAboutWindow)
        helpmenu.add_command(label="Debug info", command=self.openDebugWindow)

    def quit(self):
        sys.exit(0)
    
    def callback(self):
        print("called the callback!")

    def reloadConfig(self, parent, statusbar):
        Application.getConfig(self, parent, statusbar)

    def openAboutWindow(self):
        aboutWin = AboutWindow()
        aboutWin.mainloop()
        # aboutWin = ExampleWindow()

    def openDebugWindow(self):
        debugWin = DebugWindow()
        debugWin.mainloop()
    
    def openSettingsWindow(self):
        settingsWin = SettingsWindow()
        settingsWin.mainloop()

    def openNewIssueWindow(self):
        newIssueWin = NewIssueWindow()
        newIssueWin.mainloop()





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
    def __init__(self, root, statusbar, style_bg, style_fg):
        ttk.Notebook.__init__(self, root)

        tab1 = ttk.Frame(self, style='Issupy.TFrame')
        tab2 = ttk.Frame(self, style='Issupy.TFrame')
        tab3 = ttk.Frame(self, style='Issupy.TFrame')
        tab1.grid_columnconfigure(0, weight=1)
        tab1.grid_rowconfigure(0, weight=1)
        tab2.grid_columnconfigure(0, weight=1)
        tab2.grid_rowconfigure(0, weight=1)
        tab3.grid_columnconfigure(0, weight=1)
        tab3.grid_rowconfigure(0, weight=1)
        
        self.add(tab1, text = "Open")
        self.add(tab2, text = "Closed")
        self.add(tab3, text = "Labels")

        # emptySpacer = Label(tab1, text="     ").grid(row=0, column=0)
        '''
        Get config file
        '''
        #self.getConfig(root, statusbar)

        '''
        Tab 1 content
        '''
        listboxIssues = tk.Listbox(
            tab1,
            #font=appFont,
            selectmode=tk.SINGLE, activestyle='none',
            bg=str(style_bg), fg=str(style_fg)
        )
        listboxIssues.grid(row=0, column=0, sticky=W+E+N+S)
        self.getIssues(statusbar, listboxIssues)

        '''
        Tab 2 content
        '''

        '''
        Tab 3 content
        '''



        '''
        Keybindings
        '''
        self.bind("<Control-n>", self.keyEventNewIssue)
        listboxIssues.bind("<Control-n>", self.keyEventNewIssue)
        listboxIssues.bind("<Double-Button-1>", self.keyEventOpenIssue)

        
    def getConfig(self, root, statusbar):
        data = json.load(open('config.json', encoding='utf-8'))
        Root.loadSettings(root, data, statusbar)
        # tk.messagebox.showinfo("Configuration", "Config file successfully reloaded.\n\nUser:\n"+user+"\n\nRepository:\n"+repo+"\n\nPersonal Access Token:\n"+token)

    def getIssues(self, statusbar, listboxIssues):
        statusbar.set("Loading issues from Github, please wait...")
        data = json.load(open('test_issues.json', encoding='utf-8'))
        for issue in data:
            issueTxt = "#"+str(issue["number"])+": "+str(issue["title"])+" - "+str(issue["user"]["login"])
            listboxIssues.insert(END, issueTxt)
            statusbar.set('Fetching "'+str(issue["title"])+'"...')
            # sleep(0.01)
        statusbar.set('Idle.')
        self.update_idletasks()
        # pprint(data)

    def keyEventNewIssue(event, bla):
        newIssueWin = NewIssueWindow()
        newIssueWin.mainloop()

    def keyEventOpenIssue(self, event):
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        print( "selection:", selection, ": '%s'" % value )









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
        
        








class SettingsFrame(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root)
        data = json.load(open('config.json', encoding='utf-8'))
        print("Debug SettingsFrame")
        pprint(data)

        lblUser = Label(root, text="Username")
        lblUser.grid(row=0, column=0, sticky=W)

        lblRepo = Label(root, text="Repository")
        lblRepo.grid(row=1, column=0, sticky=W)

        lblPAT = Label(root, text="Personal Access Token")
        lblPAT.grid(row=2, column=0, sticky=W)

        lblFontsize = Label(root, text="Fontsize")
        lblFontsize.grid(row=3, column=0, sticky=W)

        lblBackground = Label(root, text="Background")
        lblBackground.grid(row=4, column=0, sticky=W)

        lblForeground = Label(root, text="Foreground")
        lblForeground.grid(row=5, column=0, sticky=W)

        entryUser = Entry(root, width=50)
        entryUser.grid(row=0, column=1, padx=5, pady=5)
        entryUser.insert(0, str(data["user"]))

        entryRepo = Entry(root, width=50)
        entryRepo.grid(row=1, column=1, padx=5, pady=5)
        entryRepo.insert(0, str(data["repo"]))

        entryPAT = Entry(root, width=50)
        entryPAT.grid(row=2, column=1, padx=5, pady=5)
        entryPAT.insert(0, str(data["token"]))

        entryFontsize = Entry(root, width=50)
        entryFontsize.grid(row=3, column=1, padx=5, pady=5)
        entryFontsize.insert(0, str(data["fontsize"]))

        entryBackground = Entry(root, width=50)
        entryBackground.grid(row=4, column=1, padx=5, pady=5)
        entryBackground.insert(0, str(data["background"]))

        entryForeground = Entry(root, width=50)
        entryForeground.grid(row=5, column=1, padx=5, pady=5)
        entryForeground.insert(0, str(data["foreground"]))

        lblResult = Label(root, text="")
        lblResult.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        buttonSave = Button(root, text="Save", width=70, command=lambda:root.saveSettings({
            "user":entryUser.get(),
            "repo":entryRepo.get(),
            "token":entryPAT.get(),
            "fontsize":entryFontsize.get(),
            "background":entryBackground.get(),
            "foreground":entryForeground.get(),
            }, lblResult))
        buttonSave.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        buttonSave = Button(root, text="Close", width=70, command=root.closeButton)
        buttonSave.grid(row=8, column=0, columnspan=2, padx=5, pady=5)


class SettingsWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("Settings")
        center(self, 460, 300)
        self.frame = SettingsFrame(self)

    def saveSettings(self, data, label):
        with open('config.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile)
        label.config(text='Saved')
        label.update_idletasks()
        sleep(0.5)
        label.config(text='')
        label.update_idletasks()

    def closeButton(self):
        self.destroy()












     








class NewIssueFrame(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root)

        Label(root, text='title').grid(row=0, column=0, sticky=W)
        Label(root, text='body').grid(row=1, column=0, sticky=W)
        Label(root, text='labels[]').grid(row=2, column=0, sticky=W)
        Label(root, text='milestone').grid(row=3, column=0, sticky=W)
        Label(root, text='assignees[]').grid(row=4, column=0, sticky=W)
        Label(root, text='status').grid(row=5, column=0, sticky=W)
        
        entryTitle = Entry(root, width=50)
        entryTitle.grid(row=0, column=1, padx=5, pady=5)

        entryBody = Text(root, width=38, height=8)
        entryBody.grid(row=1, column=1, padx=5, pady=5)

        entryLabels = Entry(root, width=50)
        entryLabels.grid(row=2, column=1, padx=5, pady=5)

        entryMilestone = Entry(root, width=50)
        entryMilestone.grid(row=3, column=1, padx=5, pady=5)

        entryAssignees = Entry(root, width=50)
        entryAssignees.grid(row=4, column=1, padx=5, pady=5)

        entryStatus = Entry(root, width=50)
        entryStatus.grid(row=5, column=1, padx=5, pady=5)

        lblResult = Label(root, text="")
        lblResult.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        buttonSave = Button(root, text="Save", width=70, command=lambda:root.saveNewIssue({
            "title":entryTitle.get(),
            "body":entryBody.get("1.0",END),
            "labels":entryLabels.get(),
            "milestone":entryMilestone.get(),
            "assignees":entryAssignees.get(),
            "status":entryStatus.get(),
            }, lblResult))
        buttonSave.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        buttonSave = Button(root, text="Close", width=70, command=root.closeButton)
        buttonSave.grid(row=8, column=0, columnspan=2, padx=5, pady=5)


class NewIssueWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("New issue")
        center(self, 450, 400)
        self.frame = NewIssueFrame(self)

    def saveNewIssue(self, data, label):
        '''
        with open('config.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile)
        '''
        label.config(text='Not Implemented')
        label.update_idletasks()
        sleep(0.5)
        label.config(text='')
        label.update_idletasks()

    def closeButton(self):
        self.destroy()






root = Root()
root.mainloop()
root.iconbitmap("./issupy.ico")