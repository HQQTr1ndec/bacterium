import time
import socket
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker




engine = create_engine("postgresql+psycopg2://postgres:07021984Apple@localhost/Forse")
Base = declarative_base()
Session = sessionmaker(bind=engine)
s = Session()

class Players(Base):
    __tablename__ = "gamers"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name =Column(String(250))
    adress = Column(String)
    x = Column(Integer,default=500)
    y = Column(Integer,default=500)
    size = Column(Integer,default=50)
    errors = Column(Integer,default=0)
    abs_speed = Column(Integer,default=1)
    speed_x = Column(Integer,default=0)
    speed_y = Column(Integer,default=0)

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







main_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
main_socket.bind(("localhost",10000))
main_socket.setblocking(False)
main_socket.listen(5)
print("сокет создан")

# players = []
players = {}
while True:
    try:
        new_socket,addr = main_socket.accept()
        print("подключился",addr)
        new_socket.setblocking(False)
        players.append(new_socket)
    except BlockingIOError:
        pass
    for sock in players:
        try:
            data = sock.recv(1024).decode()
            print("получил",data)
            sock.send("LoL".encode())

        except:
            players.remove(sock)
            sock.close()
            print("сокет закрыт")

    time.sleep(2)
