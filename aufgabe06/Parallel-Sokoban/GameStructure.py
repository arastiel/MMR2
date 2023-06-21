import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
from GameWindow import MainWindow
from GameEngine import Engine
from Player import Player
from Box import Box


class GameStructure():
    def __init__(self):
        super(GameStructure, self).__init__()

        self.init_components()  # start window,engine

        self.new_game()

    def init_components(self):
        self.main_window = MainWindow()
        self.players = [Player(5, 2), Player(2, 12), Player(12, 5), Player(14, 17)]
        self.boxes = [Box(4, 2), Box(2, 13), Box(12, 4), Box(14, 16)]
        self.goals = [Box(0, 6), Box(6, 18), Box(16, 0), Box(18, 12)]
        self.engine = Engine(self.main_window)
        self.main_window.keyPressEvent = self.catch_input

        # Menu connection
        self.main_window.winScreen.resetButton.clicked.connect(self.reset_game)

    def create_map(self):
        self.main_window.init_maps()
        # 4 Maps
        for map in self.main_window.maps:
            self.engine.draw_map(map, qc.Qt.black)

    def reset_game(self):
        #reset old positions
        for player in self.players:
            self.engine.draw_box((player.x, player.y), qc.Qt.white)
        for box in self.boxes:
            self.engine.draw_box((box.x, box.y), qc.Qt.white)

        #init positions
        self.players = [Player(5, 2), Player(2, 12), Player(12, 5), Player(14, 17)]
        self.boxes = [Box(4, 2), Box(2, 13), Box(12, 4), Box(14, 16)]
        self.goals = [Box(0, 6), Box(6, 18), Box(16, 0), Box(18, 12)]

        # draw player start pos
        for player in self.players:
            self.engine.draw_player(player.x, player.y)

        # draw boxes start pos
        for box in self.boxes:
            self.engine.draw_box((box.x, box.y), qc.Qt.yellow)

        self.main_window.winScreen.close()

    def new_game(self):
        self.create_map()

        # draw player start pos
        for player in self.players:
            self.engine.draw_player(player.x, player.y)

        # draw boxes start pos
        for box in self.boxes:
            self.engine.draw_box((box.x, box.y), qc.Qt.yellow)

        self.main_window.newAction.triggered.connect(self.reset_game)

    def you_win(self):
        if self.engine.check_win(self.boxes, self.goals):
            self.main_window.showWin()
        else:
            print("no win")

    def catch_input(self, event):
        if event.key() == qc.Qt.Key_Right:
            self.engine.move(self.players, self.boxes, self.goals, "RIGHT")
        if event.key() == qc.Qt.Key_Left:
            self.engine.move(self.players, self.boxes, self.goals, "LEFT")
        if event.key() == qc.Qt.Key_Up:
            self.engine.move(self.players, self.boxes, self.goals, "UP")
        if event.key() == qc.Qt.Key_Down:
            self.engine.move(self.players, self.boxes, self.goals, "DOWN")

        self.you_win()
