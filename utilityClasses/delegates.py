from PyQt5 import QtWidgets, QtCore, QtSql

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


class ComboBoxDelegate(QtWidgets.QStyledItemDelegate):
    #QCombobox
    def __init__(self, comboboxWithPresetModel, parent):
        super(ComboBoxDelegate, self).__init__(parent)
        self.__model = comboboxWithPresetModel.model()

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        cmb = QtWidgets.QComboBox()
        cmb.setModel(self.__model)
        return cmb

    def setEditorData(self, QWidget, QModelIndex):
        if QWidget.metaObject().className() == "QComboBox":
            print("Its a combo")
            pkModel = QModelIndex.model()
            pk = pkModel.data(QModelIndex, QtCore.Qt.DisplayRole)
            print(pk)
            #fkIndexLst = self.__model.match(self.__model.index(0, 0), QtCore.Qt.DisplayRole, pk, QtCore.Qt.MatchExactly)


            for row in range(self.__model.rowCount()):
                if self.__model.record(row).value(0) == pk:
                    break

            #fk = fkIndexLst[0].model().data(fkIndexLst[0], QtCore.Qt.EditRole)
            #print("fkIndexLst:", fkIndexLst, "Pk:", pk, "Fk:", fk, "Fk-Row:", fkIndexLst[0].row())

            #QWidget.setCurrentIndex(fkIndexLst[0].row())
            QWidget.setCurrentIndex(row)
        else:
            print("Not combo")
            super(ComboBoxDelegate, self).setEditorData(QWidget, QModelIndex)

    def setModelData(self, QWidget, QAbstractItemModel, QModelIndex):
        QAbstractItemModel.setData(QModelIndex, QWidget.currentIndex(), QtCore.Qt.EditRole)

    #def updateEditorGeometry(self, QWidget, QStyleOptionViewItem, QModelIndex):
    #    QWidget.setGeometry(QStyleOptionViewItem.rect)

    '''
    void
    ComboBoxDelegate::paint(QPainter * painter, const
    QStyleOptionViewItem & option, const
    QModelIndex & index) const
    {
    QStyleOptionViewItemV4
    myOption = option;
    QString
    text = Items[index.row()].c_str();
    
    myOption.text = text;
    
    QApplication::style()->drawControl(QStyle::CE_ItemViewItem, & myOption, painter);
    }
    '''