from tkinter import *
import sqlite3
from sqlite3 import Error
import whitelist
import keyboard

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

def update_theme(new_theme=None):
    if new_theme is not None:
        global theme
        theme = new_theme

    window.config(background=theme['background'])
    button["fg"] = theme['background']
    button["bg"] = theme['foreground']
    label_title["bg"] = theme['background']
    label_title["fg"] = theme['foreground']
    label_subtitle["bg"] = theme['background']
    label_subtitle["fg"] = theme['foreground']
    white_list["bg"] = theme['background']
    white_list["fg"] = theme['foreground']
    ajout["fg"] = theme['background']
    ajout["bg"] = theme['foreground']
    frameWL["bg"] = theme['background']
    nbLabel["bg"] = theme['background']
    nbLabel["fg"] = theme['foreground']
    frameNB["bg"] = theme['background']
    bloque["bg"] = theme['background']
    bloque["fg"] = theme['foreground']
    frameBL["bg"] = theme['background']
    history["bg"] = theme['background']
    history["fg"] = theme['foreground']
    ajoutHist["bg"] = theme['foreground']
    ajoutHist["fg"] = theme['background']
    titreWL["bg"] = theme['background']
    titreWL["fg"] = theme['foreground']
    titreBL["bg"] = theme['background']
    titreBL["fg"] = theme['foreground']
    logo1["bg"] = theme['background']
    logo2["bg"] = theme['background']
    supprimer["bg"] = theme['foreground']
    supprimer["fg"] = theme['background']

# initialisation de la whitelist
def initWhiteList():

    try:
        sqliteConnection = sqlite3.connect('Ransomtion-Protecware.db')
        dest = sqlite3.connect(':memory:')
        sqliteConnection.backup(dest)
        c = sqliteConnection.cursor()
        req = c.execute('SELECT name FROM whitelist')
        i = 0
        for row in req.fetchall():
            white_list.insert(i, row[0])
            i = i + 1

    except sqlite3.Error as er:
        print(er)
    finally:
        sqliteConnection.close()


# insertion du nouveau logiciel dans la white list
def insertNew(name):
    selection = white_list.get(0, END)
    test = 0
    for i in selection:
        if i == name:
            test = 1
    popErreur = Tk()
    Label(popErreur, text="Déjà dans la whitelist", bg='#DADADA', fg='#403E3E', font=("Space Ranger", 12, 'bold'), pady=35, padx=35).pack()
    centerPopup(popErreur)
    if(test == 0) :
        white_list.insert(END, name)

# suppression du logiciel dans la white list
def popNew(id):
    cpt = 0
    selection = white_list.get(0, END)
    for i in selection:
        if i == id:
            white_list.pop(id)


# initialisation de la whitelist
def initHistory():

    try:
        sqliteConnection = sqlite3.connect('Ransomtion-Protecware.db')
        dest = sqlite3.connect(':memory:')
        sqliteConnection.backup(dest)
        c = sqliteConnection.cursor()
        req = c.execute('SELECT name FROM history')
        i = 0
        for row in req.fetchall():
            history.insert(i, row[0])
            i = i + 1

    except sqlite3.Error as er:
        print(er)
    finally:
        sqliteConnection.close()

# --------------- Center Functions


def centerWindow(wantedWindow):
    # Gets the requested values of the height and widht.
    windowWidth = wantedWindow.winfo_reqwidth()
    windowHeight = wantedWindow.winfo_reqheight()

    # Gets both half the screen width/height and window width/height
    positionRight = int(wantedWindow.winfo_screenwidth() /
                        2 - 430)
    positionDown = int(wantedWindow.winfo_screenheight() /
                       2 - windowHeight)

    # Positions the window in the center of the page.
    wantedWindow.geometry("+{}+{}".format(positionRight, positionDown))

def centerPopup(wantedWindow):
    # Gets the requested values of the height and widht.
    windowWidth = wantedWindow.winfo_reqwidth()
    windowHeight = wantedWindow.winfo_reqheight()

    # Gets both half the screen width/height and window width/height
    positionRight = int(wantedWindow.winfo_screenwidth() /
                        2 - 100)
    positionDown = int(wantedWindow.winfo_screenheight() /
                       2 - windowHeight + 150)

    # Positions the window in the center of the page.
    wantedWindow.geometry("+{}+{}".format(positionRight, positionDown))



# Exit confirmation
def EXIT():
    exitsure = Toplevel()

    exitsure.config(background=theme['background'])
    centerPopup(exitsure)

    areyousure = Label(exitsure, text="Êtes vous sûr de vouloir quitter ?", bg=theme['background'], fg=theme['foreground'], font=("Arial", 12, 'bold'))
    areyousure.grid(column=1, row=0, pady=10)

    ExitYes = Button(exitsure, text="OUI", command=quit, font=("Space Ranger", 12),
                bg=theme['foreground'], fg=theme['background'])
    ExitYes.grid(column=0, row=1, padx=10, pady=5)

    NoYes = Button(exitsure, text="NON", command=exitsure.destroy, font=("Space Ranger", 12),
                bg=theme['foreground'], fg=theme['background'])
    NoYes.grid(column=2, row=1, padx=10, pady=5)


