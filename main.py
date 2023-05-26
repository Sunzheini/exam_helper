from support.the_gui import ExamHelperGui


class MainController:
    def __init__(self):
        self.new_gui = ExamHelperGui()

    def run(self):
        self.new_gui.run()


connection = MainController()
connection.run()
