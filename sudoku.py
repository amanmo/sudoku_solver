class Board:

    #intialize matrices            
    def __init__(self):

        self.board = [[0 for i in range(9)] for j in range(9)]
        self.fixed = [[False for i in range(9)] for j in range(9)]
        self.sector = [[self.get_sector((j,i)) for i in range(9)] for j in range(9)]
        self.possibilities = [[[] for i in range(9)] for j in range(9)]

    #returns sector of a position
    def get_sector(self, position):
        i = position[0]
        j = position[1]

        if i<3:
            if j<3: return 0
            elif j<6: return 1
            else: return 2
        elif i<6:
            if j<3: return 3
            elif j<6: return 4
            else: return 5
        else:
            if j<3: return 6
            elif j<6: return 7
            else: return 8

    #fixes a number in a position
    def set(self, position, number):
        self.board[position[0]][position[1]] = number
        self.fixed[position[0]][position[1]] = True

    #displays board
    def display_board(self):
        for i in range(9):
            print (str(self.board[i][0:3]) + "\t" + str(self.board[i][3:6]) + "\t" + str(self.board[i][6:9]))
            if i in (2,5):
                print ("")
        print ("")

    #finds all numbers in the row
    def check_row(self, position, row, arr):
        for j in range(9):
            if self.board[row][j]!=0 and self.board[row][j] not in arr:
                arr+=[self.board[row][j]]

    #finds all numbers in the column
    def check_column(self, position, column, arr):
        for i in range(9):
            if self.board[i][column]!=0 and self.board[i][column] not in arr:
                arr+=[self.board[i][column]]

    #finds all numbers in the sector
    def check_sector(self, position, sector, arr):
        for i in range(9):
            for j in range(9):
                if self.sector[i][j] == sector and self.board[i][j]!=0 and self.board[i][j] not in arr:
                    arr+=[self.board[i][j]]

    #checks whether a number is restricted to a cell by neighbouring rows and columns
    def check_borders(self, position, arr):
        i = position[0]
        j = position[1]

        for num in arr:
            #checking rows
            if i in [0,3,6]:
                if not (num in self.board[i+1] and num in self.board[i+2]):         continue
            elif i in [1,4,7]:
                if not (num in self.board[i-1] and num in self.board[i+1]):         continue
            else:
                if not (num in self.board[i-2] and num in self.board[i-1]):         continue

            #checking columns
            if j in [0,3,6]:
                if not (num in [self.board[k][j+1] for k in range(9)] and num in [self.board[k][j+2] for k in range(9)]):       continue
            elif j in [1,4,7]:
                if not (num in [self.board[k][j-1] for k in range(9)] and num in [self.board[k][j+1] for k in range(9)]):       continue
            else:
                if not (num in [self.board[k][j-2] for k in range(9)] and num in [self.board[k][j-1] for k in range(9)]):       continue

            return num
        return 0

    #check within a sector whether a number can fit in only one place
    def check_sector_possibilities(self):
        changes=0
        for i in range(9):
            for j in range(9):
                if not self.fixed[i][j]:
                    sector = self.sector[i][j]
                    arr = self.possibilities[i][j]

                    for num in arr:
                        count=0
                        for p in range(9):
                            for q in range(9):
                                if (self.sector[p][q] == sector) and (p!=i or q!=j) and (num in self.possibilities[p][q]):
                                    if (not self.fixed[p][q]) or self.board[p][q]==num:
                                        count+=1
                        if count==0:
                            self.set((i,j), num)
                            changes+=1
                            break
        return changes
                        
    #checks whether a number has been fixed in all places, else resets possibilities array                    
    def check_solved(self, end = True):
        for i in range(9):
            for j in range(9):
                if not self.fixed[i][j]:
                    if end:
                        #resetting possibilities arrays
                        self.possibilities = [[[] for i in range(9)] for j in range(9)]
                    return False
        return True

    #main solving function
    def solve(self):
        run = 1

        while not self.check_solved():

            changes = 0
            #print ("Run: " + str(run) + "\n")
            for i in range(9):
                for j in range(9):
                    if not self.fixed[i][j]:
                        nums = []
                        self.check_row((i,j), i, nums)
                        self.check_column((i,j), j, nums)
                        self.check_sector((i,j), self.sector[i][j], nums)
                        
                        for k in range(1,10):
                            if k not in nums and k not in self.possibilities[i][j]:
                                self.possibilities[i][j] += [k]
                        closed = self.check_borders((i,j), self.possibilities[i][j])

                        #print ("{}\t{}\t{}\t{}".format(i, j, closed, self.possibilities[i][j]))
                        if len(self.possibilities[i][j])==1:
                            self.set((i,j), self.possibilities[i][j][0])
                            changes += 1
			
                        elif closed!=0:
                            self.set((i,j), closed)
                            changes+=1

            count=self.check_sector_possibilities()
            run += 1
            #print ("Changes: " + str(changes+count) + "\n")
            #self.display_board()

            #Multiple solution cases
            if changes==0 and not self.check_solved(False):
                flag = True
                for i in range(9):
                    if flag:
                        for j in range(9):
                            if not self.fixed[i][j]:
                                self.set((i,j), self.possibilities[i][j][0])
                                flag = False
                                break
                    else:
                        break

b = Board()
'''
#easy example
b.board = [[0,6,0,3,0,0,8,0,4],
           [5,3,7,0,9,0,0,0,0],
           [0,4,0,0,0,6,3,0,7],
           [0,9,0,0,5,1,2,3,8],
           [0,0,0,0,0,0,0,0,0],
           [7,1,3,6,2,0,0,4,0],
           [3,0,6,4,0,0,0,1,0],
           [0,0,0,0,6,0,5,2,3],
           [1,0,2,0,0,9,0,8,0]]

#example with unique solution
b.board = [[0,0,0,0,7,8,5,4,0],
           [0,0,0,1,0,0,0,0,2],
           [0,0,0,0,3,5,1,6,0],
           [0,6,0,0,2,3,7,5,0],
           [4,0,3,0,0,0,0,0,0],
           [7,0,8,5,0,0,0,0,4],
           [3,0,4,7,0,0,0,0,5],
           [6,0,9,0,0,0,0,0,0],
           [0,1,0,0,4,6,9,8,0]]
'''
#example with multiple solutions
b.board = [[0,0,0,0,0,0,0,2,4],
           [0,7,0,1,0,0,0,0,5],
           [0,2,0,4,9,0,0,0,0],
           [0,6,0,2,0,0,1,0,0],
           [9,5,0,0,4,0,0,6,0],
           [0,0,1,0,0,3,2,0,0],
           [6,0,0,0,0,8,3,0,0],
           [0,3,7,0,1,0,0,8,0],
           [0,8,0,0,0,6,0,0,7]]

b.fixed = [[b.board[i][j]!=0 for j in range(9)] for i in range(9)]

print ("Initial Board: ")
b.display_board()

b.solve()

if (b.check_solved()):
    print ("Solved Board: ")
    b.display_board()
else:
    print ("Error: Board not solved")