def validation(popup, id, passW, mode):
    if(id.get() == "admin" and passW.get() == "admin"):
        conn = sqlite3.connect("Ransomtion-Protecware.db")
        currentName = history.get(ACTIVE)
        dest = sqlite3.connect(':memory:')
        conn.backup(dest)
        c = conn.cursor()
        print(currentName)
        cmd = "SELECT path FROM history WHERE name='" + currentName + "'"
        print(cmd)
        req = c.execute(cmd)
        row = req.fetchone()
        currentPath = row[0]
        try:
            popup.destroy()
            addPopup = Toplevel()
            centerPopup(addPopup)
            addPopup.config(background=theme['background'])
            addPopup.attributes("-topmost", 1)
            if mode == 0: # ajout manuel
                newPath = StringVar()
                newName = StringVar()
                frameMA = Frame(addPopup, background=theme['background'])
                newWhite = Label(frameMA, text="Informations du logiciel", font=(
                    "Space Ranger", 18), bg=theme['background'], fg=theme['foreground'], pady=10)
                path = Entry(frameMA, bg="white", textvariable=newPath)
                name = Entry(frameMA, bg="white", textvariable=newName)
                valida = Button(frameMA, bg=theme['foreground'], fg=theme['background'], text="Valider", font=("Space Ranger", 12),
                                command=lambda: [whitelist.add(path.get(), name.get(), conn), insertNew(name.get())])
                annul = Button(frameMA,  bg=theme['foreground'], fg=theme['background'], text="Annuler", font=("Space Ranger", 12), command=lambda: addPopup.destroy())

                pathLabel = Label(frameMA, text="Path : ", font=(
                    "Space Ranger", 12), bg=theme['background'], fg=theme['foreground'], pady=5)

                nameLabel = Label(frameMA, text="Name : ", font=(
                    "Space Ranger", 12), bg=theme['background'], fg=theme['foreground'], pady=5)
                frameMA.pack(pady=10, padx=10)
                newWhite.grid(row=0, column=0, columnspan=2)
                pathLabel.grid(row=1, column=0, sticky=E)
                nameLabel.grid(row=2, column=0, sticky=E)
                path.grid(row=1, column=1)
                name.grid(row=2, column=1)
                valida.grid(row=3, column=0)
                annul.grid(row=3, column=1)

            elif mode == 1: # ajout automatique

                currentName = history.get(ACTIVE)
                print(currentName)
                cmd = "SELECT path FROM history WHERE name='" + currentName + "'"
                print(cmd)
                req = c.execute(cmd)
                row = req.fetchone()
                currentPath = row[0]
                frameAuto = Frame(addPopup, background=bg)
                labelAuto = Label(frameAuto, text="Informations du logiciel", font=(
                    "Space Ranger", 15), bg=bg, fg=fg, pady=10)
                pa = StringVar()
                tmp = "Path : " + currentName
                pa.set(tmp)
                pathAuto = Label(frameAuto, textvariable=pa, font=(
                    "Space Ranger", 12), bg=bg, fg=fg, pady=5)
                na = StringVar()
                tmp = "Name : " + currentPath
                na.set(tmp)
                nameAuto = Label(frameAuto, textvariable=na, font=(
                    "Space Ranger", 12), bg=bg, fg=fg, pady=5)
                valida = Button(frameAuto, bg=fg, fg=bg, text="Valider", font=("Space Ranger", 12),
                                command=lambda: [whitelist.add(currentPath, currentName, conn),
                                                 insertNew(currentName), addPopup.destroy()])
                annul = Button(frameAuto,  bg=fg, fg=bg, text="Annuler", font=("Space Ranger", 12), command=lambda: addPopup.destroy())
                labelAuto.grid(row=0, column=0, columnspan=2)
                pathAuto.grid(row=1, column=0, columnspan=2)
                nameAuto.grid(row=2, column=0, columnspan=2)
                valida.grid(row=3, column=0)
                annul.grid(row=3, column=1)
                frameAuto.pack(pady=10, padx=10)
            else:
                return
            centerPopup(addPopup)
            addPopup.mainloop()
        except sqlite3.Error as er:
            print(er)
        finally:
            return

