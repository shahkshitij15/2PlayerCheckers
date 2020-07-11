import tkinter
from tkinter import *
from CheckerPiece import checkerPiece

class Board(Canvas):
    gb=tkinter.Tk()
    bluePieces=[]
    redPieces=[]
    board=[]
    highlightTile=[]
    selectedChecker=checkerPiece(0,0,"blue",False,0)
    selectedCheckerId=0
    row=8
    col=8
    Blue_Checker=1
    Red_Checker=2
    tileBorder=0.75
    checkerBorder=4
    currentPlayer="red"
    doubleJump=False
    redCount=12
    blueCount=12
    redScore=Label(gb,text="Red: %i " % redCount,fg="red",font=("Helvetica",14))
    blueScore=Label(gb,text="Blue: %i " % blueCount,fg="blue",font=("Helvetica",14))

    #create main board for checkers
    def __init__(self):
        self.gb.minsize(563,563)
        Canvas.__init__(self,self.gb,bg="light grey",height=563,width=563)
        self.redScore.pack()
        self.blueScore.pack()
        self.pack()
        self.createTiles()
        self.createChecker()
        self.gb.mainloop()

    def createTiles(self):
        width=70
        height=70
        for i in range(0,self.col):
            x1=(i*width)+self.tileBorder
            x2=((i+1)*width)-self.tileBorder
            for j in range(0,self.row):
                y1=(j*height)+self.tileBorder
                y2=((j+1)*height)-self.tileBorder
                id=0
                if( (i+j)%2 == 0):
                    id=self.create_rectangle(x1,y1,x2,y2,fill="white")
                else:
                    id=self.create_rectangle(x1,y1,x2,y2,fill="black")
                if id!=0:
                    self.board.append((id,j,i,x1,x2,y1,y2))

    def createChecker(self):
        cWidth=70
        cHeight=70

        for i in range(0,self.row):
            if(i==3 or i==4):
                continue

            y1=(i*cWidth) + self.checkerBorder
            y2=((i+1)*cWidth)-self.checkerBorder

            if i<3:
                checkerColor="blue"
            elif i>4:
                checkerColor="red"

            for j in range(0,self.col):
                if((i+j)%2 == 1):
                    x1=(j*cHeight)+self.checkerBorder
                    x2=((j+1)*cHeight)-self.checkerBorder

                    idTag=self.create_oval(x1,y1,x2,y2,fill=checkerColor) #returns object Id
                    self.tag_bind(idTag,"<ButtonPress-1>",self.CheckerClick) #tag_bind is used to handle events
                    checker=checkerPiece(i,j,checkerColor,False,idTag) #create object of each checker to keep a track of it
                    if checkerColor=="red":
                        self.redPieces.append((idTag,checker))
                    elif checkerColor=="blue":
                        self.bluePieces.append((idTag,checker))

    #returns the checkerObject of the specified Id
    def getChecker(self,id):
        for i in range(0,len(self.bluePieces)):
            if self.bluePieces[i][0]==id:
                return self.bluePieces[i][1]

        for i in range(0,len(self.redPieces)):
            if self.redPieces[i][0]==id:
                return self.redPieces[i][1]

        return 0 #if no checker is found

    #returns tileId of the tile found
    def getTile(self,row,col):
        r1=row
        c1=col
        for i in range(0,len(self.board)):
            if (row==self.board[i][1] and col==self.board[i][2]):
                return self.board[i][0]
        return 0

    #returns true if position is valid
    def checkPosition(self,row,col):
        return self.checkRow(row) and self.checkCol(col)

    #returns true if the row is valid
    def checkRow(self,row):
        if(row >=0 and row<=7):
            return True
        else:
            return False

    #returns true if the column is valid
    def checkCol(self,col):
        if(col>=0 and col<=7):
            return True
        else:
            return False

    #return true if occupied along with the color and id of the checker
    def isTileAvailable(self,row,col):
        r1=row
        c1=col
        if(not self.checkPosition(r1,c1)):
            return (False,"NA",0)

        for i in range(0,len(self.bluePieces)):
            current=self.bluePieces[i][1]
            if(r1==current.getRow()) and(c1==current.getCol()):
                return(True,"blue",self.bluePieces[i][0])

        for i in range(0,len(self.redPieces)):
            current=self.redPieces[i][1]
            if(r1==current.getRow()) and (c1==current.getCol()):
                return(True,"red",self.redPieces[i][0])

        return(False,"NA",0)

    def SwitchPlayer(self):
        if self.currentPlayer=="red":
            self.currentPlayer="blue"
        elif self.currentPlayer=="blue":
            self.currentPlayer="red"

    def stopGame(self):
        for i in self.redPieces:
            id=i[0]
            if id!=0:
                self.tag_unbind(id,"<ButtonPress-1>")
        for i in self.bluePieces:
            id=i[0]
            if id!=0:
                self.tag_unbind(id,"<ButtonPress-1>")
        self.resetTile()

    def checkWin(self):
        if self.redCount <= 0:
            b=Label(self.gb,text="BLUE WINS!!",fg="blue",font=("Helvetica",14))
            b.pack()
            self.stopGame()
        if self.blueCount <= 0:
            r=Label(self.gb,text="RED WINS!!",fg="red",font=("Helvetica",14))
            r.pack()
            self.stopGame()

    def removeChecker(self,checkerId):
        if checkerId!=0:
            self.delete(checkerId)
            for i in self.redPieces:
                if i[0]==checkerId:
                    self.redPieces.remove(i)
                    self.redCount-=1
                    self.redScore.config(text="Red %i " % self.redCount)
                    break
            for i in self.bluePieces:
                if i[0]==checkerId:
                    self.bluePieces.remove(i)
                    self.blueCount-=1
                    self.blueScore.config(text="Blue %i " % self.blueCount)
                    break
            self.checkWin()

    def showAvailableMove(self,checker1):
        checker=checker1
        isCheckerKing=checker.getKing()
        checkerColor=checker.getColor()
        open=[]

        if isCheckerKing:

            row=checker.getNE()[0]
            col=checker.getNE()[1]
            if(not self.isTileAvailable(row,col)[0]):
                open.append(checker.getNE())

            row = checker.getNW()[0]
            col = checker.getNW()[1]
            if (not self.isTileAvailable(row, col)[0]):
                open.append(checker.getNW())

            row = checker.getSE()[0]
            col = checker.getSE()[1]
            if (not self.isTileAvailable(row, col)[0]):
                open.append(checker.getSE())

            row = checker.getSW()[0]
            col = checker.getSW()[1]
            if (not self.isTileAvailable(row, col)[0]):
                open.append(checker.getSW())

        elif checkerColor=="red":
            row = checker.getNE()[0]
            col = checker.getNE()[1]
            if (not self.isTileAvailable(row, col)[0]):
                open.append(checker.getNE())

            row = checker.getNW()[0]
            col = checker.getNW()[1]
            if (not self.isTileAvailable(row, col)[0]):
                open.append(checker.getNW())

        elif checkerColor=="blue":
            row = checker.getSE()[0]
            col = checker.getSE()[1]
            if (not self.isTileAvailable(row, col)[0]):
                open.append(checker.getSE())

            row = checker.getSW()[0]
            col = checker.getSW()[1]
            if (not self.isTileAvailable(row, col)[0]):
                open.append(checker.getSW())

        for i in range(0,len(open)):
            highlightRow=open[i][0]
            highlightCol=open[i][1]
            if highlightRow==100 or highlightCol==100:
                continue
            tileId=self.getTile(highlightRow,highlightCol)
            if tileId!=0:
                self.itemconfig(tileId,outline="yellow")
                self.tag_bind(tileId,"<ButtonPress-1>",self.processTile)
                self.highlightTile.append((highlightRow,highlightCol,0))

            else:
                print("Invalid Move")

    #highlight square if jump tile is available
    def checkJump(self,row,col,jumpId):
        if not self.checkPosition(row,col):
            return 0

        if not self.isTileAvailable(row,col)[0]:
            tileId=self.getTile(row,col)
            if tileId!=0:
                self.itemconfig(tileId,outline="yellow")
                self.tag_bind(tileId,"<ButtonPress-1>",self.processTile)
                self.highlightTile.append((row,col,jumpId))

    def getJumpId(self,row,col):
        for i in self.highlightTile:
            if row==i[0] and col==i[1]:
                return i[2]
        return 0

    def showAvailableJumpMoves(self,checker1):
        checker=checker1
        checkerKing=checker.getKing()
        checkerColor=checker.getColor()

        #if checker is a king it can go in any direction
        if checkerKing:
            #check NW neighbors
            row=checker.getNW()[0]
            col=checker.getNW()[1]
            TileArray=self.isTileAvailable(row,col)
            TileOccupied=TileArray[0]
            TileColor=TileArray[1]
            jumpId=TileArray[2]

            if TileOccupied:
                if checkerColor!=TileColor:
                    jumpRow=checker.getNW()[0]
                    jumpCol=checker.getNW()[1]
                    self.checkJump(jumpRow-1,jumpCol-1,jumpId)

            #check NE neighbors
            row = checker.getNE()[0]
            col = checker.getNE()[1]
            TileArray = self.isTileAvailable(row, col)
            TileOccupied = TileArray[0]
            TileColor = TileArray[1]
            jumpId = TileArray[2]

            if TileOccupied:
                if checkerColor != TileColor:
                    jumpRow = checker.getNE()[0]
                    jumpCol = checker.getNE()[1]
                    self.checkJump(jumpRow - 1, jumpCol + 1, jumpId)

            #check SW neighbors
            row = checker.getSW()[0]
            col = checker.getSW()[1]
            TileArray = self.isTileAvailable(row, col)
            TileOccupied = TileArray[0]
            TileColor = TileArray[1]
            jumpId = TileArray[2]

            if TileOccupied:
                if checkerColor != TileColor:
                    jumpRow = checker.getSW()[0]
                    jumpCol = checker.getSW()[1]
                    self.checkJump(jumpRow + 1, jumpCol - 1, jumpId)

            #check SE neighbors
            row = checker.getSE()[0]
            col = checker.getSE()[1]
            TileArray = self.isTileAvailable(row, col)
            TileOccupied = TileArray[0]
            TileColor = TileArray[1]
            jumpId = TileArray[2]

            if TileOccupied:
                if checkerColor != TileColor:
                    jumpRow = checker.getSE()[0]
                    jumpCol = checker.getSE()[1]
                    self.checkJump(jumpRow + 1, jumpCol + 1, jumpId)

        #if checker is not king
        elif checkerColor =="red":
            # check NW neighbors
            row = checker.getNW()[0]
            col = checker.getNW()[1]
            TileArray = self.isTileAvailable(row, col)
            TileOccupied = TileArray[0]
            TileColor = TileArray[1]
            jumpId = TileArray[2]

            if TileOccupied:
                if checkerColor != TileColor:
                    jumpRow = checker.getNW()[0]
                    jumpCol = checker.getNW()[1]
                    self.checkJump(jumpRow - 1, jumpCol - 1, jumpId)

            # check NE neighbors
            row = checker.getNE()[0]
            col = checker.getNE()[1]
            TileArray = self.isTileAvailable(row, col)
            TileOccupied = TileArray[0]
            TileColor = TileArray[1]
            jumpId = TileArray[2]

            if TileOccupied:
                if checkerColor != TileColor:
                    jumpRow = checker.getNE()[0]
                    jumpCol = checker.getNE()[1]
                    self.checkJump(jumpRow - 1, jumpCol + 1, jumpId)

        elif checkerColor=="blue":
            # check SW neighbors
            row = checker.getSW()[0]
            col = checker.getSW()[1]
            TileArray = self.isTileAvailable(row, col)
            TileOccupied = TileArray[0]
            TileColor = TileArray[1]
            jumpId = TileArray[2]

            if TileOccupied:
                if checkerColor != TileColor:
                    jumpRow = checker.getSW()[0]
                    jumpCol = checker.getSW()[1]
                    self.checkJump(jumpRow + 1, jumpCol - 1, jumpId)

            # check SE neighbors
            row = checker.getSE()[0]
            col = checker.getSE()[1]
            TileArray = self.isTileAvailable(row, col)
            TileOccupied = TileArray[0]
            TileColor = TileArray[1]
            jumpId = TileArray[2]

            if TileOccupied:
                if checkerColor != TileColor:
                    jumpRow = checker.getSE()[0]
                    jumpCol = checker.getSE()[1]
                    self.checkJump(jumpRow + 1, jumpCol + 1, jumpId)

    def moveChecker(self,newRow,newCol):
        y1=(newRow * 70)+self.checkerBorder
        y2=((newRow +1)*70)-self.checkerBorder
        x1=(newCol * 70)+self.checkerBorder
        x2=((newCol+1)*70)-self.checkerBorder

        self.coords(self.selectedCheckerId,(x1,y1,x2,y2))
        self.selectedChecker.updateLocation(newRow,newCol)
        if self.selectedChecker.getKing():
            self.itemconfig(self.selectedCheckerId,outline="green")

    def resetTile(self):
        for i in self.highlightTile:
            tileId=self.getTile(i[0],i[1])
            if tileId!=0:
                self.itemconfig(tileId,outline="black")
                self.tag_unbind(tileId,"<ButtonPress-1>")

        for i in range(0,len(self.highlightTile)):
            self.highlightTile.pop()

    def processTile(self,event):
        x=self.canvasx(event.x)
        y=self.canvasy(event.y)
        id=self.find_closest(x,y)[0]

        #finding new row and column to move the selected checker

        newRow=100
        newCol=100
        jumpId=0
        for i in self.board:
            if i[0]==id:
                newRow=i[1]
                newCol=i[2]
                jumpId=self.getJumpId(newRow,newCol)

        if newRow==100:
            return

        self.moveChecker(newRow,newCol)
        self.resetTile()
        #if the checker made a jump remove the jumped checker and show more jump moves
        if jumpId!=0:
            self.removeChecker(jumpId)
            self.showAvailableJumpMoves(self.selectedChecker)

            if(len(self.highlightTile)>0):
                self.doubleJump=True
            else:
                self.SwitchPlayer()
                self.doubleJump=False
        else:
            self.SwitchPlayer()

    def CheckerClick(self,event):
        x=self.canvasx(event.x)
        y=self.canvasy(event.y)
        id=self.find_closest(x,y)[0]
        checker=self.getChecker(id)
        if checker==0:
            return

        if(self.currentPlayer==checker.getColor() and self.doubleJump==False):
            self.selectedChecker=checker
            self.selectedCheckerId=id
            self.resetTile()
            self.showAvailableMove(checker)
            self.showAvailableJumpMoves(checker)
