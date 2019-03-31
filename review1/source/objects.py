class MutableInt:
    """Integer that can be passed to a function and then modified"""
    def __init__(self, value=0):
        self.value = value

    def __add__(self, other):
        self.value += other
        return self.value + other

    def __repr__(self):
        return str(self.value)


class Field:
    """Game field"""
    def __init__(self, screen, coords):
        self.screen = screen
        self.height = coords[0]
        self.width = coords[1]

    def __repr__(self):
        return str(self.height) + ' ' + str(self.width)

    def load(self, str):
        self.height, self.width = str.split(' ')

    def draw(self):
        """Draws the game field on the screen"""
        self.screen.clear()
        for i in range(1, self.height - 2):
            for j in range(self.width):
                self.screen.addstr(i, 0, '┃' + (self.width - 3) * ' ' + '┃')
        self.screen.addstr(0, 0,
                           '┏' + (self.width - 3) * '━' + '┓')
        self.screen.addstr(self.height - 2, 0,
                           '┗' + (self.width - 3) * '━' + '┛')
        self.screen.refresh()


class Snake:
    """The snake"""
    def __init__(self, screen, field, coords, speed=(0, 1), is_alive=True):
        self.screen = screen
        self.field = field
        self.coords = coords
        self.speed = speed
        self.queue = [coords]
        self.is_alive = is_alive

    def __repr__(self):
        def tupstr(tup):
            return ' '.join(map(str, tup))

        _str = tupstr(self.speed) + '\n'
        _str += str(len(self.queue)) + '\n'
        _str += '\n'.join(map(tupstr, self.queue)) + '\n'
        _str += str(self.is_alive)
        return _str

    def move(self, food, score):
        """
        Moves the snake, determines if it dies or eats food,
        recalculates score
        """
        head = self.queue[-1]
        newhead = ((self.field.height - 3 + head[0] + self.speed[0]) %
                   (self.field.height - 3),
                   (self.field.width - 3 + head[1] + self.speed[1]) %
                   (self.field.width - 3))
        self.queue.append(newhead)
        tail = self.queue[0]
        if newhead in food:
            score += food[newhead]
            food.pop(newhead)
        else:
            self.queue.pop(0)
        if newhead in self.queue[:-1]:
            self.is_alive = False
        self.screen.addch(newhead[0] + 1, newhead[1] + 1, '#')
        self.screen.addch(tail[0] + 1, tail[1] + 1, ' ')
        self.screen.refresh()

    def draw(self):
        """Draws the snake"""
        for crd in self.queue:
            self.screen.addch(crd[0] + 1, crd[1] + 1, '#')
        self.screen.refresh()
