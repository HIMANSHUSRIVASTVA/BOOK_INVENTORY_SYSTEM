from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import messagebox,ttk
import sqlite3
connection=sqlite3.connect("Book.db")

TABLE_NAME="BOOK_TABLE"
TABLE_ID="TABLE_ID"
BOOK_NAME="BOOK_NAME"
BOOK_PRICE="BOOK_PRICE"

root=tk.Tk()
root.title("WEB_SCRAPPING_GUI")
root.geometry('800x800')
root.resizable(0,0)
root.title("BOOK INVENTORY SYSTEM")

displayLabel=tk.Label(root,text="WEB SCRAPPER",font=("Sylfaen", 16),fg="Black")
displayLabel.grid(row=0,column=2,padx=10,pady=40)






def scrappData():
    global connection
    connection.execute("CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " (" + TABLE_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " + BOOK_NAME + " TEXT, " + BOOK_PRICE + " NUMBER); ")
    print("table created successfully")

    address = "http://books.toscrape.com/catalogue/page-"
    all_values = {}
    page= int(input(" Enter a number of Pages You Want To Scrap"))

    for i in range(1, page+1):

        website_address = address + str(i) + ".html"
        result = requests.get(website_address, verify='false')

        soup = BeautifulSoup(result.text, 'html.parser')
        # print(soup.prettify())

        # print(soup.prettify())

        books = soup.findAll("article", {"class": "product_pod"})
        for book in books:
            name = book.findAll("a")[1].attrs['title']
            name= name.replace("'", "''")
            print(name)
            price = book.find("p", {"class": "price_color"}).text.strip('£')
            price = price[2:]
            connection.execute("INSERT INTO " + TABLE_NAME + " ( " + BOOK_NAME + ", "
                               +BOOK_PRICE + " ) VALUES ( '" + name + "', " + price + ");")



        connection.commit()
            ##    print(price)
            ##    print(name)
        print(all_values)



loadButton = tk.Button(root, text="DISPLAY DATA", font=("Sylfaen", 10), command=lambda: loadData(),height=10, width=30,bg='pink')
loadButton.grid(row=9,column=2,padx=30,pady=30)


def loadData():
    secondWindow = tk.Tk()
    secondWindow.title("BOOK INVENTORY DATABASE")
    appLabel = tk.Label(secondWindow, text="BOOK DATABASE", fg="purple", width=40)
    appLabel.config(font=("Algerian", 30))
    appLabel.pack()


    treeview = ttk.Treeview(secondWindow)
    treeview["columns"] = (1, 2)
    treeview.heading(1, text="BOOK NAME")
    treeview.heading(2, text="BOOK PRICE")
    cursor = connection.execute("SELECT * FROM " + TABLE_NAME + " ;")
    i = 0
    for row in cursor:
        treeview.insert('', i, text=str(i + 1), values=(row[1], row[2]))
        i = i + 1
    treeview.pack()
    secondWindow.mainloop()
scrapbutton=tk.Button(root,text="CLICK HERE TO SCRAPP DATA",font=("Sylfaen", 10), command=scrappData,bg='pink',height=10, width=30)
scrapbutton.grid(row=8,column=2,padx=50,pady=30)

root.mainloop()
