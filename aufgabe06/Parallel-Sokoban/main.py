import sys
from PyQt5 import QtWidgets as qw
from GameStructure import GameStructure

def main():
    app = qw.QApplication(sys.argv)
    game = GameStructure()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
