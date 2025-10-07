
import os
import re
import pandas as pd
import numpy as np
from PIL import Image
from tqdm import tqdm


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
        return len(self.val["X"])-len(self.val["O"])
    
    def winloss(self):
        if len(self.val["O"])==0:
            return 200
        if len(self.val["X"])==0:
            return 200
        return 0


board = Board()
board.disp()
#print(board.board)

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

img = board_to_rgb_image(board)

from ultralytics import YOLO

# Load the trained model
model = YOLO(r"/home/sachcith/Documents/Sem 3/FAI/yolo outputs/Othello Yolov11-cls 50 Epoch Test 1/weights/best.pt")

# Run prediction on one image
results = model.predict(img, verbose=False)

print(results)