from tkinter import *
import sqlite3

root = Tk()
bills = [100, 50, 20, 10, 5]
pieces = [2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]

class Application(Frame):
    def __init__(self, master, db):
        Frame.__init__(self, master)
        self.db = db

    def main(self):
        self.master.title("Money")
        self.master.resizable(width=False,height=False)
        self.entryList = []
        for i in range(len(bills)):
            label = Label(self.master, text=bills[i], bg="red", font=("arial", 10, "bold"))
            label.grid(row=0, column=i)
            entry = Entry(self.master, justify="center", font=("arial", 10), width=5)
            entry.grid(row=1, column=i)
            self.entryList.append(entry)

        for i in range(len(pieces)):
            label = Label(self.master, text=pieces[i], bg="green", font=("arial", 10, "bold"))
            label.grid(row=0, column=i+len(bills))
            entry = Entry(self.master, justify="center", font=("arial", 10), width=5)
            entry.grid(row=1, column=i+len(bills))
            self.entryList.append(entry)

        self.Total = Label(self.master, text="Total = 0€", fg="purple", font=("arial", 21))
        self.Total.grid(row=3, columnspan=13, column=0)

        OpenBtn = Button(self.master, text="open", command=self.showValue)
        SaveBtn = Button(self.master, text="save", command=lambda: self.db.save(self.checkEntry(), self))
        ExitBtn = Button(self.master, text="exit", command=self.master.quit)
        OpenBtn.grid(row=4, column=len(bills)+len(pieces)-3)
        SaveBtn.grid(row=4, column=len(bills)+len(pieces)-2)
        ExitBtn.grid(row=4, column=len(bills)+len(pieces)-1)

    def checkEntry(self):
        moneyList = []
        for i in range(len(self.entryList)):
            actualEntry = self.entryList[i].get()
            if actualEntry.isdigit() or actualEntry == "":
                moneyList.append(actualEntry)
            else:
                moneyList.append(0)
        return moneyList

    def showValue(self):
        moneyList = self.db.open()
        print(moneyList)
        for i in range(len(self.entryList)):
            actualEntry = self.entryList[i]
            actualEntry.delete(0, END)
            actualEntry.insert(0,moneyList[i])
        self.refreshTotal()

    def calcTotal(self):
        moneyList = self.db.open()
        total = 0
        total += moneyList[0] * 100
        total += moneyList[1] * 50
        total += moneyList[2] * 20
        total += moneyList[3] * 10
        total += moneyList[4] * 5
        total += moneyList[5] * 2
        total += moneyList[6] * 1
        total += moneyList[7] * 0.5
        total += moneyList[8] * 0.2
        total += moneyList[9] * 0.1
        total += moneyList[10] * 0.05
        total += moneyList[11] * 0.02
        total += moneyList[12] * 0.01
        print(total)
        return total

    def refreshTotal(self):
        total = self.calcTotal()
        self.Total.config(text="Total = {}€".format(total))


class DataBase():
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS money (m100 INTEGER, m50 INTEGER, m20 INTEGER, m10 INTEGER, m5 INTEGER, m2 INTEGER, m1 INTEGER, m05 INTEGER, m02 INTEGER, m01 INTEGER, m005 INTEGER, m002 INTEGER, m001 INTEGER)')
        self.conn.commit()

    def save(self, moneyList, tk):
        print(moneyList)
        self.cur.execute('INSERT INTO money VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', moneyList)
        self.conn.commit()
        tk.refreshTotal()

    def open(self):
        self.cur.execute('SELECT * FROM money;')
        lastrow = self.cur.fetchall()[-1]
        return(lastrow)

if __name__ == "__main__":
    db = DataBase()
    app = Application(root, db)
    app.main()
    app.mainloop()
    db.conn.close()
