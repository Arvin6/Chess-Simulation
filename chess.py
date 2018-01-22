"""
This is an assignment for Agentz.ai.
The task is to design a chessboard and handle moves for Black coins. The task breakdown (as I understood) is,
i) Initialize White and Black coins randomly, regardless of any legality in their positions (The first state of board is displayed).
ii) Select a random position in the board which is safest for the next move (Such that white doesn't attack you in the next move).
[ ii. and iii are the same task in different ways ]
iii) Move the initialized Black coin to a safe location if possible or print Error.
iv) Assume White makes the next move randomly (The move made by white is shown along with the state of chessboard after the move).
v) Make a next move such that any Black makes an attack on any white piece and handle the case when no white can be attacked by any black.(Printed with details on who attacked who).
"""

import random,sys
from pandas import *
board = 8
White = 'W'
Black = 'B'

ChessBoard = [[0 for x in range(board)] for y in range(board)]


class Coin:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.name = self.__class__.__name__
        self.Color = color

    def get_name(self):
        return self.Color+"_"+self.name
    
    def is_not_conflict(self,x,y):
        if ChessBoard[x][y] == 0:
            return True
        return False

    def check_bounds(self, x,y):
        return (x in range(board) and y in range(board))

    def set_position(self,x1,y1):
        self.x = x1
        self.y = y1
        ChessBoard[x1][y1] = self.Color+"_"+self.name

    def get_position(self):
        return (self.x,self.y)

    def possible_moves(self):
        pass
    
    def is_path_clear(self,src,dest):
        pass


class King(Coin):
    row_move = [0,1,1, 1, 0,-1,-1,-1]
    col_move = [1,1,0,-1,-1,-1, 0, 1]
    
    def is_in_range(self,x,y):
        if ChessBoard[x][y] == 0:
            return False
        return ((abs(self.x-x), abs(self.y-y)) in [(0,1),(1,0),(1,1)] and self.Color != ChessBoard[x][y][0] )

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
        if ChessBoard[x][y] == 0:
            return False
        if self.direction == 1:
            return ((self.x < x)==True and abs(self.x - x)==1 and abs(self.y-y)==1 and self.Color != ChessBoard[x][y][0])
        else:
            return ((self.x > x)==True and abs(self.x - x)==1 and abs(self.y-y)==1 and self.Color != ChessBoard[x][y][0])

    def possible_moves(self):
        return [(self.x + self.direction, self.y) if self.check_bounds(self.x+self.direction,self.y) else (self.x,self.y)]

class Bishop(Coin):
    row_move = [1,-1,-1,1]
    col_move = [1,-1, 1,-1]

    def is_in_range(self,x,y):
        if ChessBoard[x][y] == 0:
            return False
        if self.Color != ChessBoard[x][y][0] and abs(self.x-x) == abs(self.y-y):
            return self.is_path_clear(x,y)
        return False

    def is_path_clear(self, x, y):
        src_x, src_y = self.get_position()
        if (src_x,src_y) == (x,y):
            return False
        if src_x > x: # upper diagonal
            if src_y > y: # left
                for i in range(src_x-1, x, -1):
                    for j in range(src_y-1, y, -1):
                        if not self.is_not_conflict(i,j):
                            return False
            else: # right
                for i in range(src_x-1, x, -1):
                     for j in range(src_y+1, y, 1):
                        if not self.is_not_conflict(i,j):
                            return False
        elif src_x < x: # Lower diagonal
            if src_y > y: # Left
                for i in range(src_x + 1, x): 
                    for j in range(src_y-1, y, -1):
                        if not self.is_not_conflict(i,j):
                            return False
            else: # Right
                for i in range(src_x + 1, x): 
                    for j in range(src_y+1, y):
                        if not self.is_not_conflict(i,j):
                            return False
        else: 
            return False
        return True

    def possible_moves(self):
        diagonal = []
        diagonal += [(self.x-self.row_move[j]*i,self.y-self.col_move[j]*i) for i in range(board) for j in range(len(self.row_move)) if self.check_bounds(self.x-self.row_move[j]*i,self.y-self.col_move[j]*i)]
        # diagonal = [d for d in diagonal if self.is_path_clear(d[0],d[1])]
        print (diagonal)
        return list(set(diagonal))
        
