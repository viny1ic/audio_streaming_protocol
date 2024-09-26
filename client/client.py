from socket import *
import sys
sys.path.append('../')
import obj

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


userplaylist = obj.Playlist()
usercatalog = obj.Catalog()

def decodeinput(text, msg):
    text = text.split(" ")
    match text[0]:
        case "D":
            msg.setheaderparam("mode", 0)
        case "P":
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
            msg.setheaderparam("play_mode", 0)
        case "E":
            msg.setheaderparam("play_mode", 1)
        case "L":
            msg.setheaderparam("loop", 1)
        case "G":
            msg.setheaderparam("get_playlist", 1)
        case "J":
            msg.setheaderparam("now_playing", 0)
        case "N":
            msg.setheaderparam("play_next", 0)
        case "H":
            msg.setheaderparam("play_last", 0)
        case "I":
            msg.setheaderparam("mode", 0)
        case "Q":
            msg.setheaderparam("quit", 1)
          
          
          
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
    decodeinput(choice)
    if choice == "Q":
        clientSocket.close()
        break
    clientSocket.send(message.encode())
    modifiedSentence = clientSocket.recv(1024)
    print('From Server: ', modifiedSentence.decode())