from tkinter import *
import os
from database import Database
import whitelist
import history
import daemon_controller
from languages import languages # languages for traduction, in languages.py
from logo import base64 as logo_base64
import backups as bck


class App(Tk):
    themes = {
        "color": {
            "foreground": "#E07B6A",
            "background": "#1B2B4B"
        },
        "blackAndWhite": {
            "foreground": "#403E3E",
            "background": "#DADADA"
        }
    }

    language = languages['french']
    theme = themes['color']
    db = None
    authenticated = False
    running = False
    

    def __init__(self): # Interface configuration
        super().__init__()
        # window configuration
        self.title("Ransomtion Protecware")
        self.resizable(False, False)
        self.config(background=self.theme['background'])

        # menu configuration
        self.menu_bar = Menu(self)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label=self.language["hide"], command=self.hide) 
        self.prop_menu = Menu(self.menu_bar, tearoff=0)
        self.prop_menu.add_command(label=self.language["colors"], command=lambda: self.update_theme(self.themes['color']))
        self.prop_menu.add_command(label=self.language["black&white"], command=lambda: self.update_theme(self.themes['blackAndWhite']))
        self.lang_menu = Menu(self.menu_bar, tearoff=0)
        self.lang_menu.add_command(label="Français", command=lambda: self.update_language(languages['french']))
        self.lang_menu.add_command(label="English", command=lambda: self.update_language(languages['english']))
        self.save_menu = Menu(self.menu_bar, tearoff=0)
        self.save_menu.add_command(label=self.language["restore"], command=lambda: self.restore())
        self.menu_bar.add_cascade(label=self.language["file"], menu=self.file_menu)
        self.menu_bar.add_cascade(label=self.language["theme"], menu=self.prop_menu)
        self.menu_bar.add_cascade(label=self.language["language"], menu=self.lang_menu)
        self.menu_bar.add_cascade(label=self.language["backup"], menu=self.save_menu)
        self.config(menu=self.menu_bar)

        # Logo
        self.icon = PhotoImage(data=logo_base64)

        self.logo1 = Canvas(self, width=100, height=100, bg=self.theme['background'], bd=0, highlightthickness=0)
        self.logo1.create_image(50, 50, image=self.icon)

        self.logo2 = Canvas(self, width=100, height=100, bg=self.theme['background'], bd=0, highlightthickness=0)
        self.logo2.create_image(50, 50, image=self.icon)

        # Title
        self.label_title = Label(self, text="Ransomtion Protecware", font=("Space Ranger", 35), bg=self.theme['background'], fg=self.theme['foreground'], pady=20)

        # Subtitles
        self.label_subtitle = Label(self, text=self.language["load"], font=("Space Ranger", 18), bg=self.theme['background'], fg=self.theme['foreground'], pady=15)

        # Shutdown button
        self.button = Button(self, text=self.language["start"], font=("Space Ranger", 12), bg=self.theme['foreground'], fg=self.theme['background'], command=self.shutdown)

        # Frame whitelist
        self.frameWL = Frame(self, background=self.theme['background'])

        # Whitelist title
        self.titreWL = Label(self.frameWL, text=self.language["whitelist"], font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
        self.titreWL.pack()

        # Whitelist box
        self.white_list = Listbox(self.frameWL, bg=self.theme['foreground'], fg=self.theme['background'], bd=0, relief=GROOVE, borderwidth=4)
        self.white_list.pack()

        # Whitelist's add button
        self.ajout = Button(self.frameWL, text=self.language["add"], font=("Space Ranger", 15), bg=self.theme['foreground'], fg=self.theme['background'], command=lambda: self.login(lambda: self.add_whitelist(0)))
        self.ajout.pack(pady=10, padx=20)

        # Whitelist's delete button
        self.supprimer = Button(self.frameWL, text=self.language["del"], font=("Space Ranger", 15), bg=self.theme['foreground'], fg=self.theme['background'], command=lambda: self.login(self.remove_whitelist))
        self.supprimer.pack(pady=10)

        # Frame number
        self.frameNB = Frame(self, background=self.theme['background'])

        # Number of blocked software
        self.bloque = Label(self.frameNB, text=self.language["blocked"], font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
        self.bloque.pack()

        self.nb = StringVar()
        self.nbLabel = Label(self.frameNB, textvariable=self.nb, font=("Space Ranger", 18), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
        self.nbLabel.pack()

        self.frameNB.grid(row=2, column=1)

        # Frame history
        self.frameBL = Frame(self, background=self.theme['background'])

        # Blocked list's title
        self.titreBL = Label(self.frameBL, text=self.language["history"], font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
        self.titreBL.pack()

        # History
        self.history = Listbox(self.frameBL, bg=self.theme['foreground'], fg=self.theme['background'], bd=0, relief=GROOVE, borderwidth=4)
        self.history.pack()

        # Button to add from history to whitelist
        self.ajoutHist = Button(self.frameBL, text=self.language["addHist"], font=("Space Ranger", 15), bg=self.theme['foreground'], fg=self.theme['background'], command=lambda: self.login(lambda: self.add_whitelist(1)))
        self.ajoutHist.pack(pady=10, padx=20)

        # Grid
        self.logo1.grid(row=0, column=0, rowspan=2)
        self.logo2.grid(row=0, column=3, rowspan=2)
        self.label_title.grid(row=0, column=1)
        self.label_subtitle.grid(row=1, column=1)
        self.button.grid(row=10, column=1, pady=10)
        self.frameWL.grid(row=2, column=0, padx=25, pady=10)
        self.frameBL.grid(row=2, column=3, padx=25, pady=10)
        self.center_window(self)
    
    # Frame history
    def mainloop(self):
        with Database() as db:
            self.db = db

            self.white_list.data = list(whitelist.list(self.db))
            self.history.data = list(history.list(self.db))
            self.nb.set(len(self.history.data))

            self.update_white_list()
            self.update_history()

            daemon_controller.check_running(self.update_running)

            super().mainloop()

        self.db = None

    
    # Restore a backup
    def restore(self):

        if self.authenticated:
            callback()
            return

        popup = Toplevel()
        popup.config(background=self.theme['background'])
        popup.attributes("-topmost", 1)
        backu = StringVar(popup)
        listOption = bck.list_backups()
        backu.set(self.language["backup"]) 
        framePop = Frame(popup, background=self.theme['background'])
        listLabel = Label(framePop, text=self.language["restore_label"], font=("Space Ranger", 18), bg=self.theme['background'], fg=self.theme['foreground'], pady=10)
        backupList = OptionMenu(framePop, backu, *listOption) # , bg=self.theme['foreground'], fg=self.theme['background'], bd=0, relief=GROOVE, borderwidth=4
        valid = Button(framePop, bg=self.theme['foreground'], fg=self.theme['background'], text=self.language["validate"], font=("Space Ranger", 12), command=lambda: bck.restore_backup(backu.get()))
        listLabel.grid(row=0, column=0, columnspan=2)
        backupList.grid(row=1, column=0, columnspan=2, pady=20)
        valid.grid(row=3, column=0, columnspan=2)
        framePop.pack(pady=10, padx=10)
        self.center_window(popup, 100, 50)
        popup.mainloop()

    # State title update
    def update_running(self, running):
        self.running = running

        if running:
            self.label_subtitle.config(text=self.language["active"])
            self.button.config(text=self.language["shutdown"])
        else:
            self.label_subtitle.config(text=self.language["inactive"])
            self.button.config(text=self.language["start"])

    # Whitelist update
    def update_white_list(self):
        while self.white_list.get(0, END):
            self.white_list.delete(0)

        for id, path, name in self.white_list.data:
            self.white_list.insert(id, name)

    # History update (blocked software)
    def update_history(self):
        while self.history.get(0, END):
            self.history.delete(0)

        for id, path, name, reason, timestamp in self.history.data:
            self.history.insert(id, name)

    # Update color scheme of the software
    def update_theme(self, new_theme=None):
        if new_theme is not None:
            self.theme = new_theme

        self.config(background=self.theme['background'])
        self.button['fg'] = self.theme['background']
        self.button['bg'] = self.theme['foreground']
        self.label_title['bg'] = self.theme['background']
        self.label_title['fg'] = self.theme['foreground']
        self.label_subtitle['bg'] = self.theme['background']
        self.label_subtitle['fg'] = self.theme['foreground']
        self.white_list['bg'] = self.theme['foreground']
        self.white_list['fg'] = self.theme['background']
        self.ajout['fg'] = self.theme['background']
        self.ajout['bg'] = self.theme['foreground']
        self.frameWL['bg'] = self.theme['background']
        self.nbLabel['bg'] = self.theme['background']
        self.nbLabel['fg'] = self.theme['foreground']
        self.frameNB['bg'] = self.theme['background']
        self.bloque['bg'] = self.theme['background']
        self.bloque['fg'] = self.theme['foreground']
        self.frameBL['bg'] = self.theme['background']
        self.history['bg'] = self.theme['foreground']
        self.history['fg'] = self.theme['background']
        self.ajoutHist['bg'] = self.theme['foreground']
        self.ajoutHist['fg'] = self.theme['background']
        self.titreWL['bg'] = self.theme['background']
        self.titreWL['fg'] = self.theme['foreground']
        self.titreBL['bg'] = self.theme['background']
        self.titreBL['fg'] = self.theme['foreground']
        self.logo1['bg'] = self.theme['background']
        self.logo2['bg'] = self.theme['background']
        self.supprimer['bg'] = self.theme['foreground']
        self.supprimer['fg'] = self.theme['background']

    # Update the language of the software
    def update_language(self, new_language=None):
        self.menu_bar.entryconfigure(self.language["file"], label=new_language["file"])
        self.menu_bar.entryconfigure(self.language["theme"], label=new_language["theme"])
        self.menu_bar.entryconfigure(self.language["language"], label=new_language["language"])
        self.menu_bar.entryconfigure(self.language["backup"], label=new_language["backup"])
        if new_language is not None:
            self.language = new_language
        self.label_subtitle['text'] = self.language["load"]
        self.button['text'] = self.language["start"]
        self.ajout['text'] = self.language["add"]   
        self.supprimer['text'] = self.language["del"]
        self.bloque['text'] = self.language["blocked"]
        self.titreBL['text'] = self.language["history"]
        self.ajoutHist['text'] = self.language["addHist"]
        self.file_menu.entryconfigure(0, label=self.language["hide"])
        self.prop_menu.entryconfigure(0, label=self.language["colors"])
        self.prop_menu.entryconfigure(1, label=self.language["black&white"])
        self.save_menu.entryconfigure(1, label=self.language["restore"])
        
    def center_window(self, wantedWindow, offsetX=430, offsetY=200):
        windowWidth = wantedWindow.winfo_reqwidth()
        windowHeight = wantedWindow.winfo_reqheight()

        positionRight = int(wantedWindow.winfo_screenwidth() / 2 - offsetX)
        positionDown = int(wantedWindow.winfo_screenheight() / 2 - offsetY)

        wantedWindow.geometry("+{}+{}".format(positionRight, positionDown))

    # Shutdown 
    def shutdown(self):
        def confirm(popup):
            popup.destroy()
            daemon_controller.stop()
            self.update_running(False)

        if self.running:
            exitsure = Toplevel()

            exitsure.config(background=self.theme['background'])
            self.center_window(exitsure, 100, 50)

            areyousure = Label(exitsure, text=language["quit"], bg=self.theme['background'], fg=self.theme['foreground'], font=("Space Ranger", 12, "bold"))
            areyousure.grid(column=1, row=0, pady=10)

            ExitYes = Button(exitsure, text=language["yes"], command=lambda: confirm(exitsure), font=("Space Ranger", 12), bg=self.theme['foreground'], fg=self.theme['background'])
            ExitYes.grid(column=0, row=1, padx=10, pady=5)

            NoYes = Button(exitsure, text=language["no"], command=exitsure.destroy, font=("Space Ranger", 12), bg=self.theme['foreground'], fg=self.theme['background'])
            NoYes.grid(column=2, row=1, padx=10, pady=5)
        else:
            daemon_controller.start()
            self.update_running(True)
    
    # add to whitelist function of a blocked 
    def add_whitelist(self, mode):
        if mode == 0: # manual adding
            def confirm(addPopup, path, name): # add confirmation
                id = whitelist.add(path, name, self.db) # add in the whitelist db table
                if id is not None:
                    self.white_list.data.append((id, path, name))
                    self.update_white_list()
                    addPopup.destroy()
                else:
                    popErreur = Toplevel()
                    popErreur.config(background=self.theme['background'])
                    popErreur.attributes("-topmost", 1)
                    Label(popErreur, text=self.language["error_already"], bg=self.theme['background'], fg=self.theme['foreground'], font=("Space Ranger", 12, "bold"), pady=35, padx=35).pack()
                    self.center_window(popErreur, 100, 50)
                    popErreur.mainloop()

            # add popup configuration
            addPopup = Toplevel()
            addPopup.config(background=self.theme['background'])
            addPopup.attributes("-topmost", 1)
            newPath = StringVar()
            newName = StringVar()
            frameMA = Frame(addPopup, background=self.theme['background'])
            newWhite = Label(frameMA, text=self.language["soft_info"], font=("Space Ranger", 18), bg=self.theme['background'], fg=self.theme['foreground'], pady=10)
            path = Entry(frameMA, bg="white", textvariable=newPath)
            name = Entry(frameMA, bg="white", textvariable=newName)
            valida = Button(frameMA, bg=self.theme['foreground'], fg=self.theme['background'], text=self.language["validate"], font=("Space Ranger", 12), command=lambda: confirm(addPopup, newPath.get(), newName.get()))
            annul = Button(frameMA,  bg=self.theme['foreground'], fg=self.theme['background'], text=self.language["cancel"], font=("Space Ranger", 12), command=lambda: addPopup.destroy())
            pathLabel = Label(frameMA, text=self.language["path"], font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
            nameLabel = Label(frameMA, text=self.language["name"], font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
            frameMA.pack(pady=10, padx=10)
            newWhite.grid(row=0, column=0, columnspan=2)
            pathLabel.grid(row=1, column=0, sticky=E)
            nameLabel.grid(row=2, column=0, sticky=E)
            path.grid(row=1, column=1)
            name.grid(row=2, column=1)
            valida.grid(row=3, column=0)
            annul.grid(row=3, column=1)
            self.center_window(addPopup, 100, 50)
            addPopup.mainloop()

        elif mode == 1: # automatique adding
            selection = self.history.curselection() # add on cursor selection
            if not selection:
                return
            id, path, name, reason, timestamp = self.history.data[selection[0]]

            id = whitelist.add(path, name, self.db)
            if id is not None: # if not exist in the whitelist table, add
                self.white_list.data.append((id, path, name))
                self.update_white_list() # update display of the new added software
            else: # if already added, error message
                popErreur = Toplevel()
                popErreur.config(background=self.theme['background'])
                popErreur.attributes("-topmost", 1)
                Label(popErreur, text=self.language["error_already"], bg=self.theme['background'], fg=self.theme['foreground'], font=("Space Ranger", 12, "bold"), pady=35, padx=35).pack()
                self.center_window(popErreur, 100, 50)
                popErreur.mainloop()

    # Remove on cursor selection from the whitelist
    def remove_whitelist(self):
        selection = self.white_list.curselection()
        if not selection:
            return
        id, path, name = self.white_list.data[selection[0]]

        if whitelist.remove(id, self.db):
            self.white_list.data.pop(selection[0])
            self.update_white_list()

    # Authentication security for adding and deleting a software from whitelist
    def login(self, callback):
        if self.authenticated:
            callback()
            return

        popup = Toplevel()
        mdp = StringVar()
        iden = StringVar()
        popup.config(background=self.theme['background'])
        popup.attributes("-topmost", 1)
        framePop = Frame(popup, background=self.theme['background'])
        logi = Label(framePop, text=self.language["authenticate"], font=("Space Ranger", 18), bg=self.theme['background'], fg=self.theme['foreground'], pady=10)
        id = Entry(framePop, bg="white", textvariable=iden)
        idLabel = Label(framePop, text=self.language["login"], font=("Space Ranger", 10), bg=self.theme['background'], fg=self.theme['foreground'], pady=10, padx=5)
        passW = Entry(framePop, bg="white", textvariable=mdp, show="*")
        passLabel = Label(framePop, text=self.language["password"], font=("Space Ranger", 10), bg=self.theme['background'], fg=self.theme['foreground'], pady=10, padx=5)
        valid = Button(framePop, bg=self.theme['foreground'], fg=self.theme['background'], text=self.language["validate"], font=("Space Ranger", 12), command=lambda: self.check_credentials(popup, id.get(), passW.get(), callback))
        logi.grid(row=0, column=0, columnspan=2)
        id.grid(row=1, column=1)
        idLabel.grid(row=1, column=0, sticky=E)
        passW.grid(row=2, column=1)
        passLabel.grid(row=2, column=0, sticky=E)
        valid.grid(row=3, column=0, columnspan=2)
        framePop.pack(pady=10, padx=10)
        self.center_window(popup, 100, 50)
        popup.mainloop()

    # Credential checking, bcrypt to do 
    def check_credentials(self, popup, id, passW, callback):
        if id == "admin" and passW == "admin":
            self.authenticated = True
            popup.destroy()
            callback()

    # show and hide function for background running
    def show(self):
        self.update()
        self.deiconify()

    def hide(self):
        self.update()
        self.withdraw()

if __name__ == "__main__":
    try:
        os.makedirs("/var/lib/ransomtion-protecware")
    except FileExistsError:
        pass

    App().mainloop()
