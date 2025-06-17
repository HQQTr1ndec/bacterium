import math
import socket
import pygame


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
sock.connect(("localhost",10000))


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

    screen.fill("gray")
    pygame.draw.circle(screen,(255,0,0),CC,radius=radius)
    pygame.display.update()

    data = sock.recv(1024).decode()
    print("получил ",data)
pygame.quit()




























































