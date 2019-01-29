from PyQt5 import QtWidgets, QtCore
import views.viewProperty_TabCont
import controllers.contProperty_MainTable
import controllers.contProperty_MainForm

class ContProperty_TabCont(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ContProperty_TabCont, self).__init__(parent)
        self.__ui = views.viewProperty_TabCont.Ui_Form()
        self.__ui.setupUi(self)
        self.insertTabProperty_MainTable()
        self.setWindowTitle("Property")

    def insertTabProperty_MainTable(self):
        self.__ui.tabWidget.removeTab(0)
        contProperty_MainTable = controllers.contProperty_MainTable.ContProperty_MainTable(self)
        self.__ui.tabWidget.insertTab(0, contProperty_MainTable, "Properties")

    def insertTabProperty_MainForm(self):
        self.__ui.tabWidget.removeTab(0)
        contProperty_MainForm = controllers.contProperty_MainForm.ContProperty_MainForm(self)
        self.__ui.tabWidget.insertTab(0, contProperty_MainForm, "Property")

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QWidget()
    c = ContProperty_TabCont(p)
    p.show()
    sys.exit(app.exec_())
