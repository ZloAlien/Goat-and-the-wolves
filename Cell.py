# Ячейка игровой клетки
class Cell:
    # Возможные состояния игровой клетки:
    #   volf - волк
    #   koz - козлик
    #   free - свободна

    def __init__( self, row, column ):
        self.row = row
        self.column = column
        self.state = 'free'
        self.markedRed = False
        self.markedGreen = False
        