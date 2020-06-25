import pygame
import pygame.freetype

#Stałe
empty = 0
# Definicje kolorów
black = (0, 0, 0)
white = (255, 255, 255)
grey = (128, 128, 128)
gold = (255, 215, 0)
d_gold = (245, 205, 0)

class Pieces:
    def __init__(self):
        self._friendly = {'pawn': 1, 'king': 3}
        self._enemy = {'pawn': 2, 'king': 4}

    def getFrendly(self):
        return self._friendly

    def getEnemy(self):
        return self._enemy

    def place_starting_pieces(self, board):
        # Początkowe ustawienie pionków
        # Poczatkowe ustawienie czerwonych pionków
        for row in range(5, 8, 2):
            for column in range(0, 8, 2):
                board[row][column] = self._friendly['pawn']
        for row in range(6, 7):
            for column in range(1, 8, 2):
                board[row][column] = self._friendly['pawn']
        # Poczatkowe ustawienie czarnych pionków
        for row in range(0, 3, 2):
            for column in range(1, 8, 2):
                board[row][column] = self._enemy['pawn']
        for row in range(1, 2):
            for column in range(0, 8, 2):
                board[row][column] = self._enemy['pawn']

    def is_valid_selection(self, board, current_player, old_x, old_y):
        # Uniemożliwienie graczowi wyboru złego pionka, lub żadnego pionka
        board_selection = board[old_y][old_x]
        if board_selection == self._friendly['pawn'] or self._friendly['king']:
            return True
        elif board_selection == self._enemy['pawn'] or self._enemy['king']:
            print("To pionek przeciwnika, wybierz swój pionek")
            return False
        else:
            print("Nie wybrałeś żadnego pionka")
            return False

    def is_valid_move(self, current_player, board, old_x, old_y, new_x, new_y):
        # Logika poriszanie sie pionków
        # Zapobienie postawienia dwóch pionków na jednym polu.
        if board[new_y][new_x] != empty:
            print("Nie możesz stać na pionku przeciwnika")
            return False

        # Sprawdzenie możliwych ruchów dla pierwszego gracza
        if board[old_y][old_x] == 1:
            if (new_y - old_y) == -1 and (new_x - old_x) == 1:
                return True
            elif (new_y - old_y) == -1 and (new_x - old_x) == -1:
                return True
            # Sprawdzenie możliwych skoków dla pierwszego gracza
            elif (new_y - old_y) == -2 and (new_x - old_x) == 2:
                if board[new_y + 1][new_x - 1] == enemy['pawn'] or enemy['king']:
                    board[new_y + 1][new_x - 1] = empty
                    return True
                else:
                    return False
            elif (new_y - old_y) == -2 and (new_x - old_x) == -2:
                if board[new_y + 1][new_x + 1] == enemy['pawn'] or enemy['king']:
                    board[new_y + 1][new_x + 1] = empty
                    return True
                else:
                    return False
                
        # Sprawdzenie możliwych ruchów dla drugiego gracza
        elif board[old_y][old_x] == 2:
            if (new_y - old_y) == 1 and (new_x - old_x) == 1:
                return True
            elif (new_y - old_y) == 1 and (new_x - old_x) == -1:
                return True
            # Sprawdzenie możliwych skoków dla drugiego gracza
            elif (new_y - old_y) == 2 and (new_x - old_x) == 2:
                if board[new_y - 1][new_x - 1] == enemy['pawn'] or enemy['king']:
                    board[new_y - 1][new_x - 1] = empty
                    return True
                else:
                    return False
            elif (new_y - old_y) == 2 and (new_x - old_x) == -2:
                if board[new_y - 1][new_x + 1] == enemy['pawn'] or enemy['king']:
                    board[new_y - 1][new_x + 1] = empty
                    return True
                else:
                    return False
            else:
                print("Nie możesz ruszyć się o tyle pól")
                return False

    def no_chips_between(self, board, old_x, old_y, new_x, new_y):
        # Zapobieganie Damce(ang. king) przeskoczenia kilku pionów na raz
        board_y_coords = []
        board_x_coords = []
        if old_y < new_y:
            for row in range(old_y, new_y):
                board_y_coords.append(row)
        if old_y > new_y:
            for row in range(old_y, new_y, -1):
                board_y_coords.append(row)
        if old_x < new_x:
            for column in range(old_x, new_x):
                board_x_coords.append(column)
        if old_x > new_x:
            for column in range(old_x, new_x, -1):
                board_x_coords.append(column)

        board_coords = list(zip(board_x_coords, board_y_coords))
        board_values = [board[y][x] for x, y in board_coords]
        if len(board_values) > 2:
            if all(i == empty for i in board_values[1:-1]) is True:
                board[new_y][new_x] = board[old_y][old_x]
                board[old_y][old_x] = empty
                return True
                    
        # Pozwala damce "skakać" tuż obok pionków przeciwnika
        if len(board_values) == 2:
            if all(i == enemy['pawn'] for i in board_values[1:]) is True:
                board[new_y][new_x] = board[old_y][old_x]
                board[old_y][old_x] = empty
                return True
            elif all(i == enemy['king'] for i in board_values[1:]) is True:
                board[new_y][new_x] = board[old_y][old_x]
                board[old_y][old_x] = empty
                return True
            elif all(i == empty for i in board_values[1:]) is True:
                board[new_y][new_x] = board[old_y][old_x]
                board[old_y][old_x] = empty
                return True

        # Pozwala damce poruszyć się jedno pole do przodu
        elif len(board_values) == 1:
            if all(i == empty for i in board_values[1:]) is True:
                board[new_y][new_x] = board[old_y][old_x]
                board[old_y][old_x] = empty
                return True
        else:
            print("Nie możesz przeskoczyć kilku pionów na raz")
            return False

    def is_valid_king_move(self, current_player, board, old_x, old_y, new_x, new_y):
        # Logika dla Damek (ang. king)
        # Zaobieganie przed skoczeniem na zajęte pole
        if board[new_y][new_x] != 0:
            print("Na tym polu już jest pion")
            return False
        # Zapobieganie ruchom pionowym i poziomym
        if (new_y == old_y or new_x == old_x):
            print("Możesz poruszać się tylko po skosach")
            return False
        # Zapobieganie ruchom w tył(?)
        if new_x > old_x and new_y > old_y:
            if (new_x - old_x) != (new_y - old_y):
                return False
        if new_x < old_x and new_y < old_y:
            if (old_x - new_x) != (old_y - new_y):
                return False
        if new_x < old_x and new_y > old_y:
            if (old_x - new_x) != (new_y - old_y):
                return False
        if new_x > old_x and new_y < old_y:
            if (new_x - old_x) != (old_y - new_y):
                return False

            # Logika skoków Damki
            if board[old_y][old_x] == friendly['king']:
                try: 
                    if board[new_y + 1][new_x - 1] == enemy['pawn'] or enemy['king']:
                        if old_x < new_x and old_y > new_y:
                            if self.no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                                board[new_y][new_x] = friendly['king']
                                board[new_y + 1][new_x - 1] = empty
                                board_selection = empty
                                return True
                except IndexError:
                    pass
                try: 
                    if board[new_y + 1][new_x + 1] == enemy['pawn'] or enemy['king']:
                        if old_x > new_x and old_y > new_y:
                            if self.no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                                board[new_y][new_x] = friendly['king']
                                board[new_y + 1][new_x + 1] = empty
                                board_selection = empty
                                return True
                except IndexError:
                    pass
                try:
                    if board[new_y - 1][new_x - 1] == enemy['pawn'] or enemy['king']:
                        if self.no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                            if old_x < new_x and old_y < new_y:
                                board[new_y][new_x] = friendly['king']
                                board[new_y - 1][new_x - 1] = empty
                                board_selection = empty
                                return True
                except IndexError:
                    pass
                try: 
                    if board[new_y - 1][new_x + 1] == enemy['pawn'] or enemy['pawn']:
                        if self.no_chips_between(board, old_x, old_y, new_x, new_y) is True:
                            if old_x > new_x and old_y < new_y:
                                board[new_y][new_x] = friendly['king']
                                board[new_y - 1][new_x + 1] = empty
                                board_selection = empty
                                return True
                except IndexError:
                    pass


    def check_if_double_jump_possible(self, board, new_x, new_y):
        # Sprawdzanie możliwych skokow
        if current_player == 1:
            try:
                if board[new_y - 2][new_x + 2] == empty:
                    if board[new_y - 1][new_x + 1] == enemy['pawn'] or enemy['king']:
                        return True
                elif board[new_y - 2][new_x - 2] == empty:
                    if board[new_y - 1][new_x + 1] == enemy['pawn'] or enemy['king']:
                        return True
            except IndexError:
                pass
        if current_player == 2:
            try:
                if board[new_y + 2][new_x + 2] == empty:
                    if board[new_y - 1][new_x + 1] == enemy['pawn'] or enemy['king']:
                        return True
                elif board[new_y + 2][new_x - 2] == empty:
                    if board[new_y - 1][new_x + 1] == enemy['pawn'] or enemy['king']:
                        return True
            except IndexError:
                pass
        # Sprawdzanie czy podwójny skok jest możliwy
        if board[new_y][new_x] == friendly['king']:
            try:
                for i in range(8):
                    if board[new_y - i][new_x + i] == enemy['king']:
                        if board[new_y - (i+1)][new_x + (i+1)] == empty:
                            return True
                    elif board[new_y - i][new_x - i] == enemy['king']:
                        if board[new_y - (i+1)][new_x - (i+1)] == empty:
                            return True
                    elif board[new_y + i][new_x + i] ==  enemy['king']:
                        if board[new_y + (i+1)][new_x + (i+1)] == empty:
                            return True
                    elif board[new_y + i][new_x - i] == enemy['king']:
                        if board[new_y + (i+1)][new_x - (i+1)] == empty:
                            return True
            except IndexError:
                pass
        else:
            return False

    def check_for_win(self, current_player, board):
        remaining_enemy_pieces = []
        for row in board:
            remaining_enemy_pieces.append(row.count(enemy['pawn']))
            remaining_enemy_pieces.append(row.count(enemy['king']))
        if sum(remaining_enemy_pieces) == 0:
            print(f"Player {current_player} has won!")
            return True

