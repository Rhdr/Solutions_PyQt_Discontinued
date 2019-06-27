from PyQt5 import QtWidgets, QtCore

import views.


class Cont(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.__ui = views.
        self.__ui.setupUi(self)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    cont = Cont()
    cont.show()
    sys.exit(app.exec_())