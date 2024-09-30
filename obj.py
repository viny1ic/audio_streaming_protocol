import random
import json

MODE = 0
PLAYMODE = 0

def read_db():
    try:
        f = open('database.json')
        data = f.read()
        # for song in data['catalog']:
        #     tmp = song['id'], song['song_title'], song['artist'], song['album'], song['duration']
        return data

    except:
        print("Cannot Read DB")
        return False

class Message:
    headerlist =  '{ "play_last":0, "play_next":0, "now_playing":0, "get_playlist":0, "loop":0,"play_mode":0, "find":0, "remove":0, "add":0,"get_catalog":0,"mode":0,"quit":0}'
    songid = -1
    headerbytes = '0b1111'
    headervalue = 0x0
    empty_json = {} 
    body = json.dumps(empty_json) 
    def __init__(self):
        self.header = json.loads(self.headerlist)
        self.generateheader()

    def generateheader(self):
        self.headerbytes = '0b1111'
        for key, value in self.header.items():
            self.headerbytes += str(value)
        # print(hex(int(self.headerbytes, base=2)))
        self.headervalue = hex(int(self.headerbytes, base=2))

    def setheaderparam(self, param, value):
        self.header[param] = value

    def setsongid(self, songid):
        self.songid = songid

    def setbody(self, body):
        self.body = body

    def generatepacket(self):
        packet = ""
        packet+=str(self.headervalue) + "\r\n"
        packet+=str(self.songid) + "\r\n"
        packet+=str(self.body) + "\r\n\r\n"
        return packet
# msg = Message()
class Catalog:
    def request(self):
        db = read_db()
        if db != False:
            return db
        return False

class Playlist:
    _queue = []
    _shufflequeue = []
    _history = []
    mode = 0
    playmode = 0
    playing = 0

    def setdesign(self, msg):
        msg.setheaderparam("mode",0)
        self.mode = 0
    
    def setplay(self, msg):
        msg.setheaderparam("mode",1)
        self.mode = 1
    
    def append(self, id):
        self._queue.append(id)
    
    def reportlist(self):
        return 1
    
    def reportqueue(self):
        q = self._queue
        return q
    
    def remove(self, id):
        if self.playmode == 0:
            self._queue.remove(id)
            return True
        return False
    
    def findbyid(self, id):
        try:
            db = read_db()
            found = db.find('{ "id":'+str(id))
            if found == -1:
                return "Not Found"
            response = ""
            for x in db[found:]:
                if x=="\n" or x=="\r\n":
                    break
                response+=x

            return response
        except:
            print("Query Failed")
            return "False"
    
    def setdefault(self):
        self.playmode = 0
    
    def setshuffle(self):
        self._shufflequeue = self._queue
        self.playmode = 1
    
    def setloop(self):
        self.playmode = 2

    def play(self, id):
        return 1
    
    def playnext(self):
        if self.playmode!=3:
            self._history.append(self.playing)
        
        if self.playmode == 0:
            self.playing+=1%len(self._queue)

        elif self.playmode == 1:
            randsong = random.randint(0,max(self._shufflequeue))
            self.playing = randsong
            self._shufflequeue.remove(randsong)

        self.play(self._queue[self.playing])
    
    def goback(self):
        if self.playmode == 0:
            self.playing-=1%len(self._queue)

        if self.playmode == 1:
            songid = self._history[-1]
            self._history = self._history[0:-1]
            self.play(songid)
            return
        
        self.play(self._queue[self.playing])

    def quit(self):
        return 1