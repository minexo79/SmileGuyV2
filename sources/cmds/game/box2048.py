import random as ra

class box2048():

    def __init__(self):

        self.game_list = [['0','0','0','0'],['0','0','0','0'],['0','0','0','0'],['0','0','0','0']]
        self.spawn_2or4(self.game_list)
        self.num_emoji_dict={
            '0': '⬛','2': '🟥','4': '🟧','8': '🟨',
            '16':'🟩','32':'🟦','64':'🟪','128':'🟫',
            '256':'⬜','512':'❤️','1024':'🧡','2048':'💛',
            '⬛': '0','🟥': '2','🟧': '4','🟨': '8',
            '🟩':'16','🟦':'32','🟪':'64','🟫':'128',
            '⬜':'256','❤️':'512','🧡':'1024','💛':'2048',
        }
        self.score = 0 
    
    def spawn_2or4(self,curlst):
        lst=['2','2','2','2','2','2','2','2','2','2','2','2','4']
        zero_lst = []
        for i in range(len(curlst)):
            for r in range(len(curlst[i])):
                if curlst[i][r] == '0':
                    zero_lst.append([i,r])
        if len(zero_lst) == 0:
            return
        ra.shuffle(zero_lst)
        for i in range(2 if len(zero_lst)>1 else 1):
            curlst[zero_lst[i][0]][zero_lst[i][1]] = ra.choice(lst)
        return curlst

    def num_2_emoji(self):
        curlst = self.game_list
        for i in range(len(curlst)):
            for r in range(len(curlst[i])):
                a = curlst[i][r]
                if 'l' in a:
                    a = a[0:len(a)-1]
                curlst[i][r] = self.num_emoji_dict[a]
        return curlst

    def stringlize(self):
        lst = self.num_2_emoji()
        s = ''
        for i in lst:
            s += ''.join(i)
            s += '\n'
        return s,self.check()

    def matrixize(self,st):
        lst=st.split('\n')
        lst2 = []
        for i in lst:
            lst2.append([i[0],i[1],i[2],i[3]])
        return lst2

    def numerize(self):
        curlst = self.game_list
        for i in range(len(curlst)):
            for r in range(len(curlst[i])):
                a = curlst[i][r]
                curlst[i][r] = self.num_emoji_dict[a]
        return curlst

    def userinput(self,x):
        if x in ["◀","🔼","🔽","▶","⏹"]:
            y={"🔼":self.up,"🔽":self.down,"◀":self.left,"▶":self.right}
            y[x]()

    def up(self):
        curlst = self.game_list
        moved = 0
        score = 0
        chord = []
        for i in range(3):
            for r in range(4):
                w = i+1
                while w>0:
                    w -= 1
                    #[w][r]是目標方格  
                    #[i+1][r]是原方格
                    if curlst[i+1][r] == '0':
                        chord = []
                        break
                    if curlst[w][r] == '0':
                        chord = [w,r,int(curlst[i+1][r])]
                        moved = 1
                        pass
                    if curlst[i+1][r] == curlst[w][r] and not 'l' in curlst[w][r]:
                        chord = [w,r,str(int(curlst[i+1][r])*2)+'l']
                        moved = 1
                        score += int(curlst[i+1][r])*2
                        break
                    if not curlst[i+1][r] == curlst[w][r] and not curlst[w][r] == '0':
                        chord = [w+1,r,int(curlst[i+1][r])]
                        if not w+1 == i+1:
                            moved = 1
                        break
                if len(chord) == 0:
                    pass
                if len(chord) == 3:
                    curlst[i+1][r] = '0'
                    curlst[chord[0]][chord[1]] = str(chord[2])
        if moved == 1:
            self.game_list = self.spawn_2or4(curlst)
            self.score += score
        else:
            pass

    def down(self):
        curlst = self.game_list
        moved = 0
        score = 0
        chord = []
        for i in range(3):
            b = 2-i
            for r in range(4):
                w = b
                while w<3:
                    w += 1
                    if curlst[b][r] == '0':
                        chord = []
                        break
                    if curlst[w][r] == '0':
                        chord = [w,r,int(curlst[b][r])]
                        moved = 1
                        pass
                    if curlst[b][r] == curlst[w][r] and not 'l' in curlst[w][r]:
                        chord = [w,r,str(int(curlst[b][r])*2)+'l']
                        moved = 1
                        score += int(curlst[b][r])*2
                        break
                    if not curlst[b][r] == curlst[w][r] and not curlst[w][r] == '0':
                        chord = [w-1,r,int(curlst[b][r])]
                        if not w-1 == b:
                            moved = 1
                        break
                if len(chord) == 0:
                    pass
                if len(chord) == 3:
                    curlst[b][r] = '0'
                    curlst[chord[0]][chord[1]] = str(chord[2])
        if moved == 1:
            self.game_list = self.spawn_2or4(curlst)
            self.score += score
        else:
            pass

    def right(self):
        curlst = self.game_list
        moved = 0
        score = 0
        chord = []
        for i in range(3):
            b = 2-i
            for r in range(4):
                w = b
                while w<3:
                    w += 1
                    if curlst[r][b] == '0':
                        chord = []
                        break
                    if curlst[r][w] == '0':
                        chord = [r,w,int(curlst[r][b])]
                        moved = 1
                        continue
                    if curlst[r][b] == curlst[r][w] and not 'l' in curlst[r][w]:
                        chord = [r,w,str(int(curlst[r][b])*2)+'l']
                        moved = 1
                        score += int(curlst[r][b])*2
                        break
                    if not curlst[r][b] == curlst[r][w] and not curlst[r][w] == '0':
                        chord = [r,w-1,int(curlst[r][b])]
                        if not w-1 == b:
                            moved = 1
                        break
                if len(chord) == 0:
                    pass
                if len(chord) == 3:
                    curlst[r][b] = '0'
                    curlst[chord[0]][chord[1]] = str(chord[2])
        if moved == 1:
            self.game_list = self.spawn_2or4(curlst)
            self.score += score
        else:
            pass

    def left(self):
        curlst = self.game_list
        moved = 0
        score = 0
        chord = []
        for i in range(3):
            for r in range(4):
                w = i+1
                while w>0:
                    w -= 1
                    if curlst[r][i+1] == '0':
                        chord = []
                        break
                    if curlst[r][w] == '0':
                        chord = [r,w,int(curlst[r][i+1])]
                        moved = 1
                        pass
                    if curlst[r][w] == curlst[r][i+1] and not 'l' in curlst[r][w]:
                        chord = [r,w,str(int(curlst[r][w])*2)+'l']
                        moved = 1
                        score += int(curlst[r][i+1])*2
                        break
                    if not curlst[r][w] == curlst[r][i+1] and not curlst[r][w] == '0':
                        chord = [r,w+1,int(curlst[r][i+1])]
                        if not w+1 == i+1:
                            moved = 1
                        break
                if len(chord) == 0:
                    pass
                if len(chord) == 3:
                    curlst[r][i+1] = '0'
                    curlst[chord[0]][chord[1]] = str(chord[2])
        if moved == 1:
            self.game_list = self.spawn_2or4(curlst)
            self.score += score
        else:
            pass

    def check(self):
        lst = self.game_list
        length = len(lst)
        for i in lst:
            if '⬛' in i:
                return 0
        for i in range(len(lst)):
            w = i%2
            while w<len(lst):
                if w+1<length:
                    if lst[i][w+1] == lst[i][w] or lst[i][w+1] == '⬛':
                        return 0
                if w-1>-1:
                    if lst[i][w-1] == lst[i][w] or lst[i][w-1] == '⬛':
                        return 0 
                if i+1<length:
                    if lst[i+1][w] == lst[i][w] or lst[i+1][w] =='⬛':
                        return 0 
                if i-1>-1:
                    if lst[i-1][w] == lst[i][w] or lst[i-1][w] =='⬛':
                        return 0 
                w+=2
        return 1