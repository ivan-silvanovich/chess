import pygame


# Classes
class Piece:
    def __init__(self, y, x, side):
        self.x = x
        self.y = y
        self.side = side
        chessboard[y][x] = side

    def move(self, y, x):
        chessboard[y][x] = self.side
        chessboard[self.y][self.x] = 0
        self.x = x
        self.y = y

    @staticmethod
    def is_ok(self, y, x):
        pass


class Pawn(Piece):
    color = (pygame.image.load('Sprites/wh_pawn.png'), pygame.image.load('Sprites/bl_pawn.png'))

    def __init__(self, y, x, side):
        super().__init__(y, x, side)
        self.image = Pawn.color[side - 1]

    def move(self, y, x):
        super().move(y, x)
        if (self.side == 1 and y == 0) or (self.side == 2 and y == 7):
            self.choose = input('Enter your new piece: ')
            if self.choose == 'Queen':
                self = Queen(y, x, self.side)
            elif self.choose == 'Bishop':
                return Bishop(y, x, self.side)
            elif self.choose == 'Castle':
                return Castle(y, x, self.side)
            elif self.choose == 'Knight':
                return Knight(y, x, self.side)

    def is_ok(self, y, x):
        if self.side == 1:
            if chessboard[y][x] == 2 and (y + 1 == self.y and (x + 1 == self.x or x - 1 == self.x)):
                return True
            elif chessboard[y][x] == 0 and (y + 1 == self.y or (y + 2 == self.y and self.y == 6 and chessboard[y+1][x] == 0)) and x == self.x:
                return True
            else:
                return False
        elif self.side == 2:
            if chessboard[y][x] == 1 and (y - 1 == self.y and (x + 1 == self.x or x - 1 == self.x)):
                return True
            elif chessboard[y][x] == 0 and (y - 1 == self.y or (y - 2 == self.y and self.y == 1 and chessboard[y-1][x] == 0)) and x == self.x:
                return True
            else:
                return False


class Castle(Piece):
    color = (pygame.image.load('Sprites/wh_castle.png'), pygame.image.load('Sprites/bl_castle.png'))

    def __init__(self, y, x, side):
        super().__init__(y, x, side)
        self.image = Castle.color[side - 1]

    def is_possible(self, y, x):
        if self.x == x:
            for i in range(y+1, self.y, 1):
                if chessboard[i][x] != 0:
                    return False
            for i in range(y-1, self.y, -1):
                if chessboard[i][x] != 0:
                    return False
            return True
        if self.y == y:
            for i in range(x+1, self.x, 1):
                if chessboard[y][i] != 0:
                    return False
            for i in range(x-1, self.x, -1):
                if chessboard[y][i] != 0:
                    return False
            return True

    def is_ok(self, y, x):
        return (y == self.y or x == self.x) and self.is_possible(y, x) and chessboard[y][x] != self.side


class Knight(Piece):
    color = (pygame.image.load('Sprites/wh_knight.png'), pygame.image.load('Sprites/bl_knight.png'))

    def __init__(self, y, x, side):
        super().__init__(y, x, side)
        self.image = Knight.color[side - 1]

    def is_ok(self, y, x):
        if chessboard[y][x] != self.side:
            if (y + 2 == self.y and x + 1 == self.x) or (y + 2 == self.y and x - 1 == self.x):
                return True
            elif (y - 2 == self.y and x + 1 == self.x) or (y - 2 == self.y and x - 1 == self.x):
                return True
            elif (x + 2 == self.x and y + 1 == self.y) or (x + 2 == self.x and y - 1 == self.y):
                return True
            elif (x - 2 == self.x and y + 1 == self.y) or (x - 2 == self.x and y - 1 == self.y):
                return True
            else:
                return False
        else:
            return False


