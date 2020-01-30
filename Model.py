import Cell

# Модель игрового поля
class Model:

    # При запуске программы начинаем игру
    def __init__( self ):
        self.startGame()

    # Начинаем игру
    def startGame(self):
        self.rowCount = 7
        self.columnCount = 5

        self.firstStep = True
        self.gameOver = False
        # Создаём клетки доски
        self.cellsTable = []	# добавляем строки
        for row in range( self.rowCount ):
            cellsRow = []		# добавляем столбцы
            for column in range( self.getCRange(row) ):
                cellsRow.append( Cell.Cell( row, column ) )
            self.cellsTable.append( cellsRow )
        # Расставляем фигуры
        #self.SetVolfKoz()

    # Определяем сколько столбцой в строке
    def getCRange(self, row):
        if row % 2 != 0:
            return self.columnCount - 1
        else:
            return self.columnCount

    # Получаем состояние ячейки
    def getCell( self, row, column ):
        if row < 0 or column < 0 or self.rowCount <= row or self.getCRange(row) <= column:
            return None
        return self.cellsTable[ row ][ column ]

    def isWin( self ):
        for row in range( self.rowCount ):
            for column in range( self.columnCount ):
                cell = self.cellsTable[ row ][ column ]
                if not cell.mined and ( cell.state != 'free' and cell.state != 'koz' ):
                    return False

        return True

    # Если игра окончена, то присваиваем значение соответствующей переменной
    def isGameOver( self ):
        return self.gameOver

    def openCell( self, row, column ):
        cell = self.getCell( row, column )
        if not cell:
            return

        cell.open()

        if cell.mined:
            self.gameOver = True
            return
        
        if self.firstStep:
            self.firstStep = False
            self.SetVolfKoz()

        cell.counter = self.countMinesAroundCell( row, column )
        if cell.counter == 0:
            neighbours = self.getCellNeighbours( row, column )
            for n in neighbours:
                if n.state == 'volf':
                    self.openCell( n.row, n.column )

    def nextCellMark( self, row, column ):
        cell = self.getCell( row, column )
        if cell:
            cell.nextMark()

    # Ставим козлика и волков на начальные позиции
    def SetVolfKoz( self ):
        cell = self.getCell( 6, 3 )
        cell.state == 'volf'
        cell = self.getCell( 7, 1 )
        cell.state == 'volf'
        cell = self.getCell( 7, 2 )
        cell.state == 'volf'
        cell = self.getCell( 7, 3 )
        cell.state == 'volf'
        cell = self.getCell( 7, 4 )
        cell.state == 'volf'

        cell = self.getCell( 3, 3 )
        cell.state == 'koz'

    def countMinesAroundCell( self, row, column ):
        neighbours = self.getCellNeighbours( row, column )
        return sum( 1 for n in neighbours if n.mined )

    def getCellNeighbours( self, row, column ):
        neighbours = []
        for r in range( row - 1, row + 2 ):
            neighbours.append( self.getCell( r, column - 1 ) )
            if r != row:
                neighbours.append( self.getCell( r, column ) )
            neighbours.append( self.getCell( r, column + 1 ) )

        return filter( lambda n: n is not None, neighbours )
