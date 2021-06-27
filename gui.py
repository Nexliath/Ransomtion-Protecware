import traceback
from tkinter import *
from tkinter.font import BOLD
import sqlite3
import whitelist as WL
from sqlite3 import Error
import keyboard 


# class Logiciel(object):
#     path = ""
#     name = ""
#
#     def __init__(self, newPath, newName):
#         self.path = newPath
#         self.name = newName


def changeColorsNB():
    window.config(background="#DADADA")
    button["fg"] = '#DADADA'
    button["bg"] = '#403E3E'
    label_title["bg"] = '#DADADA'
    label_title["fg"] = '#403E3E'
    label_subtitle["bg"] = '#DADADA'
    label_subtitle["fg"] = '#403E3E'
    white_list["bg"] = "#DADADA"
    white_list["fg"] = "#403E3E"
    ajout["fg"] = '#DADADA'
    ajout["bg"] = '#403E3E'
    frameWL["bg"] = '#DADADA'
    nbLabel["bg"] = '#DADADA'
    nbLabel["fg"] = '#403E3E'
    frameNB["bg"] = '#DADADA'
    bloque["bg"] = '#DADADA'
    bloque["fg"] = '#403E3E'
    frameBL["bg"] = '#DADADA'
    history["bg"] = '#DADADA'
    history["fg"] = '#403E3E'
    ajoutHist["bg"] = '#403E3E'
    ajoutHist["fg"] = '#DADADA'
    titreWL["bg"] = '#DADADA'
    titreWL["fg"] = '#403E3E'
    titreBL["bg"] = '#DADADA'
    titreBL["fg"] = '#403E3E'

def changeColors():
    button["fg"] = '#1B2B4B'
    button["bg"] = '#E07B6A'
    label_title["bg"] = '#1B2B4B'
    label_title["fg"] = '#E07B6A'
    label_subtitle["bg"] = '#1B2B4B'
    label_subtitle["fg"] = '#E07B6A'
    window.config(background='#1B2B4B')
    white_list["bg"] = "#E07B6A"
    white_list["fg"] = "#1B2B4B"
    ajout["fg"] = '#1B2B4B'
    ajout["bg"] = '#E07B6A'
    frameWL["bg"] = '#1B2B4B'
    titreWL["bg"] = '#1B2B4B'
    titreWL["fg"] = '#E07B6A'
    titreBL["bg"] = '#1B2B4B'
    titreBL["fg"] = '#E07B6A'
    nbLabel["bg"] = '#1B2B4B'
    nbLabel["fg"] = '#E07B6A'
    frameNB["bg"] = '#1B2B4B'
    bloque["bg"] = '#1B2B4B'
    bloque["fg"] = '#E07B6A'
    frameBL["bg"] = '#1B2B4B'
    history["bg"] = '#E07B6A'
    history["fg"] = '#1B2B4B'
    ajoutHist["bg"] = '#E07B6A'
    ajoutHist["fg"] = '#1B2B4B'

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
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
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
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
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
    exitsure.config(background="#DADADA")
    centerPopup(exitsure)

    areyousure = Label(exitsure, text="Êtes vous sûr de vouloir quitter ?", bg='#DADADA', fg='#403E3E', font=("Arial", 12, 'bold'))
    areyousure.grid(column=1, row=0, pady=10)

    ExitYes = Button(exitsure, text="OUI", command=quit, font=("Space Ranger", 12),
                bg='#403E3E', fg='#DADADA')
    ExitYes.grid(column=0, row=1, padx=10, pady=5)

    NoYes = Button(exitsure, text="NON", command=exitsure.destroy, font=("Space Ranger", 12),
                bg='#403E3E', fg='#DADADA')
    NoYes.grid(column=2, row=1, padx=10, pady=5)


