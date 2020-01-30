import Model
import View
import Controller

#  Запуск игры
model = Model.Model()
controller = Controller.Controller( model )
view = View.View( model, controller )
view.pack()
view.mainloop()
