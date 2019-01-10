from PyQt5 import QtWidgets, QtCore

class LineEditDelegate(QtWidgets.QStyledItemDelegate):
    #def __init__(self, parent):
    #    super(LineEditDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return QtWidgets.QLineEdit(QWidget)

    def setEditorData(self, QWidget, QModelIndex):
        try:
            value = QModelIndex.model().data(QModelIndex, QtCore.Qt.EditRole)
            QWidget.setText(value)
        except:
            QWidget.setText("")

    def setModelData(self, QWidget, QAbstractItemModel, QModelIndex):
        try:
            value = QWidget.text()
            QAbstractItemModel.setData(QModelIndex, value, QtCore.Qt.EditRole)
        except:
            QAbstractItemModel.setData(QModelIndex, "", QtCore.Qt.EditRole)

    def updateEditorGeometry(self, QWidget, QStyleOptionViewItem, QModelIndex):
        QWidget.setGeometry(QStyleOptionViewItem.rect)


class SpinBoxDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return QtWidgets.QSpinBox(QWidget)

    def setEditorData(self, QWidget, QModelIndex):
        try:
            value = QModelIndex.model().data(QModelIndex, QtCore.Qt.EditRole)
            QWidget.setValue(value)
        except:
            QWidget.setValue(0)

    def setModelData(self, QWidget, QAbstractItemModel, QModelIndex):
        try:
            value = QWidget.value()
            QAbstractItemModel.setData(QModelIndex, value, QtCore.Qt.EditRole)
        except:
            QAbstractItemModel.setData(QModelIndex, 0, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, QWidget, QStyleOptionViewItem, QModelIndex):
        QWidget.setGeometry(QStyleOptionViewItem.rect)
