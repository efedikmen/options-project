import tkinter as tk
from tkinter import filedialog, Text, Entry, OptionMenu, StringVar, ttk
import os
from bs import *


root= tk.Tk()

root.title=("Option Price Calculator")
canvas1 = tk.Canvas(root, width = 500, height = 600)
canvas1.pack()
opts=["Equity-no dividend", "Equity-with dividend", "Currency", "Futures"]
clicked=StringVar()
clicked.set(opts[0])
drop1=OptionMenu(root, clicked, *opts)
canvas1.create_window(325, 20, window=drop1)
label0 = tk.Label(root, text='Underlying:')
canvas1.create_window(125, 20, window=label0)
entry1=Entry(root)
entry1.insert(-1,'100')
canvas1.create_window(325, 60, window=entry1)
label1 = tk.Label(root, text='Spot Price($):')
canvas1.create_window(125, 60, window=label1)
entry2=Entry(root)
entry2.insert(-1,'100')
canvas1.create_window(325, 90, window=entry2)
label2 = tk.Label(root, text='Strike Price($):')
canvas1.create_window(125, 90, window=label2)
entry3=Entry(root)
entry3.insert(-1,'0')
canvas1.create_window(325, 120, window=entry3)
label3 = tk.Label(root, text='Risk-free rate(%/year):')
canvas1.create_window(125, 120, window=label3)
entry4=Entry(root)
entry4.insert(-1,'30')
canvas1.create_window(325, 150, window=entry4)
label4 = tk.Label(root, text='Time to Maturity(days):')
canvas1.create_window(125, 150, window=label4)
entry5=Entry(root)
entry5.insert(-1,'30')
canvas1.create_window(325, 180, window=entry5)
label5 = tk.Label(root, text='Volatility(%/year):')
canvas1.create_window(125, 180, window=label5)
entry6=Entry(root)
entry6.insert(-1,'0')
canvas1.create_window(325, 210, window=entry6)
label6 = tk.Label(root, text='Continuous Dividend Rate(%):')
canvas1.create_window(125, 210, window=label6)
entry7=Entry(root)
entry7.insert(-1,'0')
canvas1.create_window(325, 240, window=entry7)
label7 = tk.Label(root, text='Foreign Risk-free Rate(%/year):')
canvas1.create_window(125, 240, window=label7)

labelprice = tk.Label(root, text= "0")
canvas1.create_window(250, 330, window=labelprice)

greeks=["delta","gamma","theta","vega","rho"]
label = ttk.Treeview(root, column=greeks)
canvas1.create_window(250, 300, window=label)

def price(call:bool):
    underlying=clicked.get()
    S = float(entry1.get())
    K = float(entry2.get())
    r = float(entry3.get())/100
    t = float(entry4.get())/365
    sigma = float(entry5.get())/100
    q = float(entry6.get())/100
    fr = float(entry7.get())/100
    if opts.index(underlying)==0:
        opt=Option(call,S,K,t,r,sigma)
    elif opts.index(underlying)==1:
        opt=DividendOption(call,S,K,t,r,q,sigma)
    elif opts.index(underlying)==2:
        opt=ForexOption(call,S,K,t,r,fr,sigma)
    elif opts.index(underlying)==3:
        opt=FuturesOption(call,S,K,t,r,sigma)
    labelprice.config(text=float(opt.price()))
    label.insert('', 'end', text="1", values=opt.greeks().values())

button1=tk.Button(root, text="Call Price", command=lambda: price(True))
canvas1.create_window(200, 280, window=button1)

button2=tk.Button(root, text="Put Price",command=lambda: price(False))
canvas1.create_window(300, 280, window=button2)


root.mainloop()