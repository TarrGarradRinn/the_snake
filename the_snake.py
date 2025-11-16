from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
            self,
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            body_color=None):
        """
        Инициализирует базовые атрибуты объекта.

        Args:
            position (tuple): Позиция объекта на игровом поле (x, y).
            body_color (tuple): Цвет объекта в формате RGB.
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Абстрактный метод для отрисовки объекта.

        Должен быть переопределен в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко в игре."""

    def __init__(
        self, position=None, body_color=APPLE_COLOR
    ):
        """
        Инициализирует яблоко.

        Args:
            position (tuple): Позиция яблока на игровом поле.
            Если None, будет сгенерирована случайная позиция.
            body_color (tuple): Цвет яблока в формате RGB.
        """
        super().__init__(position, body_color)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку в игре."""

    def __init__(
        self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        body_color=SNAKE_COLOR
    ):
        """
        Инициализирует начальное состояние змейки.

        Args:
            position (tuple): Начальная позиция головы змейки.
            body_color (tuple): Цвет змейки в формате RGB.
        """
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_head_position = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        if new_head_position in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(snake_object):
    """
    Обрабатывает нажатия клавиш для изменения направления движения змейки.

    Args:
        snake_object (Snake): Объект змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP
               and snake_object.direction != DOWN):
                snake_object.next_direction = UP
            elif (event.key == pygame.K_DOWN
                  and snake_object.direction != UP):
                snake_object.next_direction = DOWN
            elif (event.key == pygame.K_LEFT
                  and snake_object.direction != RIGHT):
                snake_object.next_direction = LEFT
            elif (event.key == pygame.K_RIGHT
                  and snake_object.direction != LEFT):
                snake_object.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
