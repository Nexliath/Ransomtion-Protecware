import traceback
from tkinter import *
import tkinter as tk
import sqlite3


class Logiciel(object):
    path = ""
    name = ""

    def __init__(self, newPath, newName):
        self.path = newPath
        self.name = newName


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
# _____________EXIT_______________


def EXIT():
    exitsure = tk.Toplevel()

    areyousure = tk.Label(exitsure, text="Are you sure you want to exit?")
    areyousure.grid(column=0, row=0)

    ExitYes = tk.Button(exitsure, text="Yes", command=quit)
    ExitYes.grid(column=0, row=2)

    NoYes = tk.Button(exitsure, text="No", command=exitsure.destroy)
    NoYes.grid(column=2, row=2)


def ajoutWhiteList():
    popup = Toplevel()
    popup.config(background='#1B2B4B')
    popup.mainloop()


# window
window = Tk()
window.title("Ransomtion Proteware")
# window.geometry("1080x720")
# window.minsize(1080,720)
window.config(background='#1B2B4B')

# menu
menu_bar = Menu(window)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Quitter", command=window.quit)
prop_menu = Menu(menu_bar, tearoff=0)
prop_menu.add_command(label="Noir et blanc", command=changeColorsNB)
prop_menu.add_command(label="Couleurs", command=changeColors)
menu_bar.add_cascade(label="Fichier", menu=file_menu)
menu_bar.add_cascade(label="Propriétés", menu=prop_menu)
window.config(menu=menu_bar)

# Titre
label_title = Label(window, text="Ransomtion Protecware", font=(
    "Space Ranger", 40), bg='#1B2B4B', fg='#E07B6A', pady=20)

# Sous titre
label_subtitle = Label(window, text="Logiciel actif...", font=(
    "Space Ranger", 25), bg='#1B2B4B', fg='#E07B6A', pady=15)

# Bouton éteindre
button = Button(window, text="eteindre", font=("Space Ranger", 12),
                bg='#E07B6A', fg='#1B2B4B', command=EXIT)
# frame whitlist
frameWL = Frame(window, background="#1B2B4B")
# whitelist
white_list = Listbox(frameWL, bg='#E07B6A', fg='#1B2B4B',
                     bd=0, relief=GROOVE, borderwidth=4)
white_list.pack()
initWhiteList()
# bouton ajouter whitelist
ajout = Button(frameWL, text="Ajouter", font=("Space Ranger", 15),
               bg='#E07B6A', fg='#1B2B4B', command=ajoutWhiteList)
ajout.pack(pady=10, padx=20)

# grid
label_title.grid(row=0, column=1)
label_subtitle.grid(row=1, column=1)
button.grid(row=10, column=10)
frameWL.grid(row=2, column=0, padx=25, pady=10)
window.mainloop()
