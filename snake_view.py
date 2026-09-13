def draw_board(canvas, x1, y1, x2, y2, board, info_mode):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    cell_width = (x2 - x1) / cols
    cell_height = (y2 - y1) / rows

    # Finn hodets verdi
    max_value = 0
    for row in range(rows):
        for col in range(cols):
            if board[row][col] > max_value:
                max_value = board[row][col]

    for row in range(rows):
        for col in range(cols):
            x_start = x1 + col * cell_width
            y_start = y1 + row * cell_height
            x_end = x_start + cell_width
            y_end = y_start + cell_height

            value = board[row][col]

            if value == 0:
                color = '#2f4f2f'      # mørk grønn bakgrunn
            elif value == -1:
                color = '#ff4d4d'      # rødt eple
            elif value == max_value:
                color = '#00ff99'      # slangens hode
            else:
                color = '#66cc66'      # slangekropp

            canvas.create_rectangle(
                x_start, y_start, x_end, y_end,
                fill=color,
                outline='#1a1a1a',
                width=2
            )

            if info_mode:
                canvas.create_text(
                    (x_start + x_end) / 2,
                    (y_start + y_end) / 2,
                    text=f'{row},{col}\n{value}',
                    font='Arial 10 bold',
                    fill='white'
                )