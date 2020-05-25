#this needs to be converted into a function, accepting some params like size or style

def region(row_i, row_f, col_i, col_f):
    for row in range(row_i, row_f + 1):
        for col in range(col_i, col_f + 1):
            yield row, col

def create_grid_coords(size=1):
    coords = set()
    for x, y in region(-size, size, -size, size):
        if abs(x) + abs(y) <= size:
            coords.add((x, y))

    return coords
