# Jonathan Thimesch
# ID: D696H345

from copy import deepcopy

class Puzzle():
    def __init__(self, preset=None):
        # Preset can be used to hard code puzzle layouts
        if preset:
            s = preset
        else:
            s = [[input(f'Number for coord ({j}, {i}): ') for i in range(0, 3)] 
                        for j in reversed(range(0, 3))]
        try:
            self.state = [[int(i) for i in row] for row in s]
        except TypeError:
            raise SystemExit('Inputs cannot be blank!')
        except ValueError:
            raise SystemExit('Inputs must be numeric!')
        flattenedRows = [i for row in self.state for i in row]
        if sorted(flattenedRows) != list(range(0, 9)):
            raise SystemExit('Inputs must be in range 0 to 8!')

    def __str__(self):
        s = ''
        endChar = '\n'
        for i in range(0, 3):
            rowAsStr = ' '.join([str(j) for j in self.state[i]])
            if i == 2:
                endChar = ''
            s += rowAsStr + endChar
        return s

    def __eq__(self, comp):
        if type(comp) is type(self):
            return self.__dict__ == comp.__dict__
        return False
        
    def __ne__(self, comp):
        return not self.__eq__(comp)
        
    def __hash__(self):
        uniqueID = 0
        factor = 1
        for i in range(0,3):
            for j in range(0,3):
                uniqueID += self.state[i][j] * factor
                factor *= 123
        return uniqueID
        
    def getCoordsOfBlank(self):
        for i in range(0, 3):
            for j in range(0, 3):
                if self.state[i][j] == 0:
                    x = j
                    y = i
        return (x, y)
        
    def getNeighbors(self):
        listOfNeighbors = []
        x, y = self.getCoordsOfBlank()
        if x > 0:
            right = deepcopy(self)
            right.state[y][x] = right.state[y][x - 1]
            right.state[y][x - 1] = 0
            listOfNeighbors.append(right)
        if y > 0:
            down = deepcopy(self)
            down.state[y][x] = down.state[y - 1][x]
            down.state[y - 1][x] = 0
            listOfNeighbors.append(down)
        if x < 2:
            left = deepcopy(self)
            left.state[y][x] = left.state[y][x + 1]
            left.state[y][x + 1] = 0
            listOfNeighbors.append(left)
        if y < 2:
            up = deepcopy(self)
            up.state[y][x] = up.state[y + 1][x]
            up.state[y + 1][x] = 0
            listOfNeighbors.append(up)
        return listOfNeighbors

    def doManhattanDistance(self, initial, goal):
        sum = 0
        for i in range(0, 3):
            for j in range(0, 3):
                space = initial.state[i][j]
                for m in range(0, 3):
                    for n in range(0, 3):
                        if space == goal.state[m][n]:
                            sum += abs(i - m) + abs(j + n)
        return sum
    
    def solve(self, goal):
        # Algorithm for A* Method
        # Modified from StackOverflow
        closedList = list()      
        openList = [self]
        
        gScore = {self : 0}
        fScore = {self : gScore[self] + self.doManhattanDistance(self, goal)}
        step = 0
        while (len(openList) > 0):
            step += 1
            current = None
            for node in openList:
                if current is None or fScore[node] < fScore[current]:
                    current = node

            print(f'Step {step}:\n' + str(current))

            if current == goal:
                return
                
            openList.remove(current)
            closedList.append(current)

            for neighbor in current.getNeighbors():
                if neighbor in closedList:
                    continue
                tempGScore = gScore[current] + 1
                
                # Short circuiting, don't change
                if neighbor not in openList or tempGScore < gScore[neighbor]:
                    gScore[neighbor] = tempGScore
                    fScore[neighbor] = gScore[neighbor] + self.doManhattanDistance(neighbor, goal)
                    if neighbor not in openList:
                        openList.append(neighbor)

if __name__ == '__main__':
    print('Start Puzzle:')
    start = Puzzle()
    print('Goal Puzzle:')
    goal = Puzzle()
    start.solve(goal)