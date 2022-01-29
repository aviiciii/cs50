# Morse Code Converter
#### Video Demo:  <https://youtu.be/6PL8bElJ1hY>
#### Description:
***About***
This project is a simple web application that converts English alphabets, numbers and some special characters into morse code.The web application is created using Python, Flask, SQLite, HTML and CSS.

***User Experience:***
The web applicaton has 3 pages namely homepage, converter page and learn page.

Homepage is the welcome page greeting the users with the name of the web application and giving them the option to visit the other pages namely converter page and learn page.

Converter page is the main concentration of this web application. The page is simple containing a textarea to enter text and a button to convert it. The converted morse code is displayed below.

Learn page contains the short summary about morse code and the list of all characters in the International Morse Code and their corresponding Morse Code. This page also contains a link to a website created by google for learning morse code.

***Source Code:***
The source code contain a application python file using flask, a sqlite database, 4 HTML templates and a css stylesheet.

**application.py**
This is the main source code where the converter page's logic is implemented using a simple if/else function. The input text is checked whether any text is entered and the character(s) entered has a morse code value according to the International Morse Code Language. If not, user gets a output of his error. The text is compared character to character using for loop and if conditions and a new string is created carring the morse code. Then, the user gets the morse code of the text he/she entered in the text area.

**morse.db**
This database contains a table which has two columns namely ch and mr. ch contains all the English alphabets, numbers and special characters included in the International Morse Code. mr contains morse code values for each corresponding characters. This database is user to display the list of characters and morse code in the learn page. I made this database so it would be easier to get data from it in python and send to jinja in HTML. I loaded up the database using sqlite query from a dictionary containing the data in python.

**templates**
There are 4 HTML templates in the source code. One of them is layout HTML file and other 3 is the HTML file for three respective pages namely homepage, converter page and learn page. All three pages are designed to be minimal and provides only needed functions nothing more, nothing less. HTML styling was easier using bootstrap but I learnt to style some elements without using it also. It was a good experience.

**style.css**
Stylesheet is used to style all the HTML pages of the web application and it was a fun experience learning the ways to style websites. I learnt much about hover settings while doing this project.


**Thank You CS50!**