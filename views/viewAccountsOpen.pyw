# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewAccountsOpen.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

import icons_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolCrud = QtWidgets.QToolBar(MainWindow)
        self.toolCrud.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolCrud.setObjectName("toolCrud")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolCrud)
        self.toolBar_2 = QtWidgets.QToolBar(MainWindow)
        self.toolBar_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.toolBar_2.setMovable(False)
        self.toolBar_2.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar_2.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar_2.setFloatable(False)
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBar_2)
        self.actionDelete = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/CRUD/icons/deleteRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon)
        self.actionDelete.setObjectName("actionDelete")
        self.actionAdd = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/CRUD/icons/addNewRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd.setIcon(icon1)
        self.actionAdd.setObjectName("actionAdd")
        self.actionFirst = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Navigation/icons/GoToFirstRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFirst.setIcon(icon2)
        self.actionFirst.setObjectName("actionFirst")
        self.actionPrev = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Navigation/icons/GoToPrevRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrev.setIcon(icon3)
        self.actionPrev.setObjectName("actionPrev")
        self.actionNext = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Navigation/icons/GoToNextRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNext.setIcon(icon4)
        self.actionNext.setObjectName("actionNext")
        self.actionLast = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Navigation/icons/GoToLastRecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLast.setIcon(icon5)
        self.actionLast.setObjectName("actionLast")
        self.actionRecordCount = QtWidgets.QAction(MainWindow)
        self.actionRecordCount.setObjectName("actionRecordCount")
        self.actionSearch = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/CRUD/icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSearch.setIcon(icon6)
        self.actionSearch.setObjectName("actionSearch")
        self.toolCrud.addAction(self.actionAdd)
        self.toolCrud.addAction(self.actionDelete)
        self.toolCrud.addAction(self.actionSearch)
        self.toolBar_2.addAction(self.actionLast)
        self.toolBar_2.addAction(self.actionNext)
        self.toolBar_2.addAction(self.actionRecordCount)
        self.toolBar_2.addAction(self.actionPrev)
        self.toolBar_2.addAction(self.actionFirst)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolCrud.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2"))
        self.actionDelete.setText(_translate("MainWindow", "Delete a Record"))
        self.actionDelete.setToolTip(_translate("MainWindow", "Delete a Record"))
        self.actionAdd.setText(_translate("MainWindow", "Add a Record"))
        self.actionFirst.setText(_translate("MainWindow", "Goto First Record"))
        self.actionFirst.setToolTip(_translate("MainWindow", "Goto First Record"))
        self.actionPrev.setText(_translate("MainWindow", "Goto Previous Record"))
        self.actionPrev.setToolTip(_translate("MainWindow", "Goto Previous Record"))
        self.actionNext.setText(_translate("MainWindow", "Goto Next Record"))
        self.actionNext.setToolTip(_translate("MainWindow", "Goto Next Record"))
        self.actionLast.setText(_translate("MainWindow", "Goto Last Record"))
        self.actionLast.setToolTip(_translate("MainWindow", "Goto Last Record"))
        self.actionRecordCount.setText(_translate("MainWindow", "Record ... of ..."))
        self.actionSearch.setText(_translate("MainWindow", "Search"))
        self.actionSearch.setToolTip(_translate("MainWindow", "Search"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

