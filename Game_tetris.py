import pygame
import random
import sys

# ======== НАСТРОЙКИ ========
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 690
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
INITIAL_SPEED = 0.25
MIN_SPEED = 0.05
SPEED_MULTIPLIER = 0.8
PREVIEW_X = 330  # Сдвиг влево
PREVIEW_Y = 180  # Сдвиг ниже
SCORE_FONT_SIZE = 25  # Размер шрифта для счёта

COLORS = {
    'background': (205, 192, 176),
    'grid': (139, 131, 120, 50),
    'text': (50, 50, 50),
    'shapes': [
        (0, 255, 255), (255, 255, 0), (255, 165, 0),
        (0, 0, 255), (0, 255, 0), (255, 0, 0), (128, 0, 128)
    ]
}

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# ======== ИНИЦИАЛИЗАЦИЯ ========
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 35, bold=True)
score_font = pygame.font.SysFont("Arial", SCORE_FONT_SIZE, bold=True)
small_font = pygame.font.SysFont("Arial", 25)


# ======== КЛАСС ТЕТРОМИНО ========
class Tetromino:
    def __init__(self, shape=None):
        self.shape = shape or random.choice(SHAPES)
        self.color = random.choice(COLORS['shapes'])
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        original = self.shape
        self.shape = [list(row[::-1]) for row in zip(*self.shape)]
        if self.collision():
            self.shape = original

    def collision(self, dx=0, dy=0):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if not (0 <= new_x < GRID_WIDTH and new_y < GRID_HEIGHT):
                        return True
                    if new_y >= 0 and (new_x, new_y) in locked:
                        return True
        return False


# ======== ФУНКЦИИ ========
def draw_grid():
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, COLORS['grid'],
                         (x * BLOCK_SIZE, 0),
                         (x * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, COLORS['grid'],
                         (0, y * BLOCK_SIZE),
                         (GRID_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE))


def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_preview(pieces):
    start_y = PREVIEW_Y + 40
    for i, piece in enumerate(pieces[:3]):
        offset_y = i * 80
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, piece.color,
                                     (PREVIEW_X + x * BLOCK_SIZE,
                                      start_y + y * BLOCK_SIZE + offset_y,
                                      BLOCK_SIZE - 1, BLOCK_SIZE - 1))


def new_bag():
    return [Tetromino() for _ in range(5)]


def clear_lines():
    global score, level
    full_rows = [y for y in range(GRID_HEIGHT)
                 if all((x, y) in locked for x in range(GRID_WIDTH))]

    for row in full_rows:
        for y in range(row, 0, -1):
            for x in range(GRID_WIDTH):
                if (x, y - 1) in locked:
                    locked[(x, y)] = locked[(x, y - 1)]
                else:
                    locked.pop((x, y), None)
        for x in range(GRID_WIDTH):
            locked.pop((x, 0), None)

    lines = len(full_rows)
    if lines > 0:
        score += lines ** 2 * 100
        level = score // 1000 + 1


# ======== ИГРОВАЯ ЛОГИКА ========
def game_loop():
    global locked, score, level, paused
    locked = {}
    score = 0
    level = 1
    paused = False
    current_speed = INITIAL_SPEED
    current = Tetromino()
    next_bag = new_bag()
    fall_time = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

                if not paused:
                    if event.key == pygame.K_LEFT:
                        if not current.collision(dx=-1):
                            current.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if not current.collision(dx=1):
                            current.x += 1
                    elif event.key == pygame.K_DOWN:
                        if not current.collision(dy=1):
                            current.y += 1
                    elif event.key == pygame.K_UP:
                        current.rotate()
                    elif event.key == pygame.K_ESCAPE:
                        return

        if not paused:
            fall_time += clock.get_rawtime()
            current_speed = max(
                MIN_SPEED,
                INITIAL_SPEED * (SPEED_MULTIPLIER ** (level - 1))
            )

            if fall_time / 1000 >= current_speed:
                fall_time = 0
                if not current.collision(dy=1):
                    current.y += 1
                else:
                    for y, row in enumerate(current.shape):
                        for x, cell in enumerate(row):
                            if cell:
                                locked[(current.x + x, current.y + y)] = current.color

                    clear_lines()

                    if any(y < 1 for (x, y) in locked):
                        game_over = True

                    current = next_bag.pop(0)
                    if not next_bag:
                        next_bag = new_bag()

        screen.fill(COLORS['background'])

        for (x, y), color in locked.items():
            pygame.draw.rect(screen, color,
                             (x * BLOCK_SIZE, y * BLOCK_SIZE,
                              BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        for y, row in enumerate(current.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, current.color,
                                     ((current.x + x) * BLOCK_SIZE,
                                      (current.y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        draw_grid()

        # Обновлённый интерфейс
        draw_text(f"Score: {score}", score_font, COLORS['text'], PREVIEW_X, 30)
        draw_text(f"Level: {level}", score_font, COLORS['text'], PREVIEW_X, 60)
        draw_text("Next:", font, COLORS['text'], PREVIEW_X, 140)
        draw_preview(next_bag)

        if paused:
            draw_text("PAUSED", font, (255, 0, 0), 240, 300)

        pygame.display.update()
        clock.tick(60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    return

        screen.fill(COLORS['background'])
        draw_text("GAME OVER", font, (255, 0, 0), 220, 300)
        draw_text("Press SPACE to restart", small_font, COLORS['text'], 190, 400)
        pygame.display.update()
        clock.tick(10)


# ======== ОБНОВЛЕННОЕ МЕНЮ ========
def main_menu():
    while True:
        screen.fill(COLORS['background'])
        draw_text("TETRIS", font, COLORS['text'], 100, 200)
        draw_text("Press SPACE to start", small_font, COLORS['text'], 80, 300)
        draw_text("P - Pause  ESC - Menu", small_font, COLORS['text'], 60, 400)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main_menu()