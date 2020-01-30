from tkinter import messagebox, Frame, Button, TOP, BOTTOM, LEFT, RIGHT, X, StringVar, Spinbox, Label, SUNKEN

# Отображение игрового поля
class View( Frame ):
    # Инициализируем окно, добавляем кнопки и поля настроек в самом низу
    def __init__( self, model, controller, parent = None ):
        Frame.__init__( self, parent )
        self.model = model
        self.controller = controller
        self.controller.setView( self )
        self.createBoard()

        panel = Frame( self )
        panel.pack( side = BOTTOM, fill = X )

        Button( panel, text = 'Новая игра', command = self.controller.startNewGame ).pack( side = BOTTOM )

        self.mineCount = 1
        self.rowCount = 7
        self.columnCount = 5

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
        if 'board' in locals(): 
			# очистка доски
            self.board.pack_forget()
            self.board.destroy()
			
			# количество строк, столбцов и мин - как в модели
            self.rowCount.set( self.model.rowCount )
            self.columnCount.set( self.model.columnCount )
            self.mineCount.set( self.model.mineCount )

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
            for col in range( СС ):
                btn = Button(
                    line,
                    width = 2,
                    height = 1,
                    command = lambda row = row, column = col: self.controller.onLeftClick( row, col ),
                    padx = 0,
                    pady = 0
                )
                btn.pack( side = LEFT )
                btn.bind(
                    '<Button-3>',
                    lambda e, row = row, column = col: self.controller.onRightClick( row, col )
                )
                self.buttonsRow.append( btn )

            self.buttonsTable.append( self.buttonsRow )

    # Выводсообщения о выигрыше
    def showWinMessage( self ):
        messagebox.showinfo( 'Поздравляем!', 'Вы победили!' )

    # Вывод сообщения о проигрыше
    def showGameOverMessage( self ):
        messagebox.showinfo( 'Игра окончена!', 'Вы проиграли!' )