class Bishop(Piece):
    color = (pygame.image.load('Sprites/wh_bishop.png'), pygame.image.load('Sprites/bl_bishop.png'))

    def __init__(self, y, x, side):
        super().__init__(y, x, side)
        self.image = Bishop.color[side - 1]

    def is_possible(self, y, x, a=1):
        i = 1
        if x > self.x:
            while self.x + i < x:
                if chessboard[self.y+i*a][self.x+i] != 0:
                    return False
                i += 1
            return True
        if x < self.x:
            while self.x - i > x:
                if chessboard[self.y-i*a][self.x-i] != 0:
                    return False
                i += 1
            return True

    def is_ok(self, y, x):
        if (y - self.y == x - self.x) and self.is_possible(y, x) and chessboard[y][x] != self.side:
            return True
        elif (y - self.y == (x - self.x) * -1) and self.is_possible(y, x, -1) and chessboard[y][x] != self.side:
            return True
        else:
            return False


class Queen(Piece):
    color = (pygame.image.load('Sprites/wh_queen.png'), pygame.image.load('Sprites/bl_queen.png'))

    def __init__(self, y, x, side):
        super().__init__(y, x, side)
        self.image = Queen.color[side - 1]

    def is_ok(self, y, x):
        a = Bishop(self.y, self.x, self.side)
        b = Castle(self.y, self.x, self.side)
        return a.is_ok(y, x) or b.is_ok(y, x)


class King(Piece):
    castling_line = [7, 0]
    turns = [[0, -1], [0, 1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1]]
    color = (pygame.image.load('Sprites/wh_king.png'), pygame.image.load('Sprites/bl_king.png'))

    def __init__(self, y, x, side):
        super().__init__(y, x, side)
        self.ban_space = []
        self.image = King.color[side - 1]

    def is_ok(self, y, x):
        return -1 <= self.x - x <= 1 and -1 <= self.y - y <= 1 and chessboard[y][x] != self.side and self.checking(y, x) or self.is_castling(y, x)

    def checking(self, y, x):
        global pieces
        old = chessboard[y][x]
        chessboard[y][x] = self.side
        for i in pieces:
            if i.side != self.side and i.is_ok(y, x):
                chessboard[y][x] = old
                return False
        chessboard[y][x] = old
        return True

    def is_castling(self, y, x):
        global pieces
        if x - self.x == 2 and King.castling_line[self.side-1] == y and chessboard[y][x-1] == 0 and chessboard[y][x] == 0:
            for i in pieces:
                if i.x == x + 1 and i.y == y and type(i) == Castle and i.side == self.side:
                    i.move(y, x-1)
                    return True
        elif x - self.x == -2 and King.castling_line[self.side-1] == y and chessboard[y][x+1] == 0 and chessboard[y][x] == 0:
            for i in pieces:
                if i.x == x - 1 and i.y == y and type(i) == Castle and i.side == self.side:
                    i.move(y, x+1)
                    return True
        else:
            return False

    def is_mate(self):
        global pieces
        attack_list = []
        for i in King.turns:
            y = self.y - i[0]
            x = self.x - i[1]
            if on_board(y, x) and self.is_ok(y, x):
                return False
        for i in pieces:
            if i.is_ok(self.y, self.x):
                attack_list.append(i)
        if len(attack_list) > 1:
            return True
        elif len(attack_list) == 0:
            return False
        else:
            for i in pieces:
                if i.is_ok(attack_list[0].y, attack_list[0].x):
                    return False
                else:
                    if type(attack_list[0]) == Knight:
                        return True
                    for i in King.turns:
                        y = self.y - i[0]
                        x = self.x - i[1]
                        if on_board(y, x) and attack_list[0].is_ok(y, x):
                            break
                    for i in pieces:
                        if i.side == self.side and i.is_ok(y, x):
                            return False
                    return True


# Functions
def check_checking(active_piece, pieces, y, x):
    old_x = active_piece.x
    old_y = active_piece.y
    active_piece.move(y, x)
    for i in pieces:
        if type(i) == King and i.side == active_piece.side:
            king = i
    for i in pieces:
        if i.is_ok(king.y, king.x) and i.side != king.side and not (i.x == x and i.y == y):
            active_piece.move(old_y, old_x)
            return False
    active_piece.move(old_y, old_x)
    return True


def on_board(y, x):
    return 0 <= y <= 7 and 0 <= x <= 7


