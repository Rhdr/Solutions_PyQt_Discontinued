# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewProperty_MainForm.ui'
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
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txtStreet = QtWidgets.QLineEdit(Form)
        self.txtStreet.setObjectName("txtStreet")
        self.gridLayout.addWidget(self.txtStreet, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.txtStreetNr = QtWidgets.QLineEdit(Form)
        self.txtStreetNr.setObjectName("txtStreetNr")
        self.gridLayout.addWidget(self.txtStreetNr, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.txtComplex = QtWidgets.QLineEdit(Form)
        self.txtComplex.setObjectName("txtComplex")
        self.gridLayout.addWidget(self.txtComplex, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.txtComplexNr = QtWidgets.QLineEdit(Form)
        self.txtComplexNr.setObjectName("txtComplexNr")
        self.gridLayout.addWidget(self.txtComplexNr, 1, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.txtTown = QtWidgets.QLineEdit(Form)
        self.txtTown.setObjectName("txtTown")
        self.gridLayout.addWidget(self.txtTown, 2, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)
        self.txtSuburb = QtWidgets.QLineEdit(Form)
        self.txtSuburb.setObjectName("txtSuburb")
        self.gridLayout.addWidget(self.txtSuburb, 2, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.txtAddress = QtWidgets.QLineEdit(Form)
        self.txtAddress.setObjectName("txtAddress")
        self.gridLayout.addWidget(self.txtAddress, 3, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)
        self.cmbStreetNr = QtWidgets.QComboBox(Form)
        self.cmbStreetNr.setObjectName("cmbStreetNr")
        self.gridLayout.addWidget(self.cmbStreetNr, 4, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 4, 2, 1, 1)
        self.cmbComplexNr = QtWidgets.QComboBox(Form)
        self.cmbComplexNr.setObjectName("cmbComplexNr")
        self.gridLayout.addWidget(self.cmbComplexNr, 4, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 130, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Street"))
        self.label_2.setText(_translate("Form", "Street Nr"))
        self.label_3.setText(_translate("Form", "Complex"))
        self.label_4.setText(_translate("Form", "Complex Nr"))
        self.label_6.setText(_translate("Form", "Town"))
        self.label_7.setText(_translate("Form", "Suburb"))
        self.label_5.setText(_translate("Form", "Address"))
        self.label_8.setText(_translate("Form", "FkStreetNr"))
        self.label_9.setText(_translate("Form", "FkComplexNr"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