def validationSupp(popup, id, passW, mode):
    if(id.get() == "admin" and passW.get() == "admin"):
        conn = sqlite3.connect("Ransomtion-Protecware.db")
        try:
            popup.destroy()
            suppPopup = Toplevel()
            centerPopup(suppPopup)
            suppPopup.config(background=theme['background'])
            suppPopup.attributes("-topmost", 1)
            if mode == 0: # suppression manuel
                newId = StringVar()
                frameMA = Frame(suppPopup, background=theme['background'])
                suppLabel = Label(frameMA, text="Logiciel à supprimer", font=(
                    "Space Ranger", 18), bg=theme['background'], fg=theme['foreground'], pady=10)
                idLabel = Label(frameMA, text="ID : ", font=(
                    "Space Ranger", 12), bg=theme['background'], fg=theme['foreground'], pady=5)
                idS = Entry(frameMA, bg="white", textvariable= newId)

                valida = Button(frameMA, bg=theme['foreground'], fg=theme['background'], text="Valider", font=("Space Ranger", 12),
                                command=lambda: [whitelist.remove(idS.get(), conn), popNew(idS.get())])
                annul = Button(frameMA,  bg=theme['foreground'], fg=theme['background'], text="Annuler", font=("Space Ranger", 12), command=lambda: suppPopup.destroy())
                idLabel.grid(row=1, column=0, sticky=E)
                suppLabel.grid(row=0, column=0, columnspan=2)
                idS.grid(row=1, column=1)
                valida.grid(row=2, column=0)
                annul.grid(row=2, column=1)
                frameMA.pack(pady=10, padx=10)

            else:
                return
            centerPopup(suppPopup)
            suppPopup.mainloop()
        except sqlite3.Error as er:
            print(er)
        finally:
            return

def ajoutWhiteList(mode):
    #ajout à la white list depuis une entry

    popup = Toplevel()
    mdp = StringVar()
    iden = StringVar()
    popup.config(background=theme['background'])
    popup.attributes("-topmost", 1)
    framePop = Frame(popup, background=theme['background'])
    logi = Label(framePop, text="Logiciel bloqué", font=(
        "Space Ranger", 18), bg=theme['background'], fg=theme['foreground'], pady=10)
    id = Entry(framePop, bg="white", textvariable=iden)
    idLabel = Label(framePop, text="Login :", font=(
        "Space Ranger", 10), bg=theme['background'], fg=theme['foreground'], pady=10, padx=5)
    passW = Entry(framePop, bg="white", textvariable=mdp, show='*')
    passLabel = Label(framePop, text="Password :", font=(
        "Space Ranger", 10), bg=theme['background'], fg=theme['foreground'], pady=10, padx=5)
    valid = Button(framePop, bg=theme['foreground'], fg=theme['background'],
                   text="Valider", font=("Space Ranger", 12), command=lambda: validation(popup, id, passW, mode))
    logi.grid(row=0, column=0, columnspan=2)
    id.grid(row=1, column=1)
    idLabel.grid(row=1, column=0, sticky=E)
    passW.grid(row=2, column=1)
    passLabel.grid(row=2, column=0, sticky=E)
    valid.grid(row=3, column=0, columnspan=2)
    framePop.pack(pady=10, padx=10)
    centerPopup(popup)
    popup.mainloop()

def supprimerWhiteList(mode):
    #supprimer de la white list depuis une entry

    popup = Toplevel()
    mdp = StringVar()
    iden = StringVar()
    popup.config(background=theme['background'])
    popup.attributes("-topmost", 1)
    framePop = Frame(popup, background=theme['background'])
    logi = Label(framePop, text="Logiciel bloqué", font=(
        "Space Ranger", 18), bg=theme['background'], fg=theme['foreground'], pady=10)
    id = Entry(framePop, bg="white", textvariable=iden)
    idLabel = Label(framePop, text="Login :", font=(
        "Space Ranger", 10), bg=theme['background'], fg=theme['foreground'], pady=10, padx=5)
    passW = Entry(framePop, bg="white", textvariable=mdp, show='*')
    passLabel = Label(framePop, text="Password :", font=(
        "Space Ranger", 10), bg=theme['background'], fg=theme['foreground'], pady=10, padx=5)
    valid = Button(framePop, bg=theme['foreground'], fg=theme['background'],
                   text="Valider", font=("Space Ranger", 12), command=lambda: validationSupp(popup, id, passW, mode))
    logi.grid(row=0, column=0, columnspan=2)
    id.grid(row=1, column=1)
    idLabel.grid(row=1, column=0, sticky=E)
    passW.grid(row=2, column=1)
    passLabel.grid(row=2, column=0, sticky=E)
    valid.grid(row=3, column=0, columnspan=2)
    framePop.pack(pady=10, padx=10)
    centerPopup(popup)
    popup.mainloop()

# fonction pour le masquage et le réaffichage
def show():
    window.update()
    window.deiconify()

def hide():
    window.update()
    window.withdraw()

