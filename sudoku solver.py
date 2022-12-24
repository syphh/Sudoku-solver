import numpy as np
import matplotlib.pyplot as plt


def on_click(event):
    global selected_cell
    if selected_cell:
        cells[selected_cell[0]][selected_cell[1]].set_facecolor('white')
        selected_cell = None
    if event.inaxes == ax:
        x, y = event.xdata, event.ydata
        i, j = 8-int(x//3), int(y//3)
        cells[i][j].set_facecolor('lightgreen')
        selected_cell = (i, j)
        fig.canvas.draw()


def on_press(event):
    global selected_cell
    if selected_cell:
        if event.key in '123456789':
            labels[selected_cell[0]][selected_cell[1]].set_text(event.key)
            board[selected_cell[0]][selected_cell[1]] = int(event.key)
        elif event.key == 'backspace':
            labels[selected_cell[0]][selected_cell[1]].set_text('')
            board[selected_cell[0]][selected_cell[1]] = 0
        fig.canvas.draw()


def clear(event):
    global selected_cell
    ax.set_title('', {'color': 'red', 'fontsize': 20})
    for i in range(9):
        for j in range(9):
            labels[i][j].set_text('')
            board[i][j] = 0
    if selected_cell:
        cells[selected_cell[0]][selected_cell[1]].set_facecolor('white')
        selected_cell = None
    fig.canvas.draw()


def valid_sudoku(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                k = board[i][j]
                board[i][j] = 0
                if k in board[i] or k in board[:, j] or k in board[(i//3)*3:(i//3)*3+3, (j//3)*3:(j//3)*3+3]:
                    return False
                board[i][j] = k
    return True


def solve_sudoku(board, i, j):
    if i == 9:
        return True
    if j == 9:
        return solve_sudoku(board, i+1, 0)
    if board[i][j] != 0:
        return solve_sudoku(board, i, j+1)
    for k in range(1, 10):
        if k not in board[i] and k not in board[:, j] and k not in board[(i//3)*3:(i//3)*3+3, (j//3)*3:(j//3)*3+3]:
            board[i][j] = k
            if solve_sudoku(board, i, j+1):
                return True
    board[i][j] = 0
    return False


def run(event):
    ax.set_title('', {'color': 'red', 'fontsize': 20})
    if not valid_sudoku(board):
        ax.set_title('Invalid board', {'color': 'red', 'fontsize': 20})
    elif solve_sudoku(board, 0, 0):
        for i in range(9):
            for j in range(9):
                labels[i][j].set_text(str(board[i][j]))
    else:
        ax.set_title('No solution', {'color': 'red', 'fontsize': 20})
    fig.canvas.draw()


fig, ax = plt.subplots()
fig.set_size_inches((12, 9))
cells = [[None]*9 for _ in range(9)]
board = np.zeros((9, 9), dtype=int)
selected_cell = None
labels = [[None]*9 for _ in range(9)]
for i in range(9):
    for j in range(9):
        if i%3 == 0 and j%3 == 0:
            rect = plt.Rectangle((i*3, j*3), 9, 9, edgecolor='black', linewidth=4, zorder=float('inf'), fill=False)
            ax.add_patch(rect)
        cells[8-i][j] = plt.Rectangle((i*3, j*3), 3, 3, edgecolor='black', linewidth=2, facecolor='white', fill=True)
        labels[8-i][j] = ax.annotate('', (i*3+1.5, j*3+1.5), color='black', weight='bold', fontsize=20, ha='center', va='center')
        ax.add_patch(cells[8-i][j])
ax.set_xlim((0, 27))
ax.set_ylim((0, 27))
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_aspect('equal')

ax_run = fig.add_axes([0.85, 0.05, 0.1, 0.075])
ax_clear = fig.add_axes([0.85, 0.15, 0.1, 0.075])
btn_run = plt.Button(ax_run, 'Run')
btn_clear = plt.Button(ax_clear, 'Clear')
btn_run.on_clicked(run)
btn_clear.on_clicked(clear)

fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('key_press_event', on_press)

plt.show()