class Queen(Coin):
    def is_in_range(self,x,y):
        if ChessBoard[x][y] == 0:
            return False
        return self.is_path_clear(x,y)
        
    def is_path_clear(self, x, y):
        if self.x==x or self.y==y: 
            return Rook.is_path_clear(self,x,y)
        if abs(self.x-x) == abs(self.y-y):
            return Bishop.is_path_clear(self,x,y)
        return False

    def possible_moves(self):
        moves = Bishop(self.x,self.y,self.Color).possible_moves()
        moves += Rook(self.x,self.y,self.Color).possible_moves() 
        return list(set(moves))

class Rook(Coin):
    def is_in_range(self, x, y):
        if ChessBoard[x][y] == 0:
            return False
        if self.x == x or self.y ==y:
            return self.is_path_clear(x,y) and self.Color != ChessBoard[x][y][0]
        return False

    def is_path_clear(self,x,y):
        src_x,src_y = self.get_position()
        if (src_x,src_y) == (x,y):
            return False
        if src_x == x: # If in the same row, it'll be left or right
            if src_y < y:
                for i in range(src_y+1,y):# Move Right
                    if not self.is_not_conflict(src_x,i):
                        return False
            elif src_y > y:# Move Left
                for i in range(src_y - 1, y,-1):
                    if not self.is_not_conflict(src_x, i):
                        return False
        elif src_y == y:
            if src_x < x:
                for i in range(src_x+1,x): # Move Down
                    if not self.is_not_conflict(i, src_y):
                        return False
            elif src_x > x: # Move Up
                for i in range(src_x-1,x,-1):
                    if not self.is_not_conflict(i, src_y):
                        return False
        else:
            return False
        return True

    def possible_moves(self):
        moves = []
        moves += [(self.x+i,self.y) for i in range(-board+1,board) if self.x+i in range(board)]
        moves +=[(self.x,self.y+i) for i in range(-board+1,board) if self.y+i in range(board)]
        moves  = [move for move in moves if self.is_path_clear(move[0],move[1])]
        return list(set(moves))

class Knight(Coin):
    move = [-2,2]
    def is_in_range(self, x, y):
        if ChessBoard[x][y] == 0:
            return False
        return ((x,y) in self.possible_moves() and self.Color != ChessBoard[x][y][0])
    
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
            moves = [move for move in moves if move!=(self.x,self.y)]
        return moves

