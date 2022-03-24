from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)  # required for setup
    win = QMainWindow()
    screen = app.primaryScreen()
    screen_width = screen.size().width()
    screen_height = screen.size().height()
    # set window to middle of screen
    # TODO this should probably be set w/ variables, also the sizes need to be adjusted later
    win.setGeometry(int((screen_width / 2) - (screen_width / 4)), int((screen_height / 2) - (screen_height / 4)),
                    int(screen_width/2), int(screen_height/2))
    win.setWindowTitle("Sudoku Solver")

    win.show()
    sys.exit(app.exec_())


window()