# Parameters
timer = pygame.time.Clock()

chessboard = [[2, 2, 2, 2, 2, 2, 2, 2],
              [2, 2, 2, 2, 2, 2, 2, 2],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1]]

bg = pygame.image.load('Sprites/chessboard.png')

# Pieces adding
wh_pawn1, wh_pawn2, wh_pawn3, wh_pawn4 = Pawn(6, 0, 1), Pawn(6, 1, 1), Pawn(6, 2, 1), Pawn(6, 3, 1)
wh_pawn5, wh_pawn6, wh_pawn7, wh_pawn8 = Pawn(6, 4, 1), Pawn(6, 5, 1), Pawn(6, 6, 1), Pawn(6, 7, 1)
bl_pawn1, bl_pawn2, bl_pawn3, bl_pawn4 = Pawn(1, 0, 2), Pawn(1, 1, 2), Pawn(1, 2, 2), Pawn(1, 3, 2)
bl_pawn5, bl_pawn6, bl_pawn7, bl_pawn8 = Pawn(1, 4, 2), Pawn(1, 5, 2), Pawn(1, 6, 2), Pawn(1, 7, 2)
wh_castle1, wh_castle2, bl_castle1, bl_castle2 = Castle(7, 0, 1), Castle(7, 7, 1), Castle(0, 0, 2), Castle(0, 7, 2)
wh_knight1, wh_knight2, bl_knight1, bl_knight2 = Knight(7, 1, 1), Knight(7, 6, 1), Knight(0, 1, 2), Knight(0, 6, 2)
wh_bishop1, wh_bishop2, bl_bishop1, bl_bishop2 = Bishop(7, 2, 1), Bishop(7, 5, 1), Bishop(0, 2, 2), Bishop(0, 5, 2)
wh_king, bl_king, wh_queen1, bl_queen1 = King(7, 4, 1), King(0, 4, 2), Queen(7, 3, 1), Queen(0, 3, 2)

pieces = [wh_pawn1, wh_pawn2, wh_pawn3, wh_pawn4, wh_pawn5, wh_pawn6, wh_pawn7, wh_pawn8,
          wh_castle1, wh_castle2, wh_knight1, wh_knight2, wh_bishop1, wh_bishop2, wh_queen1, wh_king,
          bl_pawn1, bl_pawn2, bl_pawn3, bl_pawn4, bl_pawn5, bl_pawn6, bl_pawn7, bl_pawn8,
          bl_castle1, bl_castle2, bl_knight1, bl_knight2, bl_bishop1, bl_bishop2, bl_king, bl_queen1]

# Main code
pygame.init()
win = pygame.display.set_mode((480, 480))
pygame.display.set_caption('Chess')

turn = 1
count = 0
run = True
while run:
    timer.tick(30)
    win.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Отслеживание закрытия окна
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and count == 1:
            x = event.pos[0] // 60  # Вычисление координат
            y = event.pos[1] // 60  # с помощью позиции клика
            if piece.is_ok(y, x) and check_checking(piece, pieces, y, x):
                for i in pieces:
                    if i.y == piece.y and i.x == piece.x and i.side == piece.side:
                        i.move(y, x)
                        turn += 1
                    elif i.y == y and i.x == x:
                        pieces.remove(i)
            count = 0
            if wh_king.is_mate():
                winner = pygame.image.load('Sprites/bl_win.png')
                run = False
            elif bl_king.is_mate():
                winner = pygame.image.load('Sprites/wh_win.png')
                run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Отслеживание нажатия левой кнопки мыши
            x = event.pos[0] // 60  # Вычисление координат
            y = event.pos[1] // 60  # с помощью позиции клика
            for i in pieces:
                if i.y == y and i.x == x and i.side % 2 == turn % 2:
                    count += 1
                    piece = i
                    break

    # Pieces print
    for i in pieces:
        win.blit(i.image, (i.x * 60, i.y * 60))
    pygame.display.update()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Отслеживание закрытия окна
            run = False
    win.blit(winner, (0, 90))
    pygame.display.update()

pygame.quit()
