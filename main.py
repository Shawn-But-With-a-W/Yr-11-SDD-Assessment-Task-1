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


def check_surroundings(maze: list[list[str]], coord: tuple[int]) -> list[str(int)]:
    '''Returns the the value of the four spaces surrounding row column in maze in order of (up, down, left, right).'''
    row = coord[0]
    column = coord[1]

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


def fill_dead_end(maze: list[list[str]], coord_list=[], start=None) -> tuple[list[tuple], tuple, tuple]:
    '''Replaces all spaces in the maze surrounded by three walls or edges, with a wall. Returns the location of the start.'''
    dead_ends_filled = 0

    if coord_list == []:
    # Loop through every value in the maze
        for row in range(len(maze)):
            for column in range(len(maze[0])):
                # Check value and determine whether to fill as dead end or append to list as empty spaces
                if maze[row][column] == '0':
                    surroundings = check_surroundings(maze, (row, column))
                    if surroundings.count('1') + surroundings.count(None) >= 3:
                        maze[row][column] = '1'
                        dead_ends_filled += 1
                    else:
                        coord_list.append((row, column))
                
                # Find the start and end coordinates for later use in walk()
                elif maze[row][column] == '5':
                    start = (row, column)

    else:
        # Loop through all known empty non-dead end spaces
        for row, column in coord_list:
            if maze[row][column] == '0':
                surroundings = check_surroundings(maze, (row, column))
                if surroundings.count('1') + surroundings.count(None) >= 3:
                    maze[row][column] = '1'
                    dead_ends_filled += 1
                    coord_list.remove((row, column))
            
    # Recur the function until no dead ends can be filled
    if dead_ends_filled > 0:
        return fill_dead_end(maze, coord_list, start)
    else:
        return start


def walk(maze: list[list[str]], current_coord: tuple, coord_list=[]):
    '''Simulates a walk to determine a single solution to the maze.'''
    DIRECTION_TO_COORDINATE = {
        0 : 'current_coord[0]-1, current_coord[1]', 
        1 : 'current_coord[0]+1, current_coord[1]', 
        2 : 'current_coord[0], current_coord[1]-1', 
        3 : 'current_coord[0], current_coord[1]+1'}

    # Change current space to a path
    maze[current_coord[0]][current_coord[1]] = '5'
    coord_list.append(current_coord)

    surroundings = check_surroundings(maze, current_coord)
    if '3' in surroundings:
        return coord_list
    junction_count = surroundings.count('0')

    # If there is/are empty space(s)
    if junction_count > 0:
        empty_direction = DIRECTION_TO_COORDINATE[surroundings.index('0')]
    elif junction_count == 0:
        return coord_list
        raise TypeError('Dead end found in walk')

    # Check if junction
    while junction_count > 1:
        # Mark a direction as blocked
        maze[eval(empty_direction)[0]][eval(empty_direction)[1]] = '1'
        surroundings[surroundings.index('0')] = '1'
        junction_count -= 1
        empty_direction = DIRECTION_TO_COORDINATE[surroundings.index('0')]

    # Walk in the only avaliable direction by changing current_coord to that space
    current_coord = eval(empty_direction)
    return walk(maze, current_coord, coord_list)


def create_path(maze: list[list[str]], coord_list: list[tuple[int]]):
    '''Replaces all given spaces with paths.'''
    for row, column in coord_list:
        maze[row][column] = '5'


# main starts below

maze = open_maze('test_maze.txt')
filled_maze = open_maze('test_maze.txt') # Can't assingn the two to same function output or they will be changed together
start = fill_dead_end(filled_maze)

for row in filled_maze:
    print('')
    for char in row:
        print(char, end=' ')
print('')

coord_list = walk(filled_maze, start)

for row in filled_maze:
    print('')
    for char in row:
        print(char, end=' ')
print('')

create_path(maze, coord_list)

for row in maze:
    print('')
    for char in row:
        print(char, end=' ')
print('')
