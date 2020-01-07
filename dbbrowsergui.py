#!/usr/bin/python3
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import sqlite3

class Browser():
    def __init__(self, master):
        self.master = master
        self.master.title('DB Browser')

        self.master.geometry('500x500')
        self.master.minsize(500,500)
        self.master.resizable('True', 'True')
        self.canvas = Canvas(self.master, scrollregion=(0,0,500,500))
        self.canvas.pack()

        self.open = Button(self.master, text='Open DB', command=self.open_db, padx=20)
        self.close = Button(self.master, text='Close DB', command=self.close_db, padx=20)
        self.open.pack()
        self.close.pack()

    def open_db(self):
        #do something to delete rows
        self.filename =  filedialog.askopenfilename()
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()
        self.create_table()

    def close_db(self):
        if self.connection: self.connection.close()
        
    def run_filters(self):     
        query = "SELECT * from books"
        for i, column in enumerate(self.data.description):
            if self.filter_text[i].get() == '': continue
            elif query == "SELECT * from books":
                query += " WHERE " + column[0] + " LIKE " + "'{}'".format(self.filter_text[i].get())
            else: 
                query += " AND " + column[0] + " LIKE " + "'{}'".format(self.filter_text[i].get())

        self.data = self.connection.execute(query)
        self.update_table()

    def clear_table_rows(self):
        self.points.destroy()

    def update_table(self):
        self.clear_table_rows()
        self.points = Frame(self.canvas)
        self.points.pack()
        self.bar = Scrollbar(self.points, orient=VERTICAL, command=self.canvas.yview)
        self.bar.pack(side=RIGHT, fill=Y)
        #if len(self.data) > 20: add scrollbar
        
        for column in self.data:
            self.frame = Frame(self.points)
            for point in column:
                Label(self.frame,width=25, text=point, borderwidth=2, relief="groove").pack(side=LEFT)
            self.frame.pack(side=TOP)       

    def create_table(self):
        table_names = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.table_name = table_names.fetchone()[0]
        #self.table_name.config(text=table_names[0])
        self.table_name = Label(self.canvas, text=table_name, pady=20)
        self.table_name.pack()

        self.data =  self.connection.execute("SELECT * from books")
        self.column_names = Frame(self.canvas)
        self.column_names.pack()
        self.filters = Frame(self.canvas)
        self.filters.pack()
        self.filter_text = []

        for column_name in self.data.description:
            Label(self.column_names, fg="blue", width=25, text=column_name[0], borderwidth=2, relief="groove").pack(side=LEFT)
            filter = Entry(self.filters, width=25 ,textvariable=StringVar)
            self.filter_text.append(filter)
            filter.pack(side=LEFT)

        Button(self.filters, text='Filter', padx=20, command=self.run_filters).pack(side=RIGHT)
    
        self.points = Frame(self.canvas)
        self.points.pack()        
        
        self.update_table()

def main():
    root = Tk()
    gui = Browser(root)
    root.mainloop()

if __name__ == "__main__": main()