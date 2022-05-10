# An example of the game board
*                .-'-._.-'-._.-'-._.-'-._.-'-.
*               |  b  |     |     |     |     |
*             .-'-._.-'-._.-'-._.-'-._.-'-._.-'
*            |     |  b  |     |     |     |
*          .-'-._.-'-._.-'-._.-'-._.-'-._.-'
*         |  r  |     |  b  |     |     |
*       .-'-._.-'-._.-'-._.-'-._.-'-._.-'
*      |     |  r  |     |  b  |     |
*    .-'-._.-'-._.-'-._.-'-._.-'-._.-'
*   |     |  r  |     |     |  b  |
*   '-._.-'-._.-'-._.-'-._.-'-._.-'

# Additional information
1. The distance we will be using is manhattan distance

# Variables and data structures required

The coordinate that we will be looking at to explore its neigbours next
```
current_coordinate = (y,x)
```

has the coordinates of the path that we follow to finish the game
```
path = [] 
```

the neighbours of current_coordinate with
**key : coordinates**
**value : distance to closest final node**
```
neighbours_dict = {key : value}
```

this will be a list of coordinates of final_coords1 + final_coords2
we can remove elements from one of the finalcoords from finalcoords in step 4
```
final_coords = []
```

# Process to follow
1. Start at initial state, keep track of last node we placed and then look at all possible moves, 
make neighbour nodes the next possible moves.
No start and end for our path, we just have to include start and end coords in path

2. put all neighbouring nodes into a dictionary 

key : coordinates
value : distance to closest final node

3. sort it by distance to the closest final coordinates and pick 1st one and add it to path
    - This is because there can be multiple nodes with the same smallest distance

4. check which node is closest to final in path and expand this to its neighbours and repeat step 2

5. once one of the coordinates in path is present in the final list, we want to find the shortest path to the other end, so we remove the coordinates of one end from the final coords list

# Process to follow (the better version)

1. Start at initial state
2. get neighbours of initial state
3. get one neighbours, neighbour list
   Do the below for every element in the list neighbour neighbours list
        a. if we place our piece and the opponent places theirs, we calculate in total how many pieces our team has
        b. then we store this value for that pair
            i. after each placement and capture we check the number of nodes in our team. 
            ii. instead of storing the value for each pair, we can compare and store only the minimum value, as we only need the minimum value.
    We choose the one with the minimum value and then assign this value to the top node

4. then we have to choose the Maximum value from the set of minimum values we have as it would be of our benefit and then we make the move that has this maximum value.

# MiniMax value function
'''
function minimax-decision:

    # this is our move
    value is a dictionary then we sort it by value to get the 
    move with the largest value and then do this move

    for each move in neighbours:
        value[move] = minimax-value (find_neighbours(move))
    end
    return largest value in valuelist

'''

'''
function minimax-value(neighbours_list, board, value):
    if neighbours_list = []:
        return value
    else 
        temp_board = deepcopy of board
        
        # This is the opponent playing

        place our move in board

        place first element of neighbours_list in board
        
        count how many of our piece are there

        if number of our pieces less than value:
            then value = number of our pieces
        
        remove the element from the neighbours list

        return minimax-value(updated neighbours_list, board, value)

'''
    


# References
(http://www.trmph.com/hexwiki/Basic_strategy_guide.html)