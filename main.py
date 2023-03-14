'''Submission for year 11 SDD assessment task 1'''

# Finds a path through a maze stored in external file, where:
# 1: walls
# 0: spaces
# 5: start
# 3: end
# All characters besides the last of the line have a trailing comma and space

__author__ = 'Shawn Li'
__copyright__ = 'Copyright 2023, Shawn Li'
__credits__ = []


def open_maze(file_name: str) -> list[list[str]]:
    '''Opens the maze file and returns it as a 2D list.'''
    with open(file_name) as f:
        maze = f.read()
        maze_list = []

        lines = maze.splitlines()
        # Loop through list of lines in file, and append current line as a list
        for line in lines:
            row = line.split(', ')
            maze_list.append(row)

    return maze_list


def check_surrounding(maze: list[list[str]], row, column) -> list:
    '''Returns the the value of the four spaces surrounding row column in maze in order of (up, down, left, right).'''
    surroundings = [None, None, None, None]
    
    if row-1 >= 0: # Index is negative if this hold false
        surroundings[0] = maze[row-1][column]

    if row+1 <= len(maze)-1: # Index is out of list range if this holds false
        surroundings[1] = maze[row+1][column]

    if column-1 >= 0: # Index is negative if this hold false
        surroundings[2] = maze[row][column-1]

    if column+1 <= len(maze[0])-1: # Index is out of list range if this holds false
        surroundings[3] = maze[row][column+1]

    return surroundings


def fill_dead_end(maze: list[list[str]], coord_list=[], start=None, end=None):
    '''Replaces all spaces in the maze surrounded by three walls or edges, with a wall. Returns coord_list, and the locations of start and end.'''
    dead_ends_filled = 0

    if coord_list == []:
    # Loop through every value
        for row in range(len(maze)):
            for column in range(len(maze[0])):
                # Check value
                if maze[row][column] == '0':
                    surroundings = check_surrounding(maze, row, column)
                    if surroundings.count('1') + surroundings.count(None) >= 3:
                        maze[row][column] = '1'
                        dead_ends_filled += 1
                    else:
                        coord_list.append((row, column))
                
                elif maze[row][column] == '5':
                    start = (row, column)
                elif maze[row][column] == '3':
                    end = (row, column)

    else:
        for row, column in coord_list:
            if maze[row][column] == '0':
                surroundings = check_surrounding(maze, row, column)
                if surroundings.count('1') + surroundings.count(None) >= 3:
                    maze[row][column] = '1'
                    coord_list.remove((row, column))
                    dead_ends_filled += 1
            
    # Recur the function until no dead ends can be filled
    if dead_ends_filled > 0:
        return(fill_dead_end(maze, coord_list, start, end))
    else:
        return coord_list, start, end


def walk(maze: list[list[str]], coord_list, current_coord, end_coord):
    '''Simulates a walk to determine a single solution to the maze.'''
    maze[current_coord[0]][current_coord[1]] = '4'

    surroundings = check_surrounding(maze, current_coord[0], current_coord[1])

    # Check if junction
    if surroundings.count('0') >= 2:
        # Choose a path to block
        pass
    else:
        empty_direction = surroundings.index('0')
        if empty_direction == 0:
            pass
        elif empty_direction == 1:
            pass
        elif empty_direction == 2:
            pass
        elif empty_direction == 3:

def create_path(maze: list[list[str]], filled_maze: list[list[str]], coord_list):
    '''Finds all spaces in filled_maze, replaces their corresponding spaces with paths in maze.'''
    # Loops through all values
    for row in range(len(filled_maze)):
        for column in range(len(filled_maze[0])):
            # Fill in corresponding space as path in maze, if the value is a possible path (empty space) in filled_maze
            if filled_maze[row][column] == '0':
                maze[row][column] = '5'


# main starts below

maze = open_maze('test_maze.txt')
filled_maze = open_maze('test_maze.txt') # Can't assingn the two to same function output or they will be changed together
coord_list, start, end = fill_dead_end(filled_maze)

for row in filled_maze:
    print('')
    for char in row:
        print(char, end=' ')

print('')

create_path(maze, filled_maze)

# Loop through whole maze and print out all values
for row in maze:
    print('')
    for char in row:
        print(char, end=' ')
