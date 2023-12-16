BOX = [{27*r+3*c + 9*i+j for i in range(3) for j in range(3)} for r in range(3) for c in range(3)]
ROW = [{9*r + c for c in range(9)} for r in range(9)]
COL = [{9*r + c for r in range(9)} for c in range(9)]


def other_box_cells(cell):
    corner = cell-cell%27 + cell%9-cell%3
    return {corner + i + 9*j for i in range(3) for j in range(3) if corner + i + 9*j != cell}

def other_row_cells(cell):
    return {i for i in range(cell - cell % 9, cell - cell % 9 + 9) if i != cell}

def other_col_cells(cell):
    return {i for i in range(cell % 9, cell % 9 + 81, 9) if i != cell}

def seen_cells(cell):
    """Get a list of cells seen by (row, col)"""
    seen = set([*other_row_cells(cell),
                *other_col_cells(cell),
                *other_box_cells(cell)
                ])
    return seen

class MarkedGrid:
    """Grid with pencil marks. Each cell gets a set of it's options"""
    def __init__(self, simple_grid) -> None:
        # Initialize grid
        self.grid = [set(range(1, 10)) for _ in range(81)]
        self.solved_cells = set()
        
        
        # Set the initial cells
        for cell, digit in enumerate(simple_grid):
            if digit != 0: self.set_cell(cell, digit)
    
    def set_cell(self, cell, digit):
        """Place a digit in a cell and remove candidates from seen cells"""
        self.grid[cell] = {digit}
        self.solved_cells.add(cell)
        for c in seen_cells(cell):
            self.remove(c, digit)
    
    def remove(self, cell, digit):
        self.grid[cell].discard(digit)
    
    def find_step(self):
        # Hidden single
        result = self.find_hidden_single()
        if result is not None:
            info, cell, digit = result
            self.apply_hidden_single(cell, digit)
            return ("HIDDEN SINGLE", info, cell, digit)
        
        # Naked single
        result = self.find_naked_single()
        if result is not None:
            cell, digit = result
            self.apply_hidden_single(cell, digit)
            return ("NAKED SINGLE", cell, digit)
        
        return None
        
    
    def find_hidden_single(self):
        # Boxes first
        for digit in range(1, 10):
            for box in range(9):
                cells_with_digit = [c for c in BOX[box] if c not in self.solved_cells and digit in self.grid[c]]
                if len(cells_with_digit) == 1:
                    return (f"BOX {box+1}", cells_with_digit[0], digit)
        
        # Rows and columns
        for digit in range(1, 10):
            for row in range(9):
                cells_with_digit = [c for c in ROW[row] if c not in self.solved_cells and digit in self.grid[c]]
                if len(cells_with_digit) == 1:
                    return (f"ROW {row+1}", cells_with_digit[0], digit)
            for col in range(9):
                cells_with_digit = [c for c in COL[col] if c not in self.solved_cells and digit in self.grid[c]]
                if len(cells_with_digit) == 1:
                    return (f"COL {col+1}", cells_with_digit[0], digit)
        return None
    
    def apply_hidden_single(self, cell, digit):
        self.set_cell(cell, digit)
    
    def find_naked_single(self):
        cell = 0
        while True:
            while cell in self.solved_cells: cell += 1
            if cell > 80: break
            if len(self.grid[cell]) == 1:
                (digit,) = self.grid[cell]
                self._last_naked_single = cell
                return (cell, digit)
            cell += 1
        return None

    def apply_naked_single(self, cell, digit):
        self.set_cell(cell, digit)
        
    
    def __str__(self) -> str:
        result = "+---------+---------+---------+ +---------+---------+---------+ +---------+---------+---------+\n"
        for row in range(9):
            result += '|'
            for col in range(9):
                cell = 9*row + col
                if cell in self.solved_cells:
                    result += f'   ({next(iter(self.grid[cell]))})   '
                else:
                    result += f"{''.join(map(str, sorted(self.grid[cell]))):^9}"
                result += '|'
                if col in [2, 5]: result += ' |'
            result += '\n'
            result += "+---------+---------+---------+ +---------+---------+---------+ +---------+---------+---------+\n"
            if row in [2, 5]: result += "+---------+---------+---------+ +---------+---------+---------+ +---------+---------+---------+\n"
        return result

grid = [0,3,4,6,7,0,0,0,0,
        6,0,0,1,9,0,0,0,0,
        0,9,8,3,4,2,0,0,0,
        8,5,0,0,0,1,4,2,3,
        4,0,0,8,0,3,7,0,0,
        0,1,3,0,2,0,0,5,6,
        9,0,0,0,3,0,0,8,4,
        0,0,0,4,1,0,6,3,5,
        3,4,5,0,8,6,0,7,9]

penciled = MarkedGrid(grid)
print(penciled)

while True:
    step = penciled.find_step()
    if step is None: break
    print(step)

print(penciled)