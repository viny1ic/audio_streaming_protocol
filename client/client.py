from socket import *
from ..src import obj


serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
message = '''What would you like to do:
1. Set Mode to Design. (enter D)
2. Set Mode to Play. (enter P)
3. Request Music Catalog. (enter C)
4. Add song to playlist (enter A followed by song ID)
5. Remove song from playlist (enter R followed by song ID)
6. Find a song in playlist (enter F followed by song ID)
7. Set playing mode to default.
8. Set playing mode to shuffle.
9. Set playing mode to loop.
10. Get playlist.
11. Get now playing.
12. Play next song.
13. Play previous song.
14. Exit playlist mode
15. Quit
'''

while True:
    choice = input(message)
    clientSocket.send(message.encode())
    modifiedSentence = clientSocket.recv(1024)
    print('From Server: ', modifiedSentence.decode())
clientSocket.close()