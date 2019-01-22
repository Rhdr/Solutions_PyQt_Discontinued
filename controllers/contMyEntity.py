from PyQt5 import QtWidgets
import views.viewSingleTable
import controllers._contGeneric
import controllers._contGenericEntity
import models.modelMyEntity

class ContMyEntity(QtWidgets.QMainWindow):
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self, parent)
        #setup ui & models & create the generic controller
        self.__ui = views.viewSingleTable.Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__modelInterface = models.modelMyEntity.ModelMyEntityInterface(self)
        self.__model = self.__modelInterface.getModel()
        self.__contGeneric = controllers._contGeneric.ContGeneric(self.__ui, self.__modelInterface, self.__model, self)
        self.__contGenericEntity = controllers._contGenericEntity.ContGenericEntity(self.__ui, self.__contGeneric, self)
        self.setWindowTitle("Main Entities")
        self.__ui.tableView.hideColumn(0)

    def closeEvent(self, event):
        self.__contGeneric.closeEvent(event)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QWidget()
    c = ContMyEntity(p)
    c.show()
    sys.exit(app.exec_())