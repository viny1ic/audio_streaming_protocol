import random
import json

def read_db():
    try:
        f = open('database.json')
        data = json.load(f)
        for song in data['catalog']:
            tmp = song['id'], song['song_title'], song['artist'], song['album'], song['duration']
        return data

    except:
        print("Cannot Read DB")
        return False



class Catalog:
    def request(self):
        db = read_db()
        if db != False:
            return db
        return False

class Playlist:
    _queue = [-1]
    _shufflequeue = [-1]
    _history = [-1]
    mode = 0
    playmode = 0
    playing = 0

    def setdesign(self):
        self.mode = 0
    
    def setplay(self):
        self.mode = 1
    
    def append(self, id):
        self._queue.append(id)
    
    def reportlist(self):
        return 1
    
    def reportqueue(self):
        q = self._queue
        return q
    
    def remove(self):
        self._queue = self._queue[0:-1]
    
    def find(self):
        return 1
    
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
        if self.playmode!=3 and self._history[-1]!=self.playing:
            self._history.append(self.playing)
        
        if self.playmode == 0:
            self.playing+=1%len(self._queue)

        elif self.playmode == 1:
            randsong = random.randint(0,len(self._shufflequeue))
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