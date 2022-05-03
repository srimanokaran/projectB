from random import randint
import referee.board as BoardFile
import referee.game as GameFile

class Player:
    
    # local game state
    board = {}
    
    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        self.board = self.create_dict(n)
        
        # put your code here

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        
        return (GameFile._ACTION_PLACE, randint(0,4), randint(0,4))

        # put your code here
    
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
        print("hi we are in agent 2")
        
        x = action[1]
        y = action[2]
        self.board[(x,y)] = player
        
        game = GameFile.Game(5)
        print(self.board)
        # put your code here

    def create_dict(self, n):
        """
        create a dictionary with coordinates of an n x n matrix as the keys and none as
        the value to initialise
        
        in the future the value could be either red, blue, blocked
        red : a piece placed by red
        blue : a piece placed by blue
        blocked : a coordinate that is blocked by design

        Args:
            n (int): size of the board

        Returns:
            dict: a dictionary with coordinates with keys as coordinates of a n x n matrix
            and value as None initially
        """
        mydict = {}
        for i in range(n):
            for j in range(n):
                mydict[(i,j)] = None
        return mydict