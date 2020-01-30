import random
#from tkinter import *
from tkinter import messagebox, Frame, Button, TOP, BOTTOM, LEFT, RIGHT, X, StringVar, Spinbox, Label

MIN_ROW_COUNT = 7
MAX_ROW_COUNT = 7

MIN_COLUMN_COUNT = 5
MAX_COLUMN_COUNT = 5

MIN_MINE_COUNT = 1
MAX_MINE_COUNT = 800

class MinesweeperCell:
    # Возможные состояния игровой клетки:
    #   volf - волк
    #   free - свободна
    #   koz - козлик

    def __init__( self, row, column ):
        self.row = row
        self.column = column
        self.state = 'volf'
        self.mined = False
        self.counter = 0

    markSequence = [ 'volf', 'koz']
    def nextMark( self ):
        if self.state in self.markSequence:
            stateIndex = self.markSequence.index( self.state )
            self.state = self.markSequence[ ( stateIndex + 1 ) % len( self.markSequence ) ]

    def open( self ):
        if self.state != 'koz':
            self.state = 'free'


class MinesweeperModel:
    def __init__( self ):
        self.startGame()

    def startGame(self):
        self.rowCount = 7
        self.columnCount = 5
        self.mineCount = 0 ### удалить

        self.firstStep = True
        self.gameOver = False
        self.cellsTable = []	# добавляем строки
        for row in range( self.rowCount ):
            cellsRow = []		# добавляем столбцы
            if row % 2 != 0:
                CRange = self.columnCount - 1
            else:
                CRange = self.columnCount
            for column in range( CRange ):
                cellsRow.append( MinesweeperCell( row, column ) )
            self.cellsTable.append( cellsRow )

    def getCell( self, row, column ):
        if row < 0 or column < 0 or self.rowCount <= row or self.columnCount <= column:
            return None

        return self.cellsTable[ row ][ column ]

    def isWin( self ):
        for row in range( self.rowCount ):
            for column in range( self.columnCount ):
                cell = self.cellsTable[ row ][ column ]
                if not cell.mined and ( cell.state != 'free' and cell.state != 'koz' ):
                    return False

        return True

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
		
###########################################################

class MinesweeperView( Frame ):
    # Инициализируем окно, добавляем кнопки и поля настроек в самом низу
    def __init__( self, model, controller, parent = None ):
        Frame.__init__( self, parent )
        self.model = model
        self.controller = controller
        self.controller.setView( self )
        self.createBoard()

        panel = Frame( self )
        panel.pack( side = BOTTOM, fill = X )

        Button( panel, text = 'Новая игра', command = self.controller.startNewGame ).pack( side = RIGHT )

        self.mineCount = StringVar( panel )
        self.mineCount.set( self.model.mineCount )
        Spinbox(
            panel,
            from_ = MIN_MINE_COUNT,
            to = MAX_MINE_COUNT,
            textvariable = self.mineCount,
            width = 5
        ).pack( side = RIGHT )
        Label( panel, text = ' Количество мин: ' ).pack( side = RIGHT )

        self.rowCount = StringVar( panel )
        self.rowCount.set( self.model.rowCount )
        Spinbox(
            panel,
            from_ = MIN_ROW_COUNT,
            to = MAX_ROW_COUNT,
            textvariable = self.rowCount,
            width = 5
        ).pack( side = RIGHT )

        Label( panel, text = ' x ' ).pack( side = RIGHT )

        self.columnCount = StringVar( panel )
        self.columnCount.set( self.model.columnCount )
        Spinbox(
            panel,
            from_ = MIN_COLUMN_COUNT,
            to = MAX_COLUMN_COUNT,
            textvariable = self.columnCount,
            width = 5
        ).pack( side = RIGHT )
        Label( panel, text = 'Размер поля: ' ).pack( side = RIGHT )

    def syncWithModel( self ):
        for row in range( self.model.rowCount ):
            for column in range( self.model.columnCount ):
                cell = self.model.getCell( row, column )
                if cell:
                    btn = self.buttonsTable[ row ][ column ]

                    if self.model.isGameOver() and cell.mined:
                        btn.config( bg = 'black', text = '' )

                    if cell.state == 'volf':
                        btn.config( text = 'V' )
                    elif cell.state == 'free':
                        btn.config( relief = SUNKEN, text = '' )
                        if cell.counter > 0:
                            btn.config( text = cell.counter )
                        elif cell.mined:
                            btn.config( bg = 'red' )
                    elif cell.state == 'koz':
                        btn.config( text = 'K' )

    def blockCell( self, row, column, block = True ):
        btn = self.buttonsTable[ row ][ column ]
        if not btn:
            return

        if block:
            btn.bind( '<Button-1>', 'break' )
        else:
            btn.unbind( '<Button-1>' )

    # Возвращает игровые настройки
    def getGameSettings( self ):
        return self.rowCount.get(), self.columnCount.get(), self.mineCount.get()

    # Создание игровой доски
    def createBoard( self ):
        try:
			# очистка доски
            self.board.pack_forget()
            self.board.destroy()
			
			# количество строк, столбцов и мин - как в модели
            self.rowCount.set( self.model.rowCount )
            self.columnCount.set( self.model.columnCount )
            self.mineCount.set( self.model.mineCount )
        except:
            pass

        self.board = Frame( self )
        self.board.pack()
        self.buttonsTable = []
        for row in range( self.model.rowCount ):
            line = Frame( self.board )
            line.pack( side = TOP )
            self.buttonsRow = []
            СС = self.model.columnCount
            if row % 2 == 0:
                СС = self.model.columnCount - 1
            else:
                СС = self.model.columnCount
            for column in range( СС ):
                btn = Button(
                    line,
                    width = 2,
                    height = 1,
                    command = lambda row = row, column = column: self.controller.onLeftClick( row, column ),
                    padx = 0,
                    pady = 0
                )
                btn.pack( side = LEFT )
                btn.bind(
                    '<Button-3>',
                    lambda e, row = row, column = column: self.controller.onRightClick( row, column )
                )
                self.buttonsRow.append( btn )

            self.buttonsTable.append( self.buttonsRow )

    # Выводсообщения о выигрыше
    def showWinMessage( self ):
        messagebox.showinfo( 'Поздравляем!', 'Вы победили!' )

    # Вывод сообщения о проигрыше
    def showGameOverMessage( self ):
        messagebox.showinfo( 'Игра окончена!', 'Вы проиграли!' )

###########################################################

class MinesweeperController:
    def __init__( self, model ):
        self.model = model

    def setView( self, view ):
        self.view = view

    def startNewGame( self ):
        gameSettings = self.view.getGameSettings()
        try:
            self.model.startGame( *map( int, gameSettings ) )
        except:
            self.model.startGame( self.model.rowCount, self.model.columnCount, self.model.mineCount )

        self.view.createBoard()

    def onLeftClick( self, row, column ):
        self.model.openCell( row, column )
        self.view.syncWithModel()
        if self.model.isWin():
            self.view.showWinMessage()
            self.startNewGame()
        elif self.model.isGameOver():
            self.view.showGameOverMessage()
            self.startNewGame()

    def onRightClick( self, row, column ):
        self.model.nextCellMark( row, column )
        self.view.blockCell( row, column, self.model.getCell( row, column ).state == 'koz' )
        self.view.syncWithModel()
		
###########################################################

model = MinesweeperModel()
controller = MinesweeperController( model );
view = MinesweeperView( model, controller )
view.pack()
view.mainloop()
