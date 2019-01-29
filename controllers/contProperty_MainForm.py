from PyQt5 import QtWidgets, QtCore, QtSql
import views._viewForm
import views.viewProperty_MainForm
import models.modelProperty
import controllers._contGeneric

class ContProperty_MainForm(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(ContProperty_MainForm, self).__init__(parent)
        # setup uiFrom & uiFormDetail
        self.parent = parent
        self.setWindowTitle("Properties")

        self.__uiForm = views._viewForm.Ui_MainWindow()
        self.__uiFormDetail = views.viewProperty_MainForm.Ui_Form()
        self.__modelInterface = models.modelProperty.ModelPropertyInterface(self)
        self.__model = self.__modelInterface.getCmdSearchModel()
        self.__mapper = QtWidgets.QDataWidgetMapper(self)
        self.__mapper.setModel(self.__model)
        contGenericForm = controllers._contGeneric.ContGeneric_Form(self.__uiForm, self.__uiFormDetail, self.__model, self.__mapper, self)

        #setup mapper
        self.__mapper.setItemDelegate(QtSql.QSqlRelationalDelegate(self))
        self.__mapper.addMapping(self.__uiFormDetail.txtStreet, self.__model.fieldIndex("Street"))
        self.__mapper.addMapping(self.__uiFormDetail.txtStreetNr, self.__model.fieldIndex("StreetNr"))
        self.__mapper.addMapping(self.__uiFormDetail.txtComplex, self.__model.fieldIndex("Complex"))
        self.__mapper.addMapping(self.__uiFormDetail.txtComplexNr, self.__model.fieldIndex("ComplexNr"))
        self.__mapper.addMapping(self.__uiFormDetail.txtSuburb, self.__model.fieldIndex("Suburb"))
        self.__mapper.addMapping(self.__uiFormDetail.txtTown, self.__model.fieldIndex("Town"))
        self.__mapper.addMapping(self.__uiFormDetail.txtAddress, self.__model.fieldIndex("Address"))

        cmbStreetNrModel = self.__modelInterface.getCmbStreetNrModel()
        cmbStreetNrRelModel = cmbStreetNrModel.relationModel(0)
        self.__uiFormDetail.cmbStreetNr.setModel(cmbStreetNrRelModel)
        self.__uiFormDetail.cmbStreetNr.setModelColumn(1)
        self.__uiFormDetail.cmbStreetNr.setEditable(True)
        self.__mapper.addMapping(self.__uiFormDetail.cmbStreetNr, self.__model.fieldIndex("Fk_StreetNrID"))
        self.__mapper.addMapping(self.__uiFormDetail.cmbComplexNr, self.__model.fieldIndex("Fk_ComplexNrID"))
        self.__mapper.toFirst()

        self.__uiForm.actionswitchView.triggered.connect(self.__switchView)

    #def closeEvent(self, event):
    #    self.__contGeneric.closeEvent(event)

    def __switchView(self):
        try:
            self.parent.insertTabProperty_MainTable()
        except:
            print("The current parent dont support switching views")

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QMainWindow()
    c = ContProperty_MainForm(p)
    c.show()
    sys.exit(app.exec_())