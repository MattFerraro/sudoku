import copy
SORTED_ROW = range(1, 10)


def solve(array):
    '''
    Given a sudoku board as an array, return a solved copy of it or raise
    a valueError
    '''
    for i in xrange(81):
        print "UNKNOWNS:", count_unknown(array)
        array = fill_spaces(array)

        if count_unknown(array) == 0:
            print "DONE"
            break

    if count_unknown(array) == 0 and validate(array):
        return array
    else:
        raise ValueError("I could not solve the sudoku!")


def fill_spaces(array):
    '''
    Given a sudoku board as an array, return a copy of the board that has
    filled in at least 1 space. If not even one space could be filled, raise
    a ValueError
    '''
    board = copy.copy(array)
    for r, row in enumerate(board):
        for c, num in enumerate(row):
            if num != 0:
                continue

            # extract the column to look like a flat list
            # Note: this may be easier in numpy?
            column = column_to_psuedo_row(board, c)
            # Note: we'll probably be doing this a lot...maybe it's worth
            # storing the board columnwise as well as row-wise in memory?

            # extract the square to look like a flat list
            # Note: this may be easier in numpy?
            square = square_to_psuedo_row(board, c / 3, r / 3)
            # Note: we'll probably be doing this a lot...maybe it's worth
            # storing the board squarewise as well as row-wise in memory?

            all_candidates = range(1, 10)
            candidates = list(
                set(all_candidates) - set(row) - set(column) - set(square))
            if len(candidates) == 1:
                print "CAN ONLY BE", candidates[0]
                board[r][c] = candidates[0]

    return board


def count_unknown(array):
    '''
    Return how many spaces are still unknown (equal to zero)

    Note that this is a simple counter, it is not nearly as strong of a
    considtion as the validate function, which checks a superset of the
    conditions that this function checks
    '''
    return sum(row.count(0) for row in array)


def validate(array):
    '''
    Given an array that represents a sudoku, return True if it is valid
    and False if invalid

    Implicitely, this function is also asserting that there are no elements
    with value equal to zero (unknown), making this a stronger check than
    count_unknown(board) == 0
    '''
    # First, check every row to make sure it contains every int from 1 to 9
    for row in array:
        if not validate_row(row):
            return False

    # Second, check every column for the same
    for i in range(9):
        psuedo_row = [row[i] for row in array]
        if not validate_row(psuedo_row):
            return False

    # Lastly, check every square
    for x in range(3):       # x is columns
        for y in range(3):   # y is rows
            # x and y are the location of the 3x3 square we're considering
            psuedo_row = square_to_psuedo_row(array, x, y)
            if not validate_row(psuedo_row):
                return False

    return True


def column_to_psuedo_row(array, x):
    '''
    Given an array and the index of the column, return a psuedo row that
    contains all the numbers in that column
    '''
    return [row[x] for row in array]


def square_to_psuedo_row(array, x, y):
    '''
    Given an array and the indices of the subsquare within in, return a psuedo
    row that contains the numbers in that box
    '''
    psuedo_row = []
    for i in xrange(3):
        psuedo_row.extend(array[y * 3 + i][x*3:x*3 + 3])
    return psuedo_row


def validate_row(row):
    '''
    given just a row of numbers, return True if it contains all the numbers
    1 through 9
    '''
    # Would it work to pre-can the sum and the product of the elemnts?
    # Are there invalid rows that would give false positives? If it works,
    # would it be a faster way?
    return sorted(row) == SORTED_ROW


def loads(sudoku_string):
    '''
    Convert a sudoku string into a 2d array and return that array
    This is meant to mimic the json library's json.loads function

    If the string cannot be parsed as a sudoku, raise an exception?
    '''
    lines = sudoku_string.strip().split("\n")
    # remove horizontal separators
    lines = lines[0:3] + lines[4:7] + lines[8:11]

    output = []
    for line in lines:
        numbers = line.split(" ")
        # remove vertical separators
        numbers = numbers[0:3] + numbers[4:7] + numbers[8:11]
        numbers = [int(n) for n in numbers]
        output.append(numbers)
    return output


def dumps(sudoku_array):
    '''
    Convert a sudoku array into a pretty string for printing or saving to
    a file. This is meant to mimic the json library's json.dumps function
    '''
    output = []
    for line in sudoku_array:
        line.insert(3, "|")
        line.insert(7, "|")
        output_line = " ".join(str(n) for n in line)
        output.append(output_line)
    output.insert(3, "------+-------+------")
    output.insert(7, "------+-------+------")
    return "\n".join(output)
