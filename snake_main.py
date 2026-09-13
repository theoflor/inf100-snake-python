import random


def make_board(rows, cols):
    return [[0] * cols for _ in range(rows)]


def place_start_snake(app):
    start_row = app.rows // 2
    start_col = max(2, app.cols // 2)

    app.board[start_row][start_col - 2] = 1
    app.board[start_row][start_col - 1] = 2
    app.board[start_row][start_col] = 3

    app.snake_size = 3
    app.head_pos = (start_row, start_col)
    app.direction = 'east'


def reset_game(app):
    app.rows = 7
    app.cols = 9
    app.board = make_board(app.rows, app.cols)

    place_start_snake(app)
    add_apple_at_random_location(app.board)

    app.state = 'active'
    app.info_mode = False


def app_started(app):
    app.timer_delay = 200
    app.info_mode = False
    app.state = 'welcome'

    # “tomt” brett så draw_board alltid kan tegne noe
    app.rows = 7
    app.cols = 9
    app.board = make_board(app.rows, app.cols)


def is_legal_move(pos, board):
    r, c = pos
    rows = len(board)
    cols = len(board[0])

    if r < 0 or r >= rows or c < 0 or c >= cols:
        return False

    if board[r][c] > 0:
        return False

    return True


def get_next_head_position(head_pos, direction):
    r, c = head_pos
    if direction == 'north':
        r -= 1
    elif direction == 'south':
        r += 1
    elif direction == 'west':
        c -= 1
    elif direction == 'east':
        c += 1
    return (r, c)


def subtract_one_from_all_positives(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] > 0:
                grid[r][c] -= 1


def add_apple_at_random_location(grid):
    empty = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 0:
                empty.append((r, c))

    if not empty:
        return

    r, c = random.choice(empty)
    grid[r][c] = -1


def move_snake(app):
    if app.state != 'active':
        return

    nxt = get_next_head_position(app.head_pos, app.direction)
    if not is_legal_move(nxt, app.board):
        app.state = 'gameover'
        return

    r, c = nxt

    if app.board[r][c] == -1:
        app.snake_size += 1
        app.head_pos = nxt
        app.board[r][c] = app.snake_size
        add_apple_at_random_location(app.board)
    else:
        subtract_one_from_all_positives(app.board)
        app.head_pos = nxt
        app.board[r][c] = app.snake_size


def timer_fired(app):
    if not app.info_mode and app.state == 'active':
        move_snake(app)


def draw_centered_text(canvas, app, y, text, size=20, color='white'):
    canvas.create_text(
        app.width / 2, y,
        text=text,
        font=f'Arial {size} bold',
        fill=color
    )


def redraw_all(app, canvas):
    from snake_view import draw_board

    # Bakgrunn
    canvas.create_rectangle(0, 0, app.width, app.height, fill='#1e1e1e', outline='')

    if app.state == 'welcome':
        draw_centered_text(canvas, app, 80, 'SNAKE', size=34, color='#7CFC00')
        draw_centered_text(canvas, app, 145, 'Trykk SPACE for å starte', size=18, color='white')
        draw_centered_text(canvas, app, 185, 'Bruk piltastene for å styre', size=16, color='#dddddd')
        draw_centered_text(canvas, app, 215, "Trykk 'p' for pause", size=16, color='#dddddd')
        draw_centered_text(canvas, app, 245, "Trykk 'i' for info-modus", size=16, color='#dddddd')
        draw_centered_text(canvas, app, 275, 'Spis epler og unngå å krasje!', size=16, color='#ffcc66')
        return

    margin = 25
    x1, y1 = margin, margin
    x2, y2 = app.width - margin, app.height - margin

    draw_board(canvas, x1, y1, x2, y2, app.board, app.info_mode)

    canvas.create_text(
        10, 10, anchor='nw',
        text=f'Lengde: {getattr(app, "snake_size", 0)}',
        font='Arial 14 bold',
        fill='white'
    )

    if app.state == 'paused':
        canvas.create_rectangle(
            app.width / 2 - 130, app.height / 2 - 55,
            app.width / 2 + 130, app.height / 2 + 55,
            fill='black', outline='white', width=2
        )
        draw_centered_text(canvas, app, app.height / 2 - 10, 'PAUSED', size=28, color='#ffd966')
        draw_centered_text(canvas, app, app.height / 2 + 22, "Trykk 'p' for å fortsette", size=14, color='white')

    elif app.state == 'gameover':
        canvas.create_rectangle(
            app.width / 2 - 170, app.height / 2 - 70,
            app.width / 2 + 170, app.height / 2 + 70,
            fill='black', outline='red', width=3
        )
        draw_centered_text(canvas, app, app.height / 2 - 16, 'GAME OVER', size=28, color='red')
        draw_centered_text(canvas, app, app.height / 2 + 20, "Trykk SPACE for å spille igjen", size=14, color='white')
        


def key_pressed(app, event):
    key = event.key

    # Velkomst: start med Space
    if app.state == 'welcome':
        if key == 'Space':
            reset_game(app)
        return

    # Gameover: restart med Space (evt med 'r')
    if app.state == 'gameover':
        if key == 'Space' or key == 'r':
            reset_game(app)
        return

    # Pause toggle
    if key == 'p':
        if app.state == 'active':
            app.state = 'paused'
        elif app.state == 'paused':
            app.state = 'active'
        return

    # Ikke styring når pauset
    if app.state != 'active':
        return

    # Info-mode toggle
    if key == 'i':
        app.info_mode = not app.info_mode
        return

    # Retning (hindrer 180-graders snu)
    if key == 'Up' and app.direction != 'south':
        app.direction = 'north'
    elif key == 'Down' and app.direction != 'north':
        app.direction = 'south'
    elif key == 'Left' and app.direction != 'east':
        app.direction = 'west'
    elif key == 'Right' and app.direction != 'west':
        app.direction = 'east'


if __name__ == '__main__':
    from uib_inf100_graphics.event_app import run_app
    run_app(width=500, height=400, title='Snake')