
input_board = [
	[0, 0, 6, 0, 0, 2, 3, 0, 0],
	[0, 5, 0, 0, 0, 6, 0, 9, 1],
	[0, 0, 9, 5, 0, 1, 4, 6, 2],
	[0, 3, 7, 9, 0, 5, 0, 0, 0],
	[5, 8, 1, 0, 2, 7, 9, 0, 0],
	[0, 0, 0, 4, 0, 8, 1, 5, 7],
	[0, 0, 0, 2, 6, 0, 5, 4, 0],
	[0, 0, 4, 1, 5, 0, 6, 0, 9],
	[9, 0, 0, 8, 7, 4, 2, 1, 0]
]


def print_board(board):
	for row in range(len(board)):
		if row%3 == 0 and row != 0:
			print("- - - - - - - - - - - -")

		for col in range(len(board[0])):
			if col%3 == 0 and col != 0:
				print(" | ", end="")
			if col == 8:
				print(board[row][col])
			else:
				print(board[row][col], end=" ")


def find_empty_slot(board):
	for row in range(len(board)):
		for col in range(len(board[0])):
			if board[row][col] == 0:
				return (row, col)
	return None


def is_valid(board, num, pos):

	# Check Rows
	for col in range(len(board[0])):
		if board[pos[0]][col] == num:
			return False

	# Check Coloumns
	for row in range(len(board)):
		if board[row][pos[1]] == num:
			return False

	# Check Square box
	box_x = pos[1] // 3 
	box_y = pos[0] // 3
	for row in range(box_y * 3, box_y *3 + 3):
		for col in range(box_x * 3, box_x * 3 + 3):
			if board[row][col] == num:
				return False
	return True


def solve(board):
	find_empty = find_empty_slot(board)
	if not find_empty:
		return True
	else:
		row, col = find_empty

	for num in range(1,10):
		if is_valid(board, num, (row, col)):
			board[row][col] = num
			if solve(board):
				return True
			board[row][col] = 0
	return False


print("Input Board")
print_board(input_board)
print("--------------------")
solve(input_board)
print("Solved Board")
print_board(input_board)
