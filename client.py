import math
import socket
import pygame
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

name = ""
color = ""

def login():
    global name
    name = row.get()
    if name and color:
        root.destroy()
        root.quit()

    else:
        tk.messagebox.showerror("Error","you dont pick color or not write the login")


def scroll(event):
    global color
    color = combo.get()
    style.configure("TCombobox",fieldbackground= color,background="white")

def find(vector:str):
    first = None
    for num, signl in enumerate(vector):
        if signl == "<" :
            first = num
        if signl ==">" and first is not None:
            second = num
            # result = vector[first + 1:second]
            # result = result.split(",")
            # result = map(float,result)
            result = vector[first + 1:second]
            return result
    return ""


def draw_bacterium(data : list[str]):
    for num,bact in enumerate(data):
        data = bact.split(" ")
        x = CC[0]+int(data[0])
        y = CC[1] + int(data[1])
        size = int(data[2])
        color = str(data[3])
        pygame.draw.circle(screen,color,(x,y),size)












root = tk.Tk()
root.title("wazzup dude")
root.geometry("300x200")

style = ttk.Style()
# style.theme_use("combo")

name_label = tk.Label(root,text="say your name")
name_label.pack()
row = tk.Entry(root,width=30,justify="center")
row.pack()
color_label = tk.Label(root,text="Choose your color")
color_label.pack()










colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown',
        'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow',
        'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'Lime Green', 'SpringGreen', 'MediumSpringGreen', 'Turquoise',
        'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'Dark Turquoise', 'DeepSkyBlue',
        'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue.']

combo = ttk.Combobox(root,values=colors,textvariable=color)
combo.bind("<<ComboboxSelected>>",scroll)
combo.pack()
name_bt = tk.Button(root,text = "Come in Game",command=login)
name_bt.pack()
root.mainloop()









sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
sock.connect(("localhost",10000))
sock.send(("color:<"+name+","+color+">").encode())


radius = 50
old = (0,0)
pygame.init()
WIGTH = 800
HEIGHT = 600
CC = (WIGTH//2,HEIGHT//2)
screen = pygame.display.set_mode((HEIGHT,WIGTH))
pygame.display.set_caption("Бактерии")



run = True
while run:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = pos[0]-CC[0],pos[1]-CC[1]

        lenv = math.sqrt(vector[0]**2 + vector[1]**2)
        vector = vector[0] / lenv,vector[1] / lenv
        if lenv <= radius:
            vector = 0, 0

        if vector != old:
            old = vector
            msg = f"<{vector[0]},{vector[1]}>"
            sock.send(msg.encode())
            # sock.send("Стихи Пушкина - https://www.culture.ru/literature/poems/author-aleksandr-pushkin?ysclid=mbqqfikkbt274040913".encode())
    data = sock.recv(1024).decode()
    data = find(data).split(",")
    print("получил ", data)
    screen.fill("gray")
    pygame.draw.circle(screen,color,CC,radius=radius)

    if data != [""]:
        draw_bacterium(data)
    pygame.display.update()



pygame.quit()




























































