from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


class Engine():
    def __init__(self, MainWindow):
        self.mainwindow = MainWindow

    def draw_player(self, x, y):
        player_canvas = self.mainwindow.gridcell_canvas[x][y]
        player_label = self.mainwindow.gridcell_label[x][y]

        self.painter = qg.QPainter(player_canvas)
        self.painter.setBrush(qc.Qt.green)
        self.painter.drawEllipse(0, 0, player_label.size().width(), player_label.size().width())
        self.painter.end()

        player_label.setPixmap(player_canvas)

    def draw_box(self, coords, color):
        canvas = self.mainwindow.gridcell_canvas[coords[0]][coords[1]]
        label = self.mainwindow.gridcell_label[coords[0]][coords[1]]

        self.painter = qg.QPainter(canvas)
        self.painter.fillRect(0, 0, self.mainwindow.box_size, self.mainwindow.box_size, color)
        self.painter.end()

        label.setPixmap(canvas)

    def draw_map(self, boxes, color):
        for coords in boxes:
            self.draw_box(coords, color)

    def move(self, players, boxes, goals, direction):
        for index in range(4):
            if direction == "LEFT":
                if (players[index].x, players[index].y - 1) == (goals[index].x, goals[index].y): #player cant move into goal, fixes some problems
                    continue
                if (players[index].x, players[index].y - 1) not in self.mainwindow.maps[index]: #if player move not in wall
                    if ((boxes[index].x, boxes[index].y) == (players[index].x, players[index].y - 1)):  # if box is left neighbour
                        if (boxes[index].x, boxes[index].y - 1) not in self.mainwindow.maps[index]:  # check if wall is neighbour of box
                            # Box draw reset old pos
                            self.draw_box((boxes[index].x, boxes[index].y), qc.Qt.white)
                            # draw new pos
                            boxes[index].y -= 1
                            self.draw_box((boxes[index].x, boxes[index].y), qc.Qt.yellow)

                            # (Player) draw reset old pos
                            self.draw_box((players[index].x, players[index].y), qc.Qt.white)
                            # draw new pos
                            players[index].y -= 1
                            self.draw_player(players[index].x, players[index].y)

                    else:  # no box as left neighbour
                        # draw reset old pos
                        self.draw_box((players[index].x, players[index].y), qc.Qt.white)
                        # draw new pos
                        players[index].y -= 1
                        self.draw_player(players[index].x, players[index].y)

            if direction == "RIGHT":
                if (players[index].x, players[index].y + 1) == (goals[index].x, goals[index].y):
                    continue
                if (players[index].x, players[index].y + 1) not in self.mainwindow.maps[index]:
                    if ((boxes[index].x, boxes[index].y) == (players[index].x, players[index].y + 1)):  # if box is right neighbour
                        if (boxes[index].x, boxes[index].y + 1) not in self.mainwindow.maps[index]:  # check if wall is neighbour of box
                            # Box draw reset old pos
                            self.draw_box((boxes[index].x, boxes[index].y), qc.Qt.white)
                            # draw new pos
                            boxes[index].y += 1
                            self.draw_box((boxes[index].x, boxes[index].y), qc.Qt.yellow)

                            # (Player) draw reset old pos
                            self.draw_box((players[index].x, players[index].y), qc.Qt.white)
                            # draw new pos
                            players[index].y += 1
                            self.draw_player(players[index].x, players[index].y)
                    else:
                        # draw reset old pos
                        self.draw_box((players[index].x, players[index].y), qc.Qt.white)
                        # draw new pos
                        players[index].y += 1
                        self.draw_player(players[index].x, players[index].y)

            if direction == "DOWN":
                if (players[index].x + 1, players[index].y) == (goals[index].x, goals[index].y):
                    continue
                if (players[index].x + 1, players[index].y) not in self.mainwindow.maps[index]:
                    if ((boxes[index].x, boxes[index].y) == (players[index].x + 1, players[index].y)):  # if box is down neighbour
                        if (boxes[index].x + 1, boxes[index].y) not in self.mainwindow.maps[index]:  # check if wall is neighbour of box
                            # Box draw reset old pos
                            self.draw_box((boxes[index].x, boxes[index].y), qc.Qt.white)
                            # draw new pos
                            boxes[index].x += 1
                            self.draw_box((boxes[index].x, boxes[index].y), qc.Qt.yellow)

                            # (Player) draw reset old pos
                            self.draw_box((players[index].x, players[index].y), qc.Qt.white)
                            # draw new pos
                            players[index].x += 1
                            self.draw_player(players[index].x, players[index].y)
                    else:
                        # draw reset old pos
                        self.draw_box((players[index].x, players[index].y), qc.Qt.white)
                        # draw new pos
                        players[index].x += 1
                        self.draw_player(players[index].x, players[index].y)

            if direction == "UP":
                if (players[index].x - 1, players[index].y) == (goals[index].x, goals[index].y):
                    continue
                if (players[index].x - 1, players[index].y) not in self.mainwindow.maps[index]:
                    if ((boxes[index].x, boxes[index].y) == (players[index].x - 1, players[index].y)):  # if box is down neighbour
                        if (boxes[index].x - 1, boxes[index].y) not in self.mainwindow.maps[index]:  # check if wall is neighbour of box
                            # Box draw reset old pos
                            self.draw_box((boxes[index].x, boxes[index].y), qc.Qt.white)
                            # draw new pos
                            boxes[index].x -= 1
                            self.draw_box((boxes[index].x, boxes[index].y), qc.Qt.yellow)

                            # (Player) draw reset old pos
                            self.draw_box((players[index].x, players[index].y), qc.Qt.white)
                            # draw new pos
                            players[index].x -= 1
                            self.draw_player(players[index].x, players[index].y)
                    else:
                        # draw reset old pos
                        self.draw_box((players[index].x, players[index].y), qc.Qt.white)
                        # draw new pos
                        players[index].x -= 1
                        self.draw_player(players[index].x, players[index].y)
            #if (boxes[index].x, boxes[index].y) == (goals[index].x, goals[index].y):
            #    print("test")
            #print(boxes[index].x, boxes[index].y)
            #print(goals[index].x, goals[index].y)


    def check_win(self, boxes, goals):
        for index in range(4):
            if (boxes[index].x, boxes[index].y) != (goals[index].x, goals[index].y):
                return False
        return True
