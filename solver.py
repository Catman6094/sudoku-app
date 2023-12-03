def seen_cells(row, col):
    """Get a list of cells seen by (row, col)"""
    seen = set([*[(row, i) for i in range(9) if i != col],
                *[(i, col) for i in range(9) if i != row],
                *[(i, j) for i in range(3*(row//3), 3*(row//3) + 3) for j in range(3*(col//3), 3*(col//3) + 3) if (i, j) != (row, col)]
                ])
    return seen

class MarkedGrid:
    """Grid with pencil marks. Each cell gets a set of it's options"""
    def __init__(self, simple_grid) -> None:
        # Initialize grid
        self.grid = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
        self.solved_cells = set()
        
        # Set all the cells
        for r, row in enumerate(simple_grid):
            for c, digit in enumerate(row):
                if digit != 0: self.set_cell(r, c, digit)
    
    def set_cell(self, row, col, digit):
        self.grid[row][col] = {digit}
        self.solved_cells.add((row, col))
        for r, c in seen_cells(row, col):
            self.remove(r, c, digit)
    
    def remove(self, row, col, digit):
        self.grid[row][col].discard(digit)
    
    def __str__(self) -> str:
        result = "+-----+-----+-----+ +-----+-----+-----+ +-----+-----+-----+\n"
        for row in range(9):
            for d_row in range(3):
                result += '|'
                for col in range(9):
                    for d_col in range(3):
                        d = d_row * 3 + d_col + 1
                        result += str(d) if d in self.grid[row][col] else '.'
                        if d_col != 2: result += ' '
                    result += '|'
                    if col in [2, 5]: result += ' |'
                result += '\n'
            result += "+-----+-----+-----+ +-----+-----+-----+ +-----+-----+-----+\n"
            if row in [2, 5]: result += "+-----+-----+-----+ +-----+-----+-----+ +-----+-----+-----+\n"
        return result

grid = [[0 for _ in range(9)] for _ in range(9)]
grid[0][0] = 1
grid[0][1] = 3
grid[0][2] = 2
grid[4][4] = 7
penciled = MarkedGrid(grid)
print(penciled)