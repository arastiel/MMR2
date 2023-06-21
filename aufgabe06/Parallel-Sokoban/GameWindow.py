from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

class WinScreen(qw.QMainWindow):
    def __init__(self, mainWindow):
        super(WinScreen, self).__init__()

        self.mainWindow = mainWindow
        self.setGeometry(300, 300, 350, 250)

        self.label = qw.QLabel("You Win!")
        self.label.setFont(qg.QFont('Arial', 100))

        self.exitButton = qw.QPushButton("Exit")
        self.exitButton.clicked.connect(self.closeAll)

        self.resetButton = qw.QPushButton("Reset")

        self.layout = qw.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.exitButton)
        self.layout.addWidget(self.resetButton)

        self.centWidget = qw.QWidget()
        self.centWidget.setLayout(self.layout)

        self.setCentralWidget(self.centWidget)

    def closeAll(self):
        self.close()
        self.mainWindow.close()



class MainWindow(qw.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        # Main Widget
        self.gamegrid()

        self.exitAction = qw.QAction(qg.QIcon('Icons/shutdown.png'), 'Exit', self)  # Toolbar
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

        self.newAction = qw.QAction(qg.QIcon('Icons/new.png'), 'New', self)  # Toolbar
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setStatusTip('New Game')

        self.statusBar()

        # Menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.exitAction)
        fileMenu.addAction(self.newAction)

        # Toolbar
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(self.exitAction)
        toolbar.addAction(self.newAction)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Parallel Sokoban')

        self.winScreen = WinScreen(self)

        self.show()

    def showWin(self):
        self.winScreen.show()

    def gamegrid(self):
        self.grid_x = 19
        self.box_size = 49  #px size for the canvas/label
        self.centralwidget = qw.QWidget()
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setStyleSheet("background-color: black")

        self.gridLayout = qw.QGridLayout()
        self.gridLayout.setSpacing(1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        # creating grid with QLabel(for modern design)
        self.gridcell_canvas = []
        self.gridcell_label = []
        for i in range(self.grid_x):
            tmp = []
            tmp2 = []
            for j in range(self.grid_x):
                box_label = qw.QLabel()
                box_label.setFixedSize(self.box_size, self.box_size)

                # create box canvas
                box_canvas = qg.QPixmap(self.box_size, self.box_size)
                # paint box color
                self.painter = qg.QPainter(box_canvas)
                self.painter.fillRect(0, 0, self.box_size, self.box_size, qc.Qt.white)
                self.painter.end()

                # set label to show box_canvas
                box_label.setPixmap(box_canvas)

                tmp.append(box_canvas)
                tmp2.append(box_label)

                self.gridLayout.addWidget(box_label, i, j)
                self.gridLayout.setColumnMinimumWidth(j, self.grid_x+1)

            self.gridcell_canvas.append(tmp)
            self.gridcell_label.append(tmp2)
            self.gridLayout.setRowMinimumHeight(i, self.grid_x+1)

        self.centralwidget.setLayout(self.gridLayout)

    # ---------------------------------------------------- Maps -------------------------------------------------------#

    def init_maps(self):
        # Walls
        self.map1 = (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 7), (0, 8), (1, 0), (1, 8), (2, 0), (2, 2), (
            2, 3), (
                        2, 8), (3, 0), (3, 3), (3, 8), (4, 0), (4, 3), (4, 8), (5, 0), (5, 8), (6, 0), (6, 3), (6, 4), (
                        6, 5), (
                        6, 8), (7, 0), (7, 8), (8, 0), (8, 1), (
                        8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)
        self.map2 = (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (1, 10), (1, 12), (
            1, 16), (1, 17), (1, 18), (2, 10), (2, 17), (2, 18), (3, 10), (3, 12), (3, 13), (3, 14), (3, 18), (4, 10), (
                        4, 18), (5, 10), (5, 15), (5, 18), (6, 10), (6, 15), (7, 10), (7, 15), (7, 18), (8, 10), (
                        8, 11), (8, 12), (8, 13), (8, 14), (8, 15), (8, 16), (8, 17), (8, 18)
        self.map3 = (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (11, 0), (11, 4), (
            11, 8), (12, 0), (12, 7), (12, 8), (13, 0), (13, 4), (13, 8), (14, 0), (14, 1), (14, 2), (14, 3), (14, 4), (
                        14, 8), (15, 0), (15, 4), (15, 8), (16, 7), (16, 8), (17, 0), (17, 8), (18, 0), (18, 1), (
                        18, 2), (18, 3), (18, 4), (18, 5), (18, 6), (18, 7), (18, 8)
        self.map4 = (10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15), (10, 16), (10, 17), (10, 18), (
            11, 10), (11, 18), (12, 10), (12, 18), (13, 10), (13, 14), (13, 15), (13, 18), (14, 10), (14, 11), (
                        14, 12), (14, 14), (14, 18), (15, 10), (15, 14), (15, 15), (15, 18), (16, 10), (16, 14), (
                        16, 18), (17, 10), (17, 17), (17, 18), (18, 10), (18, 11), (18, 13), (18, 14), (18, 15), (
                        18, 16), (18, 17), (18, 18)
        self.maps = [self.map1, self.map2, self.map3, self.map4]
