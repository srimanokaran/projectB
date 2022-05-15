

from typing import final
from matplotlib.pyplot import connect
from numpy import number
from agent1.board import Board
import referee.game as GameFile
import agent1.constant as const
import copy

class Player:
    """
    The coordinates in board follow the format (y,x)
    
        - Two turn functions are called
            - one for agent 1
            - other for agent 2
        - These functions are called for the sole purpose of updating the local board we have 
        and for the referee to update the global board

    In this version of our player's possible move is always a neighbour node
    
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
        if (player == const.RED):
            self.final_coords1 = self.return_red_coords1()
            self.final_coords2 = self.return_red_coords2()
        else:
            self.final_coords1 = self.return_blue_coords1()
            self.final_coords2 = self.return_blue_coords2()
        
            
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
        if ((self.turn_counter == 2) and (self.player == const.BLUE)): 
            self.last_move = (1, 0)
            return (GameFile._ACTION_PLACE, 1, 0)
    
        # if it is not the first move
        
        # get neighbours of the initial state
        neighbours = self.board._coord_neighbours(self.last_move)
        
        removed_neighbours = self.remove_occupied(neighbours, self.board)
        
        final_coordinate = self.final_coordinate(removed_neighbours)
        
        if (final_coordinate):
            self.last_move = final_coordinate
        else:
            # if not a final move then get minimax decision
            minimax_coord = self.minimax_decision(removed_neighbours, self.board)
            
            if (minimax_coord == False):
                
                """check for a depth 2 move/capture and if so proceed with that"""
                capture_coord = self.check_capture()
                print(f"capture_coord: {capture_coord}")
                if(capture_coord):
                    return (GameFile._ACTION_PLACE, int(capture_coord[0]), int(capture_coord[1]))
                    # self.last_move = capture_coord
                else:
                    """check for a backtrack move and proceed with that"""
                    back_track_coord = self.back_track()
                    print(f"back_track_coord : {back_track_coord}")
                    if (back_track_coord):
                        self.last_move = back_track_coord
                
            else:
                print("placing minimax coordinate")
                self.last_move = minimax_coord 
        
        return (GameFile._ACTION_PLACE, int(self.last_move[0]), int(self.last_move[1]))
        

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
                
        # The position of this would be an error
        self.turn_counter += 1
            
    def minimax_decision(self, neighbours, board):
        """
        
        returns the node that we are going to place the board based on minimax
        calculation taught in lectures
        
        or returns false if there is no conclusive move
        
        neighbours : list of neighbours of the last node that was placed on
        the grid
        
        board : last game state of the board that we had 
        
        """
        
        # key : coordinate
        # value : the number of neighbours
        value = {}
        
        # go through any move that we can possibly do next
        # in our case we limit this to neighbours of the current node
        for move in neighbours:
            
            # get the possible moves the opponent can do
            # in our case we limit this to  the neighbours of our possible move
            neighbours_list_all = board._coord_neighbours(move)
            
            # add neighbours of neighbours as a possible move to figure out if you could do a possible 
            
            # the possible moves cant consist of already taken nodes
            neighbours_list = self.remove_occupied(neighbours_list_all,board)
            
            if len(neighbours_list) == 0:
                value[move] = 0
                continue
            
            # get the minimax utility value from the minimax_value function
            value[move] = self.minimax_value(neighbours_list,  
                                        move, 
                                        board,
                                        const.A_LARGE_VALUE)

            
            
        
        # Get the node which would lead us to have the largest number of pieces
        # after minimax calculation
        print("The initial move is:")
        print(self.last_move)
        print("The value is: ")
        print(value)
        
        # maximum will be the highest utility value
        maximum = const.A_SMALL_VALUE
        for key in value:
            if value[key] > maximum:
                maximum = value[key] 
        print(f"maximum: {maximum}")  
              
        # Get nodes with highest utility value from the possible moves we can do and place it in a list
        possible_moves_temp = []
        for key in value:
            if (value[key] == maximum):
                # Moves that can be captured are not appened
                possible_moves_temp.append(key)
        
        
        
        possible_moves = self.remove_occupied(possible_moves_temp, board)
        print(f"Possible moves after removed: {possible_moves}")
        
        if (len(possible_moves) == 0):
            return False
        
        # we have to come up a different method for this section of the code
        # Find the move in our list of possible moves which has the which has the least number of
        # neighbouring occupied nodes, this will be our final move   
        maximum = const.A_SMALL_VALUE
        for move in possible_moves:
            
            # Get neighbours
            temp = self.board._coord_neighbours(move)
            
            # get neighbours that are free
            temp_removed = self.remove_occupied(temp, board)
            
            number_of_free_nodes = len(temp_removed)

            # print(f"number of free nodes is {number_of_free_nodes}")
            if number_of_free_nodes > maximum:
                maximum = number_of_free_nodes
                final_coord = move

        # print(f"final move is {final_coord}")
        return final_coord

    def minimax_value(self, neighbours_list, move, board, value):
        
        """
        returns the utility value for our current move
            - utility value : the number of our piece that we have on the board left 
            - since the opponenet would want us to have the least number of pieces in the board,
            this function goes through all possible opponent moves and choose the move that would 
            be least beneficial for us
            - then return the number of nodes that would be left in the board if that move is made
            by the opponent

              
        
        utility value : (the number of pieces our colour has on the grid) - (number of opponent pieces on  the grid)
        
        neighbours_list : is the list of nodes that the opponent could do 
        
        move : the move that we do
        
        board : current game state of the board

        value : the utility value
        
        """
        
        if neighbours_list == []:
            return value
        else:
            # get opponent move
            opponent_move = neighbours_list[0]
            
            # would reset to the earliest state we know of
            temp_board = copy.deepcopy(board)
            
            
            # print ("before move")
            # place our move on the board
            move_x = int(move[0]) 
            move_y = int(move[1])
            new_move = (move_x, move_y)

            temp_board.place(self.player,new_move)

            # place the opponent move on the board
            # print("before opponent move")
            
            op_x = int(opponent_move[0])
            op_y = int(opponent_move[1])
            opponent_move = (op_x, op_y)
            
            if (self.player == const.RED):
                temp_board.place(const.BLUE,opponent_move)
            else:
                temp_board.place(const.RED, opponent_move)
            
            # count number of our pieces
            num_of_our_pieces = self.count_number_of_pieces(self.player, temp_board)
            
            if (self.player == const.RED):
                num_of_opponent_pieces = self.count_number_of_pieces(const.BLUE, temp_board)
            else:
                num_of_opponent_pieces = self.count_number_of_pieces(const.RED, temp_board)
            
            print(f"The oppnent move is : {opponent_move}")
            print(f"number of our pieces : {num_of_our_pieces}")
            print(f"number of opponent pieces : {num_of_opponent_pieces}")
            utility_value = (num_of_our_pieces) - (num_of_opponent_pieces)

            # check if smallest and replace value as opponent will want 
            # the least for us
            if utility_value < value:
                value = utility_value
                
            # remove the node from the top
            neighbours_list.pop(0)
            
            # print(f"our {move} = {neighbours_list}")
            
            # returns self.minimax_value(updated_neighbours)
            return self.minimax_value(neighbours_list,
                                 move,
                                 board,
                                 value)
    
    def final_move(self, move, connected_coords):
        
        final_coord = False
        
        if (self.in_one_row(connected_coords) == True):
            if (move in self.final_coords2):
                
                final_coord = move
                
        elif (self.in_the_other_row(connected_coords) == True):
            if (move in self.final_coords1):
                final_coord = move
        
        return final_coord
    
    def in_one_row(self, connected_coords):
        
        """
        
        if a node in final_coords1 is in the path we have now
        return True else False
        
        """
        
        temp = []
            
        
        for node in self.final_coords1:            
            if node in connected_coords:
                return True 
        return False
            
    def in_the_other_row(self, connected_coords):
        
        """
        
        if a node in final_coords2 is in the path we have now
        return True else False
        
        """
        
        for node in self.final_coords2:
            if node in connected_coords:
                return True
                
        return False
    
    def get_occupied(self ,board):
        
        """
        At a given instance return the occupied cells in the board
        """
        
        occupied = []
        size = self.size
        for i in range(size):
            for j in range(size):
                if (board[(i,j)] != None):
                    occupied.append((i,j))
        
        return occupied

    def remove_occupied(self, neighbours_list, board):
        """
        
        from neighbours_list remove all elements from occupied list and return the list
        
        occupied_list has all the nodes in the board that are occupied
        """
        
        occupied_list = self.get_occupied(board)
        
        for coord in occupied_list:
            if coord in neighbours_list:
                neighbours_list.remove(coord)
        
        return neighbours_list 
    
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
            array.append((size-1,i))
        
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
            array.append((i,size-1))
        
        return array

    def convert_coords_to_int(self, coords_list):
        """
        
        Convert all coordinates in coords_list from numpy.int64 to int

        Args:
            coords_list ([(x,y)]): where x and y are of type int64
        Returns:
            [(x,y)]: where x and y are of type int
        """
        
        final_list = []
        
        for coord in coords_list:
            final_list.append((int(coord[0]), int(coord[1])))
        
        return final_list
    
    def count_number_of_pieces(self, colour, temp_board):
        
        """
        Returns the number of pieces of a colour in temp_board

        Returns:
            int : numbero of pieces of a certain colour in a board
        """
        
        num_of_pieces = 0
        for i in range(self.size):
            for j in range(self.size):
                if(temp_board[(i,j)] == colour):
                    num_of_pieces  += 1
        
        return num_of_pieces

    def check_capture(self):
        
        neighbours = self.board._coord_neighbours(self.last_move)
        
        print("capture mechanism")
        
        # for a move, check all it's neighborus.
        neighbours_neighbour_option = []
        for move in neighbours:
            for move1 in self.board._coord_neighbours(move):
                if move1 not in self.get_occupied(self.board):
                    neighbours_neighbour_option.append(move1)
        
        # remove duplicates
        neighbours_neighbour_option = list(dict.fromkeys(neighbours_neighbour_option))
        # print(neighbours_neighbour_option)
        int_neighbours = self.convert_coords_to_int(neighbours_neighbour_option)
        minimax_coord = self.minimax_decision(int_neighbours, self.board)
        
        if(minimax_coord):
            return minimax_coord
        
        
        return False

    def final_coordinate(self, neighbours):
        """
        
        final_coordinate
        
        """
        
        # Final coordinates check:
        for move in neighbours:
            
            connected_coords = self.board.connected_coords(self.last_move)
            int_connected_coords = self.convert_coords_to_int(connected_coords)
            last_coord = self.final_move(move, int_connected_coords)
            print(f"final_coords1 == : {self.final_coords1}")
            print(f"final_coords2 == : {self.final_coords2}")
            
            print(f"int_connected_coords: {int_connected_coords}")
            print(f"last_coord: {last_coord}")
            
            if (last_coord):
                return last_coord
        
        return False

    def back_track(self):
        """
        
            backtrack
        
        """
        
        # get a list of path that you can back track in
        connected_coords = self.board.connected_coords(self.last_move)
        # removed_coords = self.remove_occupied(connected_coords, self.board)
        int_coords = self.convert_coords_to_int(connected_coords)
        print("backtrack")
        print(f"self.last_move value is {self.last_move} and the type is {self.board[(0,0)]}")
        print(f"the value of (1,0) is {self.board[(1,0)]}")
        print(f"self.last_move is {self.last_move}")
        print(f"connected_coords is {connected_coords}")
        print(f"int coords is {int_coords}")
        for coord in int_coords:
            
            neighbours = self.board._coord_neighbours(coord)
            removed_neighbours = self.remove_occupied(neighbours, self.board)
            int_neighbours = self.convert_coords_to_int(removed_neighbours)
            
            minimax_coord = self.minimax_decision(int_neighbours, self.board)
            
            if (minimax_coord):
                return minimax_coord
        
        return False