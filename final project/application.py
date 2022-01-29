import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session


# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///morse.db")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#HOME


@app.route("/")
def index():
    """Home page"""
    return render_template("index.html")

#ABOUT


@app.route("/about")
def about():
    """About morse code and its history"""
    return render_template("about.html")

#CONVERT


@app.route("/convert", methods=["GET", "POST"])
def convert():
    """Convert english to morse code"""
    if request.method == "POST":
        eng = request.form.get("eng").lower().strip()

        if not eng:
            return render_template("convert.html", message="No text entered.")

        morse = ""

        for letter in eng:

            # if space
            if letter.isspace() == True:
                    morse = morse + " / "

            # for special characters
            elif letter == ".":
                morse = morse + ".-.-.-"
            elif letter == ",":
                morse = morse + "--..--"
            elif letter == "?":
                morse = morse + "..--.."
            elif letter == "'":
                morse = morse + ".----."
            elif letter == "!":
                morse = morse + "-.-.--"
            elif letter == "/":
                morse = morse + "-..-."
            elif letter == "(":
                morse = morse + "-.--."
            elif letter == ")":
                morse = morse + "-.--.-"
            elif letter == "&":
                morse = morse + ".-..."
            elif letter == ":":
                morse = morse + "---..."
            elif letter == ";":
                morse = morse + "-.-.-."
            elif letter == "=":
                morse = morse + "-...-"
            elif letter == "+":
                morse = morse + ".-.-."
            elif letter == "-":
                morse = morse + "-....-"
            elif letter == "_":
                morse = morse + "..--.-"
            elif letter == "$":
                morse = morse + "...-..-"
            elif letter == "@":
                morse = morse + ".--.-."

            # for numbers
            elif letter.isnumeric() == True:
                if letter == "0":
                    morse = morse + "-----"
                elif letter == "1":
                    morse = morse + ".----"
                elif letter == "2":
                    morse = morse + "..---"
                elif letter == "3":
                    morse = morse + "...--"
                elif letter == "4":
                    morse = morse + "....-"
                elif letter == "5":
                    morse = morse + "....."
                elif letter == "6":
                    morse = morse + "-...."
                elif letter == "7":
                    morse = morse + "--..."
                elif letter == "8":
                    morse = morse + "---.."
                elif letter == "9":
                    morse = morse + "----."

            # for alphabets
            elif letter.isalpha() == True:
                if letter == "a":
                    morse = morse + ".-"
                elif letter == "b":
                    morse = morse + "-..."
                elif letter == "c":
                    morse = morse + "-.-."
                elif letter == "d":
                    morse = morse + "-.."
                elif letter == "e":
                    morse = morse + "."
                elif letter == "f":
                    morse = morse + "..-."
                elif letter == "g":
                    morse = morse + "--."
                elif letter == "h":
                    morse = morse + "...."
                elif letter == "i":
                    morse = morse + ".."
                elif letter == "j":
                    morse = morse + ".---"
                elif letter == "k":
                    morse = morse + "-.-"
                elif letter == "l":
                    morse = morse + ".-.."
                elif letter == "m":
                    morse = morse + "--"
                elif letter == "n":
                    morse = morse + "-."
                elif letter == "o":
                    morse = morse + "---"
                elif letter == "p":
                    morse = morse + ".--."
                elif letter == "q":
                    morse = morse + "--.-"
                elif letter == "r":
                    morse = morse + ".-."
                elif letter == "s":
                    morse = morse + "..."
                elif letter == "t":
                    morse = morse + "-"
                elif letter == "u":
                    morse = morse + "..-"
                elif letter == "v":
                    morse = morse + "...-"
                elif letter == "w":
                    morse = morse + ".--"
                elif letter == "x":
                    morse = morse + "-..-"
                elif letter == "y":
                    morse = morse + "-.--"
                elif letter == "z":
                    morse = morse + "--.."

            # unsupported characters error
            else:
                return render_template("convert.html", message="The character(s) you have entered does not have morse code values.", eng=eng)

            # space after every letter in morse
            morse = morse + " "

        return render_template("convert.html", message="Morse Code : "+morse, eng=eng)
    else:
        return render_template("convert.html")

#LEARN


@app.route("/learn")
def learn():
    """Learn morse code"""
    # UPDATING INTO DATABASE (ONE TIME USE)
    while False:
        characters = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..',
        'E':'.', 'F':'..-.', 'G':'--.', 'H':'....','I':'..', 'J':'.---',
        'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.','O':'---', 'P':'.--.',
        'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-','U':'..-', 'V':'...-',
        'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..','1':'.----', '2':'..---',
        '3':'...--','4':'....-', '5':'.....', '6':'-....', '7':'--...',
        '8':'---..', '9':'----.', '0':'-----', ',':'--..--','.':'.-.-.-',
        '?':'..--..', '/':'-..-.', '-':'-....-', '(':'-.--.',
        ')':'-.--.-', "'":'.----.', '!':'-.-.--', '&':'.-...', ':':'---...',
        ';':'-.-.-.', '=':'-...-', '+':'.-.-.', '_':'..--.-', '$':'...-..-',
        '@':'.--.-.'}

        ch_list = list(characters.keys())
        mr_list = list(characters.values())

        i=1000
        while i<len(ch_list):
            db.execute(
                "INSERT INTO morsedata (ch, mr) VALUES (?, ?)",
                ch_list[i],
                mr_list[i]
            )
            i+=1

    # Select Character and Morse code from database
    cha_mor = db.execute(
        "SELECT ch, mr FROM morsedata"
    )

    return render_template("learn.html", characters=cha_mor)