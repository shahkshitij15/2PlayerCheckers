class checkerPiece:
    id=0
    row=0
    col=0
    color=""
    king=False
    ne=[]
    se=[]
    nw=[]
    sw=[]

    def __init__(self,row,col,color,king,id):
        self.row=row
        self.col=col
        self.color=color
        self.king=king
        self.id=id
        self.assignNeighbors()

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def getColor(self):
        return self.color

    def getKing(self):
        return self.king

    def setKing(self):
        self.king=True

    def getId(self):
        return self.id

    def getNE(self):
        return self.ne

    def getNW(self):
        return self.nw

    def getSW(self):
        return self.sw

    def getSE(self):
        return self.se

    def updateLocation(self,row,col):
        self.row=row
        self.col=col
        self.assignNeighbors()
        if(row==0 and self.color=="red"):
            if not self.getKing():
                self.setKing()
        if(row==7 and self.color=="blue"):
            if not self.getKing():
                self.setKing()

    def assignNeighbors(self):
        north=100
        south=100
        west=100
        east=100

        if(self.row-1) >= 0:
            north=self.row-1
        if(self.row+1) <= 7:
            south=self.row +1
        if(self.col-1) >= 0:
            west=self.col-1
        if(self.col+1) <= 7:
            east=self.col+1

        self.ne=(north,east)
        self.nw=(north,west)
        self.se=(south,east)
        self.sw=(south,west)