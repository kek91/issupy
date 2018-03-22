# -*- coding: utf-8 -*-

import json
import os
import sys
from time import sleep
import urllib.request
from pprint import pprint #debug
import webbrowser
from tkinter import font
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, RAISED, W, S, E, END
from tkinter.ttk import Frame, Button, Label, Entry, Style
from tkinter.colorchooser import *

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


def restartApp():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def syncRepo(statusbar):
    settings = json.load(open('config.json', encoding='utf-8'))
    try:
        statusbar.set("Cleaning issues...")
        statusbar.update_idletasks()
        os.remove('./.cache/issues_'+settings['repo']+'.json')
        statusbar.set("Cleaning closed issues...")
        statusbar.update_idletasks()
        os.remove('./.cache/closed_issues_'+settings['repo']+'.json')
        statusbar.set("Cleaning labels...")
        statusbar.update_idletasks()
        os.remove('./.cache/labels_'+settings['repo']+'.json')
        statusbar.set("Cleaning milestones...")
        statusbar.update_idletasks()
        os.remove('./.cache/milestones_'+settings['repo']+'.json')
        statusbar.set("Cleaning contributors...")
        statusbar.update_idletasks()
        os.remove('./.cache/contributors_'+settings['repo']+'.json')
        restartApp()
    except OSError as e:
        statusbar.set("Sync error: "+e.strerror+". Try again later...")
        statusbar.update_idletasks()
def syncRepoIssues(statusbar):
    settings = json.load(open('config.json', encoding='utf-8'))
    try:
        statusbar.set("Cleaning issues...")
        statusbar.update_idletasks()
        os.remove('./.cache/issues_'+settings['repo']+'.json')
        statusbar.set("Cleaning closed issues...")
        statusbar.update_idletasks()
        os.remove('./.cache/closed_issues_'+settings['repo']+'.json')
        restartApp()
    except OSError as e:
        statusbar.set("Sync error: "+e.strerror+". Try again later...")
        statusbar.update_idletasks()

def colorPicker(self):
    color = askcolor(parent=self)
    return color[1]


