from PyQt5 import QtWidgets
import views._viewTableSingle
import controllers._contGeneric
import models.modelOwnersProperty

class ContOwnersProperty_MainTable(QtWidgets.QMainWindow):
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self, parent)
        #setup ui & models & create the generic controller
        self.__ui = views._viewTableSingle.Ui_MainWindow()
        self.__modelInterface = models.modelOwnersProperty.ModelOwnersPropertyInterface(self)
        self.__model = self.__modelInterface.getModel()
        self.__contGeneric = controllers._contGeneric.ContGeneric_Table(self.__ui, self.__modelInterface, self.__model, self)
        #self.__contGenericEntity = controllers._contGeneric.ContGeneric_TableEntity(self.__ui, self.__contGeneric, self)
        self.setWindowTitle("Owners Property")
        #self.__ui.tableView.hideColumn(0)

    def closeEvent(self, event):
        self.__contGeneric.closeEvent(event)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QWidget()
    c = ContOwnersProperty_MainTable(p)
    c.show()
    sys.exit(app.exec_())