####################################################

# window
window = Tk()
window.title("Ransomtion Protecware")
# window.geometry("1080x720")
# window.minsize(1080,720)
window.config(background='#1B2B4B')

# menu
menu_bar = Menu(window)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Masquer", command=hide)
prop_menu = Menu(menu_bar, tearoff=0)
prop_menu.add_command(label="Noir et blanc", command=lambda: update_theme(themes.blackAndWhite))
prop_menu.add_command(label="Couleurs", command=lambda: update_theme(themes.color))
menu_bar.add_cascade(label="Fichier", menu=file_menu)
menu_bar.add_cascade(label="Propriétés", menu=prop_menu)
window.config(menu=menu_bar)

# Logo
window.iconbitmap('./assets/logo.ico')

logo1 = Canvas(window, width=100, height=100, bg='#1B2B4B', bd=0, highlightthickness=0)
icon = PhotoImage(file = './assets/logo_small.png')
logo1.create_image(50, 50, image = icon)

logo2 = Canvas(window, width=100, height=100, bg='#1B2B4B', bd=0, highlightthickness=0)
logo2.create_image(50, 50, image = icon)

# Titre
label_title = Label(window, text="Ransomtion Protecware", font=(
    "Space Ranger", 35), bg='#1B2B4B', fg='#E07B6A', pady=20)

# Sous titre
label_subtitle = Label(window, text="Logiciel actif...", font=(
    "Space Ranger", 18), bg='#1B2B4B', fg='#E07B6A', pady=15)

# Bouton éteindre
button = Button(window, text="eteindre", font=("Space Ranger", 12),
                bg='#E07B6A', fg='#1B2B4B', command=EXIT)
# frame whitlist
frameWL = Frame(window, background="#1B2B4B")

# titre white list
titreWL = Label(frameWL, text="WhiteList\n", font=(
    "Space Ranger", 12), bg='#1B2B4B', fg='#E07B6A', pady=5)
titreWL.pack()

# whitelist
white_list = Listbox(frameWL, bg='#E07B6A', fg='#1B2B4B',
                    bd=0, relief=GROOVE, borderwidth=4)
white_list.pack()
initWhiteList()

# bouton ajouter whitelist
ajout = Button(frameWL, text="Ajouter", font=("Space Ranger", 15),
            bg='#E07B6A', fg='#1B2B4B', command=lambda: ajoutWhiteList(0))
ajout.pack(pady=10, padx=20)

# bouton supprimer whitelist
supprimer = Button(frameWL, text="Supprimer", font=("Space Ranger", 15),
            bg='#E07B6A', fg='#1B2B4B', command=lambda: supprimerWhiteList(0))
supprimer.pack(pady=10)

# frame number
frameNB = Frame(window, background="#1B2B4B")

# logiciels bloqués
bloque = Label(frameNB, text="Nombre de malware bloqués", font=(
    "Space Ranger", 12), bg='#1B2B4B', fg='#E07B6A', pady=5)
bloque.pack()

# nombre de ransom évités
nb = StringVar()
nb.set(3) # TODO
nbLabel = Label(frameNB, textvariable=nb, font=(
    "Space Ranger", 18), bg='#1B2B4B', fg='#E07B6A', pady=5)
nbLabel.pack()

frameNB.grid(row=2, column=1)

# frame history
frameBL = Frame(window, background="#1B2B4B")

# titre liste bloqué
titreBL = Label(frameBL, text="Liste des \nlogiciels bloqués", font=(
    "Space Ranger", 12), bg='#1B2B4B', fg='#E07B6A', pady=5)
titreBL.pack()

# history
history = Listbox(frameBL, bg='#E07B6A', fg='#1B2B4B',
                    bd=0, relief=GROOVE, borderwidth=4)
history.pack()
initHistory()

# bouton ajouter whitelist depuis history
ajoutHist = Button(frameBL, text="Ajouter", font=("Space Ranger", 15),
            bg='#E07B6A', fg='#1B2B4B', command=lambda: ajoutWhiteList(1))
ajoutHist.pack(pady=10, padx=20)



# raccourcis clavier
keyboard.add_hotkey('ctrl+alt+s', show)
keyboard.add_hotkey('ctrl+alt+h', hide)
keyboard.add_hotkey('ctrl+alt+q', EXIT)

# masquer avec la croix
window.protocol("WM_DELETE_WINDOW", hide)

# center
# grid
logo1.grid(row=0, column=0, rowspan=2)
logo2.grid(row=0, column=3, rowspan=2)
label_title.grid(row=0, column=1)
label_subtitle.grid(row=1, column=1)
button.grid(row=10, column=1)
frameWL.grid(row=2, column=0, padx=25, pady=10)
frameBL.grid(row=2, column=3)
centerWindow(window)
window.mainloop()
