'''Submission for year 11 Software Development & Design assessment task 1

Finds a path through a maze stored in external file, where:
1: walls
0: spaces
5: start
3: end
All characters besides the last of the line have a trailing comma and space
'''

__author__ = 'Shawn Li'
__copyright__ = 'Copyright 2023, Shawn Li'
__credits__ = ['Xavier Rowley', 'Zen Syahrizal']


def open_maze(file_name: str) -> list[list[str(int)]]:
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


def check_surroundings(maze: list[list[str(int)]], coord: tuple[int, int]) -> list[str(int), str(int), str(int), str(int)]:
    '''Returns the the value of the four spaces surrounding row column in maze in order of (up, down, left, right). Edges are '1' too.'''
    row = coord[0]
    column = coord[1]
    surroundings = ['1', '1', '1', '1']
    
    if row-1 >= 0: # Index is negative if this is false
        surroundings[0] = maze[row-1][column]
    if row+1 <= len(maze)-1: # Index is out of list range if this is false
        surroundings[1] = maze[row+1][column]
    if column-1 >= 0: # Index is negative if this is false
        surroundings[2] = maze[row][column-1]
    if column+1 <= len(maze[0])-1: # Index is out of list range if this is false
        surroundings[3] = maze[row][column+1]

    return surroundings


def fill_dead_end(maze: list[list[str(int)]], start_coord=None, end_coord=None, space_list=[]) -> tuple[tuple[int, int], tuple[int, int]]:
    '''Replaces dead ends in maze with a wall. Returns the coordinates of the start and end.'''
    dead_ends_filled = 0

    if space_list == []:
    # Loop through every value in the maze
        for row in range(len(maze)):
            for column in range(len(maze[0])):
                if maze[row][column] == '0':
                    # Check if there are more than/equal to 3 walls/edges surrounding the empty space
                    surroundings = check_surroundings(maze, (row, column))
                    if surroundings.count('1') >= 3:
                        # Fill in as a dead end with a wall
                        maze[row][column] = '1'
                        dead_ends_filled += 1
                    else:
                        # Add to space_list as an empty space
                        space_list.append((row, column))
                
                # Find the start and end coordinates for later use in walk()
                elif maze[row][column] == '5':
                    start_coord = (row, column)
                elif maze[row][column] == '3':
                    end_coord = (row, column)

    else:
        # Loop through all known empty non-dead end spaces from space_list
        for row, column in space_list:
            # Check if there are more than/equal to 3 walls/edges surrounding the empty space
            surroundings = check_surroundings(maze, (row, column))
            if surroundings.count('1') >= 3:
                maze[row][column] = '1'
                dead_ends_filled += 1
                space_list.remove((row, column))
            
    # Call the function until no dead ends can be filled
    if dead_ends_filled > 0:
        return fill_dead_end(maze, start_coord, end_coord, space_list)
    else:
        return start_coord, end_coord


def walk(filled_maze: list[list[str(int)]], current_coord: tuple[int, int], end_coord: tuple[int, int], path_list=[]):
    '''Simulates a walk to determine a single solution to the maze.'''
    current_row = current_coord[0]
    current_column = current_coord[1]

    DIRECTION_TO_COORDINATE = {
        0 : [current_row-1, current_column], 
        1 : [current_row+1, current_column], 
        2 : [current_row, current_column-1], 
        3 : [current_row, current_column+1]}

    # Change current space to a path and add to list
    filled_maze[current_coord[0]][current_coord[1]] = '5'
    path_list.append(current_coord)

    surroundings = check_surroundings(filled_maze, current_coord)
    # End recursion if ending space is directly next to the current space
    if '3' in surroundings:
        return path_list
    junction_count = surroundings.count('0')
    # Value of current_coord may be changed if a more optimal direction is found later in code
    current_coord = DIRECTION_TO_COORDINATE[surroundings.index('0')] # Determines coordinates of first empty space in surroundings

    # Error handler
    if junction_count == 0:
        raise Exception('Dead end found in walk')

    # If a junction exists
    elif junction_count > 1:
            end_row = end_coord[0]
            end_column = end_coord[1]

            end_direction_row = current_row
            end_direction_column = current_column

            # Ignoring if there is a wall, determine which horizontal(up or down) and vertical (left or right) directions would be the shortest paths to reach ending space
            if end_row < current_row:
                end_direction_row -= 1
            elif end_row > current_row:
                end_direction_row += 1
            if end_column < current_column:
                end_direction_column -= 1
            elif end_column > current_column:
                end_direction_column += 1
            
            # Walk in optimal direction if possible
            if filled_maze[end_direction_row][current_column] == '0':
                current_coord = (end_direction_row, current_column)
            elif filled_maze[current_row][end_direction_column] == '0':
                current_coord = (current_row, end_direction_column)

    # Recur the function with a new coordinate
    return walk(filled_maze, current_coord, end_coord, path_list)


def create_path(maze: list[list[str(int)]], path_list: list[tuple[int, int]]):
    '''Replaces all given spaces with paths.'''
    for row, column in path_list:
        maze[row][column] = '5'

# -----------------------------------------------------------------
# main starts below

maze = open_maze('test_maze.txt')
filled_maze = open_maze('test_maze.txt') # Can't assingn the two to same function output or they will be changed together

start_coord, end_coord = fill_dead_end(filled_maze)
path_list = walk(filled_maze, start_coord, end_coord)
create_path(maze, path_list)

# Loop through every value of maze and print out their values
# Each row on a new line, each character with a trailing space
for row in maze:
    for char in row:
        print(char, end=' ')
    print('')