def validation(popup, id, passW, mode):
    if(id.get() == "admin" and passW.get() == "admin"):
        conn = sqlite3.connect("Ransomtion-Protecware.db")
        try:
            popup.destroy()
            addPopup = Toplevel()
            centerPopup(addPopup)
            addPopup.config(background="#DADADA")
            addPopup.attributes("-topmost", 1)
            if mode == 0: # ajout manuel
                newPath = StringVar()
                newName = StringVar()
                frameMA = Frame(addPopup, background="#DADADA")
                newWhite = Label(frameMA, text="Informations du logiciel", font=(
                    "Space Ranger", 18), bg='#DADADA', fg='#403E3E', pady=10)
                path = Entry(frameMA, bg="white", textvariable=newPath)
                path.insert(0, "Path")
                name = Entry(frameMA, bg="white", textvariable=newName)
                name.insert(0, "Name")
                valida = Button(frameMA, bg='#403E3E', fg='#DADADA', text="Valider", font=("Space Ranger", 12),
                                command=lambda: [WL.addToWhitelist(name.get(), path.get(), conn), insertNew(name.get())])
                newWhite.pack()
                path.pack()
                name.pack()
                valida.pack()
                frameMA.pack(pady=10, padx=10)

            elif mode == 1: # ajout automatique

                dest = sqlite3.connect(':memory:')
                conn.backup(dest)
                c = conn.cursor()

                currentName = history.get(ACTIVE)
                print(currentName)
                cmd = "SELECT path FROM history WHERE name='" + currentName + "'"
                print(cmd)
                req = c.execute(cmd)
                row = req.fetchone()
                currentPath = row[0]
                frameAuto = Frame(addPopup, background="#DADADA")
                labelAuto = Label(frameAuto, text="Informations du logiciel", font=(
                    "Space Ranger", 15), bg='#DADADA', fg='#403E3E', pady=10)
                pa = StringVar()
                tmp = "Path : " + currentName
                pa.set(tmp)
                pathAuto = Label(frameAuto, textvariable=pa, font=(
                    "Space Ranger", 12), bg='#DADADA', fg='#403E3E', pady=5)
                na = StringVar()
                tmp = "Name : " + currentPath
                na.set(tmp)
                nameAuto = Label(frameAuto, textvariable=na, font=(
                    "Space Ranger", 12), bg='#DADADA', fg='#403E3E', pady=5)
                valida = Button(frameAuto, bg='#403E3E', fg='#DADADA', text="Valider", font=("Space Ranger", 12),
                                command=lambda: [WL.addToWhitelist(currentName, currentPath, conn),
                                                 insertNew(currentName), addPopup.destroy()])
                annul = Button(frameAuto,  bg='#403E3E', fg='#DADADA', text="Annuler", font=("Space Ranger", 12), command=lambda: addPopup.destroy())
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
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        finally:
            return

def ajoutWhiteList(mode):
    #ajout à la white list depuis une entry

    popup = Toplevel()
    mdp = StringVar()
    iden = StringVar()

    popup.config(background="#DADADA")
    popup.attributes("-topmost", 1)
    framePop = Frame(popup, background="#DADADA")
    logi = Label(framePop, text="Logiciel bloqué", font=(
        "Space Ranger", 18), bg='#DADADA', fg='#403E3E', pady=10)
    id = Entry(framePop, bg="white", textvariable=iden)
    idLabel = Label(framePop, text="Login :", font=(
        "Space Ranger", 10), bg='#DADADA', fg='#403E3E', pady=10, padx=5)
    passW = Entry(framePop, bg="white", textvariable=mdp, show='*')
    passLabel = Label(framePop, text="Password :", font=(
        "Space Ranger", 10), bg='#DADADA', fg='#403E3E', pady=10, padx=5)
    valid = Button(framePop, bg='#403E3E', fg='#DADADA',
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
prop_menu.add_command(label="Noir et blanc", command=changeColorsNB)
prop_menu.add_command(label="Couleurs", command=changeColors)
menu_bar.add_cascade(label="Fichier", menu=file_menu)
menu_bar.add_cascade(label="Propriétés", menu=prop_menu)
window.config(menu=menu_bar)

# Logo
window.iconbitmap('Logo.ico')

logo = Canvas(window, width=192, height=192, bg='#1B2B4B', bd=0, highlightthickness=0)

icon = PhotoImage(file = 'Logo_petit.png')
logo.create_image(96, 96, image = icon)
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

# frame number
frameNB = Frame(window, background="#1B2B4B")

# logiciels bloqués
bloque = Label(frameNB, text="Nombre de malware bloqués", font=(
    "Space Ranger", 12), bg='#1B2B4B', fg='#E07B6A', pady=5)
bloque.pack()

# nombre de ransom évités
file = open("nb.txt", "r")
nb = StringVar()
nb.set(file.read())
nbLabel = Label(frameNB, textvariable=nb, font=(
    "Space Ranger", 18), bg='#1B2B4B', fg='#E07B6A', pady=5)
nbLabel.pack()
file.close()

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

frameBL.grid(row=2, column=3)

# raccourcis clavier
keyboard.add_hotkey('ctrl+alt+s', show)
keyboard.add_hotkey('ctrl+alt+h', hide)
keyboard.add_hotkey('ctrl+alt+q', EXIT)

# masquer avec la croix
window.protocol("WM_DELETE_WINDOW", hide)

# center
# grid
logo.grid(row=0, column=0, rowspan=2)
label_title.grid(row=0, column=1)
label_subtitle.grid(row=1, column=1)
button.grid(row=10, column=1)
frameWL.grid(row=2, column=0, padx=25, pady=10)
centerWindow(window)
window.mainloop()
