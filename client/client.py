from socket import *
import sys
sys.path.append('../')
import obj
import time

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

userplaylist = obj.Playlist()
usercatalog = obj.Catalog()

def decodeinput(text, msg):
    text = text.split(" ")
    match text[0].upper():
        case "D":
            obj.MODE = 0
            msg.setheaderparam("mode", 0)
        case "P":
            obj.MODE = 1
            msg.setheaderparam("mode", 1)
        case "C":
            msg.setheaderparam("get_catalog", 1)
        case "A":
            msg.setheaderparam("add", 1)
            msg.setsongid(text[1])

        case "R":
            msg.setheaderparam("remove", 1)
            msg.setsongid(text[1])
        case "F":
            msg.setheaderparam("find", 1)
            msg.setsongid(text[1])
        case "B":
            obj.PLAYMODE = 0
            msg.setheaderparam("play_mode", 0)
        case "E":
            obj.PLAYMODE = 1
            msg.setheaderparam("play_mode", 1)
        case "L":
            msg.setheaderparam("loop", 1)
        case "G":
            msg.setheaderparam("get_playlist", 1)
        case "J":
            msg.setheaderparam("now_playing", 1)
        case "N":
            msg.setheaderparam("play_next", 1)
        case "H":
            msg.setheaderparam("play_last", 1)
        case "I":
            msg.setheaderparam("mode", 0)
        case "Q":
            msg.setheaderparam("quit", 1)
    # print(msg.headerbytes)
          
          
          
message = '''What would you like to do:
1. Set Mode to Design. (enter D)
2. Set Mode to Play. (enter P)
3. Request Music Catalog. (enter C)
4. Add song to playlist (enter A followed by space and song ID)
5. Remove song from playlist (enter R followed by space and song ID)
6. Find a song in playlist (enter F followed by space and song ID)
7. Set playing mode to default. (enter B)
8. Set playing mode to shuffle. (enter E)
9. Set playing mode to loop. (enter L)
10. Get playlist. (enter G)
11. Get now playing. (enter J)
12. Play next song. (enter N)
13. Play previous song. (enter H)
14. Exit playlist mode (enter I)
15. Quit (enter Q)
'''


while True:
    msg = obj.Message()
    choice = input(message)
    decodeinput(choice, msg)
    msg.setheaderparam("mode", obj.MODE)
    msg.setheaderparam("play_mode", obj.PLAYMODE)
    msg.generateheader()
    packet = msg.generatepacket()
    print(msg.headerbytes)
    clientSocket.send(packet.encode())
    modifiedSentence = clientSocket.recv(1024)
    if choice.upper() == "Q":
        time.sleep(2)
        clientSocket.close()
        break
    print('From Server: ', modifiedSentence.decode())