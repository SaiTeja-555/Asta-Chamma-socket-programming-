import socket #module used to create server
from _thread import *
from player import Player
import pickle #for transferring objects via server
from game import Game

#only bytes data type can be transfered via server. That's why we use str.encode() function to convert string to bytes data type


server = "10.11.4.234"
port = 5555
max_connections = 2

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #AF_INET indicate that we bind address family of ip_address
                                                     #SOCK_STREAM indicate that we use protocol of "stream"(TCP)           

try:
    s.bind((server,port))
    s.listen(max_connections)
    print("Waiting for a connection, Server Started")
except socket.error as e:
    print(str(e))


# players = [Player(1,2,0,(255,0,0),(-1,0),(0,-1)),
#             Player(2,2,4,(0,255,0),(1,0),(0,1)),
#             Player(3,0,2,(0,0,255),(0,1),(-1,0)),
#             Player(4,4,2,(255,255,0),(0,-1),(1,0))]

connected = set()
games = {}
idCount = 0
gameId = 0

def threaded_client(conn, p, gameId):
    global idCount
    
    reply = ""
    while True:
        
        try:
            data = conn.recv(2048).decode() 
            if gameId in games:
                game = games[gameId]

            if not data:
                print("Disconnected")
                break
            else:
                if data == "get":
                    game.reset_player_blitting()
                elif "dice" in data:
                    if "increase" in data:
                        game.dice_increase()
                    elif "click" in data:
                        game.dice_click(int(data[-1]))
                    elif "eligibility" in data:
                        game.dice_eligibility()
                    elif "selection" in data:
                        game.dice_selection(int(data[-1]))
                    elif "cancel" in data:
                        game.dice_cancel()
                elif "blink" in data:
                    game.blink_increase()
                elif "pawn_select" in data:
                    game.pawn_selection(int(data[-1]))
                elif "move" in data:
                    game.move()
                
                reply = game
            conn.sendall(pickle.dumps(reply))
                    
        except socket.error as e:
            print("Data receiving error"+str(e))
            break
    print("Lost Connection")
    try:            #trying because 2 player might close the same game at a time
        del game[gameId]
        print("Closing Game",gameId)
    except: 
        pass
    conn.close() 

num_of_players = 0
game_started = False
while True:
    try:
        conn, addr = s.accept() #waits until some client gets connected and returns the conn object and ip_addr of client
        print("Connected to :", addr)
    except:
        print("Error")
        break
    
    idCount += 1
    if not game_started:
        p = 1
    else:
        p += 1
            
    try:
        conn.send(str.encode(str(p)))
    except socket.error as e:
        print(e)
        conn.close()
    if p == 1:
        game_started = True
        try:
            num_of_players = int(conn.recv(1024).decode())
            conn.send(pickle.dumps(None))
        except socket.error as e:
            print(e)
            conn.close()
        gameId += 1
        games[gameId] = Game(gameId,num_of_players)
        print("Creating a new game ...")
    elif p == num_of_players:
        game_started = False
        games[gameId].connected = True
    start_new_thread(threaded_client,(conn, p, gameId))
    
