from tkinter import *
from database import Database
import whitelist
import history
import keyboard

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

    def __init__(self):
        super().__init__()

        # window
        self.title("Ransomtion Protecware")
        # self.geometry("1080x720")
        # self.minsize(1080,720)
        self.config(background=self.theme['background'])

        # menu
        menu_bar = Menu(self)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Masquer", command=self.hide)
        prop_menu = Menu(menu_bar, tearoff=0)
        prop_menu.add_command(label="Couleurs", command=lambda: self.update_theme(themes['color']))
        prop_menu.add_command(label="Noir et blanc", command=lambda: self.update_theme(themes['blackAndWhite']))
        menu_bar.add_cascade(label="Fichier", menu=file_menu)
        menu_bar.add_cascade(label="Thème", menu=prop_menu)
        self.config(menu=menu_bar)

        # Logo
        self.iconbitmap("./assets/logo.ico")
        icon = PhotoImage(file = "./assets/logo_small.png")

        logo1 = Canvas(self, width=100, height=100, bg=self.theme['background'], bd=0, highlightthickness=0)
        logo1.create_image(50, 50, image=icon)

        logo2 = Canvas(self, width=100, height=100, bg=self.theme['background'], bd=0, highlightthickness=0)
        logo2.create_image(50, 50, image=icon)

        # Titre
        label_title = Label(self, text="Ransomtion Protecware", font=("Space Ranger", 35), bg=self.theme['background'], fg=self.theme['foreground'], pady=20)

        # Sous titre
        label_subtitle = Label(self, text="Logiciel actif...", font=("Space Ranger", 18), bg=self.theme['background'], fg=self.theme['foreground'], pady=15)

        # Bouton éteindre
        button = Button(self, text="eteindre", font=("Space Ranger", 12), bg=self.theme['foreground'], fg=self.theme['background'], command=exit)

        # Frame whitlist
        frameWL = Frame(self, background=self.theme['background'])

        # Titre white list
        titreWL = Label(frameWL, text="WhiteList\n", font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
        titreWL.pack()

        # Whitelist
        self.white_list = Listbox(frameWL, bg=self.theme['foreground'], fg=self.theme['background'], bd=0, relief=GROOVE, borderwidth=4)
        self.white_list.pack()

        # Bouton ajouter whitelist
        ajout = Button(frameWL, text="Ajouter", font=("Space Ranger", 15), bg=self.theme['foreground'], fg=self.theme['background'], command=lambda: self.login(lambda: self.add_whitelist(0)))
        ajout.pack(pady=10, padx=20)

        # Bouton supprimer whitelist
        supprimer = Button(frameWL, text="Supprimer", font=("Space Ranger", 15), bg=self.theme['foreground'], fg=self.theme['background'], command=lambda: self.login(self.remove_whitelist))
        supprimer.pack(pady=10)

        # Frame number
        frameNB = Frame(self, background=self.theme['background'])

        # Logiciels bloqués
        bloque = Label(frameNB, text="Nombre de malware bloqués", font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
        bloque.pack()

        # Nombre de ransom évités
        self.nb = StringVar()
        nbLabel = Label(frameNB, textvariable=self.nb, font=("Space Ranger", 18), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
        nbLabel.pack()

        frameNB.grid(row=2, column=1)

        # Frame history
        frameBL = Frame(self, background=self.theme['background'])

        # Titre liste bloqué
        titreBL = Label(frameBL, text="Liste des\nlogiciels bloqués", font=("Space Ranger", 12), bg=self.theme['background'], fg=self.theme['foreground'], pady=5)
        titreBL.pack()

        # History
        self.history = Listbox(frameBL, bg=self.theme['foreground'], fg=self.theme['background'], bd=0, relief=GROOVE, borderwidth=4)
        self.history.pack()

        # Bouton ajouter whitelist depuis history
        ajoutHist = Button(frameBL, text="Ajouter", font=("Space Ranger", 15), bg=self.theme['foreground'], fg=self.theme['background'], command=lambda: self.login(lambda: self.add_whitelist(1)))
        ajoutHist.pack(pady=10, padx=20)

        # Raccourcis clavier
        keyboard.add_hotkey("ctrl+alt+s", self.show)
        keyboard.add_hotkey("ctrl+alt+h", self.hide)
        keyboard.add_hotkey("ctrl+q", quit)

        # Quitter avec la croix
        self.protocol("WM_DELETE_WINDOW", quit)

        # Grid
        logo1.grid(row=0, column=0, rowspan=2)
        logo2.grid(row=0, column=3, rowspan=2)
        label_title.grid(row=0, column=1)
        label_subtitle.grid(row=1, column=1)
        button.grid(row=10, column=1)
        frameWL.grid(row=2, column=0, padx=25, pady=10)
        frameBL.grid(row=2, column=3)
        self.center_window(self)

    def mainloop(self):
        with Database() as db:
            self.db = db

            self.white_list.data = list(whitelist.list(self.db))
            self.history.data = list(history.list(self.db))
            self.nb.set(len(self.history.data))

            self.update_white_list()
            self.update_history()
            self.update_white_list()
            self.update_history()

            super().mainloop()

        self.db = None

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
            global theme
            theme = new_theme

        window.config(background=self.theme['background'])
        button['fg'] = self.theme['background']
        button['bg'] = self.theme['foreground']
        label_title['bg'] = self.theme['background']
        label_title['fg'] = self.theme['foreground']
        label_subtitle['bg'] = self.theme['background']
        label_subtitle['fg'] = self.theme['foreground']
        white_list['bg'] = self.theme['background']
        white_list['fg'] = self.theme['foreground']
        ajout['fg'] = self.theme['background']
        ajout['bg'] = self.theme['foreground']
        frameWL['bg'] = self.theme['background']
        nbLabel['bg'] = self.theme['background']
        nbLabel['fg'] = self.theme['foreground']
        frameNB['bg'] = self.theme['background']
        bloque['bg'] = self.theme['background']
        bloque['fg'] = self.theme['foreground']
        frameBL['bg'] = self.theme['background']
        history['bg'] = self.theme['background']
        history['fg'] = self.theme['foreground']
        ajoutHist['bg'] = self.theme['foreground']
        ajoutHist['fg'] = self.theme['background']
        titreWL['bg'] = self.theme['background']
        titreWL['fg'] = self.theme['foreground']
        titreBL['bg'] = self.theme['background']
        titreBL['fg'] = self.theme['foreground']
        logo1['bg'] = self.theme['background']
        logo2['bg'] = self.theme['background']
        supprimer['bg'] = self.theme['foreground']
        supprimer['fg'] = self.theme['background']

    def center_window(self, wantedWindow, offsetX=430, offsetY=200):
        windowWidth = wantedWindow.winfo_reqwidth()
        windowHeight = wantedWindow.winfo_reqheight()

        positionRight = int(wantedWindow.winfo_screenwidth() / 2 - offsetX)
        positionDown = int(wantedWindow.winfo_screenheight() / 2 - offsetY)

        wantedWindow.geometry("+{}+{}".format(positionRight, positionDown))

    def exit(self):
        exitsure = Toplevel()

        exitsure.config(background=self.theme['background'])
        self.center_window(exitsure, 100, 50)

        areyousure = Label(exitsure, text="Êtes vous sûr de vouloir quitter ?", bg=self.theme['background'], fg=self.theme['foreground'], font=("Arial", 12, "bold"))
        areyousure.grid(column=1, row=0, pady=10)

        ExitYes = Button(exitsure, text="OUI", command=quit, font=("Space Ranger", 12), bg=self.theme['foreground'], fg=self.theme['background'])
        ExitYes.grid(column=0, row=1, padx=10, pady=5)

        NoYes = Button(exitsure, text="NON", command=exitsure.destroy, font=("Space Ranger", 12), bg=self.theme['foreground'], fg=self.theme['background'])
        NoYes.grid(column=2, row=1, padx=10, pady=5)

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
                    Label(popErreur, text="Déjà dans la whitelist", bg=self.theme['background'], fg=self.theme['foreground'], font=("Space Ranger", 12, 'bold'), pady=35, padx=35).pack()
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
                Label(popErreur, text="Déjà dans la whitelist", bg=self.theme['background'], fg=self.theme['foreground'], font=("Space Ranger", 12, 'bold'), pady=35, padx=35).pack()
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
        passW = Entry(framePop, bg="white", textvariable=mdp, show='*')
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
    App().mainloop()
