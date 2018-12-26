import heapq

class Board():

	def __init__(self,grid,space_cords = None):
		self.grid = grid
		if space_cords is None:
			self.space_cords = self.__locate_space()
		else:
			self.space_cords = space_cords
		self.string_representation = self.__str_representation()

	def iter(self):
		space_x,space_y = self.space_cords
		for delta in [(1,0),(0,1),(0,-1),(-1,0)]:
			new_space_x = space_x + delta[0]
			new_space_y = space_y + delta[1]
			if(self.__possible(new_space_x,new_space_y)):
				new_grid = [row[:] for row in self.grid]
				temp = new_grid[space_x][space_y]
				new_grid[space_x][space_y] = new_grid[new_space_x][new_space_y]
				new_grid[new_space_x][new_space_y] = temp
				yield Board(new_grid,space_cords = (new_space_x,new_space_y))

	def iter_grid_sequential(self):
		for i in range(len(self.grid)):
			for j in range(len(self.grid[i])):
				yield (i,j,self.grid[i][j])

	def __locate_space(self):
		for (i,j,element) in self.iter_grid_sequential():
			if element == ' ':
				return (i,j)

	def __possible(self,i,j):
		return  i>=0 and i< len(self.grid) and j>=0 and j<len(self.grid[0])

	def __str_representation(self):
		arr = []
		for (i,j,element) in self.iter_grid_sequential():
			arr.append(str(element))
		return "".join(arr)

	def __eq__(self, other):		
		return self.string_representation == other.string_representation

	def __str__(self):
		output = []
		for i in range(3):
			output.append(self.grid[i].__str__())

		return "\n".join(output)

	__repr__ = __str__

class State():

	def __init__(self,id,pid,depth,board):
		self.id = id
		self.pid = pid
		self.depth = depth
		self.board = board
		self.heuristic = self.calcHeuristic()
		self.priority = self.depth + self.heuristic


	def __lt__(self,other):
		return self.priority < other.priority


	def calcHeuristic(self):
		heuristic = 0
		for i in range(3):
			for j in range(3):
				og_i,og_j = map[self.board.grid[i][j]]
				# manhatten heuristics
				heuristic += abs(i-og_i) + abs(j-og_j)

		return heuristic

def solvable(grid):
	flatten = [x for row in grid for x in row if x!= ' '] 
	inv_count = 0
	n = len(flatten)

	for i in range(n):
		for j in range(i,n):
			if flatten[i] > flatten[j]:
				inv_count+=1 

	return inv_count%2  == 0


def solver(initial_grid):
	if not solvable(initial_grid):
		print("Cannot solve the puzzle..")
		return 	
	current_id = 0
	intial_state = State(id = current_id,pid = -1,depth = 0,board = Board(initial_grid))

	visited_game_grids = set()
	visited_game_grids.add(intial_state.board.string_representation)

	explored_states = [intial_state]
	pq = [intial_state]

	final_board = Board( [[1,2,3],[4,5,6],[7,8,' ']])
	final_state = None
	while len(pq)>0 :
		state = heapq.heappop(pq)

		if(state.board == final_board):
			final_state = state
			break

		for new_board in state.board.iter():
			if  new_board.string_representation not in visited_game_grids:
				visited_game_grids.add(new_board.string_representation)
				current_id+=1
				new_state = State(id = current_id,pid = state.id,depth = state.depth + 1 , board = new_board)
				heapq.heappush(pq,new_state)
				explored_states.append(new_state)

	if final_state == None:
		print("Cannot solve the puzzle..")
	else:
		moves = []
		state = final_state

		while(state.pid != -1):
			moves.append(state.board)
			state = explored_states[state.pid]

		moves.append(state.board)
		moves.reverse()

		for board in moves[:-1]:
			print(board)
			print("\nthen..\n")

		print(moves[-1],end="\nDone!!\n")



if __name__ == "__main__":
	map = dict()
	val = 1
	for i in range(3):
		for j in range(3):
			if i!=2 or j!=2:
				map[val]=(i,j)
				val+=1
	map[' ']=(2,2)

	initial_grid = [ [' ',3,1], [4,2,5],[7,8,6]]
	solver(initial_grid)