class Window:
    def __init__(self):
        self._width = 800
        self._height = 700
        self._size = [self._width, self._height]
    
    def getSize(self):
        return self._size

    def getWidth(self):
        return self._width
    
    def getHeight(self):
        return self._height

class BoardWindow(Window):
    def __init__(self):
        self._width = 600
        self._height = 600
        self._size = [self._width, self._height]
    
    def getSize(self):
        return self._size

    def getWidth(self):
        return self._width
    
    def getHeight(self):
        return self._height

class Board:  
    def __init__(self, offsetX, offsetY):
        self._rows = 8
        self._columns = 8
        self._board = [[empty for column in range(self._columns)] for row in range(self._rows)]
        self._offsetX = offsetX
        self._offsetY = offsetY
    
    def getBoard(self):
        return self._board

    def getRow(self):
        return self._rows

    def getColumns(self):
        return self._columns

    def draw_board(self, board):
        for row in range(self._rows):
            for column in range(self._columns):
                # zmienna dla pygame.draw
                # rysowanie czarnych i białych kwadratów
                if (row + column) % 2 == 0:
                    color = white
                else:
                    color = black
                rect = pygame.draw.rect(screen, color, [gWidth * column + self._offsetX, gHeight * row + self._offsetY, gWidth, gHeight])
                rect_center = rect.center
                if board[row][column] == 1:
                    pygame.draw.circle(screen, white, rect_center, radius)
                if board[row][column] == 2:
                    pygame.draw.circle(screen, black, rect_center, radius)
                    # Rysowanie ramki woków czarnych pionów by były widoczne
                    pygame.draw.circle(screen, grey, rect_center, radius, border)
                # Rysowanie dam
                if board[row][column] == 3:
                    pygame.draw.circle(screen, white, rect_center, radius)
                    pygame.draw.circle(screen, gold, rect_center, radius, border)
                if board[row][column] == 4:
                    pygame.draw.circle(screen, gold, rect_center, radius, border)


