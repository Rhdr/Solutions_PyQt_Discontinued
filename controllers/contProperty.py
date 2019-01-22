from PyQt5 import QtWidgets, QtCore
import views.viewSingleTable
import controllers._contGeneric
import utilityClasses.delegates
import models.modelProperty

class ContProperty(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(ContProperty, self).__init__(parent)
        #setup ui & models & create the generic controller
        self.__ui = views.viewSingleTable.Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__modelInterface = models.modelProperty.ModelPropertyInterface(self)
        self.__model = self.__modelInterface.getModel()
        self.__contGeneric = controllers._contGeneric.ContGeneric(self.__ui, self.__modelInterface, self.__model, self)
        self.setWindowTitle("Properties")
        self.__ui.tableView.hideColumn(0)

        lineEditDelegate = utilityClasses.delegates.LineEditDelegate(self.__ui.tableView)
        lineEditDelegateStreet = utilityClasses.delegates.LineEditDelegate(self.__ui.tableView)
        spinBoxDelegate = utilityClasses.delegates.SpinBoxDelegate(self.__ui.tableView)
        self.__ui.tableView.setItemDelegateForColumn(1, lineEditDelegateStreet)
        self.__ui.tableView.setItemDelegateForColumn(2, lineEditDelegate)
        self.__ui.tableView.setItemDelegateForColumn(3, lineEditDelegate)
        self.__ui.tableView.setItemDelegateForColumn(4, lineEditDelegate)
        self.__ui.tableView.setItemDelegateForColumn(5, lineEditDelegate)
        self.__ui.tableView.setItemDelegateForColumn(6, lineEditDelegate)
        self.__ui.tableView.setItemDelegateForColumn(7, lineEditDelegate)
        self.__ui.tableView.setItemDelegateForColumn(8, spinBoxDelegate)
        self.__ui.tableView.setItemDelegateForColumn(9, spinBoxDelegate)
        spinBoxDelegate.commitData.connect(self.__contGeneric.delegateCommitData)
        lineEditDelegate.commitData.connect(self.__contGeneric.delegateCommitData)
        lineEditDelegateStreet.commitData.connect(self.__contGeneric.delegateCommitData)
        lineEditDelegateStreet.commitData.connect(self.test)

    def test(self):
        print("Update Address Field")

    def closeEvent(self, event):
        self.__contGeneric.closeEvent(event)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QWidget()
    c = ContProperty(p)
    c.show()
    sys.exit(app.exec_())