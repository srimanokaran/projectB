from random import randint
from typing import final
from agent1.board import Board
import referee.game as GameFile
import agent1.constant as const
import copy

class Player:
    """
    The coordinates in board follow the format (y,x)
    
    For every action done by a player 
        - Two turn functions are called
            - one for agent 1
            - other for agent 2
        - These functions are called for the sole purpose of updating the local board we have 
        and for the referee to update the global board
    
    """
    
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
        self.player = player
        self.turn_counter = 1
        self.last_move = (0,0) # this is just a temp move
        
        # getting the final set of coordinates for future reference
        if (player == "red"):
            final_coords1 = self.return_red_coords1()
            final_coords2 = self.return_red_coords2()
        else:
            final_coords1 = self.return_blue_coords1()
            final_coords2 = self.return_blue_coords2()
            
    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        
        print ("hi we are in agent 1 : action function")
        center = round((self.size / 2))
        
        # Since we cant place the first piece in the middle we will place it a bit off a corner
        # that way it cant be completely blocked, and form a path
        # the below link was used to decide the opening strategy
        # http://www.trmph.com/hexwiki/Basic_strategy_guide.html
        if ((self.turn_counter == 1) and (self.player == const.RED)):
            self.last_move = (0, 1)
            return (GameFile._ACTION_PLACE, 0, 1)
        
        # if it is blue we will place it in the center everytime to get control of the board
        if ((self.turn_counter == 1) and (self.player == const.BLUE)): 
            self.last_move = (center, center)
            return (GameFile._ACTION_PLACE, center, center)
    
        # if it is not the first move
        
        
        # get neighbours of the initial state
        neighbours = self.board._coord_neighbours(self.last_move)
        
        print(f"the neighbours of {self.last_move} is {neighbours}")
        
        # Get a neighbour's neighbour's list
        for our_possible_moves in neighbours:
            
            opponent_possible_moves = temp_board._coord_neighbours(our_possible_moves)
            
            # Keep  
            for opponent_move in opponent_possible_moves:
                
                temp_board = copy.deepcopy(self.board)
                
                temp_board.place(opponent_move)
                
                # count
        

    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of 
        their chosen action. Update your internal representation of the 
        game state based on this. The parameter action is the chosen 
        action itself. 
        
        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        
        Turn doesnt affect any action, the whole purpose of turn is to 
        just update the local board in player
        """
        
        print("hi we are in agent 1 : turn function")
        print (f"The turn counter value for {player} is {self.turn_counter}")
        
        
        # if its a place action then you just place the point on the board
        if (action[0] == GameFile._ACTION_PLACE):
            y = action[1]
            x = action[2]
            self.board.place(player, (y,x))
        
        # if it is a steal action then you also check whether its the second turn
        # as this is the only turn where a steal can possibly happen
        # if they are both true then  do steal
        elif (action[0] == GameFile._ACTION_STEAL):
            if (self.turn_counter == const.ALLOWED_TO_STEAL_TURN):
                self.board.swap()
        
        
        for i in range(self.size):
            for j in range(self.size):
                print(f"({i},{j}) = {self.board.__getitem__((i,j))}")


        # The position of this would be an error
        self.turn_counter += 1

    def return_red_coords1(self):
        """
        return the bottom row of coordinates in a list of tuples
        """
        
        size = self.size
        array = []
        
        for i in range(size):   
            array.append((0,i))
        
        return array
    
    def return_red_coords2(self):
        """
        return the top row coordinates in a list of tuples
        """
        
        size = self.size
        array = []
        
        for i in range(size):   
            array.append((size,i))
        
        return array

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

    def minimax_decision(self, neighbours, board):
        """
        
        returns the node that we are going to place the board based on minimax
        calculation taught in lectures
        
        neighbours : list of neighbours of the last node that was placed on
        the grid
        
        board : last game state of the board that we had 
        
        """
        
        # value is a dictionary with
        # key : coordinate
        # value : the number of neighbours
        value = {}
        
        # go through any move that we can possibly do next
        # in our case we limit this to neighbours of the current node
        for move in neighbours:
            
            # get the possible moves the opponent can do
            # in our case we limit this to  the neighbours of neigbhours
            neighbours_list = board._coord_neighbours(move)
            
            # get the minimax utility value from the minimax_value function
            value[move] = minimax_value(neighbours_list, move, board)
        
        # Get the node which would lead us to have the largest number of pieces
        # after minimax calculation
        maximum = const.A_SMALL_VALUE
        for key in value:
            if value[key] > maximum:
                final_move = key
        
        return final_move
    
    def minimax_value(neighbours_list, move, board):
        
        """
        
        returns the utility value 
        
        utility value : the number of pieces our colour has on the grid
        
        neighbours_list : is the list of nodes that the opponent could do 
        
        move : the move that we do
        
        board : current game state of the board
        
        """
        for opponent_move in neighbours_list:
            
            # would reset to the earliest state we know of
            temp_board = copy.deepcopy(board)
            
            # place our move on the board
            temp_board.place(move)
            
            # place the opponent move on the board
            temp_board.place(opponent_move)
            
            # count number of our pieces
            # we dont know how to do this yet
            number_of_pieces = 5
             
            # check if smallest and replace value as opponent will want 
            # the least for us
            if number_of_pieces < value:
                value = number_of_pieces            
        
        return value
        # This is the opponent playing
        # place first element of neighbours_list in board
        # temp_board.place(???, ())
        
        # count how many of our piece are there

        
        