def getIssueData(id, data):
    settings = json.load(open('config.json', encoding='utf-8'))
    jsondata = json.load(open('./.cache/'+data+'_'+str(settings['repo'])+'.json', encoding='utf-8'))
    if data == 'issues':
        for i in jsondata:
            if str(i["number"]) == str(id):
                return i
    else:
        return jsondata
        









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
        center(self, 1366, 768)

        self.status = StatusBar(self)
        self.status.pack(side='bottom', fill='x')
        self.status.set('Issupy initialized.')
        
        self.config(menu=MenuBar(self, self.status))

        self.style = ttk.Style()
        self.style_bg = ''
        self.style_fg = ''
        try:
            data = json.load(open('config.json', encoding='utf-8'))
            self.loadSettings(data, self.status)
            self.appFrame = Application(self, self.status, self.style_bg, self.style_fg)
            self.appFrame.pack(side='top', fill='both', expand='True')
        except:
            tk.messagebox.showerror("Error", "Error occured while instantiating Application frame.\n\nCheck config.json for errors.")
            self.status.set('Error occured while instantiating Application frame. Check config.json for errors.')
        
    def loadSettings(root, jsondata, statusbar):
        root.default_font = font.nametofont("TkDefaultFont")
        root.default_font.configure(size=int(jsondata["fontsize"])) #, family="Verdana")
        root.winfo_toplevel().title("Issupy - "+str(jsondata["user"])+"/"+str(jsondata["repo"]))
        root.style = ttk.Style()
        root.style.configure('Issupy.TFrame', background=str(jsondata["background"]))
        # root.style.configure('Issupy.TNotebook', background=str(jsondata["background"]), tabposition='')
        root.style.configure("Issupy.TNotebook.Tab", foreground='#444')
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
        filemenu.add_command(label="New issue", command=self.openNewIssueWindow, accelerator="Ctrl+N")
        filemenu.add_separator()
        filemenu.add_command(label="Settings", command=self.openSettingsWindow)
        filemenu.add_separator()
        filemenu.add_command(label="Resync issues", command=lambda:self.callSyncRepoIssues(parent, statusbar))
        filemenu.add_command(label="Resync all data", command=lambda:self.callSyncRepo(parent, statusbar))
        #filemenu.add_command(label="Reload config", command=lambda:self.reloadConfig(parent, statusbar))
        filemenu.add_command(label="Restart app", command=restartApp, accelerator="Ctrl+R")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", underline=1, command=self.quit, accelerator="Ctrl+Q")

        helpmenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self.openAboutWindow)
        helpmenu.add_command(label="License", command=self.openLicenseWindow)
        helpmenu.add_separator()
        helpmenu.add_command(label="Debug info", command=self.openDebugWindow)
        helpmenu.add_separator()
        helpmenu.add_command(label="Help/tutorial (Web)", command=self.openWiki)
        helpmenu.add_command(label="Issue tracker (Web)", command=self.openIssueTracker)

    def quit(self):
        sys.exit(0)
    
    def callback(self):
        print("called the callback!")

    def callSyncRepo(self, parent, statusbar):
        syncRepo(statusbar)
    def callSyncRepoIssues(self, parent, statusbar):
        syncRepoIssues(statusbar)


    def reloadConfig(self, parent, statusbar):
        Application.getConfig(self, parent, statusbar)

    def openAboutWindow(self):
        aboutWin = AboutWindow()
        aboutWin.mainloop()
        # aboutWin = ExampleWindow()
    
    def openLicenseWindow(self):
        licenseWin = LicenseWindow()
        licenseWin.mainloop()

    def openDebugWindow(self):
        debugWin = DebugWindow()
        debugWin.mainloop()
    
    def openSettingsWindow(self):
        settingsWin = SettingsWindow()
        settingsWin.mainloop()

    def openNewIssueWindow(self):
        newIssueWin = NewIssueWindow()
        newIssueWin.mainloop()

    def openIssueTracker(self):
        webbrowser.open("https://github.com/kek91/issupy/issues")
    
    def openWiki(self):
        webbrowser.open("https://github.com/kek91/issupy/wiki")












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
        ttk.Notebook.__init__(self, root, style='Issupy.TNotebook')

        tab1 = ttk.Frame(self, style='Issupy.TFrame')
        tab2 = ttk.Frame(self, style='Issupy.TFrame')
        tab3 = ttk.Frame(self, style='Issupy.TFrame')
        tab4 = ttk.Frame(self, style='Issupy.TFrame')
        tab5 = ttk.Frame(self, style='Issupy.TFrame')
        tab6 = ttk.Frame(self, style='Issupy.TFrame')
        tab7 = ttk.Frame(self, style='Issupy.TFrame')
        tab8 = ttk.Frame(self, style='Issupy.TFrame')
        tab1.grid_columnconfigure(0, weight=1)
        tab1.grid_rowconfigure(0, weight=1)
        tab2.grid_columnconfigure(0, weight=1)
        tab2.grid_rowconfigure(0, weight=1)
        tab3.grid_columnconfigure(0, weight=1)
        tab3.grid_rowconfigure(0, weight=1)
        tab4.grid_columnconfigure(0, weight=1)
        tab4.grid_rowconfigure(0, weight=1)
        tab5.grid_columnconfigure(0, weight=1)
        tab5.grid_rowconfigure(0, weight=1)
        tab6.grid_columnconfigure(0, weight=1)
        tab6.grid_rowconfigure(0, weight=1)
        tab7.grid_columnconfigure(0, weight=1)
        tab7.grid_rowconfigure(0, weight=1)
        tab8.grid_columnconfigure(0, weight=1)
        tab8.grid_rowconfigure(0, weight=1)
        
        self.add(tab1, text = "Open")
        self.add(tab2, text = "Closed")
        self.add(tab3, text = "Labels")
        self.add(tab4, text = "Milestones")
        self.add(tab5, text = "Contributors")
        self.add(tab6, text = "My Repositories (Public)")
        self.add(tab7, text = "My Repositories (Private)")
        self.add(tab8, text = "Notepad")

        listboxIssues = tk.Listbox(
            tab1,
            #font=appFont,
            selectmode=tk.SINGLE, activestyle='none',
            bg=str(style_bg), fg=str(style_fg)
        )
        listboxIssues.grid(row=0, column=0, sticky=W+E+N+S)

        listboxIssuesClosed = tk.Listbox(
            tab2,
            selectmode=tk.SINGLE, activestyle='none',
            bg=str(style_bg), fg=str(style_fg)
        )
        listboxIssuesClosed.grid(row=0, column=0, sticky=W+E+N+S)

        listboxLabels = tk.Listbox(
            tab3,
            selectmode=tk.SINGLE, activestyle='none',
            bg=str(style_bg), fg=str(style_fg)
        )
        listboxLabels.grid(row=0, column=0, sticky=W+E+N+S)

        listboxMilestones = tk.Listbox(
            tab4,
            selectmode=tk.SINGLE, activestyle='none',
            bg=str(style_bg), fg=str(style_fg)
        )
        listboxMilestones.grid(row=0, column=0, sticky=W+E+N+S)

        listboxContributors = tk.Listbox(
            tab5,
            selectmode=tk.SINGLE, activestyle='none',
            bg=str(style_bg), fg=str(style_fg)
        )
        listboxContributors.grid(row=0, column=0, sticky=W+E+N+S)

        listboxRepositories = tk.Listbox(
            tab6,
            selectmode=tk.SINGLE, activestyle='none',
            bg=str(style_bg), fg=str(style_fg)
        )
        listboxRepositories.grid(row=0, column=0, sticky=W+E+N+S)

        listboxRepositoriesPrivate = tk.Listbox(
            tab7,
            selectmode=tk.SINGLE, activestyle='none',
            bg=str(style_bg), fg=str(style_fg)
        )
        listboxRepositoriesPrivate.grid(row=0, column=0, sticky=W+E+N+S)

        textNotepad = tk.Text(
            tab8,
            bg=str(style_bg), fg=str(style_fg)
        )
        textNotepad.grid(row=0, column=0, sticky=W+E+N+S)

        '''
        Fetch data for every tabs
        '''
        self.getData(statusbar, listboxIssues, 'issues')
        self.getData(statusbar, listboxIssuesClosed, 'closed_issues')
        self.getData(statusbar, listboxLabels, 'labels')
        self.getData(statusbar, listboxMilestones, 'milestones')
        self.getData(statusbar, listboxContributors, 'contributors')
        self.getData(statusbar, listboxRepositories, 'public_repos')
        self.getData(statusbar, listboxRepositoriesPrivate, 'private_repos')
        self.getData(statusbar, textNotepad, 'notepad')



        '''
        Keybindings
        '''
        self.bind("<Control-n>", self.keyEventNewIssue)
        listboxIssues.bind("<Control-n>", self.keyEventNewIssue)

        self.bind("<Control-r>", self.keyEventRestartApp)
        listboxIssues.bind("<Control-r>", self.keyEventRestartApp)
        
        self.bind("<Control-q>", self.keyEventQuitApp)
        listboxIssues.bind("<Control-q>", self.keyEventQuitApp)

        listboxIssues.bind("<Double-Button-1>", self.keyEventOpenIssue)
        # listboxIssuesClosed.bind("<Double-Button-1>", self.keyEventOpenIssue)
        # listboxLabels.bind("<Double-Button-1>", self.keyEventOpenIssue)
        listboxRepositories.bind("<Double-Button-1>", self.keyEventChangeRepository)
        listboxRepositoriesPrivate.bind("<Double-Button-1>", self.keyEventChangeRepository)
        textNotepad.bind("<Key>", lambda e:self.keyEventKeyDownNotepad(self, tab8))
        textNotepad.bind("<FocusOut>", lambda e:self.keyEventSaveNotepad(self, tab8, textNotepad))
        textNotepad.bind("<Control-s>", lambda e:self.keyEventSaveNotepad(self, tab8, textNotepad))

        
    def getConfig(self, root, statusbar):
        data = json.load(open('config.json', encoding='utf-8'))
        Root.loadSettings(root, data, statusbar)
        # tk.messagebox.showinfo("Configuration", "Config file successfully reloaded.\n\nUser:\n"+user+"\n\nRepository:\n"+repo+"\n\nPersonal Access Token:\n"+token)

    def getData(self, statusbar, listbox, type = 'issues'):
        statusbar.set("Loading "+str(type)+", please wait...")
        statusbar.update_idletasks()
        settings = json.load(open('config.json', encoding='utf-8'))
        try:
            jsondata = None
            data = None
            if type == 'notepad':
                if os.path.exists('./'+type+'.json'):
                    data = json.load(open('./'+type+'.json', encoding='utf-8'))
            elif type == 'public_repos' or type == 'private_repos':
                if os.path.exists('./.cache/'+type+'.json'):
                    data = json.load(open('./.cache/'+type+'.json', encoding='utf-8'))
                else:
                    jsondata = urllib.request.urlopen("https://api.github.com/user/repos?visibility="+str(type).split('_')[0]+"&per_page=100&access_token="+settings["token"])
                    data = json.loads(jsondata.read().decode())
                    with open('./.cache/'+type+'.json', 'w', encoding='utf-8') as outfile:
                        json.dump(data, outfile)
            else:
                if os.path.exists('./.cache/'+type+'_'+settings['repo']+'.json'):
                    data = json.load(open('./.cache/'+type+'_'+settings['repo']+'.json', encoding='utf-8'))
                else:
                    if type == 'issues':
                        jsondata = urllib.request.urlopen("https://api.github.com/repos/"+settings["user"]+"/"+settings["repo"]+"/issues?per_page=100&access_token="+settings["token"])
                    elif type == 'closed_issues':
                        jsondata = urllib.request.urlopen("https://api.github.com/repos/"+settings["user"]+"/"+settings["repo"]+"/issues?state=closed&per_page=100&access_token="+settings["token"])
                    elif type == 'labels':
                        jsondata = urllib.request.urlopen("https://api.github.com/repos/"+settings["user"]+"/"+settings["repo"]+"/labels?per_page=100&access_token="+settings["token"])
                    elif type == 'milestones':
                        jsondata = urllib.request.urlopen("https://api.github.com/repos/"+settings["user"]+"/"+settings["repo"]+"/milestones?per_page=100&access_token="+settings["token"])
                    elif type == 'contributors':
                        jsondata = urllib.request.urlopen("https://api.github.com/repos/"+settings["user"]+"/"+settings["repo"]+"/assignees?per_page=100&access_token="+settings["token"])
                    data = json.loads(jsondata.read().decode())
                    with open('./.cache/'+type+'_'+settings['repo']+'.json', 'w', encoding='utf-8') as outfile:
                        json.dump(data, outfile)
            if type == 'notepad':
                txt = str(data["text"])
                listbox.insert(END, txt)
            else:
                for i in data:
                    txt = ''
                    if type == 'issues':
                        txt = "#"+str(i["number"])+": "+str(i["title"])+" - "+str(i["user"]["login"])
                    elif type == 'closed_issues':
                        txt = "#"+str(i["number"])+": "+str(i["title"])+" - "+str(i["user"]["login"])
                    elif type == 'labels':
                        txt = str(i["name"])+" #"+str(i["color"])
                    elif type == 'milestones':
                        txt = "#" + str(i["number"])+" - "+str(i["title"])+" - "+str(i["state"])
                    elif type == 'contributors':
                        txt = "#" + str(i["login"])+" - "+str(i["type"])+" - "+str(i["avatar_url"])
                    elif type == 'public_repos':
                        txt = str(i["full_name"])+" - "+str(i["description"]) #+" - "+("Private" if str(i["private"]) == "True" else "Public")
                    elif type == 'private_repos':
                        txt = str(i["full_name"])+" - "+str(i["description"])
                    listbox.insert(END, txt)
            statusbar.set('Idle.')
            self.update_idletasks()
        except Exception:
            tk.messagebox.showerror("Error", "Could not retrieve Github data ("+str(type)+").\n\nPlease check spelling of repository and your Personal Access Token in Settings.")
            statusbar.set('Idle. Error fetching Github data.')
            self.update_idletasks()

    def keyEventNewIssue(event, bla):
        newIssueWin = NewIssueWindow()
        newIssueWin.mainloop()

    def keyEventOpenIssue(self, event):
        issuenumber = event.widget.get(event.widget.curselection()[0]).split(':')[0].replace('#', '')
        openIssueWin = IssueWindow(issuenumber)
        openIssueWin.mainloop()

    def keyEventChangeRepository(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        repo = str(value.split('/')[1].split(' - ')[0])
        settings = json.load(open('config.json', encoding='utf-8'))
        settings["repo"] = repo
        with open('config.json', 'w', encoding='utf-8') as outfile:
            json.dump(settings, outfile)
        restartApp()
        
        print('Changing repo to '+str(repo))

    def keyEventKeyDownNotepad(self, notebookwidget, tabwidget):
        notebookwidget.tab(tabwidget, text="Notepad *")

    def keyEventSaveNotepad(self, notebookwidget, tabwidget, textwidget):
        jsontxt = {"text":textwidget.get(0.0,END)}
        with open('notepad.json', 'w', encoding='utf-8') as outfile:
            json.dump(jsontxt, outfile)
        notebookwidget.tab(tabwidget, text="Notepad")

    def keyEventRestartApp(self, event):
        restartApp()
    def keyEventQuitApp(self, event):
        sys.exit(0)



























class AboutFrame(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root)
        
        aboutTxt = '''
        Issupy is a simple GUI client for managing Github issues.
        It was built out of my own needs for the reasons below:

        - I couldn't find any existing desktop clients for Linux
        - Many of the web apps feels clunky/laggy
        - I need something lightweight without bloat, only for issues
        - Cross platform because I also work on Windows and I'd like the same UI
        - Lightning fast! (ok not as fast as native C app, but faster and lighter than an Electron behemoth)

        The application uses the Tkinter GUI toolkit so it looks a bit ugly,
        but the graphical interface isn't a priority for the moment.

        Source code:
        https://github.com/kek91/issupy
        '''
        lblResult = Label(root, text=aboutTxt)
        lblResult.grid(row=0, column=0)

        btnClose = Button(root, text="Close", width=20, command=root.closeButton)
        btnClose.grid(row=1, column=0, columnspan=1, sticky=E, padx=5, pady=5)

class AboutWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("About Issupy")
        center(self, 750, 300)
        self.frame = AboutFrame(self)
    def closeButton(self):
        self.destroy()














class LicenseFrame(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self, root)
        
        licenseTxt = '''
        MIT License

        Copyright (c) 2018 Kim Eirik Kvassheim

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.

        https://github.com/kek91/issupy/blob/master/LICENSE
        '''
        lblResult = Label(root, text=licenseTxt)
        lblResult.grid(row=0, column=0)

        btnClose = Button(root, text="Close", width=20, command=root.closeButton)
        btnClose.grid(row=1, column=0, columnspan=1, sticky=E, padx=5, pady=5)

class LicenseWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("Issupy License")
        center(self, 750, 500)
        self.frame = LicenseFrame(self)
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

        buttonColorPickerBg = Button(root, text='Select Color', command=lambda:self.callColorPicker(entryBackground))
        buttonColorPickerBg.grid(row=4, column=2)

        buttonColorPickerFg = Button(root, text='Select Color', command=lambda:self.callColorPicker(entryForeground))
        buttonColorPickerFg.grid(row=5, column=2)

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
    
    def callColorPicker(self, entry):
        color = colorPicker(self)
        entry.delete(0, END)
        entry.insert(0, str(color))


class SettingsWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("Settings")
        center(self, 600, 300)
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

        entryBody = Text(root, width=57, height=8)
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
        center(self, 600, 400)
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




















class IssueFrame(ttk.Frame):
    def __init__(self, root, jsonissue, jsonlabels, jsonmilestones, jsoncontributors):
        ttk.Frame.__init__(self, root)
        irow = 0
        icol = 0
        # Label(root, text='Title').grid(row=0, column=0, sticky=W)
        
        # print(jsonissue["milestone"])
        
        '''
        Layout:
        0       1         2         3
                  Title
        Labels      |   Description
        Milestone   |   Comments
        Status      |   Comments
        Assignees   |   Comments

        '''

        entryTitle = Entry(root, width=80, font = 'Verdana 14 normal') # width=50,
        entryTitle.grid(row=irow, column=0, sticky=W+E+N+S, padx=5, pady=5)
        entryTitle.insert(0, jsonissue["title"])
        
        irow += 1


        Label(root, text='Labels').grid(row=irow, column=0, sticky=E+W)
        irow += 1
        checks = {}
        for label in jsonlabels:
            # setattr(checks, label["name"], '')
            checks[label["name"]] = ''
            c = tk.Checkbutton(root, text=label["name"], variable=checks[label["name"]])
            c.grid(row=irow, column=0, sticky=W)
            print(label)
            irow += 1
        entryLabels = Entry(root) # width=50
        entryLabels.grid(row=irow, column=0, padx=5, pady=5, sticky=E+W)
        entryLabels.insert(0, str(jsonissue["labels"]))

        irow += 1
        Label(root, text='Milestone').grid(row=irow, column=0, sticky=E+W)
        irow += 1
        entryMilestone = Entry(root, width=50)
        entryMilestone.grid(row=irow, column=0, padx=5, pady=5, sticky=E+W)
        entryMilestone.insert(0, str(jsonissue["milestone"]))

        irow += 1
        Label(root, text='Assignees').grid(row=irow, column=0, sticky=E+W)
        irow += 1
        entryAssignees = Entry(root, width=50)
        entryAssignees.grid(row=irow, column=0, padx=5, pady=5, sticky=E+W)
        entryAssignees.insert(0, jsonissue["assignees"])

        irow += 1
        Label(root, text='Status').grid(row=irow, column=0, sticky=E+W)
        irow += 1
        entryStatus = Entry(root, width=50)
        entryStatus.grid(row=irow, column=0, padx=5, pady=5, sticky=E+W)
        entryStatus.insert(0, jsonissue["state"])

        irow += 1
        Label(root, text='Description').grid(row=irow, column=0, sticky=E+W)
        irow += 1
        entryBody = Text(root, font='Verdana 10 normal')
        entryBody.grid(row=irow, column=0, columnspan=2, padx=5, pady=5, sticky=N+E+S+W)
        entryBody.insert(0.0, jsonissue["body"])

        # lblResult = Label(root, text="")
        # lblResult.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        irow += 1
        buttonSave = Button(root, text="Save", command=lambda:root.saveIssue({
            "title":entryTitle.get(),
            "body":entryBody.get("1.0",END),
            "labels":entryLabels.get(),
            "milestone":entryMilestone.get(),
            "assignees":entryAssignees.get(),
            "status":entryStatus.get(),
            }, lblResult))
        buttonSave.grid(row=irow, column=0, columnspan=4, padx=5, pady=5)

        irow += 1
        buttonClose = Button(root, text="Close", command=root.closeButton)
        buttonClose.grid(row=irow, column=0, columnspan=4, padx=5, pady=5)


class IssueWindow(tk.Tk):
    def __init__(self, issue, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        jsonissue = getIssueData(issue, 'issues')
        print('Issue details:\n'+str(jsonissue))
        jsonlabels = getIssueData(issue, 'labels')
        print('Issue jsonlabels:\n'+str(jsonlabels))
        jsonmilestones = getIssueData(issue, 'milestones')
        print('Issue jsonmilestones:\n'+str(jsonmilestones))
        jsoncontributors = getIssueData(issue, 'contributors')
        print('Issue jsoncontributors:\n'+str(jsoncontributors))
        self.winfo_toplevel().title("Issue #"+str(jsonissue["number"])+": "+str(jsonissue["title"]))
        center(self, 1024, 800)
        self.frame = IssueFrame(self, jsonissue, jsonlabels, jsonmilestones, jsoncontributors)

    def saveIssue(self, data, label):
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
# root.iconbitmap("./issupy.ico")