class Coin_Instance:
    """
    This is the instance class of each player [Black and white]
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
                # print ("Coin at",x,y,"will be in attack range of the",coin.Color+"_"+coin.name,"which is at",coin.get_position())
                return True
        return False
    
    def find_safe_position(self, opponent_instance, Color):
        """
        Check if any possible move for any piece is in attack range of opponent
        """
        for piece in self._Pieces:
            moves = piece.possible_moves()
            for move in moves:
                if check_if_unoccupied(move[0],move[1]):
                    init_position = piece.get_position()
                    ChessBoard[move[0]][move[1]] = piece.Color+"_"+piece.name
                    ChessBoard[init_position[0]][init_position[1]] = 0
                    if not opponent_instance.check_if_in_attack_range(move[0],move[1]):
                        if piece.is_path_clear(move[0],move[1]):
                            print (piece.Color+"_"+piece.name,"at",piece.get_position(),"Moved to",move)
                            # x1,y1 = piece.get_position()
                            # ChessBoard[x1][y1] = 0
                            # ChessBoard[move[0]][move[1]] = piece.Color+"_"+piece.name
                            piece.set_position(move[0],move[1])
                            return
                    ChessBoard[move[0]][move[1]] = 0
                    ChessBoard[init_position[0]][init_position[1]] = piece.Color+"_"+piece.name
        else:
            print ("No safe positions")

    
    def attack_random_opponent(self, opponent_instance):    
        for coin_position in opponent_instance._Pieces:
            for coin in self._Pieces:
                x = coin_position.x
                y = coin_position.y
                if coin.is_in_range(x,y):
                    if coin.is_path_clear(x,y):
                        print ("Attacking Coin",ChessBoard[x][y],"at",x,y,"with our",coin.Color+"_"+coin.name,"which is at ",coin.get_position(),"\n")
                        init_x, init_y = coin.get_position() 
                        ChessBoard[x][y] = ChessBoard[init_x][init_y]
                        ChessBoard[init_x][init_y] = 0
                        coin.set_position(x,y)
                        opponent_instance._Pieces.remove(coin_position)
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

def print_ChessBoard():
    print (DataFrame(ChessBoard))

def get_piece_list(color):
    pawn   = [color+'_p']*8
    king   = [color+'_k']
    queen  = [color+'_q']
    rook   = [color+'_r']*2
    bishop = [color+'_b']*2
    knight = [color+'_n']*2
    return pawn+king+queen+rook+bishop+knight


def get_piece_names(color):
    pawn   = [color+'_p']
    king   = [color+'_k']
    queen  = [color+'_q']
    rook   = [color+'_r']
    bishop = [color+'_b']
    knight = [color+'_n']
    return pawn+king+queen+rook+bishop+knight

def get_random_piece(color):
    piece_list = get_piece_names(color)
    return GetPieceInstance(random.choice(piece_list),-1,-1,color)

def randomInitialize(color):
    pieces_list = get_piece_list(color)
    piece_list = []
    while(len(pieces_list)>0):
        x = random.randrange(board)
        y = random.randrange(board)
        if check_bounds(x,y) and check_if_unoccupied(x,y):
            element = pieces_list.pop(0)
            if (element == color+'_p') :
                if (color == White and x == board-1) or (color == Black and x == 0):
                    # Not placing pawn in the opponent territory                    
                    pieces_list.append(element)
                    continue
            piece = GetPieceInstance(element,x,y,color)
            if piece:
                ChessBoard[x][y] = piece.get_name()
                piece_list.append(piece)
    return piece_list

list_white = randomInitialize(White)
# list_black = randomInitialize(Black)

White_instance = Coin_Instance(list_white)
Black_instance = Coin_Instance([])

print ("Randomly initialized board\n")
print (DataFrame(ChessBoard))


selection = input("Enter your choice of coin if any: ")
if selection:
    choice = selection.lower()
    if choice == "knight":
        piece = Black+'_n'
    elif choice == "king":
        piece = Black+'_k'
    elif choice == "queen":
        piece = Black+'_q'
    elif choice == "pawn":
        piece = Black+'_p'
    elif choice == "rook":
        piece = Black+'_r'
    elif choice == "bishop":
        piece = Black+'_b'
    else:
        print ("Your input is invalid, choosing random coin")
        piece = 'random'
    
    if piece == 'random':
        Black_random_piece = get_random_piece(Black)
    else:    
        Black_random_piece = GetPieceInstance(piece,-1,-1,Black)
else:
    Black_random_piece = get_random_piece(Black)

print ("\nThe Chosen Piece is",Black_random_piece.get_name())

n = board*board
while(n>0):
    x = random.randrange(board)
    y = random.randrange(board)
    if check_bounds(x,y) and check_if_unoccupied(x,y):
        ChessBoard[x][y] = Black_random_piece.get_name()
        if not White_instance.check_if_in_attack_range(x,y):
            print("Random safest position for the",Black_random_piece.get_name(),"in the Board is",x,y)
            Black_random_piece.set_position(x,y)
            Black_instance._Pieces.append(Black_random_piece)
            break
        ChessBoard[x][y] = 0
    n-=1
else:
    print ("No random safe positions here")
    sys.exit(0)

print_ChessBoard()
draw_line()

for position in White_instance.get_all_positions():
    if Black_random_piece.is_in_range(position[0],position[1]):
        print (Black_random_piece.get_name(),"at",Black_random_piece.get_position(),"Can attack",ChessBoard[position[0]][position[1]],"at",position)
        break
else:
    print ("\nCan't attack any piece")
