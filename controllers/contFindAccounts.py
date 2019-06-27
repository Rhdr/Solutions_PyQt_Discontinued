from PyQt5 import QtWidgets

import views.viewFindAccounts


class ContFindAccounts(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.__ui = views.viewFindAccounts.Ui_Form()
        self.__ui.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    cont = ContFindAccounts(w)
    cont.show()
    sys.exit(app.exec_())