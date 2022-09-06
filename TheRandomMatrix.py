import random
import time

# INTRO :
# In this file I've created "The Random Matrix".
# At first, a matrix of size 5x9 is created randomly (meaning each spot in the matrix is assigned with a value in a random mannner).
# Each value is either 'b' representing the color blue, 'y' representing the color yellow or 'p' representing the color pink.
# This matrix contains our pyramid.  

# RULES :
# There are 3 rules that the pyramid must hold -
# 1. The color blue cannot be found withing the perimeter of the pyramid (meaning its edges).
#    in case we find one or more, the spot's color will be randomly reassigned.
# 2. The color pink cannot be found on the right\left side of a blue colored spot, nor above or under a blue covered spot.
#    in case we find one or more, the pink spot's color will be randomly reassigned.
# 3. There cannot be a row in the pyramid that contains 4 or more yellow spots. if so, the entire row will be randomly reassigned.

# ABOUT :
# The game runs from start to finish by itself, informing the viewers in every round of the game about the current state of the pyramid.
# If a rule violation is detected, the program will notify the viewers and continue to fix it.
# The program ends the game in two ways - either it succesfully managed to get a pyramid that hold all of the given rules,
# or its calculations took too much time, so it terminated. I've set the timer to 20 seconds.

# So, now that we know everything, let start our wonderfull game !
# Written by Roy Hamamy.

# edges possition will be importent when verifying our rules
left_edge_of_matrix = [[0,4],[1,3],[2,2],[3,1],[4,0]]
right_edge_of_matrix = [[0,4],[1,5],[2,6],[3,7],[4,8]]
bottom_edege_of_matrix = [[4,0],[4,1],[4,2],[4,3],[4,4],[4,5],[4,6],[4,7],[4,8]]

# This function will help us assign random colors to a spot in the matrix
def randomize_spot():
    rand = random.randint(1,3)
    if rand == 1 :
        return 'y'
    if rand == 2 :
        return 'b'
    if rand == 3 :
        return 'p'

