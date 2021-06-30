from tkinter import *
import os
from database import Database
import whitelist
import history
import daemon_controller
from logo import base64 as logo_base64
# import keyboard

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

    theme = themes['color']
    db = None
    authenticated = False
    running = False

    def __init__(self):
        super().__init__()

        # window
        self.title("Ransomtion Protecware")
        # self.geometry("1080x720")
        # self.minsize(1080,720)
        self.resizable(False, False)
        self.config(background=self.theme['background'])

        # menu
        menu_bar = Menu(self)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Masquer", command=self.hide)
        prop_menu = Menu(menu_bar, tearoff=0)
        prop_menu.add_command(label="Couleurs", command=lambda: self.update_theme(self.themes['color']))
        prop_menu.add_command(label="Noir et blanc", command=lambda: self.update_theme(self.themes['blackAndWhite']))
        menu_bar.add_cascade(label="Fichier", menu=file_menu)
        menu_bar.add_cascade(label="Thème", menu=prop_menu)
        self.config(menu=menu_bar)

        # Logo
        self.icon = PhotoImage(data=logo_base64)

        self.logo1 = Canvas(self, width=100, height=100, bg=self.theme['background'], bd=0, highlightthickness=0)
        self.logo1.create_image(50, 50, image=self.icon)

        self.logo2 = Canvas(self, width=100, height=100, bg=self.theme['background'], bd=0, highlightthickness=0)
        self.logo2.create_image(50, 50, image=self.icon)

        # Titre
        self.label_title = Label(self, text="Ransomtion Protecware", font=("Space Ranger", 35), bg=self.theme['background'], fg=self.theme['foreground'], pady=20)

        # Sous titre
        self.label_subtitle = Label(self, text="Chargement...", font=("Space Ranger", 18), bg=self.theme['background'], fg=self.theme['foreground'], pady=15)

        # Bouton éteindre
        self.button = Button(self, text="allumer", font=("Space Ranger", 12), bg=self.theme['foreground'], fg=self.theme['background'], command=self.shutdown)

        # Frame whitlist
        self.frameWL = Frame(self, background=self.theme['background'])

        # Titre white list
        self.titreWL = Label(self.frameWL, text="WhiteList\n", font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
        self.titreWL.pack()

        # Whitelist
        self.white_list = Listbox(self.frameWL, bg=self.theme['foreground'], fg=self.theme['background'], bd=0, relief=GROOVE, borderwidth=4)
        self.white_list.pack()

        # Bouton ajouter whitelist
        self.ajout = Button(self.frameWL, text="Ajouter", font=("Space Ranger", 15), bg=self.theme['foreground'], fg=self.theme['background'], command=lambda: self.login(lambda: self.add_whitelist(0)))
        self.ajout.pack(pady=10, padx=20)

        # Bouton supprimer whitelist
        self.supprimer = Button(self.frameWL, text="Supprimer", font=("Space Ranger", 15), bg=self.theme['foreground'], fg=self.theme['background'], command=lambda: self.login(self.remove_whitelist))
        self.supprimer.pack(pady=10)

        # Frame number
        self.frameNB = Frame(self, background=self.theme['background'])

        # Logiciels bloqués
        self.bloque = Label(self.frameNB, text="Nombre de malware bloqués", font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
        self.bloque.pack()

        # Nombre de ransom évités
        self.nb = StringVar()
        self.nbLabel = Label(self.frameNB, textvariable=self.nb, font=("Space Ranger", 18), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
        self.nbLabel.pack()

        self.frameNB.grid(row=2, column=1)

        # Frame history
        self.frameBL = Frame(self, background=self.theme['background'])

        # Titre liste bloqué
        self.titreBL = Label(self.frameBL, text="Liste des\nlogiciels bloqués", font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
        self.titreBL.pack()

        # History
        self.history = Listbox(self.frameBL, bg=self.theme['foreground'], fg=self.theme['background'], bd=0, relief=GROOVE, borderwidth=4)
        self.history.pack()

        # Bouton ajouter whitelist depuis history
        self.ajoutHist = Button(self.frameBL, text="Ajouter", font=("Space Ranger", 15), bg=self.theme['foreground'], fg=self.theme['background'], command=lambda: self.login(lambda: self.add_whitelist(1)))
        self.ajoutHist.pack(pady=10, padx=20)

        # Raccourcis clavier
        # keyboard.add_hotkey("ctrl+alt+s", self.show)
        # keyboard.add_hotkey("ctrl+alt+h", self.hide)
        # keyboard.add_hotkey("ctrl+q", quit)

        # Quitter avec la croix
        # self.protocol("WM_DELETE_WINDOW", quit)

        # Grid
        self.logo1.grid(row=0, column=0, rowspan=2)
        self.logo2.grid(row=0, column=3, rowspan=2)
        self.label_title.grid(row=0, column=1)
        self.label_subtitle.grid(row=1, column=1)
        self.button.grid(row=10, column=1)
        self.frameWL.grid(row=2, column=0, padx=25, pady=10)
        self.frameBL.grid(row=2, column=3)
        self.center_window(self)

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

    def update_running(self, running):
        self.running = running

        if running:
            self.label_subtitle.config(text="Logiciel actif...")
            self.button.config(text="eteindre")
        else:
            self.label_subtitle.config(text="Logiciel inactif !")
            self.button.config(text="allumer")

    def update_white_list(self):
        while self.white_list.get(0, END):
            self.white_list.delete(0)

        for id, path, name in self.white_list.data:
            self.white_list.insert(id, name)

    def update_history(self):
        while self.history.get(0, END):
            self.history.delete(0)

        for id, path, name, reason, timestamp in self.history.data:
            self.history.insert(id, name)

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
        self.white_list['bg'] = self.theme['background']
        self.white_list['fg'] = self.theme['foreground']
        self.ajout['fg'] = self.theme['background']
        self.ajout['bg'] = self.theme['foreground']
        self.frameWL['bg'] = self.theme['background']
        self.nbLabel['bg'] = self.theme['background']
        self.nbLabel['fg'] = self.theme['foreground']
        self.frameNB['bg'] = self.theme['background']
        self.bloque['bg'] = self.theme['background']
        self.bloque['fg'] = self.theme['foreground']
        self.frameBL['bg'] = self.theme['background']
        self.history['bg'] = self.theme['background']
        self.history['fg'] = self.theme['foreground']
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

    def center_window(self, wantedWindow, offsetX=430, offsetY=200):
        windowWidth = wantedWindow.winfo_reqwidth()
        windowHeight = wantedWindow.winfo_reqheight()

        positionRight = int(wantedWindow.winfo_screenwidth() / 2 - offsetX)
        positionDown = int(wantedWindow.winfo_screenheight() / 2 - offsetY)

        wantedWindow.geometry("+{}+{}".format(positionRight, positionDown))

    def shutdown(self):
        def confirm(popup):
            popup.destroy()
            daemon_controller.stop()
            self.update_running(False)

        if self.running:
            exitsure = Toplevel()

            exitsure.config(background=self.theme['background'])
            self.center_window(exitsure, 100, 50)

            areyousure = Label(exitsure, text="Êtes vous sûr de vouloir quitter ?", bg=self.theme['background'], fg=self.theme['foreground'], font=("Space Ranger", 12, "bold"))
            areyousure.grid(column=1, row=0, pady=10)

            ExitYes = Button(exitsure, text="OUI", command=lambda: confirm(exitsure), font=("Space Ranger", 12), bg=self.theme['foreground'], fg=self.theme['background'])
            ExitYes.grid(column=0, row=1, padx=10, pady=5)

            NoYes = Button(exitsure, text="NON", command=exitsure.destroy, font=("Space Ranger", 12), bg=self.theme['foreground'], fg=self.theme['background'])
            NoYes.grid(column=2, row=1, padx=10, pady=5)
        else:
            daemon_controller.start()
            self.update_running(True)

    def add_whitelist(self, mode):
        if mode == 0: # ajout manuel
            def confirm(addPopup, path, name):
                id = whitelist.add(path, name, self.db)
                if id is not None:
                    self.white_list.data.append((id, path, name))
                    self.update_white_list()
                    addPopup.destroy()
                else:
                    popErreur = Toplevel()
                    popErreur.config(background=self.theme['background'])
                    popErreur.attributes("-topmost", 1)
                    Label(popErreur, text="Déjà dans la whitelist", bg=self.theme['background'], fg=self.theme['foreground'], font=("Space Ranger", 12, "bold"), pady=35, padx=35).pack()
                    self.center_window(popErreur, 100, 50)
                    popErreur.mainloop()

            addPopup = Toplevel()
            addPopup.config(background=self.theme['background'])
            addPopup.attributes("-topmost", 1)
            newPath = StringVar()
            newName = StringVar()
            frameMA = Frame(addPopup, background=self.theme['background'])
            newWhite = Label(frameMA, text="Informations du logiciel", font=("Space Ranger", 18), bg=self.theme['background'], fg=self.theme['foreground'], pady=10)
            path = Entry(frameMA, bg="white", textvariable=newPath)
            name = Entry(frameMA, bg="white", textvariable=newName)
            valida = Button(frameMA, bg=self.theme['foreground'], fg=self.theme['background'], text="Valider", font=("Space Ranger", 12), command=lambda: confirm(addPopup, newPath.get(), newName.get()))
            annul = Button(frameMA,  bg=self.theme['foreground'], fg=self.theme['background'], text="Annuler", font=("Space Ranger", 12), command=lambda: addPopup.destroy())
            pathLabel = Label(frameMA, text="Path : ", font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
            nameLabel = Label(frameMA, text="Name : ", font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
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

        elif mode == 1: # ajout automatique
            selection = self.history.curselection()
            if not selection:
                return
            id, path, name, reason, timestamp = self.history.data[selection[0]]

            id = whitelist.add(path, name, self.db)
            if id is not None:
                self.white_list.data.append((id, path, name))
                self.update_white_list()
            else:
                popErreur = Toplevel()
                popErreur.config(background=self.theme['background'])
                popErreur.attributes("-topmost", 1)
                Label(popErreur, text="Déjà dans la whitelist", bg=self.theme['background'], fg=self.theme['foreground'], font=("Space Ranger", 12, "bold"), pady=35, padx=35).pack()
                self.center_window(popErreur, 100, 50)
                popErreur.mainloop()

    def remove_whitelist(self):
        selection = self.white_list.curselection()
        if not selection:
            return
        id, path, name = self.white_list.data[selection[0]]

        if whitelist.remove(id, self.db):
            self.white_list.data.pop(selection[0])
            self.update_white_list()

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
        logi = Label(framePop, text="Authentification nécessaire", font=("Space Ranger", 18), bg=self.theme['background'], fg=self.theme['foreground'], pady=10)
        id = Entry(framePop, bg="white", textvariable=iden)
        idLabel = Label(framePop, text="Login :", font=("Space Ranger", 10), bg=self.theme['background'], fg=self.theme['foreground'], pady=10, padx=5)
        passW = Entry(framePop, bg="white", textvariable=mdp, show="*")
        passLabel = Label(framePop, text="Password :", font=("Space Ranger", 10), bg=self.theme['background'], fg=self.theme['foreground'], pady=10, padx=5)
        valid = Button(framePop, bg=self.theme['foreground'], fg=self.theme['background'], text="Valider", font=("Space Ranger", 12), command=lambda: self.check_credentials(popup, id.get(), passW.get(), callback))
        logi.grid(row=0, column=0, columnspan=2)
        id.grid(row=1, column=1)
        idLabel.grid(row=1, column=0, sticky=E)
        passW.grid(row=2, column=1)
        passLabel.grid(row=2, column=0, sticky=E)
        valid.grid(row=3, column=0, columnspan=2)
        framePop.pack(pady=10, padx=10)
        self.center_window(popup, 100, 50)
        popup.mainloop()

    def check_credentials(self, popup, id, passW, callback):
        if id == "admin" and passW == "admin":
            self.authenticated = True
            popup.destroy()
            callback()

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