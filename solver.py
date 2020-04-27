# -*- coding: utf-8 -*-
import pycosat

# Find row and column given index and size of grid
def grid(size, index):
    return (index - 1) // size, (index - 1) % size

# Return index of grid variable given row and column
def grid_id(size, row, col):
    if (row >= size or col >= size):
        raise Exception('Row or column out of bounds');
    return row * size + col + 1;

# Find pattern row/col and number given index
def pattern(size, rows, cols, index):
    i = (index - 1) // size - size
    count = 0
    if (i < 0):
        return 'Grid variable'
    for r, row in enumerate(rows):
        n = count + len(row)
        if (i < n):
            return 'Row: %d Pattern: %d Start Column: %d Length: %d' %(r, i - count, (index - 1) % size, rows[r][i - count])
        count = n
    for c, col in enumerate(cols):
        n = count + len(col)
        if (i < n):
            return 'Col: %d Pattern: %d Start Row: %d Length: %d' %(c, i - count, (index - 1) % size, cols[c][i - count])
        count = n
    return 'Not pattern variable'

# Assign id to each pattern
def pattern_id(size, rows, cols):
    rows_id = []
    cols_id = []
    count = size * size + 1
    for row in rows:
        row_id = []
        for pat in row:
            row_id.append(count)
            count += size
        rows_id.append(row_id)
    for col in cols:
        col_id = []
        for pat in col:
            col_id.append(count)
            count += size
        cols_id.append(col_id)
    return rows_id, cols_id

# Read puzzle
def read(fname):
    f = open(fname)
    l = [[int(i) for i in line.split()] for line in f]
    size = len(l) // 2
    for line in l:
        for pat in line:
            if (pat <= 0 or pat > size):
                raise Exception('Pattern out of bounds at line: ' + str(line))
    return size, l[:size], l[size:]

# Compute possible index range for all patterns
def pattern_range(size, rows, cols):
    rows_range = []
    cols_range = []
    for row in rows:
        l = len(row)
        count = 0
        lower = [0 for _ in range(l)]
        for i in range(l):
            lower[i] = count;
            count += row[i] + 1
        count = size
        upper = [0 for _ in range(l)]
        for i in range(l-1, -1, -1):
            count -= row[i] + 1
            upper[i] = count + 2;
            
        rows_range.append([(lower[i], upper[i]) for i in range(l)])
    for col in cols:
        l = len(col)
        count = 0
        lower = [0 for _ in range(l)]
        for i in range(l):
            lower[i] = count;
            count += col[i] + 1
        count = size
        upper = [0 for _ in range(l)]
        for i in range(l-1, -1, -1):
            count -= col[i] + 1
            upper[i] = count + 2;
            
        cols_range.append([(lower[i], upper[i]) for i in range(l)])
    return rows_range, cols_range
            
# A pattern implies all corresponding cells are shaded
def pattern_shade(size, rows, cols, rows_range, cols_range, rows_id, cols_id):
    clauses = []
    for r, row in enumerate(rows):
        for p in range(len(row)):
            pat_len = rows[r][p]
            pat_id = rows_id[r][p]
            lower, upper = rows_range[r][p]
            for start in range(lower, upper):
                for c in range(start, start + pat_len):
                    clauses.append([-(pat_id + start), grid_id(size, r, c)])
    for c, col in enumerate(cols):
        for p in range(len(col)):
            pat_len = cols[c][p]
            pat_id = cols_id[c][p]
            lower, upper = cols_range[c][p]
            for start in range(lower, upper):
                for r in range(start, start + pat_len):
                    clauses.append([-(pat_id + start), grid_id(size, r, c)])
    return clauses

# A shaded cell implies there exists a pattern that covers it
def cell_shade(size, rows, cols, rows_range, cols_range, rows_id, cols_id):
    clauses = []
    for r in range(size):
        for c in range(size):
            clause = [-grid_id(size, r, c)]
            for p in range(len(rows[r])):
                pat_len = rows[r][p]
                pat_id = rows_id[r][p]
                lower, upper = rows_range[r][p]
                for start in range(max(c-pat_len+1, lower), min(c+1, upper)):
                    clause.append(pat_id + start)
            clauses.append(clause)
            clause = [-grid_id(size, r, c)]
            for p in range(len(cols[c])):
                pat_len = cols[c][p]
                pat_id = cols_id[c][p]
                lower, upper = cols_range[c][p]
                for start in range(max(r-pat_len+1, lower), min(r+1, upper)):
                    clause.append(pat_id + start)
            clauses.append(clause)
    return clauses

