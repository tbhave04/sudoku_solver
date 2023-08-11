import sys; args = sys.argv[1:]
puzzles = open(args[0], "r").read().splitlines()
import time

# optional helper function
def select_unassigned_var(assignment, variables, neighbors):
   minLen = 10
   minIndex = 0
   for i in variables:
      len_variables = len(variables[i])
      if len_variables == 1: 
         return i
      if assignment[i] == "." and len_variables < minLen:
         minLen = len_variables
         minIndex = i
   return minIndex

#optional helper function
def ordered_domain(var_index, variables, q_table):
   lst = list(variables[var_index])
   length = len(lst)
   if length == 1:
      return lst
   if length == 2:
      if (q_table[lst[0]] > q_table[lst[1]]):
         return lst
      else:
         return lst[::-1]
   else:
      d = {}
      for key in lst:
         d[key] = q_table[key]
      t = sorted(d, key = d.get)
      return t[::-1]

# optional helper function
def update_variables(value, var_index, assignment, variables, neighbors):
   for neighbor in neighbors[var_index]:
       if assignment[neighbor] == "." and len(variables[neighbor]) == 0:
          return False, variables

   deep = {k:{v for v in vals} for k,vals in variables.items() if k != var_index}
   for neighbor in neighbors[var_index]:
      if neighbor in deep and value in deep[neighbor]:
         deep[neighbor] -= {value}
   return True, deep
   
def solve(puzzle, neighbors):
   # initialize_ds function is optional helper function. You can change this part. 
   variables, puzzle, q_table = initialize_ds(puzzle, neighbors)  # q_table is quantity table {'1': number of value '1' occurred, ...}
   # print (puzzle)
   # print (variables)
   return recursive_backtracking(puzzle, variables, neighbors, q_table)

# optional helper function: you are allowed to change it
def recursive_backtracking(assignment, variables, neighbors, q_table):
   if assignment.find('.') == -1:
      return assignment
   var = select_unassigned_var(assignment, variables, neighbors)
   temp = ordered_domain(var, variables, q_table)
   for num in temp:
      valid, temp_variables = update_variables(num, var, assignment, variables, neighbors)
      if valid:
         copy  = assignment[:var] + str(num) + assignment[1+var: ]
         q_table[num] += 1
         result = recursive_backtracking(copy, temp_variables, neighbors, q_table)
         if result != None:
            return result
         else:
            q_table[num] -= 1
   return None

def sudoku_csp(n=9):
   lst = []
   temp = []
   for i in range (0, 82):
      if i%n == 0:
         lst.append(temp)
         temp = []
      temp.append(i)
   
   for i in range (0,n-1):
      add = n
      temp = [i]
      for j in range (0,n-1):
         temp.append(i+add)
         add = add + n
      lst.append(temp)
   lst.append([8,17,26,35,44,53,62,71,80])

   box1 = [0,1,2,9,10,11,18,19,20]
   box2 = [27,28,29,36,37,38,45,46,47]
   box3 = [54,55,56,63,64,65, 72,73,74]
   lst.append(box1)
   lst.append(box2)
   lst.append(box3)
   for i in range(1,3):
      temp = []
      temp2 = []
      temp3 = []
      for num in box1:
         temp.append(num+3*i)
      for num in box2:
         temp2.append(num+3*i)
      for num in box3:
         temp3.append(num+3*i)
      lst.append(temp)
      lst.append(temp2)
      lst.append(temp3)
   return lst[1:]

def sudoku_neighbors(csp_table): # neighbors numbers are type int {0:[0, 1, 2, 3, 4, ...., 8, 9, 18, 27, 10, 11, 19, 20], 1:
   neighbors = {}
   for index in range(81):
      neighbors[index] = set()
      for line in csp_table:
         if index in line:
            neighbors[index].update(line)
      neighbors[index] -= {index}
   return neighbors

# Optional helper function
def initialize_ds(puzzle, neighbors):
   variables = {}
   for index in neighbors:
      if puzzle[index] == ".":
         variables[index] = set()
         lst = [str(i) for i in range(1, int(len(puzzle)**.5)+1)]
         variables[index].update(lst)
         temp = set()
         for num in neighbors[index]:
            if puzzle[num] != ".":
               temp.add(puzzle[num])
         variables[index] = variables[index] - temp
         if len(variables[index]) == 1:
            puzzle = puzzle[:index] + variables[index].pop() + puzzle[index+1:]
            del variables[index]

   q_table = {}
   for i in range(1,int(len(puzzle)**.5)+1):
      q_table[str(i)] = puzzle.count(str(i))

   return variables, puzzle, q_table


# sum of all ascii code of each char - (length of the solution * ascii code of min char)
def checksum(solution):
   output = 0
   for i in solution:
      output = output + ord(i)
   return output - (ord('1') * len(solution))

def main():
   csp_table = sudoku_csp()   # rows, cols, and sub_blocks
   neighbors = sudoku_neighbors(csp_table)   # each position p has its neighbors {p:[positions in same row/col/subblock], ...}
   start_time = time.time()
   for line, puzzle in enumerate(puzzles):
      line, puzzle = line+1, puzzle.rstrip()
      if line == 61:
         continue
      print ("{}: {}".format(line, puzzle)) 
      solution = solve(puzzle, neighbors)
      if solution == None:print ("No solution found."); break
      print ("{}{} {}".format(" "*(len(str(line))+2), solution, checksum(solution)))
   print ("Duration:", (time.time() - start_time))

if __name__ == '__main__': main()
# Required comment: Your name, Period #, 2022
# Check the example below. You must change the line below before submission.
# Tanvi Bhave, Period 7, 2021
