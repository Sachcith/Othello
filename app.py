from flask import Flask,render_template,redirect
from flask_socketio import SocketIO
import time


import os
import re
import pandas as pd
import numpy as np
from PIL import Image
from tqdm import tqdm
from ultralytics import YOLO



app = Flask(__name__)
socketio = SocketIO(app)

class Board:
    undo = None
    def __init__(self,size=8):
        self.size = size
        self.board = self.createMatrix()
        self.board[3][3]="O"
        self.board[4][4]="O"
        self.board[3][4]="X"
        self.board[4][3]="X"
        self.undo1 = [[[0 for i in range(8)] for j in range(8)]]
        self.val = {"X":[(3,4),(4,3)],"O":[(3,3),(4,4)]}
        self.undo_Dict = []

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
                if flag and index!=-1:
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
                if flag and index!=-1:
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
                if flag and index!=-1:
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
                if flag and index!=-1:
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
                if flag and index!=-1:
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
                if flag and index!=-1:
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
                if flag and index!=-1:
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
                if flag and index!=-1:
                    ans.add((index,i[1]+i[0]-index,6))

        return list(ans)
    
    def copy(self,x):
        return [i[:] for i in x]
    
    def copy_dict(self,x):
        temp = {}
        for i in x:
            temp[i]=[]
            temp[i].extend(x[i])
        return temp
    
    def insert(self,row,column,val):
        if (row,column) not in [i[:-1] for i in self.valid(val)]:
            return False
        if self.board[row][column]!=0:
            return False
        self.undo1.append(self.copy(self.board))
        self.undo_Dict.append(self.copy_dict(self.val))
        for i in self.valid(val):
            if (row,column)==i[:-1]: 
                if i[2]==0: # Up
                    for j in range(i[0]-1,-1,-1):
                        if self.board[j][i[1]]==val:
                            break
                        self.board[j][i[1]]=val
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
        self.board = self.copy(self.undo1.pop())
        self.val = self.copy_dict(self.undo_Dict.pop())

    def heuristic(self):
        weights = [
            [100, -20, 10, 5, 5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, 1, 1, 1, 1, -2, 10],
            [5, -2, 1, 0, 0, 1, -2, 5],
            [5, -2, 1, 0, 0, 1, -2, 5],
            [10, -2, 1, 1, 1, 1, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100]
        ]
        penality = 0
        for i in range(len(self.val["X"])):
            penality += weights[self.val["X"][i][0]][self.val["X"][i][1]]
        for i in range(len(self.val["O"])):
            penality -= weights[self.val["O"][i][0]][self.val["O"][i][1]]
        return penality
    
    def winloss(self):
        if len(self.val["O"])==0:
            return 200
        if len(self.val["X"])==0:
            return 200
        return 0

class Othello:
    board = None
    player = None
    
    def __init__(self):
        self.board = Board()
        self.player = False
        
    def next_move_alpha_beta(self,player,max_depth,cur_depth=0,row=-1,column=-1,alpha=float("-inf"),beta=float("inf")):
        if self.board.val["O"]==[]:
            return 10**5,row,column
        if self.board.val["X"]==[]:
            return -1*10**5,row,column
        if self.board.winloss()!=0:
            return self.board.winloss(),row,column
        if cur_depth == max_depth:
            return self.board.heuristic(),row,column
        moves = self.board.valid("X" if player else "O")
        if moves==[]:
            return self.board.heuristic(), row, column
        
        if player:
            ma = float('-inf')
            row = -1
            col = -1
            flag = False
            for i in self.board.valid("X"):
                flag = True
                #self.board.disp_val("X")
                self.board.insert(i[0],i[1],"X")
                heur,r,c = self.next_move_alpha_beta(False,max_depth,cur_depth+1,i[0],i[1],alpha,beta)
                self.board.undo()
                if heur!=None and heur>ma and r!=-1 and c!=-1:
                    ma = heur
                    row = i[0]
                    col = i[1]
                if heur!=None and r!=-1 and c!=-1:
                    alpha = max(alpha,heur)
                    if alpha >= beta:
                        break
            if flag:
                return ma,row,col
            return None,row,col
        else:
            mi = float('inf')
            row = -1
            col = -1
            flag = False
            for i in self.board.valid("O"):
                flag = True
                self.board.insert(i[0],i[1],"O")
                heur,r,c = self.next_move_alpha_beta(True,max_depth,cur_depth+1,i[0],i[1],alpha,beta)
                self.board.undo()
                if heur!=None and heur<=mi and r!=-1 and c!=-1:
                    mi = heur
                    row = i[0]
                    col = i[1]
                if heur!=None and r!=-1 and c!=-1:
                    beta = min(beta,heur)
                    if alpha >= beta:
                        break
            if flag:
                return mi,row,col
            return None,row,col

board = Othello()
difficulty = "easy"
statement = "Debug Statements Appear Here"


COLOR_MAP = {
    "X": (0, 0, 0),          # black
    "O": (255, 255, 255),    # white
    0: (34, 139, 34)         # green (empty)
}

BOARD_SIZE = 8

