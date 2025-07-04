import time
import pygame
import socket
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker
from rus import rusname



pygame.init()

WIGHT_ROOM,HEIGHT_ROOM = 4000,4000
WIGHT_SERVER,HEIGHT_SERVER = 300,300
MOBS_QUANTITY = 25


FPS = 100

colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown',
        'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow',
        'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'SpringGreen', 'MediumSpringGreen', 'Turquoise',
        'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DeepSkyBlue',
        'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']

screen = pygame.display.set_mode((WIGHT_SERVER,HEIGHT_SERVER))
pygame.display.set_caption("Сервер")
clock = pygame.time.Clock()

engine = create_engine("postgresql+psycopg2://postgres:07021984Apple@localhost/Forse")
Base = declarative_base()
Session = sessionmaker(bind=engine)
s = Session()


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
            result = map(int,vector[first + 1 :second].split(","))
            return result
    return ""


def find_color(info:str):
    first = None
    for num, signl in enumerate(info):
        if signl == "<":
            first = num
        if signl == ">" and first is not None:
            second = num
            result = info[first + 1 :second].split(",")
            return result
        return ""






class Players(Base):
    __tablename__ = "gamers"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name =Column(String(250))
    adress = Column(String)
    x = Column(Integer,default=500)
    y = Column(Integer,default=500)
    size = Column(Integer,default=50)
    errors = Column(Integer,default=0)
    abs_speed = Column(Integer,default=2)
    speed_x = Column(Integer,default=2)
    speed_y = Column(Integer,default=2)
    color = Column(String(250),default="red")
    w_vision = Column(Integer,default=800)
    h_vision = Column(Integer,default=600)





    def __init__(self,name,adress):
        self.name = name
        self.adress = adress


class LocalPlayer:

    def __init__(self,id,name,sock,addr):
        self.id = id
        self.name = name
        self.sock = sock
        self.address = addr
        self.db:Players = s.get(Players,self.id)
        self.x = 500
        self.y = 500
        self.errors = 0
        self.abs_speed = 1
        self.speed_x = 0
        self.speed_y = 0
        self.color = "red"
        self.w_vision = 800
        self.h_vision = 600

    def sync(self):
        self.db.size = self.size
        self.db.abs_speed = self.abs_speed
        self.db.speed_x = self.speed_x
        self.db.speed_y = self.speed_y
        self.db.errors = self.errors
        self.db.x = self.x
        self.db.y = self.y
        self.db.color = self.color
        self.db.w_vision = self.w_vision
        self.db.h_vision =  self.h_vision
        s.merge(self.db)
        s.commit()

    def load(self):
        self.size = self.db.size
        self.abs_speed = self.db.abs_speed
        self.speed_x = self.db.speed_x
        self.speed_y = self.db.speed_y
        self.errors = self.db.errors
        self.x = self.db.x
        self.y = self.db.y
        self.color = self.db.color
        self.w_vision = self.db.w_vision
        self.h_vision = self.db.h_vision
        return self




    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def update2(self):
        
        if self.x - self.size <= 0:
            if self.speed_x >= 0:
                self.x += self.speed_x
        elif self.x + self.size >= WIGHT_ROOM:
            if self.speed_x <= 0:
                self.x += self.speed_x
        else:
            self.x += self.speed_x


        if self.y - self.size <= 0:
            if self.speed_y >= 0:
                self.y += self.speed_y
        elif self.y + self.size >= HEIGHT_ROOM:
            if self.speed_y <= 0:
                self.y += self.speed_y
        else:
            self.y += self.speed_y
    def change_speed(self,vector):
        vector = find(vector)
        if vector[0] == 0 and vector[1] == 0:
            self.speed_x = self.speed_y = 0
        else:
            vector = vector[0] * self.abs_speed,vector[1] * self.abs_speed
            self.speed_x = vector[0]
            self.speed_y = vector[1]







main_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
main_socket.bind(("localhost",10000))
main_socket.setblocking(False)
main_socket.listen(5)
print("сокет создан")

# players = []
players = {}
server_wokrs = True
while server_wokrs:
    try:
        new_socket,addr = main_socket.accept()
        print("подключился",addr)
        new_socket.setblocking(False)
        login = new_socket.recv(1024).decode()
        # players.append(new_socket)
        player = Players("имя",addr)
        if login.startswith("color"):
            data = find_color(login[6:])
            player.name,player.color = data
        s.merge()
        addr = f"({addr[0]},{addr[1]})"
        data = s.query(Players).filter(Players.adress == addr)
        for user in data:
            player = LocalPlayer(user.id,"имя",new_socket,addr).load()
            players[user.id] = player


    except BlockingIOError:
        pass
    for id in list(players):
        try:
            data = players[id].sock.recv(1024).decode()

            print("получил",data)
            players[id].change_speed(data)
        except:
            pass
            # players.remove(sock)
            # sock.close()
            # print("сокет закрыт")

    for id in list(players):
        try:
            players[id].sock.send("Игра".encode())
        except:
            players[id].sock.close()
            del players[id]
            s.query(Players).filter(Players.id == id).delete()
            s.commit()
            print("сокет закрыт")
    for event in pygame.event.get():
        if event == pygame.QUIT:
            server_wokrs = False
    screen.fill("blue")

    for id in list(players):
        player = players[id]
        x = player.x * WIGHT_SERVER // WIGHT_ROOM
        y = player.y *HEIGHT_SERVER // HEIGHT_ROOM
        size = player.size * WIGHT_SERVER // WIGHT_ROOM
        pygame.draw.circle(screen,player.color,(x,y),size)



    for id in list(players):
         player = players[id]
         players[id].update()

    visible_bacterium = []
    for id in list(players):
        visible_bacterium[id] = []

    pairs = list(players.items())
    for i in range(0,len(pairs)):
        for j in range(i+1 ,len(pairs)):
            hero_1 : Players = pairs[i][1]
            hero_2 : Players = pairs[j][1]
            dist_x = hero_2.x-hero_1.x
            dist_y = hero_2.y - hero_1.y
            if abs(dist_x) <= hero_1.w_vision // 2 + hero_2.size and abs(dist_y) <= hero_1.h_vision // 2 + hero_2.size:
                x_ = str(round(dist_x))
                y_ = str(round(dist_y))
                size_ = str(round(hero_2.size))
                color_ = hero_2.color
                data = x_+" "  + y_ +" " + size_ + " " + color_
                visible_bacterium[hero_1.id].append(data)
            if abs(dist_x) >= hero_2.w_vision // 2 + hero_1.size and abs(dist_y) <= hero_2.h_vision // 2 + hero_1.size:
                x_ = str(round(-dist_x))
                y_ = str(round(-dist_y))
                size_ = str(round(hero_2.size))
                color_ = hero_1.color
                data = x_+" "  + y_ +" " + size_ + " " + color_
                visible_bacterium[hero_2.id].append(data)


    for id in list(players):
        visible_bacterium[id] = "<" + ",".join(visible_bacterium[id]) + ">"

    for id in list(players):
        try:
            players[id].sock.send(visible_bacterium[id].encode())
        except:
            pass






    pygame.display.update()

clock.tick(FPS)
pygame.quit()
main_socket.close()
s.query(Players).delete()
s.commit()








