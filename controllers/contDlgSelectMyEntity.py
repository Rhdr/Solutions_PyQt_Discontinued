from PyQt5 import QtWidgets

import models.modelMyEntity
import views.viewDlgSelectMyEntity


class ContDlgSelectMyEntity(QtWidgets.QDialog):
    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.__ui = views.viewDlgSelectMyEntity.Ui_Dialog()
        self.__ui.setupUi(self)

        #load model
        self.__clsModel =  models.modelMyEntity.ModelMyEntity(self)
        self.__clsModel.connect()
        self.__model = self.__clsModel.getModel()
        self.__clsModel.closeConnection()

        #load data
        self.__ui.listView.setModel(self.__model)

        self.__ui.btnBox.accepted.connect(self.btnBoxAccepted)

    def btnBoxAccepted(self):
        import controllers.contFindAccounts
        self.c = controllers.contFindAccounts()
        self.c.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    a = ContDlgSelectMyEntity()
    a.show()
    sys.exit(app.exec_())