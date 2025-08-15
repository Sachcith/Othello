class Board:
    def __init__(self,size=8):
        self.size = size
        self.board = self.createMatrix()
        #self.valid = [0 for i in range(self.size)]

    def createMatrix(self):
        return [[0 for i in range(self.size)] for j in range(self.size)]
    
    def disp(self):
        for i in range(len(self.board)):
            for j in self.board[i]:
                if j=="X":
                    print("⚫",end="")
                elif j=="O":
                    print("⚪",end="")
                else:
                    print("⭕",end="")
            print(i+1)
        for i in range(self.size):
            print(i+1,end=" ")
        print("\n")

    def valid(self,val):
        ans = set()
        
        pass

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
temp.board[3][3]="X"
temp.board[4][4]="O"
temp.disp()
