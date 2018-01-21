"""
This is an assignment for Agentz.ai.
The task is to design a chessboard and handle moves for Black coins. The task breakdown (as I understood) is,
i) Initialize White and Black coins randomly, regardless of any legality in their positions (The first state of board is displayed).
ii) Select a random position in the board which is safest for the next move (Such that white doesn't attack you in the next move).
[ ii. and iii are the same task in different ways ]
iii) Move the initialized Black coin to a safe location if possible or print Error.
iv) Assume White makes the next move randomly (The move made by white is shown along with the state of chessboard after the move).
v) Make a next move such that any Black makes an attack on any white piece and handle the case when no white can be attacked by any black.(Printed with details on who attacked who).

The Confusion:
i) Checking elements on the path before attacking (Is this also included in this assignment?).
(At this point, If a friendly or enemy piece is inbetween our coin and the target coin when attacking, it skips and assumes that the path is clear)
For Pawn, King and Knight this is still valid since they attack the coin right next to them or do jump attacks.
Need to tweak a little for Queen, Bishop and Rook with BFS for path finding (blocking pieces) incase if this is also needed.
I'm assuming that isn't included with this assignment and submitting this as is.
"""

import random
import numpy

board = 8
White = 'W'
Black = 'B'

class Coin:
    x,y = 0,0
    Color = ''

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.name = self.__class__.__name__
        self.Color = color
    
    def check_conflict(self,x,y):
        if ChessBoard[x][y] != 0:
            return False
        return True

    def check_bounds(self, x,y):
        return (x in range(board) and y in range(board) and self.check_conflict(x,y))

    def set_position(self,x1,y1):
        self.x = x1
        self.y = y1

    def get_position(self):
        return (self.x,self.y)

    def possible_moves(self):
        pass

class King(Coin):
    row_move = [0,1,1, 1, 0,-1,-1,-1]
    col_move = [1,1,0,-1,-1,-1, 0, 1]
    
    def is_in_range(self,x,y):
        return (abs(self.x-x), abs(self.y-y)) in [(0,1),(1,0)]

    def possible_moves(self):
        return [(self.x + self.row_move[i],self.y+self.col_move[i]) for i in range(len(self.row_move)) if self.check_bounds(self.x+self.row_move[i],self.y+self.col_move[i])]

class Pawn(Coin):
    def __init__(self, x, y, color):
        super().__init__(x,y,color)
        if color == White:
            self.direction = 1
        else:
            self.direction = -1
    
    def is_in_range(self,x,y):
        if self.direction == 1:
            return ((self.x < x)==True and abs(self.x - x)==1 and abs(self.y-y)==1)
        else:
            return ((self.x > x)==True and abs(self.x - x)==1 and abs(self.y-y)==1)

    def possible_moves(self):
        return [(self.x + self.direction, self.y) if self.x + self.direction in range(board) else (self.x,self.y)]

class Bishop(Coin):
    row_move = [1,-1,-1,1]
    col_move = [1,-1, 1,-1]

    def is_in_range(self,x,y):
        return abs(self.x-x) == abs(self.y-y)

    def possible_moves(self):
        diagonal = []
        diagonal += [(self.x-self.row_move[j]*i,self.y-self.col_move[j]*i) for i in range(board) for j in range(len(self.row_move)) if self.check_bounds(self.x-self.row_move[j]*i,self.y-self.col_move[j]*i)]
        return list(set(diagonal))
        
class Queen(Coin):
    row_move = [1,-1,-1, 1,0,1]
    col_move = [1,-1, 1,-1,1,0]

    def is_in_range(self,x,y):
        return (abs(self.x-x) == abs(self.y-y) or self.x == x or self.y == y)

    def possible_moves(self):
        moves = []
        moves += [(self.x-self.row_move[j]*i,self.y-self.col_move[j]*i) for i in range(board) for j in range(len(self.row_move)) if self.check_bounds(self.x-self.row_move[j]*i, self.y-self.col_move[j]*i)]
        return list(set(moves))

class Rook(Coin):
    def is_in_range(self, x, y):
        return self.x==x or self.y==y

    def possible_moves(self):
        moves = []
        moves += [(self.x+i,self.y) for i in range(-board+1,board) if self.x+i in range(board)]
        moves +=[(self.x,self.y+i) for i in range(-board+1,board) if self.y+i in range(board)]
        return list(set(moves))

class Knight(Coin):
    move = [-2,2]
    def is_in_range(self, x, y):
        return (x,y) in self.possible_moves()
    
    def possible_moves(self):
        moves = []
        for i in range(len(self.move)):
            if self.x+self.move[i] in range(board):
                if self.y - 1 in range(board):
                    moves.append((self.x+self.move[i] , self.y-1))
                if self.y + 1 in range(board):
                    moves.append((self.x+self.move[i] , self.y+1))
            if self.y+self.move[i] in range(board):
                if self.x - 1 in range(board):
                    moves.append((self.x-1 , self.y+self.move[i]))
                if self.x + 1 in range(board):
                    moves.append((self.x+1 , self.y+self.move[i]))
        return moves

