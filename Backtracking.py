class Board:
    __undo = None
    def __init__(self,size=8):
        self.size = size
        self.board = self.createMatrix()
        self.board[3][3]="O"
        self.board[4][4]="O"
        self.board[3][4]="X"
        self.board[4][3]="X"
        self.__undo = self.board
        self.val = {"X":[(3,4),(4,3)],"O":[(3,3),(4,4)]}
        self.__undo_Dict = self.val
        #self.valid = [0 for i in range(self.size)]

    def createMatrix(self):
        return [[0 for i in range(self.size)] for j in range(self.size)]
    
    def disp(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j]=="X":
                    print("⚫",end="")
                elif self.board[i][j]=="O":
                    print("⚪",end="")
                else:
                    print("⭕",end="")
            print(i)
        for i in range(self.size):
            print(i,end=" ")
        print("\n")


    def disp_val(self,val="X"):
        temp = self.valid(val)
        for i in range(len(temp)):
            temp[i]=temp[i][:-1]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i,j) in temp:
                    print("✳️",end="")
                elif self.board[i][j]=="X":
                    print("⚫",end="")
                elif self.board[i][j]=="O":
                    print("⚪",end="")
                else:
                    print("⭕",end="")
            print(i)
        for i in range(self.size):
            print(i,end=" ")
        print("\n")

    def opposite(self,val):
        if val=="X":
            return "O"
        return "X"

    def valid(self,val):
        ans = set()
        temp = self.val[val]
        for i in temp:
            if i[0]-1>=0 and self.board[i[0]-1][i[1]]==self.opposite(val): # Up
                flag = True
                index = -1
                for j in range(i[0]-1,-1,-1):
                    if self.board[j][i[1]]==val:
                        flag = False
                        break
                    elif self.board[j][i[1]]==0:
                        index = j
                        break
                if flag:
                    ans.add((index,i[1],1))

            if i[0]+1<self.size and self.board[i[0]+1][i[1]]==self.opposite(val): # Down
                flag = True
                index = -1
                for j in range(i[0]+1,self.size):
                    if self.board[j][i[1]]==val:
                        flag = False
                        break
                    elif self.board[j][i[1]]==0:
                        index = j
                        break
                if flag:
                    ans.add((index,i[1],0))

            if i[1]-1>=0 and self.board[i[0]][i[1]-1]==self.opposite(val): # Left
                flag = True
                index = -1
                for j in range(i[1]-1,-1,-1):
                    if self.board[i[0]][j]==val:
                        flag = False
                        break
                    elif self.board[i[0]][j]==0:
                        index = j
                        break
                if flag:
                    ans.add((i[0],index,3))

            if i[1]+1<self.size and self.board[i[0]][i[1]+1]==self.opposite(val): # Right
                flag = True
                index = -1
                for j in range(i[1]+1,self.size):
                    if self.board[i[0]][j]==val:
                        flag = False
                        break
                    elif self.board[i[0]][j]==0:
                        index = j
                        break
                if flag:
                    ans.add((i[0],index,2))

            if i[0]-1>=0 and i[1]-1>=0 and self.board[i[0]-1][i[1]-1]==self.opposite(val): # Top Left
                flag = True
                index = -1
                for j in range(i[0]-1,-1,-1):
                    if i[1]-i[0]+j>=0:
                        if self.board[j][i[1]-i[0]+j]==val:
                            flag = False
                            break
                        elif self.board[j][i[1]-i[0]+j]==0:
                            index = j
                            break
                    else:
                        break
                if flag:
                    ans.add((index,i[1]-i[0]+index,5))

            if i[0]+1<self.size and i[1]+1<self.size and self.board[i[0]+1][i[1]+1]==self.opposite(val): # Bottom Right
                flag = True
                index = -1
                for j in range(i[0]+1,self.size):
                    if i[1]-i[0]+j<self.size:
                        if self.board[j][i[1]-i[0]+j]==val:
                            flag = False
                            break
                        elif self.board[j][i[1]-i[0]+j]==0:
                            index = j
                            break
                    else:
                        break
                if flag:
                    ans.add((index,i[1]-i[0]+index,4))

            if i[0]-1>=0 and i[1]+1<self.size and self.board[i[0]-1][i[1]+1]==self.opposite(val): # Top Right
                flag = True
                index = -1
                for j in range(i[0]-1,-1,-1):
                    if i[1]+i[0]-j<self.size:
                        if self.board[j][i[1]+i[0]-j]==val:
                            flag = False
                            break
                        elif self.board[j][i[1]+i[0]-j]==0:
                            index = j
                            break
                    else:
                        break
                if flag:
                    ans.add((index,i[1]+i[0]-index,7))

            if i[0]+1<self.size and i[1]-1>=0 and self.board[i[0]+1][i[1]-1]==self.opposite(val): # Bottom Left
                flag = True
                index = -1
                for j in range(i[0]+1,self.size):
                    if i[1]+i[0]-j>=0:
                        if self.board[j][i[1]+i[0]-j]==val:
                            flag = False
                            break
                        elif self.board[j][i[1]+i[0]-j]==0:
                            index = j
                            break
                    else:
                        break
                if flag:
                    ans.add((index,i[1]+i[0]-index,6))

        return list(ans)
    
    def copy(self,x):
        return [i[:] for i in x]
    
    def copy_dict(self,x):
        temp = {}
        for i in x:
            temp[i]=x[i]
        return temp
    
    def insert(self,row,column,val):
        if (row,column) not in [i[:-1] for i in self.valid(val)]:
            return False
        if self.board[row][column]!=0:
            return False
        self.__undo = self.copy(self.board)
        self.__undo_Dict = self.copy_dict(self.val)
        for i in self.valid(val):
            if (row,column)==i[:-1]: 
                if i[2]==0: # Up
                    for j in range(i[0]-1,-1,-1):
                        if self.board[j][i[1]]==val:
                            break
                        self.board[j][i[1]]==val
                        self.val[val].append((j,i[1]))
                        self.val[self.opposite(val)].remove((j,i[1]))

                elif i[2]==1: # Down
                    for j in range(i[0]+1,self.size):
                        if self.board[j][i[1]]==val:
                            break
                        self.board[j][i[1]]=val
                        self.val[val].append((j,i[1]))
                        self.val[self.opposite(val)].remove((j,i[1]))

                elif i[2]==2: # Left
                    for j in range(i[1]-1,-1,-1):
                        if self.board[i[0]][j]==val:
                            break
                        self.board[i[0]][j]=val
                        self.val[val].append((i[0],j))
                        self.val[self.opposite(val)].remove((i[0],j))

                elif i[2]==3: # Right
                    for j in range(i[1]+1,self.size):
                        if self.board[i[0]][j]==val:
                            break
                        self.board[i[0]][j]=val
                        self.val[val].append((i[0],j))
                        self.val[self.opposite(val)].remove((i[0],j))
            
                elif i[2]==4: # Top Left
                    for j in range(i[0]-1,-1,-1):
                        if i[1]-i[0]+j>=0:
                            if self.board[j][i[1]-i[0]+j]==val:
                                break
                            self.board[j][i[1]-i[0]+j]=val
                        self.val[val].append((j,i[1]-i[0]+j))
                        self.val[self.opposite(val)].remove((j,i[1]-i[0]+j))

                elif i[2]==5: # Bottom Right
                    for j in range(i[0]+1,self.size):
                        if i[1]-i[0]+j<self.size:
                            if self.board[j][i[1]-i[0]+j]==val:
                                break
                            self.board[j][i[1]-i[0]+j]=val
                        self.val[val].append((j,i[1]-i[0]+j))
                        self.val[self.opposite(val)].remove((j,i[1]-i[0]+j))

                elif i[2]==6: # Top Right
                    for j in range(i[0]-1,-1,-1):
                        if i[1]+i[0]-j<self.size:
                            if self.board[j][i[1]+i[0]-j]==val:
                                break
                            self.board[j][i[1]+i[0]-j]=val
                        self.val[val].append((j,i[1]+i[0]-j))
                        self.val[self.opposite(val)].remove((j,i[1]+i[0]-j))

                else: # Bottom Left
                    for j in range(i[0]+1,self.size):
                        if i[1]+i[0]-j>=0:
                            if self.board[j][i[1]+i[0]-j]==val:
                                break
                            self.board[j][i[1]+i[0]-j]=val
                        self.val[val].append((j,i[1]+i[0]-j))
                        self.val[self.opposite(val)].remove((j,i[1]+i[0]-j))
        self.board[row][column]=val
        self.val[val].append((row,column))
        return True
    
    def undo(self):
        self.board = self.copy(self.__undo)
        self.val = self.copy_dict(self.__undo_Dict)

class Othello:
    __board = None
    __player = None
    
    def __init__(self):
        self.__board = Board()
        self.__player = True

    def start_game(self):
        count = 64 - 4
        self.__board.disp()
        while count!=0:
            count-=1
            if self.__player:
                self.__player = False
                self.__board.disp_val("X")
                row = int(input("Enter Row: "))
                col = int(input("Enter Col: "))
                self.__board.insert(row,col,"X")
            else:
                self.__player = True
                self.__board.disp_val("O")
                row = int(input("Enter Row: "))
                col = int(input("Enter Col: "))
                self.__board.insert(row,col,"O")


'''    
temp = Board()
temp.board[2][2]="O"
temp.board[2][3]="O"
temp.board[2][4]="O"
temp.board[3][2]="O"
temp.board[3][3]="X"
temp.board[3][4]="O"
temp.board[4][2]="O"
temp.board[4][3]="O"
temp.board[4][4]="O"
print(temp.valid("X"))
temp.disp()
temp.board[1][3]="X"
print(temp.insert(3,5,"X"))
temp.disp()
temp.undo()
temp.disp()
'''
temp = Othello()
temp.start_game()