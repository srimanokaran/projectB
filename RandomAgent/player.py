from random import randint
from referee.board import Board
import referee.game as GameFile

class Player:
    
    
    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        self.board = Board(n)
        self.size = n
        
        # put your code here

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        print("hi we are in agent 2 : action function")
        
        x = randint(0,self.size-1)
        y = randint(0,self.size-1)
        
        while(True):
            if(self.board[x,y] == None):
                return (GameFile._ACTION_PLACE, x,y)
            else:
                x = randint(0,self.size-1)
                y = randint(0,self.size-1)

    
    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of 
        their chosen action. Update your internal representation of the 
        game state based on this. The parameter action is the chosen 
        action itself. 
        
        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """
        print("hi we are in agent 2 : turn function")
        
        x = action[1]
        y = action[2]
        self.board[(x,y)] = player
        
        """""
        for i in range(self.size):
            for j in range(self.size):
                print(f"({i},{j}) = {self.board.__getitem__((i,j))}")
        """
    def return_blue_coords1(self):
        """
        return the bottom row of coordinates in a list of tuples
        """
        
        size = self.size
        array = []
        
        for i in range(size):   
            array.append((i,0))
        
        return array
    
    def return_blue_coords2(self):
        """
        return the top row coordinates in a list of tuples
        """
        
        size = self.size
        array = []
        
        for i in range(size):   
            array.append((i,size))
        
        return array