class Coin_Instance:
    """
    This is the instance class of each coin [Black and white]
    It takes care of the positions and holds each coin instance in it's list _Pieces
    """
    def __init__(self, pieces):
        self._Pieces = pieces

    def check_if_unoccupied(self, x, y):
        return not ChessBoard[x][y]

    def check_if_in_attack_range(self,x,y):
        """
        Checks if any of it's coin can attack the position x,y
        """
        for coin in self._Pieces:
            if coin.is_in_range(x,y):
                print ("Coin at",x,y,"will be in attack range of the",coin.Color+"_"+coin.name,"which is at ",coin.get_position())
                return True
        return False
    
    def find_safe_position(self, opponent_instance):
        """
        Check if any possible move for any piece is in attack range of opponent
        """
        for piece in self._Pieces:
            moves = piece.possible_moves()
            for move in moves:
                if check_if_unoccupied(move[0],move[1]):
                    if not opponent_instance.check_if_in_attack_range(move[0],move[1]):
                        print (piece.Color+"_"+piece.name,"at",piece.get_position(),"Moved to",move)
                        x1,y1 = piece.get_position()
                        ChessBoard[x1][y1] = 0
                        ChessBoard[move[0]][move[1]] = piece.Color+"_"+piece.name 
                        return
        else:
            print ("No safe positions")

    def attack_random_opponent(self, opponent_pos):
        for coin_position in opponent_pos:    
            for coin in self._Pieces:
                x = coin_position[0]
                y = coin_position[1]
                if coin.is_in_range(x,y):
                    print ("Attacking Coin",ChessBoard[x][y],"at",x,y,"with our",coin.Color+"_"+coin.name,"which is at ",coin.get_position(),"\n")
                    init_x, init_y = coin.get_position() 
                    ChessBoard[x][y] = ChessBoard[init_x][init_y]
                    ChessBoard[init_x][init_y] = 0
                    return True
        return False


    def get_all_positions(self):
        return [coin.get_position() for coin in self._Pieces]

    def make_random_move(self):
        """
        Takes a random coin and makes a random move based on possible moves
        """
        piece_list = list(self._Pieces)
        n = len(piece_list)-1
        while (n>0):
            rand_index = random.randrange(n)
            coin = piece_list.pop(rand_index)
            move_list = coin.possible_moves()
            for move in move_list:
                if ChessBoard[move[0]][move[1]] == 0:
                    init_position = coin.get_position()
                    print (coin.Color,coin.name,"from",init_position[0],init_position[1],"moved to",move[0],move[1])
                    ChessBoard[init_position[0]][init_position[1]] = 0
                    coin.set_position(move[0],move[1])
                    ChessBoard[move[0]][move[1]] = coin.Color+'_'+coin.name
                    return True
            n-=1
        return False


ChessBoard = [[0 for x in range(board)] for y in range(board)]

def check_bounds(x,y):
    return (x in range(board) and y in range(board))

def GetPieceInstance(piece, x, y, color):
    if piece == color+"_p":
        return Pawn(x,y,color)
    elif piece == color+"_k":
        return King(x,y,color)        
    elif piece == color+"_q":
        return Queen(x,y,color)        
    elif piece == color+"_r":
        return Rook(x,y,color)        
    elif piece == color+"_b":
        return Bishop(x,y,color)        
    elif piece == color+"_n":
        return Knight(x,y,color)
    else:
        return False      

def draw_line():
    print ("__"*20)

def check_if_unoccupied(x,y):
    return not ChessBoard[x][y]

def randomInitialize(color):
    pawn   = [color+'_p']*8
    king   = [color+'_k']
    queen  = [color+'_q']
    rook   = [color+'_r']*2
    bishop = [color+'_b']*2
    knight = [color+'_n']*2
    White_p_list = []
    pieces_list = pawn+king+queen+rook+bishop+knight
    # print (pieces_list)
    while(len(pieces_list)>0):
        x = random.randrange(board)
        y = random.randrange(board)
        if check_bounds(x,y) and check_if_unoccupied(x,y):
            element = pieces_list.pop(0)
            if (element == color+'_p') :
                if (color == White and x == board-1) or (color == Black and x == 0):        
                    pieces_list.append(element)
                    continue
            piece = GetPieceInstance(element,x,y,color)
            if piece:
                ChessBoard[x][y] = color+'_'+piece.name
                White_p_list.append(piece)
    return White_p_list

list_white = randomInitialize(White)
list_black = randomInitialize(Black)

White_instance = Coin_Instance(list_white)
Black_instance = Coin_Instance(list_black)

num = 0 
print ("Randomly initialized board\n")
print(numpy.array(ChessBoard))

n = 64 - 32
while(n>0):
    x = random.randrange(board)
    y = random.randrange(board)
    if check_bounds(x,y) and check_if_unoccupied(x,y):
        print("\nChecking for",x,y)
        if not White_instance.check_if_in_attack_range(x,y):
            print("Random safest position in the Board is ",x,y)
            break
        n-=1
else:
    print ("No random safe positions here")

draw_line()
#--- This is another way to find safe positions where we use our initialized Black coins and check with White coins---#
print ("Now finding safest position based on our random initialization i.e, Select a random Black piece from init and find its safe position")
Black_instance.find_safe_position(White_instance)
print (numpy.array(ChessBoard))
# --- #
draw_line()
print ("Random move from White coin instance")
White_instance.make_random_move()
print ("\nThe Chessboard now")
print(numpy.array(ChessBoard))
draw_line()
white_pos = White_instance.get_all_positions()
if not Black_instance.attack_random_opponent(white_pos):
    print ("Cannot attack any white at this state\n")
print(numpy.array(ChessBoard))
draw_line()
