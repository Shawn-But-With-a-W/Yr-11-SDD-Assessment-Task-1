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

def check_dead_end(maze: list[list[str]], row, column) -> bool:
    '''Checks if a space is a dead-end. If yes, fill in the space with a wall and return True; else, return False'''
    # If it is a 0, check the number of walls/edges that it is surrounded by
    if maze[row][column] == '0':
        walls_and_edges = 0 
        
        if row+1 >= len(maze): # Index is out of list range if this holds true
            walls_and_edges += 1
        elif maze[row+1][column] == '1':
            walls_and_edges += 1

        if row-1 < 0:
            walls_and_edges += 1
        elif maze[row-1][column] == '1':
            walls_and_edges += 1

        if column+1 >= len(maze[0]):
            walls_and_edges += 1
        elif maze[row][column+1] == '1':
            walls_and_edges += 1

        if column-1 < 0:
            walls_and_edges += 1
        elif maze[row][column-1] == '1':
            walls_and_edges += 1

        # Replace the space with a wall if it is surrounded by three or more walls/edges
        if walls_and_edges >= 3:
            maze[row][column] = '1'
            return True

    # Return False if either the space is a wall or is a space but surruonded by less than 3 walls
    return False

def fill_dead_end(maze: list[list[str]], coord_list=[]):
    '''Replaces all spaces in the maze surrounded by three walls or edges, with a wall.'''
    dead_ends_filled = 0

    if coord_list == []:
    # Loop through every value
        for row in range(len(maze)):
            for column in range(len(maze[0])):
                if check_dead_end(maze, row, column):
                    dead_ends_filled += 1
                else:
                    # Add to coord_list as empty spaces in the maze
                    coord_list.append((row, column))

    else:
        for row, column in coord_list:
            if check_dead_end(maze, row, column):
                dead_ends_filled += 1
                # Remove from coord_list once filled as wall
                coord_list.remove((row, column))
    
    # Recur the function until no dead ends can be filled with walls
    if dead_ends_filled > 0:
        fill_dead_end(maze, coord_list)

def create_path(maze: list[list[str]], filled_maze: list[list[str]]):
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
fill_dead_end(filled_maze)
create_path(maze, filled_maze)

# Loop through whole maze and print out all values
for row in maze:
    print('')
    for char in row:
        print(char, end=' ')
