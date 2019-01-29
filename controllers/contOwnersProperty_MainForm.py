from PyQt5 import QtWidgets, QtCore, QtSql
import views._viewForm
import views.viewOwnersProperty
import models.modelOwnersProperty
import controllers._contGeneric
import utilityClasses.delegates

class contOwnersProperty_MainForm(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(contOwnersProperty_MainForm, self).__init__(parent)
        # setup uiFrom & uiFormDetail
        self.parent = parent
        self.setWindowTitle("Properties")

        self.__uiForm = views._viewForm.Ui_MainWindow()
        self.__uiFormDetail = views.viewOwnersProperty.Ui_Form()
        self.__modelInterface = models.modelOwnersProperty.ModelOwnersPropertyInterface(self)
        self.__model = self.__modelInterface.getModel()
        #self.__model = self.__modelInterface.getCmdSearchModel()
        self.__mapper = QtWidgets.QDataWidgetMapper(self)
        self.__mapper.setModel(self.__model)
        contGenericForm = controllers._contGeneric.ContGeneric_Form(self.__uiForm, self.__uiFormDetail, self.__model, self.__mapper, self)

        #setup mapper
        #self.__mapper.setItemDelegate(QtSql.QSqlRelationalDelegate(self))



        self.__modelcmbPk_PropertyOwnerID = self.__modelInterface.getCmbPk_PropertyOwnerID()
        self.__uiFormDetail.cmbPk_PropertOwnerID.setModel(self.__modelcmbPk_PropertyOwnerID)
        self.__uiFormDetail.cmbPk_PropertOwnerID.setModelColumn(1)
        self.__uiFormDetail.cmbPk_PropertOwnerID.setEditable(True)
        self.__uiFormDetail.cmbPk_PropertOwnerID.setEditable(True)

        #cmb = self.__uiFormDetail.cmbPk_PropertOwnerID
        #cmbDelegate = utilityClasses.delegates.ComboBoxDelegate(cmb, self)

        #self.__mapper.setItemDelegate(cmbDelegate)
        self.__mapper.addMapping(self.__uiFormDetail.txtPk_PropertOwnerID, self.__model.fieldIndex("Pk_PropertyOwnerID"))
        self.__mapper.addMapping(self.__uiFormDetail.cmbPk_PropertOwnerID, self.__model.fieldIndex("Pk_PropertyOwnerID"))
        #self.__mapper.addMapping(self.__uiFormDetail.txtPk_PropertyID, self.__model.fieldIndex("Pk_PropertyID"))
        #self.__mapper.addMapping(self.__uiFormDetail.cmbPk_PropertyID, self.__model.fieldIndex("Pk_PropertyID"))


        self.__mapper.currentIndexChanged.connect(self.__mapperCurrentIndexChanged)

        self.__mapper.toFirst()

        self.__uiForm.actionswitchView.triggered.connect(self.__switchView)

    def __mapperCurrentIndexChanged(self, currentRow):
        pk = self.__model.data(self.__model.index(currentRow, 0), QtCore.Qt.DisplayRole)
        #index = self.__modelcmbPk_PropertyOwnerID.index(0, 0)  # (row 0,) column 0
        #result = self.__modelcmbPk_PropertyOwnerID.match(index, QtCore.Qt.EditRole, pk, QtCore.Qt.MatchExactly)
        #fk = self.__modelcmbPk_PropertyOwnerID.match(index, QtCore.Qt.DisplayRole, pk)
        for row in range(self.__modelcmbPk_PropertyOwnerID.rowCount()):
            if self.__modelcmbPk_PropertyOwnerID.record(row).value(0) == pk:
                break

        #if len(fk) > 0:
            #row = fk[0].row()
        self.__uiFormDetail.cmbPk_PropertOwnerID.setCurrentIndex(row)


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
    c = contOwnersProperty_MainForm(p)
    c.show()
    sys.exit(app.exec_())