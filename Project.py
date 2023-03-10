# Sudoku solver
# Marek Holík, I. ročník, zimný semester 2021/2022
# Programovanie 1


from tkinter import *
from tkinter.font import Font
import random
import numpy as np

# creating instance - window
root = Tk()

# creating custom font
custom_font = Font(family="Helvetica", size=18, weight="bold")

# creating window, width, height in pixels
root.title("sudoku Solver")
root.geometry("525x720")
# fixing window sizes, so they cant be scalable
root.maxsize(525, 720)
root.minsize(525, 720)
# labels - heading, result labels, grids represent their position on window
label = Label(root, text="fill numbers", fg="blue", font=custom_font)
label.grid(row=0, column=1, columnspan=10)
errlabel = Label(root, text="", fg="red", font=custom_font)
errlabel.grid(row=25, column=1, columnspan=10)
solvedlabel = Label(root, text="", fg="green", font=custom_font)
solvedlabel.grid(row=25, column=1, columnspan=10)


# returning bool if input is number or not
def validateNumber(P):
    out = (P.isdigit() or P == "") and len(P) < 2
    return out


reg = root.register(validateNumber)
N = 9
# dictionary of values in table
cells = {}


# checking, if number can be placed into table
def possible(board, row, col, num):
    for i in range(9):  # check rows
        if board[row][i] == num:
            return False
    for i in range(9):  # check columns
        if board[i][col] == num:
            return False
    x0 = col - (col % 3)  # check squares
    y0 = row - (row % 3)
    for i in range(3):
        for j in range(3):
            if board[y0 + i][x0 + j] == num:
                return False
    return True


# Function is solving table using recursion
def solve(board, row, col):
    if row == N - 1 and col == N:  # if we are in bottom right corner, return
        return True
    if col == N:
        row += 1
        col = 0
    if board[row][col] > 0:
        return solve(board, row, col + 1)  # recursively put values into board
    for num in range(1, N + 1):
        if possible(board, row, col, num):
            board[row][col] = num
            if solve(board, row, col + 1):
                return True
        board[row][col] = 0
    return False  # return False if there is no solution


# if there exist any solution, we will return filled board with solution, otherwise return Unsolvable
def solvable(board):
    if solve(board, 0, 0):
        return board
    else:
        errlabel.configure(text="no solution", font=custom_font)


# drawing 3x3 grid without values
def draw3x3(row, column, bgcolor):
    for i in range(3):
        for j in range(3):
            e = Entry(root, width=4, bg=bgcolor, justify="center", validate="key", validatecommand=(reg, "%P"),
                      font=custom_font)
            e.grid(row=row + i + 1, column=column + j + 1, sticky="nsew", padx=1, pady=1, ipady=10)
            cells[(row + i + 1, column + j + 1)] = e


# drawing table without values, setting colors
def draw9x9():
    buttons()  # adding buttons to the window
    color = "#0000EE"
    for row in range(1, 10, 3):
        for col in range(0, 9, 3):
            draw3x3(row, col, color)
            if color == "#0000EE":
                color = "#B23AEE"
            else:
                color = "#0000EE"


# clearing all values in table
def clearValues():
    errlabel.configure(text="", font=custom_font)  # reseting label texts
    solvedlabel.configure(text="", font=custom_font)  # reseting label texts
    for row in range(2, 11):  # deleting valuesin cells
        for col in range(1, 10):
            cell = cells[(row, col)]
            cell.delete(0, "end")


# putting values from table to list
def getValues():
    board = []
    errlabel.configure(text="", font=custom_font)
    solvedlabel.configure(text="", font=custom_font)
    for row in range(2, 11):
        rows = []
        for col in range(1, 10):
            val = cells[(row, col)].get()  # getting value from input
            if val == "":
                rows.append(0)
            else:
                rows.append(int(val))
        board.append(rows)
    updateValue(board)


# updating values in table
def updateValue(board):
    if solvable(board):
        for rows in range(2, 11):
            for col in range(1, 10):
                cells[(rows, col)].delete(0, "end")
                cells[(rows, col)].insert(0, board[rows - 2][col - 1])
        solvedlabel.configure(text="Sudoku solved", font=custom_font)
    else:
        errlabel.configure(text="no solution", font=custom_font)


# tips window
def tips():
    new = Toplevel()
    custom_font_2 = Font(family="Helvetica", size=12, weight="bold")
    new.title("rules")
    new.geometry("330x250")
    new.minsize(330, 250)
    new.maxsize(330, 250)
    solvedlabel.configure(text="", font=custom_font)
    tip1 = Label(new, text="Tip No. 1\n Click on squares to put values 1-9 into it\n", font=custom_font_2)
    tip1.grid(row=0)  # what is first button doing
    tip2 = Label(new, text="Tip No. 2\n Click on solve to fill table with values\n", font=custom_font_2)
    tip2.grid(row=10)  # what is second buton doing
    tip3 = Label(new, text="Tip No. 3\n Click on clear to remove values from table\n", font=custom_font_2)
    tip3.grid(row=20)  # what is third button doing
    tip4 = Label(new, text="Tip No. 4\n Click to generate random solvable puzzle\n", font=custom_font_2)
    tip4.grid(row=30)  # what is fourth button doing


# creating random solvable board
def ran():
    clearValues()
    board = np.zeros((9, 9), dtype=int)
    for row in range(9):  # looping board and filling cells with random values
        for col in range(9):
            val = random.randint(0, 9)
            if possible(board, row, col, val) and solve(board, row, col):  # checking if number can be there
                board[row][col] = val
            else:
                board[row][col] = 0
    board = [[int(ele) for ele in sub] for sub in board]  # configuration for solve button
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                board[i][j] = ""
    for rows in range(2, 11):
        for col in range(1, 10):
            cells[(rows, col)].delete(0, "end")
            cells[(rows, col)].insert(0, board[rows - 2][col - 1])


# Buttons for solve and clear table, tips and random
def buttons():
    btn = Button(root, command=getValues, text="solve", fg="black", width=10, font=custom_font)
    btn.grid(row=20, column=1, columnspan=6, pady=10)
    btn1 = Button(root, command=clearValues, text="clear", fg="black", width=10, font=custom_font)
    btn1.grid(row=20, column=4, columnspan=6, pady=10)
    btn2 = Button(root, command=tips, text="rules", fg="black", width=10, font=custom_font)
    btn2.grid(row=21, column=1, columnspan=6, pady=10)
    btn3 = Button(root, command=ran, text="random", width=10, font=custom_font)
    btn3.grid(row=21, column=4, columnspan=6, pady=10)


# main loop
def main():
    draw9x9()
    root.mainloop()


if __name__ == "__main__":
    main()
