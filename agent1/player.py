from random import randint
import referee.board as Board
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
        
        the return type is (The action that happened , x , y)
        """
        x = randint(0,4)
        y = randint(0,4)
        
        # you cant place in the center
        center = round( (self.size / 2) )
        
        while(True):
            if(self.board[(x,y)] == None):
                
                if (x,y) != (center, center):
                    
                    return (GameFile._ACTION_PLACE, x,y)
                
            else:
                x = randint(0,4)
                y = randint(0,4)


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
        
        # captures and placement 
        self.board[(x,y)] = player
        
        game = GameFile.Game(5)
        print(self.board)
        # put your code here