# A pattern means following patterns come after it
def pattern_order(size, rows, cols, rows_range, cols_range, rows_id, cols_id):
    clauses = []
    for r, row in enumerate(rows):
        for p in range(len(row) - 1):
            pat_len = rows[r][p]
            pat_id = rows_id[r][p]
            npat_id = rows_id[r][p+1]
            lower, upper = rows_range[r][p]
            nlower, nupper = rows_range[r][p+1]
            for start in range(lower, upper):
                for nstart in range(nlower, min(start + pat_len + 1, nupper)):
                    clauses.append([-(pat_id + start), -(npat_id + nstart)])
    for c, col in enumerate(cols):
        for p in range(len(col) - 1):
            pat_len = cols[c][p]
            pat_id = cols_id[c][p]
            npat_id = cols_id[c][p+1]
            lower, upper = cols_range[c][p]
            nlower, nupper = cols_range[c][p+1]
            for start in range(lower, upper):
                for nstart in range(nlower, min(start + pat_len + 1, nupper)):
                    clauses.append([-(pat_id + start), -(npat_id + nstart)])
    return clauses

# A pattern exists in at least its possible locations
def pattern_atleast_one(size, rows, cols, rows_range, cols_range, rows_id, cols_id):
    clauses = []
    for r, row in enumerate(rows):
        for p in range(len(row)):
            pat_id = rows_id[r][p]
            lower, upper = rows_range[r][p]
            clauses.append([pat_id + i for i in range(lower, upper)])
            
    for c, col in enumerate(cols):
        for p in range(len(col)):
            pat_id = cols_id[c][p]
            lower, upper = cols_range[c][p]
            clauses.append([pat_id + i for i in range(lower, upper)])
    return clauses

# A pattern exists in at most its possible locations
def pattern_atmost_one(size, rows, cols, rows_range, cols_range, rows_id, cols_id):
    clauses = []
    for r, row in enumerate(rows):
        for p in range(len(row)):
            pat_id = rows_id[r][p]
            lower, upper = rows_range[r][p]
            for i in range(lower, upper-1):
                for j in range(i+1, upper):
                    clauses.append([-(pat_id + i), -(pat_id + j)])          
    for c, col in enumerate(cols):
        for p in range(len(col)):
            pat_id = cols_id[c][p]
            lower, upper = cols_range[c][p]
            for i in range(lower, upper-1):
                for j in range(i+1, upper):
                    clauses.append([-(pat_id + i), -(pat_id + j)])
    return clauses

# Solve nonogram given filename
def solve(size, rows, cols):
    rows_range, cols_range = pattern_range(size, rows, cols)
    rows_id, cols_id = pattern_id(size, rows, cols)
    clauses = []
    clauses += pattern_shade(size, rows, cols, rows_range, cols_range, rows_id, cols_id)
    clauses += cell_shade(size, rows, cols, rows_range, cols_range, rows_id, cols_id)
    clauses += pattern_order(size, rows, cols, rows_range, cols_range, rows_id, cols_id)
    clauses += pattern_atleast_one(size, rows, cols, rows_range, cols_range, rows_id, cols_id)
    clauses += pattern_atmost_one(size, rows, cols, rows_range, cols_range, rows_id, cols_id)
    literals = pycosat.solve(clauses)
    solved_grid = [[0] * size for _ in range(size)]
    if (literals == 'UNSAT'):
        print('Impossible puzzle')
        return solved_grid
    num = size * size
    for i in literals:
        if (i > 0 and i <= num):
            row, col = grid(size, i)
            solved_grid[row][col] = 1
    return solved_grid

def pretty_print(l):
    for line in l:
        print(line)
        
def grid_print(solved_grid):
    for line in solved_grid:
        print('|', end='')
        for i in line:
            if i == 1:
                print('O', end='')
            else:
                print(' ', end='')
            print('|', end='')
        print()
        
def test(solved_grid, size, rows, cols):
    for r, row in enumerate(rows):
        count = 0
        num_pat = len(row)
        i = 0
        for c in range(size+1):
            if (c == size or solved_grid[r][c] == 0):
                if (count > 0):
                    if (i >= num_pat or count != rows[r][i]):
                        raise Exception('Row %d Pattern %d mismatch' %(r, i))
                    count = 0
                    i += 1
            else:
                count += 1
    for c, col in enumerate(cols):
        count = 0
        num_pat = len(col)
        i = 0
        for r in range(size+1):
            if (r == size or solved_grid[r][c] == 0):
                if (count > 0):
                    if (i >= num_pat or count != cols[c][i]):
                        raise Exception('Column %d Pattern %d mismatch' %(c, i))
                    count = 0
                    i += 1
            else:
                count += 1
    return True
