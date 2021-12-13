class BattleShip:
    def __init__(self, canDisplayColor):
        self.c = self.Colors()
        self.canDisplayColor = canDisplayColor
        
        self.board = [[0 for y in range(8)] for x in range(8)]
        self.ships = self._get_ship_locations()
        self.hitPoints = 5 + 4 + 3 + 3 + 2

        self.enemyBoard = [[0 for y in range(8)] for x in range(8)]
        self.enemyHitPoints = 5 + 4 + 3 + 3 + 2

    class Colors:
        def __init__(self):            
            self.GREEN = '\033[92m'
            self.OKBLUE = '\033[94m'
            self.MAGENTA = '\033[95m'
            self.WHITEHIGHLIGHT = '\033[47m'
            self.BLACK = '\033[30m'
            self.WHITE = '\033[29m'
            self.BLUEHIGHLIGHT = '\033[44m'
            self.GREENHIGHLIGHT = '\033[42m'
            self.REDHIGHLIGHT = '\033[41m'
            self.CYANHIGHLIGHT = '\033[46m'
            self.OKCYAN = '\033[96m'
            self.WARNING = '\033[93m'
            self.FAIL = '\033[91m'
            self.GREY = '\033[90m'
            self.ENDC = '\033[0m'
            self.NEGATIVE1 = '\033[3m'

    def _get_ship_locations(self):
        # Ask if they want to place the ship horizontally or vertically
        shipInfo = [["Carrier", 5], ["Battleship", 4], ["Destroyer", 3], ["Submarine", 3], ["Patrol_Boat", 2]]
        ships = {}
        validPlacement = False

        for ship in shipInfo:
            shipName = ship[0]
            shipSize = ship[1]

            # Display the board
            if self.canDisplayColor:
                self._show_your_colored_board()
            else:
                self._show_your_board()


            while not validPlacement:
                shipLayout = input(f"Do you want to place your {shipName} of size {shipSize} horizontally or vertically? (h/v) ")
                position = input(f"Ships will be place from the left-most part or the top-most part.\nWhere do you want to place your {shipName}? (eg., a1) ")
                
                try:
                    position = self._position_decoder(position)
                    ships[shipName] = [position, shipLayout, shipSize]
                    validPlacement = self._can_place_ship(ships, shipName)

                except Exception:
                    validPlacement = False

                if validPlacement:
                    print(ships[shipName])
                    self._place_ship(ships[shipName])
                    print(f"Your {shipName} has been placed.\n")
                else:
                    print(f"Not a valid move. Please pick a different spot to place your {shipName}")

            validPlacement = False

        return ships
    
    def _get_range(self, ship):
        shipRange = None
        startPos = ship[0]
        if ship[1] == "v":
            start = startPos[0]
            end = start + ship[2]
            shipRange = [(row, startPos[1]) for row in range(start, end)]
        else:
            start = startPos[1]
            end = start + ship[2]
            shipRange = [(startPos[0], col) for col in range(start, end)]
        return shipRange

    def _place_ship(self, ship):
        shipRange = self._get_range(ship)
        for pos in shipRange:
            self.board[pos[0]][pos[1]] = 1
        
    
    def _can_place_ship(self, ships, name):
        if self._is_off_map(ships[name]):
            print(f"cannot place ship because it is off of the map.\n")
            return False
        
        for shipName, value in ships.items():
            ship = value
            if shipName != name:
                newShip = ships[name]

                if self._position_crossover(newShip, ship):
                    print(f"cannot place ship because there is a crossover.")
                    print(self._get_range(newShip), self._get_range(ship))
                    print()
                    return False
                    
        
        return True

    def _position_decoder(self, position):
        letterPos = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        row = int(letterPos[position[0]])
        col = int(position[1])
        
        return (row, col)
    
    def _position_crossover(self, ship1, ship2):

        ship1Range = self._get_range(ship1)
        ship2Range = self._get_range(ship2)

        for pos in ship1Range:
            if pos in ship2Range:
                print(pos, ship2Range)
                return True
        
        return False
        
    def _is_off_map(self, ship):
        pos = ship[0]
        size = ship[2]
        if ship[1] == "v":
            if pos[0] + size > 8 or pos[0] < 0:
                return True
        else:
            if pos[1] + size > 8 or pos[1] < 0:
                return True
        
        return False

        
    def _show_your_colored_board(self):
        newBoard = list(row[:] for row in self.board)
        sidePos = ["a","b","c","d","e","f","g","h"]
        
        # Show the horizontal numbers for the boards coordinates
        for num in range(len(self.board)):
            if num == 0:
                print(f"   {num}", end="")
            else:
                print(f"  {num}", end="")
        print()

        for y in range(len(newBoard)):
            for x in range(len(newBoard[y])):
                if newBoard[y][x] == 0:
                    newBoard[y][x] = self.c.BLUEHIGHLIGHT + self.c.BLACK + " 0 " + self.c.ENDC
                elif newBoard[y][x] == 1:
                    newBoard[y][x] = self.c.GREENHIGHLIGHT + self.c.BLACK + " 1 " + self.c.ENDC
                elif newBoard[y][x] == 2:
                    newBoard[y][x] = self.c.REDHIGHLIGHT + self.c.BLACK + " X " + self.c.ENDC
                elif newBoard[y][x] == 3:
                    newBoard[y][x] = self.c.CYANHIGHLIGHT + self.c.BLACK + " - " + self.c.ENDC

        for i in range(len(newBoard)):
            row = newBoard[i]
            line = sidePos[i] + " "
            for index in range(len(row)):
                line += f"{row[index]}"

            print(line)        
    
        
    def _show_enemy_colored_board(self):
        newBoard = list(row[:] for row in self.enemyBoard)
        sidePos = ["a","b","c","d","e","f","g","h"]
        
        # Show the horizontal numbers for the boards coordinates
        for num in range(len(self.board)):
            if num == 0:
                print(f"   {num}", end="")
            else:
                print(f"  {num}", end="")
        print()

        for y in range(len(newBoard)):
            for x in range(len(newBoard[y])):
                if newBoard[y][x] == 0:
                    newBoard[y][x] = self.c.CYANHIGHLIGHT + self.c.BLACK + " 0 " + self.c.ENDC
                elif newBoard[y][x] == 1:
                    newBoard[y][x] = self.c.CYANHIGHLIGHT + self.c.BLACK + " 0 " + self.c.ENDC
                elif newBoard[y][x] == 2:
                    newBoard[y][x] = self.c.REDHIGHLIGHT + self.c.BLACK + " X " + self.c.ENDC
                elif newBoard[y][x] == 3:
                    newBoard[y][x] = self.c.BLUEHIGHLIGHT + self.c.BLACK + " - " + self.c.ENDC

        for i in range(len(newBoard)):
            row = newBoard[i]
            line = sidePos[i] + " "
            for index in range(len(row)):
                line += f"{row[index]}"

            print(line)        

    def _show_your_board(self):
        newBoard = list(row[:] for row in self.board)
        sidePos = ["a","b","c","d","e","f","g","h"]
        
        # Show the horizontal numbers for the boards coordinates
        for num in range(len(self.board)):
            if num == 0:
                print(f"   {num}", end="")
            else:
                print(f"  {num}", end="")
        print()
        
        for y in range(len(newBoard)):
            for x in range(len(newBoard[y])):
                if newBoard[y][x] == 0:
                    newBoard[y][x] = " 0 "
                elif newBoard[y][x] == 1:
                    newBoard[y][x] = " 1 "
                elif newBoard[y][x] == 2:
                    newBoard[y][x] = " X "
                elif newBoard[y][x] == 3:
                    newBoard[y][x] = " - "

        for i in range(len(newBoard)):
            row = newBoard[i]
            line = sidePos[i] + " "
            for index in range(len(row)):
                line += f"{row[index]}"

            print(line) 
            
    def _show_enemy_board(self):
        newBoard = list(row[:] for row in self.enemyBoard)
        sidePos = ["a","b","c","d","e","f","g","h"]
        
        # Show the horizontal numbers for the boards coordinates
        for num in range(len(self.board)):
            if num == 0:
                print(f"   {num}", end="")
            else:
                print(f"  {num}", end="")
        print()
        
        for y in range(len(newBoard)):
            for x in range(len(newBoard[y])):
                if newBoard[y][x] == 0:
                    newBoard[y][x] = " 0 "
                elif newBoard[y][x] == 1:
                    newBoard[y][x] = " 0 "
                elif newBoard[y][x] == 2:
                    newBoard[y][x] = " X "
                elif newBoard[y][x] == 3:
                    newBoard[y][x] = " - "

        for i in range(len(newBoard)):
            row = newBoard[i]
            line = sidePos[i] + " "
            for index in range(len(row)):
                line += f"{row[index]}"

            print(line) 

    def display_board(self):
        # Display your board
        print(f"YOUR BOARD:\n")
        self._show_your_board()

        # Display your view of enemies board
        print(f"\nENEMY BOARD:\n")
        self._show_enemy_board()

    def display_board_colored(self):
        # Display your board
        print(f"{self.c.OKBLUE}YOUR BOARD:{self.c.ENDC}\n")
        self._show_your_colored_board()

        # Display your view of enemies board
        print(f"\n{self.c.FAIL}ENEMY BOARD:{self.c.ENDC}\n")
        self._show_enemy_colored_board()


    def load_enemy_pos(self, enemyShipsPosStr):
        enemyShips = enemyShipsPosStr.split(" ")
        enemyShipsPos = []
        for pos in enemyShips:
            enemyShipsPos.append(pos.split(","))

        for pos in enemyShipsPos:
            row = int(pos[0])
            col = int(pos[1])
            self.enemyBoard[row][col] = 1

    def send_ships_pos(self):
        yourShipsPos = ""
        for name, data in self.ships.items():
            for pos in self._get_range(data):
                yourShipsPos += f"{pos[0]},{pos[1]} "

        return yourShipsPos[:len(yourShipsPos)-1]

    def fire_on_enemy(self, pos):
        pos = self._position_decoder(pos)
        row = pos[0]
        col = pos[1]
        if self.enemyBoard[row][col] == 1:
            # The enemy is hit, track their lost point
            print("DIRECT HIT!\n")
            self.enemyBoard[row][col] = 2
            self.enemyHitPoints -= 1
        
        elif self.enemyBoard[row][col] == 2 or self.enemyBoard[row][col] == 3:
            print("The definition of insanity is trying the same thing again \nand again and expecting different results.\n")
        
        else:
            print("I'm sorry, you missed, but I'm sure your enemy is happy...\n")
            self.enemyBoard[row][col] = 3
    
    def recieve_fire(self, pos):
        pos = self._position_decoder(pos)
        row = pos[0]
        col = pos[1]
        if self.board[row][col] == 1:
            # You are hit, track your lost point
            print("YOU'VE BEEN HIT!\n")
            self.board[row][col] = 2
            self.hitPoints -= 1
        
        elif self.board[row][col] == 2 or self.board[row][col] == 3:
            print("Now's your chance, your enemy waisted a theirs!\n")
        
        else:
            print("Yahoo they missed!\n")
            self.board[row][col] = 3
    
    def has_lost(self):
        return self.hitPoints <= 0

    def has_won(self):
        return self.enemyHitPoints <= 0

    def reset(self):
        self.board = [[0 for y in range(8)] for x in range(8)]
        self.ships = self._get_ship_locations()
        self.hitPoints = 5 + 4 + 3 + 3 + 2

        self.enemyBoard = [[0 for y in range(8)] for x in range(8)]
        self.enemyHitPoints = 5 + 4 + 3 + 3 + 2