class Game:
    def __init__(self):
        self.restart = False
        self.offsetX = 0
        self.offsetY = 100
        self.game_over = False
        self.b = Board(self.offsetX,self.offsetY)
        self.board = self.b.getBoard()
        self.pieces = Pieces()
        self.friendly = self.pieces.getFrendly()
        self.enemy = self.pieces.getEnemy()
        self.pieces.place_starting_pieces(self.board)

        self.myfont = pygame.freetype.Font('CaviarDreams.ttf', 30)
        self.myfontB = pygame.freetype.Font('Caviar_Dreams_Bold.ttf', 30)

        # Ustawienie wymiarów okna aplikacji
        self.window = Window()
        self.screen = pygame.display.set_mode(self.window.getSize())
        self.boardWindow = BoardWindow()

        # Tytuł
        pygame.display.set_caption("Checkers")

        # Potrzebne do odświerzania ekranu
        self.clock = pygame.time.Clock()

        self.width = self.window.getWidth()
        self.height = self.window.getHeight()

        # Wymiary pól
        self.gWidth = (self.boardWindow.getWidth() // self.b.getColumns())
        self.gHeight = (self.boardWindow.getHeight() // self.b.getRow())

        # Ustawienie promienia piona
        self.radius = (self.boardWindow.getWidth() // 20)
        self.border = (self.boardWindow.getWidth() // 200)

        # Informacja kogo teraz ruch
        self.current_player = 1
        #print("White's Turn")
        pygame.draw.rect(self.screen, black, (0, 0, 800, 100))
        text_surface, rect = self.myfont.render("White's Turn", white)
        self.screen.blit(text_surface, (320, 30))

    def main(self):
        # pobieranie informacji o ruchach użytkowanika
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
        
            # macierz współrzędnych myszy dla planszy
            mouse_matrix_pos_b = ((mouse_pos[0] - self.offsetX)// self.gWidth, (mouse_pos[1] - self.offsetY)// self.gHeight)
        
            if 601+200 > mouse_pos[0] > 601 and 100+600 > mouse_pos[1] > 100:
                pygame.draw.rect(self.screen, gold, (601, 100, 200, 600))
            
                if click[0] == 1:
                    pass

            else:
                pygame.draw.rect(self.screen, grey, (601, 100, 200, 600))
            text_surface, rect = self.myfontB.render("Restart", white)
            self.screen.blit(text_surface, (650, 390))

            # Gdy użytkownik zamknie okno
            if event.type == pygame.QUIT:
                self.game_over = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Przełożenie pozycji myszy na planszę
                old_x = mouse_matrix_pos_b[0]
                old_y = mouse_matrix_pos_b[1]

                previous_piece_total = sum([sum(row) for row in self.board])

                if self.pieces.is_valid_selection(self.board, self.current_player, old_x, old_y) == True:
                    # Nic je rób jeśli wybór gracza był poprawny
                    pass
                else:
                    # Powtarzaj dopóki gracz nie wykona poprawnego ruchu
                    continue

                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.QUIT:
                        self.game_over = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        new_pos = pygame.mouse.get_pos()
                        # Przełożenie pozycji myszy na planszę
                        new_x = ((new_pos[0] - self.offsetX )// self.gWidth)
                        new_y = ((new_pos[1] - self.offsetY )// self.gHeight)

                        if self.board[old_y][old_x] == self.friendly['pawn']:
                            if self.pieces.is_valid_move(self.current_player, self.board, old_x, old_y, new_x, new_y) is True:
                                self.board[new_y][new_x] = self.friendly['pawn']
                                self.board[old_y][old_x] = empty

                                if self.pieces.check_for_win(self.current_player, self.board) is True:
                                    self.game_over = True

                                # If the total amount of chips has changed and a double
                                # jump opportunity is available do not switch sides.
                                self.current_piece_total = sum([sum(row) for row in self.board])

                                if previous_piece_total > current_piece_total:
                                    if self.pieces.check_if_double_jump_possible(self.board, new_x, new_y) is True:
                                        pass
                                    else:
                                        # Swap sides
                                        pygame.draw.rect(self.screen, black, (0, 0, 800, 100))
                                        if self.current_player == 1:
                                            self.current_player = 2
                                            #print("Black's Turn")
                                            text_surface, rect = self.myfont.render("Black's Turn", white)
                                            self.screen.blit(text_surface, (320, 30))
                                        else:
                                            self.current_player = 1
                                            #print("White's Turn")
                                            text_surface, rect = self.myfont.render("White's Turn", white)
                                            self.screen.blit(text_surface, (320, 30))

                                        self.friendly, self.enemy = self.enemy, self.friendly
                                else:
                                    # Swap sides
                                    pygame.draw.rect(self.screen, black, (0, 0, 800, 100))
                                    if self.current_player == 1:
                                        self.current_player = 2
                                        #print("Black's Turn")
                                        text_surface, rect = self.myfont.render("Black's Turn", white)
                                        self.screen.blit(text_surface, (320, 30))
                                    else:
                                        self.current_player = 1
                                        #print("White's Turn")
                                        text_surface, rect = self.myfont.render("White's Turn", white)
                                        self.screen.blit(text_surface, (320, 30))

                                    self.friendly, self.enemy = self.enemy, self.friendly

                        if self.board[old_y][old_x] == (self.friendly['king']):
                            if self.pieces.is_valid_king_move(self.current_player, self.board, old_x, old_y, new_x, new_y) is True:

                                if self.pieces.check_for_win(self.current_player, self.board) is True:
                                    self.game_over = True

                                # If the total amount of chips has changed and a double
                                # jump opportunity is available do not switch sides.
                                current_piece_total = sum([sum(row) for row in self.board])

                                if previous_piece_total > current_piece_total:
                                    if self.pieces.check_if_double_jump_possible(self.board, new_x, new_y) is True:
                                        pass
                                    else:
                                        pygame.draw.rect(self.screen, black, (0, 0, 800, 100))
                                        if self.current_player == 1:
                                            self.current_player = 2
                                            #print("Black's Turn")
                                            text_surface, rect = self.myfont.render("Black's Turn", white)
                                            self.screen.blit(text_surface, (320, 30))
                                        else:
                                            self.current_player = 1
                                            #print("White's Turn")
                                            text_surface, rect = self.myfont.render("White's Turn", white)
                                            self.screen.blit(text_surface, (320, 30))

                                        self.friendly, self.enemy = self.enemy, self.friendly
                                else:
                                    pygame.draw.rect(self.screen, black, (0, 0, 800, 100))
                                    if self.current_player == 1:
                                        self.current_player = 2
                                        #print("Black's Turn")
                                        text_surface, rect = self.myfont.render("Black's Turn", white)
                                        self.screen.blit(text_surface, (320, 30))
                                    else:
                                        self.current_player = 1
                                        #print("White's Turn")
                                        text_surface, rect = self.myfont.render("White's Turn", white)
                                        self.screen.blit(text_surface, (320, 30))

                                    self.friendly, self.enemy = self.enemy, self.friendly

                        # Turn player into king if they make it to the opposite side of the board
                        for row in range(self.b.getRow()):
                            for column in range(self.b.getColumns()):
                                # Checking for player 1 king pieces
                                if self.board[0][column] == 1:
                                    self.board[0][column] = 3
                                # Cecking for player 2 king pieces
                                elif self.board[7][column] == 2:
                                    self.board[7][column] = 4
                        break

        # Limit to 60 frames per second
        self.clock.tick(60)

        # Draw onto screen)
        self.b.draw_board(self.board)

        # Update screen with what we drew
        pygame.display.flip()

    def begin(self):
        self.restart = True
        while self.restart:
            new_game = Game()
            new_game.main()


# Inizjalizacja pygame
pygame.init()

game = Game()
# Głown pętla gry 
game.begin()


# Exit the game
pygame.quit()