# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewEntity.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(761, 614)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txtSearch = QtWidgets.QLineEdit(self.centralwidget)
        self.txtSearch.setClearButtonEnabled(True)
        self.txtSearch.setObjectName("txtSearch")
        self.verticalLayout.addWidget(self.txtSearch)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolbNav = QtWidgets.QToolBar(MainWindow)
        self.toolbNav.setMovable(False)
        self.toolbNav.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolbNav.setObjectName("toolbNav")
        MainWindow.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolbNav)
        self.toolbCrud = QtWidgets.QToolBar(MainWindow)
        self.toolbCrud.setMovable(True)
        self.toolbCrud.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolbCrud.setObjectName("toolbCrud")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbCrud)
        self.actionNewRecord = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/CRUD_S/icons/addNewRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewRecord.setIcon(icon)
        self.actionNewRecord.setObjectName("actionNewRecord")
        self.actionFirst = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/navigation/icons/GoToFirstRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFirst.setIcon(icon1)
        self.actionFirst.setText("")
        self.actionFirst.setObjectName("actionFirst")
        self.actionPrev = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/navigation/icons/GoToPrevRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrev.setIcon(icon2)
        self.actionPrev.setText("")
        self.actionPrev.setObjectName("actionPrev")
        self.actionNext = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/navigation/icons/GoToNextRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNext.setIcon(icon3)
        self.actionNext.setText("")
        self.actionNext.setObjectName("actionNext")
        self.actionLast = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/navigation/icons/GoToLastRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLast.setIcon(icon4)
        self.actionLast.setText("")
        self.actionLast.setObjectName("actionLast")
        self.actionRecordNr = QtWidgets.QAction(MainWindow)
        self.actionRecordNr.setObjectName("actionRecordNr")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/CRUD_S/icons/deleteRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon5)
        self.actionDelete.setObjectName("actionDelete")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/CRUD_S/icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon6)
        self.actionSave.setObjectName("actionSave")
        self.actionFind = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/CRUD_S/icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFind.setIcon(icon7)
        self.actionFind.setObjectName("actionFind")
        self.toolbNav.addAction(self.actionFirst)
        self.toolbNav.addAction(self.actionPrev)
        self.toolbNav.addAction(self.actionRecordNr)
        self.toolbNav.addAction(self.actionNext)
        self.toolbNav.addAction(self.actionLast)
        self.toolbNav.addAction(self.actionNewRecord)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Entity"))
        self.label.setText(_translate("MainWindow", "Entity"))
        self.toolbNav.setWindowTitle(_translate("MainWindow", "toolBar_2"))
        self.toolbCrud.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNewRecord.setText(_translate("MainWindow", "Insert New Record"))
        self.actionNewRecord.setToolTip(_translate("MainWindow", "Insert a New Record"))
        self.actionFirst.setToolTip(_translate("MainWindow", "Go to First Record"))
        self.actionPrev.setToolTip(_translate("MainWindow", "Go to Previous Record"))
        self.actionNext.setToolTip(_translate("MainWindow", "Go to Next Record"))
        self.actionLast.setToolTip(_translate("MainWindow", "Go to Last Record"))
        self.actionRecordNr.setText(_translate("MainWindow", "Record ... of ..."))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.actionDelete.setToolTip(_translate("MainWindow", "Delete Record/s"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save all Records"))
        self.actionFind.setText(_translate("MainWindow", "Find"))
        self.actionFind.setToolTip(_translate("MainWindow", "Find a record"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

