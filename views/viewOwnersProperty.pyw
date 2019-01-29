# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewOwnersProperty.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(707, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 130, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.txtPk_PropertOwnerID = QtWidgets.QLineEdit(Form)
        self.txtPk_PropertOwnerID.setObjectName("txtPk_PropertOwnerID")
        self.gridLayout.addWidget(self.txtPk_PropertOwnerID, 0, 1, 1, 1)
        self.txtPk_PropertyID = QtWidgets.QLineEdit(Form)
        self.txtPk_PropertyID.setObjectName("txtPk_PropertyID")
        self.gridLayout.addWidget(self.txtPk_PropertyID, 0, 3, 1, 1)
        self.cmbPk_PropertyID = QtWidgets.QComboBox(Form)
        self.cmbPk_PropertyID.setObjectName("cmbPk_PropertyID")
        self.gridLayout.addWidget(self.cmbPk_PropertyID, 1, 3, 1, 1)
        self.cmbPk_PropertOwnerID = QtWidgets.QComboBox(Form)
        self.cmbPk_PropertOwnerID.setObjectName("cmbPk_PropertOwnerID")
        self.gridLayout.addWidget(self.cmbPk_PropertOwnerID, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_8.setText(_translate("Form", "Property Owner"))
        self.label_9.setText(_translate("Form", "Property"))
        self.label.setText(_translate("Form", "Pk_PropertOwnerID"))
        self.label_2.setText(_translate("Form", "Pk_PropertyID"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

