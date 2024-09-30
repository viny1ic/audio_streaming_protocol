from socket import *
import sys
sys.path.append('../')
import obj

def decodeheader(header):
    return int(header, base=16)

def recievepacket():
    msg = obj.Message()
    packet = connectionSocket.recv(1024).decode()
    packet = packet.split("\r\n")
    # print(packet)
    msg.headervalue = decodeheader(packet[0])
    msg.headerbytes = bin(msg.headervalue)
    # print(msg.headerbytes)
    msg.songid = packet[1]
    msg.body = packet[2]
    return msg

def sendpacket(body):
    packet = "" + msg.headervalue + "\r\n"
    msg.body = body
    packet += str(msg.songid) + "\r\n"
    packet += str(msg.body) + "\r\n\r\n"
    connectionSocket.send(packet.encode())

def requesthandler(header, songid):
    print(header)
    print("[i] ", end="")
    if header[-1] == "1":
        playlist.quit()
        connectionSocket.close()
        exit(1)

    if header[-3] == "1":
        body = obj.read_db()
        print("sending music catalog to client")
        return body

    if header[-4] == "1":
        playlist.append(songid)
        body = "Added song to playlist"
        print("added song to playlist")
        return body

    if header[-5] == "1":
        playlist.remove(songid)
        body = "Song removed from playlist"
        print("Song removed from playlist")
        return body

    if header[-6] == "1":
        body = playlist.findbyid(songid)   
        print("Queried song")
        return body

    if header[-8] == "1":
        playlist.setloop()
        body = "Mode changed to loop"
        print("Mode changed to loop")
        return body

    if header[-9] == "1":
        body = "Songs in order of playing: " + ", ".join(playlist.reportqueue()).rstrip(", ")
        print("reporting playlist to client")
        return body
    
    if header[-10] == "1":
        body = "Now playing: " + playlist._queue[playlist.playing]
        print("reporting now playing")
        return body

    if header[-11] == "1":
        playlist.playnext()
        body = "Playing next song"
        print("Playing next Song")
        return body
    
    if header[-12] == "1":
        playlist.goback()
        body = "playing previous song"
        print("Playing previous song")
        return body

    if header[-7] == "1":
        playlist.setshuffle()
        body = "Play mode changed to shuffle"
        print("Play mode changed to shuffle")
        return body

    if header[-2] == "1":
        playlist.mode = 1
        body = "Mode changed to playing"
        print("mode changed to Playing")
        return body

    if header[-2] == "0":
        playlist.mode = 0
        body = "mode changed to design"
        print("mode changed to design")

    if header[-7] == "0":
        playlist.setdefault()
        body = "Play mode changed to default"
        print("Play mode changed to default")

    else:
        body = "Bad request"
        print("Bad request")
    
    return "[i] " + str(body)



serverPort = 12000
playlist = obj.Playlist()
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
connectionSocket, addr = serverSocket.accept()

print( "The server is ready to receive: " )
while(True):    
    try:
        msg = obj.Message()
        pkt = recievepacket()
        body = requesthandler(pkt.headerbytes, pkt.songid)
        sendpacket(body)
    
    except Exception as e:
        print(Exception, e)
        continue