def board_to_rgb_image(board_obj, upscaled_size=32, color_map=COLOR_MAP):
    arr = np.zeros((BOARD_SIZE, BOARD_SIZE, 3), dtype=np.uint8)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            cell = board_obj.board[r][c]
            if cell == "X":
                arr[r, c] = color_map["X"]
            elif cell == "O":
                arr[r, c] = color_map["O"]
            else:
                arr[r, c] = color_map[0]
    img = Image.fromarray(arr, mode="RGB")
    if upscaled_size != BOARD_SIZE:
        img = img.resize((upscaled_size, upscaled_size), resample=Image.NEAREST)
    return img

model = YOLO(r"best.pt")

@app.route('/')
def home():
    print(board.board.valid("X"))
    return render_template('index.html',board=board.board.board,legal=[i[:-1] for i in board.board.valid("X")],black=len(board.board.val["X"]),white=len(board.board.val["O"]),statement=statement,board_prev=board.board.undo1[-1],legal_prev=[])

def temp(x,v):
    ans = [[0 for i in range(8)] for j in range(8)]
    b = x
    v = [i[:-1] for i in v]
    print("V",v)
    for i in range(8):
        for j in range(8):
            if (i,j) in v:
                ans[i][j]="N"
            else:
                ans[i][j]=b[i][j]
    return ans
@socketio.on("move")
def move(data):
    global statement
    print("Inside move")
    i,j = int(data["i"]),int(data["j"])
    print(f"Clicked: {i,j}")
    x = board.board.valid("X")
    if board.board.insert(i,j,"X")==False:
        socketio.emit("output",{"output":"Invalid Move!!","flag":0})
        socketio.emit("unlock",{"flag":1})
    else:
        socketio.emit("output",{"output":"⚪ is Thinking!!","flag":1,"board":temp(board.board.board,board.board.valid("O")),"black":len(board.board.val["X"]),"white":len(board.board.val["O"]),"prev":temp(board.board.undo1[-1],[])})
        x = board.board.valid("O")
        statement = "⚪ is Thinking!!"
        t = 1
        if difficulty=="hard":
            while board.board.valid("O")!=[]:
                print(board.board.valid("O"))
                print(t)
                t+=1
                temptime = time.time()
                heur,row,col = board.next_move_alpha_beta(False,6)
                print("Thingy",row,col,heur)
                if heur!=None and row!=-1 and col!=-1:
                    board.board.insert(row,col,"O")
                temptime = time.time() - temptime
                if temptime<1:
                    #time.sleep(1)
                    pass
                if board.board.valid("X")!=[]:
                    break
        elif difficulty=="medium":
            while board.board.valid("O")!=[]:
                print(board.board.valid("O"))
                print(t)
                t+=1
                temptime = time.time()
                heur,row,col = board.next_move_alpha_beta(False,3)
                print("Thingy",row,col,heur)
                if heur!=None and row!=-1 and col!=-1:
                    board.board.insert(row,col,"O")
                temptime = time.time() - temptime
                if temptime<1:
                    #time.sleep(1)
                    pass
                if board.board.valid("X")!=[]:
                    break
        else:
            z = time.time()
            x = board.board.valid("O")
            ans = -1
            pos = None
            for i in range(len(x)):
                board.board.insert(x[i][0],x[i][1],"O")
                img = board_to_rgb_image(board.board)  
                results = model.predict(img, verbose=False)
                probs = results[0].probs.data.cpu().numpy().tolist()
                names = list(model.names.values())
                prob_dict = dict(zip(names, probs))
                print(prob_dict)
                board.board.undo()
                if prob_dict["player_minus"]>ans:
                    ans = prob_dict["player_minus"]
                    pos = x[i][:2]
            print(time.time()-z)
            if ans!=-1:
                board.board.insert(pos[0],pos[1],"O")
        if board.board.valid("X")!=[]:
            socketio.emit("output",{"output":"⚫ Can play now!!","flag":1,"board":temp(board.board.board,board.board.valid("X")),"black":len(board.board.val["X"]),"white":len(board.board.val["O"]),"prev":temp(board.board.undo1[-1],[])}) #use x if you wanna show prev steps valid too
            statement = "⚫ Can play now!!"
            socketio.emit("unlock",{"flag":1})

  


@app.route('/resetThing',methods=["GET","POST"])
def reset1():
    print("Inside Reset................................................")
    board.board.board = board.board.createMatrix()
    board.board.board[3][3]="O"
    board.board.board[4][4]="O"
    board.board.board[3][4]="X"
    board.board.board[4][3]="X"
    board.board.undo1 = [[[0 for i in range(8)] for j in range(8)]]
    board.board.val = {"X":[(3,4),(4,3)],"O":[(3,3),(4,4)]}
    board.board.undo_Dict = []
    return redirect('/')

@app.route('/easy',methods=["GET","POST"])
def easy():
    global difficulty
    difficulty = "easy"
    print(difficulty)
    return reset1()

@app.route('/hard',methods=["GET","POST"])
def hard():
    global difficulty
    difficulty = "hard"
    print(difficulty)
    return reset1()

@app.route('/medium',methods=["GET","POST"])
def medium():
    global difficulty
    difficulty = "medium"
    print(difficulty)
    return reset1()

if __name__=="__main__":
    app.run(debug=True)