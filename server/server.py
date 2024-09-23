from socket import *
from ..src import obj
import json

def decodeheader(header):
    return int(header, base=16)

def recievepacket():
    msg = obj.Message()
    packet = connectionSocket.recv(1024).decode()
    packet = packet.split("\r\n")
    msg.headervalue = decodeheader(packet[0])
    msg.headerbytes = bin(msg.headervalue)[2:]
    msg.songid = packet[1]
    msg.body = packet[2]
    return msg

def sendpacket(body):
    msg = obj.Message()
    packet = "" + msg.headervalue + "\r\n"
    msg.body = body
    packet += msg.songid + "\r\n"
    packet += msg.body + "\r\n\r\n"
    connectionSocket.send(packet.encode())
    connectionSocket.close()

def requesthandler(header, songid):
    if header[-1] == "1":
        playlist.quit()
    elif header[-2] == "0":
        playlist.mode = 0
        body = "True"
        print("mode changed to design")
    elif header[-2] == "1":
        playlist.mode = 1
        body = "True"
        print("mode changed to Playing")
    elif header[-3] == "1":
        body = obj.read_db()
        print("sending music catalog to client")

    elif header[-4] == "1":
        playlist.append(songid)
        body = "True"
        print("added song to playlist")

    elif header[-5] == "1":
        playlist.remove(songid)
        body = "True"
        print("Song removed from playlist")


    elif header[-6] == "1":
        body = playlist.find(songid)
        print("Queried song")


    elif header[-7] == "0":
        playlist.setdefault()
        body = "True"
        print("Play mode changed to default")

    elif header[-7] == "1":
        playlist.setshuffle()
        body = "True"
        print("Play mode changed to default")

    elif header[-8] == "1":
        playlist.setloop()
        body = "True"
        print("Mode changed to loop")

    elif header[-9] == "1":
        body = playlist.reportqueue()
        print("reporting playlist to client")
    
    elif header[-10] == "1":
        body = playlist._queue[playlist.playing]

    elif header[-11] == "1":
        playlist.playnext()
        body = "True"
        print("Playing next Song")
    elif header[-12] == 1:
        playlist.goback()
        body = "True"
        print("Playing last song")
    else:
        body = "False"
        print("Bad request")
    sendpacket(body)



serverPort = 12000
playlist = obj.Playlist()
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print( "The server is ready to receive: " )
while(True):
    msg = obj.Message()
    connectionSocket, addr = serverSocket.accept()
    pkt = recievepacket()
    # if playlist.mode == 0:

