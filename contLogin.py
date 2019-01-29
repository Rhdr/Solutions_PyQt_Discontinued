from PyQt5 import QtWidgets, QtCore
import views.viewLogin
import controllers.contMainMenu
import models._databaseConnection
import utilityClasses.paletteFunctions
import utilityClasses.keyboardFunctions

class ContLogin(QtWidgets.QDialog):
    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.__ui = views.viewLogin.Ui_qdlgLogin()
        self.__ui.setupUi(self)
        self.__p = utilityClasses.paletteFunctions.Pallet()
        self.__conn = models._databaseConnection.DBConnection(self)

        #setup signals
        self.__ui.btnLogin.clicked.connect(self.__login)
        self.__ui.txtUsername.returnPressed.connect(self.__login)
        self.__ui.txtPassword.returnPressed.connect(self.__login)
        self.__ui.txtUsername.clicked.connect(lambda: self.__gotFocusTxtLogin(self.__ui.txtUsername))
        self.__ui.txtPassword.clicked.connect(lambda: self.__gotFocusTxtLogin(self.__ui.txtPassword))
        self.__ui.txtUsername.gotFocus.connect(lambda: self.__gotFocusTxtLogin(self.__ui.txtUsername))
        self.__ui.txtUsername.lostFocus.connect(lambda: self.__lostFocusTxtLogin(self.__ui.txtUsername))
        self.__ui.txtPassword.gotFocus.connect(lambda: self.__gotFocusTxtLogin(self.__ui.txtPassword))
        self.__ui.txtPassword.lostFocus.connect(lambda: self.__lostFocusTxtLogin(self.__ui.txtPassword))

        self.__ui.lblCapsLock.hide()
        self.__displayCapsLockState()
        self.__checkConnectionStatus()

    def __gotFocusTxtLogin(self, __txt):
        #clear default value else select all
        __txt.selectAll()

        if __txt.objectName() == "txtPassword":
            __txt.clear()
            __txt.setEchoMode(QtWidgets.QLineEdit.Password)


    def __lostFocusTxtLogin(self, __txt):
        #display default text if empty
        if __txt.text() == "":
            if __txt.objectName() == "txtUsername":
                __txt.setText("Enter Your Username")
            else:
                __txt.setText("Enter Your Password")
                __txt.setEchoMode(QtWidgets.QLineEdit.Normal)

    def keyPressEvent(self, event):
        #test if capslock is pressed
        if event.key() == 16777252:
            self.__displayCapsLockState()

    def __displayCapsLockState(self):
        #test if capslock is on or not (then display on ui if on)
        self.__ui.lblCapsLock.setVisible(utilityClasses.keyboardFunctions.get_CapsLockEnabled())

    def __login(self):
        #if connected & if the password + username is correct login
        if self.__conn.connect():
            #self.__conn.closeConnection()
            self.__cntMain = controllers.contMainMenu.ContMainMenu()
            self.__cntMain.showMaximized()
            self.__keepConnectionOpen = True
            self.close()
        else:
            #connection failed check status
            #self.__conn.closeConnection()
            self.__checkConnectionStatus()

    def __checkConnectionStatus(self):
        #check and display connection status
        #disable controls if there is no connection & recheck for a connection
        if self.__conn.connect() == True:
            #the connection is good
            self.__p.set_greenPallet()
            self.__ui.lblDBConnStatus.setPalette(self.__p)
            self.__ui.lblDBConnStatus.setText("Connected")
            self.__ui.txtUsername.setEnabled(True)
            self.__ui.txtPassword.setEnabled(True)
            self.__ui.btnLogin.setEnabled(True)
        else:
            #the connection is bad
            self.__p.set_redPallet()
            self.__ui.lblDBConnStatus.setPalette(self.__p)
            self.__ui.lblDBConnStatus.setText("Connection Error: Reattempting to Connect...")
            self.__ui.txtUsername.clear()
            self.__ui.txtUsername.setEnabled(False)
            self.__ui.txtPassword.clear()
            self.__ui.txtPassword.setEnabled(False)
            self.__ui.btnLogin.setEnabled(False)
        QtCore.QTimer.singleShot(15000, lambda: self.__checkConnectionStatus())
        #self.__conn.closeConnection()

    def closeEvent(self, event):
        try:
            if self.__keepConnectionOpen == False:
                self.__conn.closeConnection()
        except:
            self.__conn.closeConnection()
        finally:
            event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg = ContLogin()
    dlg.show()
    sys.exit(app.exec_())