# The following two functions will help us display our matrix and pyramid to the viewers
def print_matrix(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    print('\n')

def print_pyramid(matrix):
    print("\t\t\t\t" + matrix[0][4])
    print("\t\t\t" + '\t'.join(matrix[1][i] for i in range(3,6)))
    print("\t\t" + '\t'.join(matrix[2][i] for i in range(2,7)))
    print("\t" + '\t'.join(matrix[3][i] for i in range(1,8)))
    print('\t'.join(matrix[4][i] for i in range(0,9)))
    print('\n')

# This function checks the edges of the pyramid for blue colored spots
def check_blue_in_edges(matrix) :
    for spot in left_edge_of_matrix:
        if matrix[spot[0]][spot[1]] == 'b': 
            return spot
    for spot in right_edge_of_matrix:
        if matrix[spot[0]][spot[1]] == 'b': 
            return spot
    for spot in bottom_edege_of_matrix:
        if matrix[spot[0]][spot[1]] == 'b': 
            return spot
    return []                                    # This means there were no blue spots on the edges    


# In this function we follow rule #1 in the above text. if the rule doesn't hold, a notification is sent and the spot is reassigned randomly.
def verify_no_blue_edges(matrix):
    test = check_blue_in_edges(matrix)
    if test == []:
        return 0                                 # This means there were no blue spots on the edges 
    while test != [] :
        print(f'There seems to be a blue color at the edge of {test[0]+1,test[1]+1}.' + " lets fix it ! \n")
        print("Here is our fixed pyramid for this round : \n")
        matrix[test[0]][test[1]] = randomize_spot()
        print_pyramid(matrix)
        test = check_blue_in_edges(matrix)
    return 1                                     # This means that we found blue spots on the edges (and fixed it)

# The next 4 functions check for a blue spot on a certain side of a given indexed spot in the matrix
def check_bottom_part(matrix, index):
    if matrix[index[0]+1][index[1]] == 'b':
        return [index[0]+1,index[1]]
    return []                               

def check_upper_part(matrix, index):
    if matrix[index[0]-1][index[1]] == 'b':
        return [index[0]-1,index[1]]
    return []

def check_left_part(matrix, index):
    if matrix[index[0]][index[1]-1] == 'b':
        return [index[0],index[1]-1]
    return []

def check_right_part(matrix, index):
    if matrix[index[0]][index[1]+1] == 'b':
        return [index[0],index[1]+1]
    return []

# In order to apply rule #2 in the above text, we must check if every pink has a blue spot near it and if so, return the blue spot's location
def check_pink_position(matrix, index):
    if index in left_edge_of_matrix:             # If its in the left edge, we can only check the right\bottom side of the pyramid
        if index in bottom_edege_of_matrix:
            # Here we specifically check the bottom-left spot (edge case)
            if matrix[4][1] == 'b':
                return [4,1]
            return []
        else:
            possition = check_bottom_part(matrix,index)
            if possition == [] :
                possition =  check_right_part(matrix,index)
            return possition

    if index in right_edge_of_matrix:           # If its in the right edge, we can only check the left\bottom side of the pyramid
        if index in bottom_edege_of_matrix:
            # Here we specifically check the bottom-right spot (edge case)
            if matrix[4][7] == 'b':
                return [4,7]
            return []
        else:
            possition = check_bottom_part(matrix,index)
            if possition == [] :
                possition =  check_left_part(matrix,index)
            return possition     

    if index in bottom_edege_of_matrix:         # If its in the bottom edge, we can only check the left\righ\upper side of the pyramid
        possition = check_left_part(matrix,index)
        if possition == [] :
            possition = check_right_part(matrix,index)
            if possition == []:
                possition = check_upper_part(matrix,index)
        return possition
        
    else:                                       # If its not in any edge, we check every side of the spot
        possition = check_left_part(matrix,index)
        if possition == [] :
            possition = check_right_part(matrix,index)
            if possition == [] :
                possition = check_upper_part(matrix,index)
                if possition == [] :
                    possition = check_bottom_part(matrix,index)
        return possition

# In this function we loop through the matrix and verify that the pyramid holds rule #2. if not, we inform the viewers and fix the necessary spots
def verify_pink_possition(matrix):
    verify = False                              # This will inform us if we found a rule violation 
    status = 0                                  # This is for later purposes (will inform us that there was a change in the pyramid)
    # Here we specificaly check the top of the pyramid (edge case)
    if(matrix[0][4] == 'p'):
        if(matrix[1][4] == 'b'):
            print(f'We seem to have a pink in {[0,4]} that has a blue near it. let fix it ! \n')
            print("Here is our fixed pyramid for this round : \n")
            matrix[0][4] = randomize_spot()
            print_pyramid(matrix)
    while(not verify):        
        verify = True                           # As long as we dont find a rule violation, it will remain True and loop will terminate
        for row in range(1,5):
            for spot in range(4-row,5+row):
                if matrix[row][spot] == 'p':
                    location = check_pink_position(matrix,[row,spot])
                    if(location != []):         # This means we found a rule violation
                        status = 1              # we need to make a change in the pyramid because of the rule violation
                        verify = False          # because there was a rule violation, we need to loop again and check for new or more violations
                        print(f'We seem to have a pink in {[row+1,spot+1]} that has a blue near it. let fix it ! \n')
                        print("Here is our fixed pyramid for this round : \n")
                        matrix[row][spot] = randomize_spot()
                        print_pyramid(matrix)
    return status

# This function checks rows in the pyramid that have at least 4 spots and verify that rule #3 hold. if not, it informs the viewers and fix the necessary row
def verify_yellow_spots(matrix):
    verify = False                              # This will inform us if we found a rule violation
    status = 0                                  # This is for later purposes (will inform us that there was a change in the pyramid)
    count = 0                                   # This will help us count how many yellow spots are in each row
    while(not verify):                          
        verify = True                           # As long as we dont find a rule violation, it will remain True and loop will terminate
        for row in range(2,5):
            for spot in range(4-row,5+row):
                if matrix[row][spot] == 'y':
                    count = count + 1
            
            if count >= 4:                      # This means we found a rule violation
                status = 1                      # we need to make a change in the pyramid because of the rule violation
                verify = False                  # because there was a rule violation, we need to loop again and check for new or more violations
                print(f'We seem to have a problem with row number {row+1}. it has 4 or more yellow spots. lets fix it ! \n')
                print("Here is our fixed pyramid for this round : \n")
                for spot in range(4-row,5+row):
                    matrix[row][spot] = randomize_spot()
                print_pyramid(matrix)
            count = 0                           # We are about to search a new row, so we nust reset our counter
    return status

# In this function we run our matrix through a loop that keeps checking if the all the rules hold.
# Every verifying function we created returns a status flag (1 means a violation has been found, 0 means everyting was ok).
# In order to make sure that our final pyramid is valid, it must get an Ok (meaning 0) from all the verifying functions.
# If it did get an Ok - we inform the viewers and end the game.
# Otherwise, we countinue to verify and fix the pyramid using our functions.
# This function has a timer, set to 20 seconds. if the function doesnt return an answer in under 20 seconds, it terminates and inform the viewers about it.
def manage_game(matrix):
    verify = 1                                  # This will inform us if the matrix has been changed due to a rule violation
    time_start = time.time()
    time_end = time_start + 20
    while(verify > 0):
        verify = verify_yellow_spots(matrix) + verify_pink_possition(matrix) + verify_no_blue_edges(matrix)       # As long as we dont find a rule violation, it will be set to zero and the loop will terminate
        if time.time() >= time_end :
            print("ERROR : Calculations took too much time. program terminated manually.")
            return

    print("Hurray ! we have managed to get our desired pyramid succesfully ! \n")
    print("Here is our final pyramid : \n")
    print_pyramid(matrix)
    return 0


# This is our main function. here we create the matrix and assign it with random colors.
# We then inform the viewers about our initial matrix and pyramid, and start the game.
# Note : I've added an example of a matrix that calculates and stops after a few steps, because usually the function doesnt stop when given random values.
# Example matrix :
#                 [['b','b','b','b','p','b','b','b','b'],
#                  ['b','b','b','y','y','y','b','b','b'],
#                  ['b','b','y','p','y','y','p','b','b'],
#                  ['b','p','p','p','p','p','y','p','b'],
#                  ['b','p','p','p','p','p','p','p','p']]

def main():
    matrix = [ [] , [] , [] , [] , [] ]
    for row in range(5):
        for slot in range(9):
            matrix[row].append(randomize_spot())

    print("Here is our initial matrix : \n")
    print_matrix(matrix)
    print("That means our pyramid is : \n")         
    print_pyramid(matrix)
    print("Now, lets begin our fun little game ! :) \n")

    manage_game(matrix)                         
#                                   TO ACTIVATE THE GAME - DELETE THE COMMENT FROM THE NEXT LINE   
#main()

                                   



            





            





            