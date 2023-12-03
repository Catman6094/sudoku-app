import random
import time
import os
from datetime import datetime

option = -1

solution = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

while option != 0:
    print("0. exit")
    print("1. generate")
    print("2. play")
    print("3. quick play")
    print("4. make pack")
    print("5. play from pack")
    print("6. play daily puzzle (WARNING: hard)")
    print("7. view puzzle")
    print("8. view pack")
    print("9. join discord server")
    option = int(input("Select option: "))

    if option == 1:
        difficulty = 0
        mindifficulty = float(input("Insert minimum difficulty(0.00 - 4.00): "))
        maxdifficulty = float(input("Insert maximum difficulty(0.00 - 4.00): "))

        if mindifficulty <= maxdifficulty and maxdifficulty <= 4:
            difficulty = random.randint(int(mindifficulty * 4), int(maxdifficulty * 4)) / 4
            puzzle = [row[:] for row in solution]  # Create a copy of the solution
            digitsremoved = int(30 + (difficulty * 4))
            lefttoberemoved = digitsremoved

            while lefttoberemoved > 0:
                i = random.randint(0, 8)
                j = random.randint(0, 8)

                if puzzle[i][j] != 0:
                    puzzle[i][j] = 0
                    lefttoberemoved -= 1
                    print("Digits remaining to be removed:", lefttoberemoved)

            print("Generated Sudoku (Difficulty: {:.2f}):".format(difficulty))
            print("+-------+-------+-------+")
            for i, row in enumerate(puzzle):
                if i % 3 == 0 and i != 0:
                    print("+-------+-------+-------+")
                print("| " + " ".join(str(num) if num != 0 else "." for num in row[:3]), end=" ")
                print("| " + " ".join(str(num) if num != 0 else "." for num in row[3:6]), end=" ")
                print("| " + " ".join(str(num) if num != 0 else "." for num in row[6:9]), end=" |\n")
            print("+-------+-------+-------+")

            save_option = input("Do you want to save this Sudoku? (yes/no): ")
            if save_option.lower() == "yes":
                user_input_name = input("Enter a name for the Sudoku: ")
                sudoku_text = f"Difficulty: {difficulty}\n" + "".join("".join(map(str, row)) for row in puzzle)
            
                # Check if the "puzzle" folder exists, if not, create it
                puzzle_folder = "puzzle"
            if not os.path.exists(puzzle_folder):
                os.makedirs(puzzle_folder)
        
            # Save the Sudoku inside the "puzzle" folder
            filename = os.path.join(puzzle_folder, f"{user_input_name}.txt")
            with open(filename, "w") as file:
                file.write(sudoku_text)
        
            print(f"Sudoku '{user_input_name}' saved successfully!")

        else:
            if maxdifficulty > 4:
                print("Error: difficulty", maxdifficulty, "not accepted. Values up to 4.00 are accepted.")
            else:
                print("Error: the maximum difficulty should be above the minimum difficulty")


    elif option == 2:
        sudoku_name = input("Enter the name of the Sudoku (excluding .txt): ")
        filename = f"puzzle/{sudoku_name}.txt"
        
        try:
            with open(filename, "r") as file:
                content = file.readlines()
                difficulty = float(content[0].split(": ")[1])
                sudoku_line = content[1].strip()
    
                puzzle = [[int(sudoku_line[i * 9 + j]) for j in range(9)] for i in range(9)]
    
    
                start_time = time.time()
                # Inside the while loop where you're accepting user input for the Sudoku puzzle
                while True:
                    print(f"Difficulty: {difficulty}")
                    print("+-------+-------+-------+")
                    for i, row in enumerate(puzzle):
                        if i % 3 == 0 and i != 0:
                            print("+-------+-------+-------+")
                        print("| " + " ".join(str(num) if num != 0 else "." for num in row[:3]), end=" ")
                        print("| " + " ".join(str(num) if num != 0 else "." for num in row[3:6]), end=" ")
                        print("| " + " ".join(str(num) if num != 0 else "." for num in row[6:9]) + " |")
                    print("+-------+-------+-------+")
                    user_input = input("Enter cell (e.g., A3), or Q to quit: ").upper()
                    if user_input == 'Q':
                        print("Quitting the puzzle.")
                        break
                
                    # Check if the input is a valid cell position (e.g., A1, B2, etc.)
                    if len(user_input) == 2 and user_input[0].isalpha() and user_input[1].isdigit():
                        row = ord(user_input[0]) - ord('A')
                        col = int(user_input[1]) - 1
                
                        if 0 <= row < 9 and 0 <= col < 9:
                            cell_value = int(input(f"Enter value for {user_input}: "))
                            if cell_value == 0:
                                puzzle[row][col] = 0
                            elif 1 <= cell_value <= 9:
                                puzzle[row][col] = cell_value
                                pass
                            else:
                                print("Invalid cell value! Please enter a number between 1 and 9. Use 0 to erase.")
                        else:
                            print("Invalid cell position! Please enter a valid cell position such as A1, B2, etc.")
                    else:
                        print("Invalid input format! Please enter a valid cell position such as A1, B2, etc.")

                    
                    # Check if the puzzle matches the solution
                    if puzzle == solution:
                        end_time = time.time()
                        total_time = end_time - start_time
                        seconds = total_time
                        minutes = 0
                        while (seconds >= 60):
                            minutes = minutes + 1
                            seconds = seconds - 60
                        print("Congratulations! Sudoku completed.")
                        print(f"Total time taken: {minutes} minutes, {seconds:.2f} seconds")
                        break
    
        except FileNotFoundError:
            print("Sudoku file not found. Please make sure the file exists.")



    elif option == 3:
        mindifficulty = float(input("Insert minimum difficulty(0.00 - 4.00): "))
        maxdifficulty = float(input("Insert maximum difficulty(0.00 - 4.00): "))

        if mindifficulty <= maxdifficulty and maxdifficulty <= 4:
            difficulty = random.randint(int(mindifficulty * 4), int(maxdifficulty * 4)) / 4
            puzzle = [row[:] for row in solution]  # Create a copy of the solution
            digitsremoved = int(30 + (difficulty * 4))
            lefttoberemoved = digitsremoved

            while lefttoberemoved > 0:
                i = random.randint(0, 8)
                j = random.randint(0, 8)

                if puzzle[i][j] != 0:
                    puzzle[i][j] = 0
                    lefttoberemoved -= 1
                    print("Digits remaining to be removed:", lefttoberemoved)

            start_time = time.time()
            while True:
                print(f"Difficulty: {difficulty}")
                print("+-------+-------+-------+")
                for i, row in enumerate(puzzle):
                    if i % 3 == 0 and i != 0:
                        print("+-------+-------+-------+")
                    print("| " + " ".join(str(num) if num != 0 else "." for num in row[:3]), end=" ")
                    print("| " + " ".join(str(num) if num != 0 else "." for num in row[3:6]), end=" ")
                    print("| " + " ".join(str(num) if num != 0 else "." for num in row[6:9]) + " |")
                print("+-------+-------+-------+")
                user_input = input("Enter cell (e.g., A3), or Q to quit: ").upper()
                if user_input == 'Q':
                    print("Quitting the puzzle.")
                    break

                # Check if the input is a valid cell position (e.g., A1, B2, etc.)
                if len(user_input) == 2 and user_input[0].isalpha() and user_input[1].isdigit():
                    row = ord(user_input[0]) - ord('A')
                    col = int(user_input[1]) - 1

                    if 0 <= row < 9 and 0 <= col < 9:
                        cell_value = int(input(f"Enter value for {user_input}: "))
                        if cell_value == 0:
                            puzzle[row][col] = 0
                        elif 1 <= cell_value <= 9:
                            puzzle[row][col] = cell_value
                            pass
                        else:
                            print("Invalid cell value! Please enter a number between 1 and 9. Use 0 to erase.")
                    else:
                        print("Invalid cell position! Please enter a valid cell position such as A1, B2, etc.")
                else:
                    print("Invalid input format! Please enter a valid cell position such as A1, B2, etc.")

                # Check if the puzzle matches the solution
                if puzzle == solution:
                    end_time = time.time()
                    total_time = end_time - start_time
                    seconds = total_time
                    minutes = 0
                    while (seconds >= 60):
                        minutes = minutes + 1
                        seconds = seconds - 60
                    print("Congratulations! Sudoku completed.")
                    print(f"Total time taken: {minutes} minutes, {seconds:.2f} seconds")
                    break

        else:
            if maxdifficulty > 4:
                print("Error: difficulty", maxdifficulty, "not accepted. Values up to 4.00 are accepted.")
            else:
                print("Error: the maximum difficulty should be above the minimum difficulty")


    elif option == 4:  # Code for generating a pack of Sudoku puzzles
        pack_name = input("Enter a name for the pack: ")
        num_puzzles = int(input("Enter the number of puzzles in the pack: "))
        min_difficulty = float(input("Enter the minimum difficulty (0.00 - 4.00): "))
        max_difficulty = float(input("Enter the maximum difficulty (0.00 - 4.00): "))
        sort_choice = input("Do you want the puzzles sorted by difficulty? (yes/no)")
        if (sort_choice.lower() == "yes"):
            difficulties = sorted([random.randint(int(min_difficulty * 4), int(max_difficulty * 4)) / 4 for _ in range(num_puzzles)])
        else:
            difficulties = [random.randint(int(min_difficulty * 4), int(max_difficulty * 4)) / 4 for _ in range(num_puzzles)]

        puzzles_text = ""

        # Generate Sudoku puzzles with specified difficulties
        for level, difficulty in enumerate(difficulties, start=1):
            puzzle = [row[:] for row in solution]
            digits_removed = int(30 + (difficulty * 4))
            left_to_be_removed = digits_removed

            while left_to_be_removed > 0:
                i = random.randint(0, 8)
                j = random.randint(0, 8)

                if puzzle[i][j] != 0:
                    puzzle[i][j] = 0
                    left_to_be_removed -= 1

            # Create the formatted string for Sudoku
            sudoku_text = f"Level: {level} - Difficulty: {difficulty:.2f}\n" + "".join("".join(map(str, row)) for row in puzzle)
            # Simulate best time (replace this logic with actual best times)
            best_time = "Not solved"
            sudoku_text += f"\n{best_time}\n\n"
    
            puzzles_text += sudoku_text

        # Check if the "puzzle" folder exists, if not, create it
        puzzle_folder = "packs"
        if not os.path.exists(puzzle_folder):
            os.makedirs(puzzle_folder)

        # Save all puzzles into a single text file
        filename = os.path.join(puzzle_folder, f"{pack_name}.txt")
        with open(filename, "w") as file:
            file.write(puzzles_text)

        print(f"Pack '{pack_name}' created successfully with {num_puzzles} puzzles.")


        
    elif option == 5:  # Code to play from a pack of Sudoku puzzles
        pack_name = input("Enter the name of the pack: ")
        level_to_play = int(input("Enter the level to play: "))
    
        try:
            # Open the pack file
            pack_filename = f"packs/{pack_name}.txt"
            with open(pack_filename, "r") as pack_file:
                pack_content = pack_file.read().split('\n\n')  # Split puzzles based on the double newline separator
    
                # Check if the specified level exists in the pack
                if level_to_play > len(pack_content):
                    print("Level not found in the pack. Please select a valid level.")
                else:
                    selected_puzzle_details = pack_content[level_to_play - 1].strip().split('\n')
                    difficulty_info = selected_puzzle_details[0]  # Difficulty information
                    sudoku_line = selected_puzzle_details[1]  # Sudoku puzzle representation
    
                    difficulty_info_parts = difficulty_info.split(" - Difficulty: ")
                    level = difficulty_info_parts[0].split(": ")[1]
                    difficulty = float(difficulty_info_parts[1])

                    print(f"Level: {level} - Difficulty: {difficulty:.2f}")
                    print(sudoku_line[:9])  # Display first row separately to format the grid
                    for i in range(9):
                        print(sudoku_line[i * 9:i * 9 + 9])
    
                    # Logic for playing the selected puzzle
                    puzzle = [[int(sudoku_line[i * 9 + j]) for j in range(9)] for i in range(9)]
    
                    start_time = time.time()
                    while True:
                        print(f"Level: {level} - Difficulty: {difficulty:.2f}")
                        print("+-------+-------+-------+")
                        for i, row in enumerate(puzzle):
                            if i % 3 == 0 and i != 0:
                                print("+-------+-------+-------+")
                            print("| " + " ".join(str(num) if num != 0 else "." for num in row[:3]), end=" ")
                            print("| " + " ".join(str(num) if num != 0 else "." for num in row[3:6]), end=" ")
                            print("| " + " ".join(str(num) if num != 0 else "." for num in row[6:9]) + " |")
                        print("+-------+-------+-------+")
                        user_input = input("Enter cell (e.g., A3), or Q to quit: ").upper()
                        if user_input == 'Q':
                            print("Quitting the puzzle.")
                            break
    
                        # Check if the input is a valid cell position (e.g., A1, B2, etc.)
                        if len(user_input) == 2 and user_input[0].isalpha() and user_input[1].isdigit():
                            row = ord(user_input[0]) - ord('A')
                            col = int(user_input[1]) - 1
    
                            if 0 <= row < 9 and 0 <= col < 9:
                                cell_value = int(input(f"Enter value for {user_input}: "))
                                if cell_value == 0:
                                    puzzle[row][col] = 0
                                elif 1 <= cell_value <= 9:
                                    puzzle[row][col] = cell_value
                                    pass
                                else:
                                    print("Invalid cell value! Please enter a number between 1 and 9. Use 0 to erase.")
                            else:
                                print("Invalid cell position! Please enter a valid cell position such as A1, B2, etc.")
                        else:
                            print("Invalid input format! Please enter a valid cell position such as A1, B2, etc.")
    
                        # Check if the puzzle matches the solution
                        if puzzle == solution:
                            end_time = time.time()
                            total_time = end_time - start_time
                            seconds = total_time
                            minutes = 0
                            while seconds >= 60:
                                minutes += 1
                                seconds -= 60
                            print("Congratulations! Sudoku completed.")
                            print(f"Total time taken: {minutes} minutes, {seconds:.2f} seconds")
                            break
    
        except FileNotFoundError:
            print("Pack file not found. Please make sure the file exists.")
    elif option == 6:
        current_date = datetime.now()
        current_date_str = current_date.strftime('%d-%m-%Y')  # Convert datetime object to string
        current_day = datetime.strptime(current_date_str, '%d-%m-%Y')

        # Define the base date (January 1, 2000)
        base_date = datetime(2000, 1, 1)
        # Calculate the difference in days between the input date and the base date
        last_day = (current_date - base_date).days + 1

        day = input("Insert the day, starting from 01-01-2000 (format: dd-mm-yyyy): ")
        daily_puzzle = datetime.strptime(day, '%d-%m-%Y')

        difference = (daily_puzzle - base_date).days + 1

        if difference > last_day:
            print("No playing puzzles in the future! Only past and present dates are allowed.")
        elif difference <= 0:
            print("You've gone too far backwards! The earliest date you can write is 01/01/2000.")
        else:
            seed = difference
            random.seed(seed)
            puzzleID = []
            givens = int(0)
            for i in range(9):
                value = random.randint(0, 511)
                puzzleID.append(value)

            # Convert each number into a binary representation and organize them into a 2D array
            puzzle_grid = []
            for number in puzzleID:
                binary_representation = format(number, '09b')  # Get the binary representation with leading zeros
                binary_row = [int(bit) for bit in binary_representation]
                puzzle_grid.append(binary_row)

            for i in range(len(puzzle_grid)):
                for j in range(len(puzzle_grid[i])):
                    if (puzzle_grid[i][j] == 1):
                        givens+= 1
                    puzzle_grid[i][j] *= solution[i][j]
            
            difficulty = (51 - givens) / 4
            start_time = time.time()
            puzzle = puzzle_grid
            while True:
                print(f"Daily puzzle #{difference} - Difficulty: {difficulty}")
                print("+-------+-------+-------+")
                for i, row in enumerate(puzzle):
                    if i % 3 == 0 and i != 0:
                        print("+-------+-------+-------+")
                    print("| " + " ".join(str(num) if num != 0 else "." for num in row[:3]), end=" ")
                    print("| " + " ".join(str(num) if num != 0 else "." for num in row[3:6]), end=" ")
                    print("| " + " ".join(str(num) if num != 0 else "." for num in row[6:9]) + " |")
                print("+-------+-------+-------+")
                user_input = input("Enter cell (e.g., A3), or Q to quit: ").upper()
                if user_input == 'Q':
                    print("Quitting the puzzle.")
                    break

                # Check if the input is a valid cell position (e.g., A1, B2, etc.)
                if len(user_input) == 2 and user_input[0].isalpha() and user_input[1].isdigit():
                    row = ord(user_input[0]) - ord('A')
                    col = int(user_input[1]) - 1

                    if 0 <= row < 9 and 0 <= col < 9:
                        cell_value = int(input(f"Enter value for {user_input}: "))
                        if cell_value == 0:
                            puzzle[row][col] = 0
                        elif 1 <= cell_value <= 9:
                            puzzle[row][col] = cell_value
                            pass
                        else:
                            print("Invalid cell value! Please enter a number between 1 and 9. Use 0 to erase.")
                    else:
                        print("Invalid cell position! Please enter a valid cell position such as A1, B2, etc.")
                else:
                    print("Invalid input format! Please enter a valid cell position such as A1, B2, etc.")

                # Check if the puzzle matches the solution
                if puzzle == solution:
                    end_time = time.time()
                    total_time = end_time - start_time
                    seconds = total_time
                    minutes = 0
                    while (seconds >= 60):
                        minutes = minutes + 1
                        seconds = seconds - 60
                    print("Congratulations! Sudoku completed.")
                    print(f"Total time taken: {minutes} minutes, {seconds:.2f} seconds")
                    break
    elif option == 7:
        sudoku_name = input("Enter the name of the Sudoku (excluding .txt): ")
        filename = f"puzzle/{sudoku_name}.txt"
        
        try:
            with open(filename, "r") as file:
                content = file.readlines()
                difficulty = float(content[0].split(": ")[1])
                sudoku_line = content[1].strip()
    
                puzzle = [[int(sudoku_line[i * 9 + j]) for j in range(9)] for i in range(9)]
    
    
                start_time = time.time()
                # Inside the while loop where you're accepting user input for the Sudoku puzzle
                print(f"Difficulty: {difficulty}")
                print("+-------+-------+-------+")
                for i, row in enumerate(puzzle):
                    if i % 3 == 0 and i != 0:
                        print("+-------+-------+-------+")
                    print("| " + " ".join(str(num) if num != 0 else "." for num in row[:3]), end=" ")
                    print("| " + " ".join(str(num) if num != 0 else "." for num in row[3:6]), end=" ")
                    print("| " + " ".join(str(num) if num != 0 else "." for num in row[6:9]) + " |")
                print("+-------+-------+-------+")
                wait = input ("Press any key to continue. ")
    
        except FileNotFoundError:
            print("Sudoku file not found. Please make sure the file exists.")
    elif option == 8:
        pack_name = input("Enter the name of the pack: ")
        level_to_play = int(input("Enter the level to view (0 if you want to view all puzzles): "))

        try:
            pack_filename = f"packs/{pack_name}.txt"
            with open(pack_filename, "r") as pack_file:
                pack_content = pack_file.read().split('\n\n')

                if level_to_play > len(pack_content):
                    print("Level not found in the pack. Please select a valid level.")
                else:
                    if level_to_play == 0:
                        for idx, puzzle_details in enumerate(pack_content, start=1):
                            puzzle_info = puzzle_details.strip().split('\n')
                            if len(puzzle_info) >= 2:
                                difficulty_info = puzzle_info[0]
                                sudoku_line = puzzle_info[1]
                                difficulty, puzzle_grid = float(difficulty_info.split(" - Difficulty: ")[1]), []
                                print(f"Level: {idx} - Difficulty: {difficulty:.2f}")
                                for i in range(9):
                                    puzzle_grid.append([int(sudoku_line[i * 9 + j]) for j in range(9)])

                                print("+-------+-------+-------+")
                                for i, row in enumerate(puzzle_grid):
                                    if i % 3 == 0 and i != 0:
                                        print("+-------+-------+-------+")
                                    print("| " + " ".join(str(num) if num != 0 else "." for num in row[:3]), end=" ")
                                    print("| " + " ".join(str(num) if num != 0 else "." for num in row[3:6]), end=" ")
                                    print("| " + " ".join(str(num) if num != 0 else "." for num in row[6:9]) + " |")
                                print("+-------+-------+-------+")
                        wait = input("Press enter to quit: ")
                    else:
                        selected_puzzle_details = pack_content[level_to_play - 1].strip().split('\n')
                        difficulty_info = selected_puzzle_details[0]
                        sudoku_line = selected_puzzle_details[1]

                        difficulty, puzzle_grid = float(difficulty_info.split(" - Difficulty: ")[1]), []
                        for i in range(9):
                            puzzle_grid.append([int(sudoku_line[i * 9 + j]) for j in range(9)])

                        print(f"Level: {level_to_play} - Difficulty: {difficulty:.2f}")
                        print("+-------+-------+-------+")
                        for i, row in enumerate(puzzle_grid):
                            if i % 3 == 0 and i != 0:
                                print("+-------+-------+-------+")
                            print("| " + " ".join(str(num) if num != 0 else "." for num in row[:3]), end=" ")
                            print("| " + " ".join(str(num) if num != 0 else "." for num in row[3:6]), end=" ")
                            print("| " + " ".join(str(num) if num != 0 else "." for num in row[6:9]) + " |")
                        print("+-------+-------+-------+")
                        wait = input("Press enter to quit: ")                        

        except FileNotFoundError:
            print("Pack file not found. Please make sure the file exists.")
    elif option == 9:
        wait = input("Join the discord server with this invite link: https://discord.gg/hYRVtUPgWg\nPress enter to return to the menu.")
