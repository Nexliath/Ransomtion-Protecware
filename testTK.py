import traceback
from tkinter import *
import sqlite3


class Logiciel(object):
    path = ""
    name = ""

    def __init__(self, newPath, newName):
        self.path = newPath
        self.name = newName


def changeColorsNB():
    button["fg"] = 'white'
    button["bg"] = 'grey'
    label_title["bg"] = 'white'
    label_title["fg"] = 'darkgrey'
    label_subtitle["bg"] = 'white'
    label_subtitle["fg"] = 'darkgrey'
    window.config(background="white")


def changeColors():
    button["fg"] = '#1B2B4B'
    button["bg"] = '#E07B6A'
    label_title["bg"] = '#1B2B4B'
    label_title["fg"] = '#E07B6A'
    label_subtitle["bg"] = '#1B2B4B'
    label_subtitle["fg"] = '#E07B6A'
    window.config(background='#1B2B4B')


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
            i = i+1

    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        sqliteConnection.close()


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
button = Button(window, text="eteindre", font=("Space Ranger", 18),
                bg='#E07B6A', fg='#1B2B4B', command=window.destroy)

# whitelist
white_list = Listbox(window, bg='#E07B6A', fg='#1B2B4B', bd=0, padx=15)
initWhiteList()

# grid
label_title.grid(row=0, column=1)
label_subtitle.grid(row=1, column=1)
button.grid(row=10, column=10)
white_list.grid(row=2, column=0)
window.mainloop()
