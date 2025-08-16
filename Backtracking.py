class Board:
    def __init__(self,size=8):
        self.size = size
        self.board = self.createMatrix()
        self.board[3][3]="O"
        self.board[4][4]="O"
        self.board[3][4]="X"
        self.board[4][3]="X"
        self.val = {"X":[(3,4),(4,3)],"O":[(3,3),(4,4)]}
        #self.valid = [0 for i in range(self.size)]

    def createMatrix(self):
        return [[0 for i in range(self.size)] for j in range(self.size)]
    
    def disp(self):
        temp = self.valid("X")
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
            if self.board[i[0]-1][i[1]]==self.opposite(val): # Up
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
                    ans.add((index,i[1]))

            if self.board[i[0]+1][i[1]]==self.opposite(val): # Down
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
                    ans.add((index,i[1]))

            if self.board[i[0]][i[1]-1]==self.opposite(val): # Left
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
                    ans.add((i[0],index))

            if self.board[i[0]][i[1]+1]==self.opposite(val): # Right
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
                    ans.add((i[0],index))

            if self.board[i[0]-1][i[1]-1]==self.opposite(val): # Top Left
                flag = True
                index = -1
                for j in range(i[1]-1,-1,-1):
                    if self.board[(i[0]-i[1])+j][j]==val:
                        flag = False
                        break
                    elif self.board[(i[0]-i[1])+j][j]==0:
                        index = j
                        break
                if flag:
                    ans.add(((i[0]-i[1])+index,index))

            if self.board[i[0]+1][i[1]-1]==self.opposite(val): # Bottom Left
                flag = True
                index = -1
                for j in range(i[1]+1,self.size):
                    print((i[0]-i[1])+j,j)

        return list(ans)

    '''
    def insert(self,column,data):
        if self.valid[column]==self.height:
            return False
        self.board[self.height-self.valid[column]-1][column]=data
        self.valid[column]+=1
        return True
    
    def delete(self,column):
        if self.valid[column]==0:
            return False
        self.valid[column]-=1
        self.board[self.height-self.valid[column]-1][column]=0
        return True
    '''
    
temp = Board()
#temp.board[4][2]="X"
temp.board[2][3]="O"
temp.board[1][2]="X"
temp.board[5][2]="O"
temp.board[3][2]="O"
#temp.board[3][2]="O"
print(temp.valid("X"))
temp.disp()
