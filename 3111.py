import pygame
import random
import os

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROWS = 6  # количество строк
COLS = 6  # количество столбцов
MARGIN = 2  # отступ между фрагментами

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Пазл')
clock = pygame.time.Clock()

# Загрузка случайного изображения
pictures = os.listdir('pictures')
picture = random.choice(pictures)
image = pygame.image.load(os.path.join('pictures', picture))

# Рассчет размеров фрагментов
image_width, image_height = image.get_size()
TILE_WIDTH = image_width // COLS
TILE_HEIGHT = image_height // ROWS

# Разрезание изображения на фрагменты
tiles = []
for i in range(ROWS):
    for j in range(COLS):
        rect = pygame.Rect(j * TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
        tile = image.subsurface(rect)
        tiles.append(tile)

# Сохранение оригинального порядка и перемешивание
original_tiles = tiles.copy()
random.shuffle(tiles)

# Переменные игры
selected = None  # выбранный фрагмент
swaps = 0  # счетчик перестановок
running = True  # флаг работы игры


def draw_tiles():
    """Отрисовка всех фрагментов пазла"""
    for i in range(len(tiles)):
        row = i // COLS
        col = i % COLS
        x = col * (TILE_WIDTH + MARGIN) + MARGIN
        y = row * (TILE_HEIGHT + MARGIN) + MARGIN

        # Выделение выбранного фрагмента зеленой рамкой
        if i == selected:
            pygame.draw.rect(screen, (0, 255, 0),
                             (x - MARGIN, y - MARGIN,
                              TILE_WIDTH + MARGIN * 2,
                              TILE_HEIGHT + MARGIN * 2))

        screen.blit(tiles[i], (x, y))


def show_message():
    """Показ сообщения о завершении игры"""
    font = pygame.font.SysFont('Arial', 64)
    text = font.render('Ура, картинка собрана!', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(40, 40))
    screen.blit(text, text_rect)


def draw_swaps():
    """Отображение количества перестановок"""
    font = pygame.font.SysFont('Arial', 32)
    text = font.render(f'Перестановок: {swaps}', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topleft = (10, 10)
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(10, 10))
    screen.blit(text, text_rect)


# Основной игровой цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка клика мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Определение кликнутого фрагмента
            for i in range(len(tiles)):
                row = i // COLS
                col = i % COLS
                x = col * (TILE_WIDTH + MARGIN) + MARGIN
                y = row * (TILE_HEIGHT + MARGIN) + MARGIN

                if x <= mouse_x <= x + TILE_WIDTH and y <= mouse_y <= y + TILE_HEIGHT:
                    if selected is not None and selected != i:
                        # Меняем местами выбранные фрагменты
                        tiles[i], tiles[selected] = tiles[selected], tiles[i]
                        selected = None
                        swaps += 1
                    elif selected == i:
                        # Снимаем выделение, если кликнули на тот же фрагмент
                        selected = None
                    else:
                        # Выбираем новый фрагмент
                        selected = i

    # Отрисовка
    screen.fill((0, 0, 0))  # Черный фон
    draw_tiles()
    draw_swaps()

    # Проверка завершения игры
    if tiles == original_tiles:
        show_message()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()