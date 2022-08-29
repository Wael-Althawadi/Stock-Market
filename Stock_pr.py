from tkinter import *
from tkinter import messagebox, ttk
import requests 
from PIL import Image,ImageTk
import pandas as pd
import matplotlib.pyplot as plt


root = Tk()
root.geometry("850x540+270+100")
root.title("$Stock Market$")
root.resizable(width = False,height = False)
root.config(bg = "#ecf0f1")

df = ""

menu = Menu(root,bg = "#1a5276",fg = "white",bd = 3,relief = "raised")

sub1 = Menu(menu,tearoff = 0)
menu.add_cascade(label = "edit",font = 7,menu = sub1)
sub1.add_command(label = "move")
sub1.add_command(label = "delete")

menu.add_command(label = "exit",font = 7,command = root.destroy)

root.config(menu = menu)

im = Image.open("/home/wael/Downloads/stock_image_ed.jpg")
image = ImageTk.PhotoImage(im)

l_im = Label(root,image = image)
l_im.place(x = 20,y = 20)

l_im2 = Label(root,image = image)
l_im2.place(x = 720,y = 20)

frame1 = Frame(root,width = 500,height = 150,bg = "silver",bd = 2,relief = "raised")
frame1.place(x = 175,y = 10)

frame2 = Frame(root,width = 830,bg = "silver",bd = 2,relief = "raised")
frame2.place(height = 360,x = 10,y = 168)

frame3 = Frame(root,width = 850,height = 50 ,bg = "#1a5276",bd = 2,relief = "raised")
frame3.place(x = 0,y = 527)

frame4 = Frame(root,width = 10,height = 540 ,bg = "#1a5276",bd = 2,relief = "raised")
frame4.place(x = 0,y = 0)

frame5 = Frame(root,width = 10,height = 540 ,bg = "#1a5276",bd = 2,relief = "raised")
frame5.place(x = 840,y = 0)

title = Label(frame1,text = "Stock Market Prices",bg = "#1a5276" ,fg = "white",font = ("Arial",20),bd = 2,relief = "groove")
title.place(x = 130,y = 5)

var = StringVar()


Radiobutton(frame1,text = "Apple",font = 16,fg = "#1a5276",variable = var,value = 1).place(x = 10,y = 60)
Radiobutton(frame1,text = "Nike",font = 16,fg = "#1a5276",variable = var,value = 2).place(x = 100,y = 60)
Radiobutton(frame1,text = "Tesla",font = 16,fg = "#1a5276",variable = var,value = 3).place(x = 190,y = 60)
Radiobutton(frame1,text = "Disney",font = 16,fg = "#1a5276",variable = var,value = 4).place(x = 290,y = 60)
Radiobutton(frame1,text = "Google",font = 16,fg = "#1a5276",variable = var,value = 5).place(x = 390,y = 60)


sc = Scrollbar(root)
sc.place(height = 290,x = 820,y = 184)

my_tree = ttk.Treeview(frame2,yscrollcommand = sc.set)

style = ttk.Style()
style.theme_use("alt")
style.configure("Treeview",
               background = "silver",
               fieldbackground = "silver")
style.map("Treeview",background = [("selected","#28b463")] )

var2 = StringVar()

def dark():
    
    if var2.get() == "1":
        root.configure(bg = "#121212")
        frame1["bg"] = "#121212"
        frame2["bg"] = "#121212"
        if style != "":
            style.configure("Treeview",foreground = "white",background = "#121212",fieldbackground = "#121212")
    elif var2.get() == "0":
        root.configure(bg = "#ecf0f1")
        frame1["bg"] = "silver"
        frame2["bg"] = "silver"
        if style != "":
            style.configure("Treeview",foreground = "black",background = "silver",fieldbackground = "silver")

    
Checkbutton(root,text = "Dark Mode",fg = "#121212",font = 12,variable = var2,command = dark).place(x = 10,y = 140)

def get_data(s_n):
    global df
    global req3
    
    for i in my_tree.get_children():
        my_tree.delete(i)

        
    try:
        req3 = requests.get(f"http://api.marketstack.com/v1/eod?access_key=ae46c9de8fcfc33c9591520cd686d10f&symbols={s_n}").json()
    except :
        messagebox.showerror("error","check connection!")
    
    else:
        l = ["date","open","high","low","close","volume","adj_close","split_factor","dividend","symbol","exchange"]
        df = pd.DataFrame(req3["data"])
        df.dropna(axis=1,how="all",inplace=True)
        df = df.reindex(columns=l)
        df["date"] = pd.to_datetime(df["date"])
    
        my_tree["columns"] = [i for i in df.columns]
        my_tree["show"] = "headings"
        
        
        for x in df.columns:
            my_tree.heading(x,text = x)
        

        for data in df.values.tolist():
            my_tree.insert("","end",values = data)
            
    

    my_tree.place(width = 800,height = 290,x = 5,y = 15)
    sc.config(command = my_tree.yview)

def get():
    if var.get() == "1":
        get_data("AAPL")
    elif var.get() == "2":
        get_data("NKE")
    elif var.get() == "3":
        get_data("TSLA")
    elif var.get() == "4":
        get_data("DIS")
    elif var.get() == "5":
        get_data("GOOGL")
    else:
        messagebox.showerror("error","choose a stock!")

b = Button(frame1,text = "Get Data",fg = "white",font = ("Arial",16),bg = "#28b463",bd = 2 ,relief = "raised",
           command = get)
b.place(width = 165,x = 180,y = 100)

def chart():
    try:

        options = [i for i in set(df["date"].dt.month)]
    except :
        messagebox.showerror("error","Get Data Firist!")
    
    else:
        top = Toplevel()
        top.geometry("300x170+500+190")
        
        l = Label(top,text = "Choose month!",fg = "blue",font = ("Arial",12),bg = "white",relief = "groove")
        l.place(x = 92,y = 6)

        var3 = StringVar()
        OptionMenu(top,var3,*options).place(width = 90,x = 106,y = 50)
        var.set("monthly")
    
        def show():

            monthly = df[["date","open"]][(df["date"] >= f"2022-0{var3.get()}-01")&(df["date"] < f"2022-0{str(int(var3.get()) + 1)}-01")]
            plt.barh(monthly["date"],monthly["open"],label = "Stock$price 'M' ")
            plt.style.use("fivethirtyeight")
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.legend()
            plt.tight_layout()
            plt.show()

        ch_b = Button(top,text = "show",padx = 20,bg = "green",fg = "white",command = show)
        ch_b.place(x = 115,y = 100)

b2 = Button(frame2,text = "Get Chart",padx = 29,pady = 7,fg = "white",bg = "red",command = chart)
b2.place(x = 365,y = 315)

mainloop()
