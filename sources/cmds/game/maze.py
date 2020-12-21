import random
import copy
import math
class Game():
    def __init__(self,level = None):
        self.map = []
        self.height = 11
        self.width = 11 
        if level != None :
            if level/2 == 0 :
                level+=1
            if level > 21 :
                level = 21
            self.height += level
            self.width += level
      
        for i in range(self.height): #generate a blank map
            self.map.append([])
            for x in range(self.width):
                self.map[i].append("⬛")
        self.list = [[2,0],[0,2],[-2,0],[0,-2]] #right under left up 
        self.record = []
        self.x = 1
        self.y = 1
        self.max = 0
        self.maxXY = [self.x,self.y]
        self.generate()
        self.map[self.maxXY[1]][self.maxXY[0]] = "🟥"
    def generate(self):
        while 1 :
            self.map[self.y][self.x] = '⬜'
            List = random.sample(self.list,4)
            number = 0
            for i in List :
                if self.go(i[0],i[1]) :
                    number += 1
                    break
            if not number :
                if not len(self.record) :
                    break
                else :
                    self.x,self.y = self.record[len(self.record)-1]
                    del self.record[len(self.record)-1]
            if len(self.record) > self.max : #Farthest position
                self.maxXY = [self.x,self.y]
                self.max = len(self.record)
                        
    def go(self,x,y): #mobile
        if not 0 < self.x < self.width and 0 < self.y <self.height : return
        if 0 < self.y+y <self.height and 0 < self.x+x <self.width :
            if self.map[self.y+y][self.x+x] != '⬜' :
                self.map[int(self.y+y/2)][int(self.x+x/2)] = "⬜"
                self.x += x
                self.y += y
                self.record.append([self.x,self.y])
                return True        
    def returnmap(self):
        return self.map
class Play():
    def __init__(self,level,number):
        if level == None :
            self.map = Game().returnmap()
        elif level.isdigit() :
            self.map = Game(int(level)).returnmap()
        else :
            self.map = Game(number).returnmap()
        self.level = level
        self.player = [1,1]
        self.list = {"🔼":[0,-1],"🔽":[0,1],"◀":[-1,0],"▶":[1,0]}
    def userinput(self,x) :
        if x in self.list.keys() :
            if self.go(self.list[x][0],self.list[x][1]) :
                return True
    def go(self,x,y) :
        if self.map[self.player[1]+y][self.player[0]+x] == "🟥" : return True #end
        if self.map[self.player[1]+y][self.player[0]+x] == "⬜" :
            self.player[0] += x
            self.player[1] += y
    def print(self) :
        w = copy.deepcopy(self.map)
        w[self.player[1]][self.player[0]] = '🟨' #player
        if self.level == "limit" :
            w = self.limit(w)
        return "\n".join(map(lambda x : "".join(x),w))
    def limit(self,Map) :
        for i in range(len(Map)) :
            for x in range(len(Map[i])) :
                if 2 < math.sqrt(abs((self.player[0] - x)**2 + (self.player[1] - i)**2)) :
                    Map[i][x] = "🔳"
        return Map