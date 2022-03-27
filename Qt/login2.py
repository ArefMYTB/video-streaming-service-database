import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow, QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import *
import MySQLdb as mdb
from main import *

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('login.ui',self)
        

        #############################
        #### Buttons actions ########
        #############################

        self.register_Button.clicked.connect(lambda: self.register())
        self.login_Button.clicked.connect(lambda: self.log_in())

    def closeEvent(self, event):
        print("close")

    def log_in(self):

        current_username = self.username_login_lineEdit.text()
        current_password = "('"+self.password_login_lineEdit.text()+"',)"

        #############################
        #### connect to database ####
        #############################
        try:
            db = mdb.connect('localhost','root','','test')
            cursor = db.cursor()
            cursor.execute("SELECT password FROM user where username = '"+current_username+"'")
            m = cursor.fetchone()
            if(str(m) == current_password):
                # app2.exit()
                start(current_username)
            elif(str(m) == "None"):
                error_message("Wrong username")
            else:
                error_message("Wrong password")
        except:
            error_message("Can't connect to the database.")
        finally:
            db.close()

    def register(self):

        reg_name = self.firstname_lineEdit.text() + " " + self.lastname_lineEdit.text()
        reg_username = self.username_register_lineEdit.text()
        reg_email = self.email_lineEdit.text()
        reg_phone = self.phone_lineEdit.text()
        reg_password = self.password_register_lineEdit.text()
        reg_introducer = self.introducer_lineEdit.text()
        if(len(reg_introducer) == 0):    
            reg_introducer = "NULL"
        else:
            reg_introducer = "'"+reg_introducer+"'"

        #############################
        #### connect to database ####
        #############################
        try:
            db = mdb.connect('localhost','root','','test')
            cursor = db.cursor() # not handeling duplicate username and email
            cursor.execute("INSERT INTO `user` (`Uid`, `name`, `username`, `email`, `cellphone`, `password`, `Introducer`, `score`, `amount`, `Type`, `remain_time`) VALUES (NULL, '"+reg_name+"', '"+reg_username+"', '"+reg_email+"', '"+reg_phone+"', '"+reg_password+"', "+reg_introducer+", '0', '0', 'typical', '2021-07-14 14:09:31.000000')")
            db.commit()
        except(db.Error) as e:
            error_message(e)
        finally:
            db.close()



if __name__ == "__main__":
    app2 = QApplication(sys.argv)
    mainwindow2 = Login()
    widget2 = QtWidgets.QStackedWidget()
    widget2.addWidget(mainwindow2)

    widget2.show()
    sys.exit(app2.exec_())

