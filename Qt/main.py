import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import *
import MySQLdb as mdb

class admin(QMainWindow):
    def __init__(self):
        
        super(admin, self).__init__()
        loadUi('admin.ui',self)

        self.home()

        #navigate to Home page
        self.btn_page_1.clicked.connect(lambda: self.home())
        #home page
        query = "SELECT DISTINCT name, year, score, view, price FROM movie ORDER BY Mid DESC" # Priority is given to newer ones
        table = self.tableWidget
        self.loadingData(table, query+" LIMIT 0,10")

        #navigate to New movie page
        self.btn_page_2.clicked.connect(lambda: self.new_movie())

        #navigate to Log page
        self.btn_page_3.clicked.connect(lambda: self.log_admin())
    
    def loadingData(self, table, query):
        
        res = database(query)
        table.setRowCount(0)
        for row_number, row_data in enumerate(res):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
            
        #Table will fit the screen horizontally
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)        

    def next_list(self,table,query):
        global current_table
        current_table += 10
        self.loadingData(table, query+" LIMIT "+str(current_table)+",10")
        self.update()

    def previous_list(self,table,query):
        global current_table
        if(current_table > 9):
            current_table -= 10
        self.loadingData(table, query+" LIMIT "+str(current_table)+",10")
        self.update()

    def home(self):
        
        self.stackedWidget.setCurrentWidget(self.page_1)  
        #home page
        query = "SELECT DISTINCT name, year, score, view, price FROM movie ORDER BY Mid DESC" # Priority is given to newer ones
        table = self.tableWidget
        self.loadingData(table, query+" LIMIT 0,10")

        self.pushButton_8.clicked.connect(lambda: self.next_list(table,query))
        self.pushButton_7.clicked.connect(lambda: self.previous_list(table,query))
        self.pushButton.clicked.connect(lambda: self.search_movie())

        # select a cell in the tabel        
        self.tableWidget.selectionModel().selectionChanged.connect(self.selected_movie) # problem: when we select one, selection stay on it

    def search_movie(self):
        movies = self.lineEdit.text()
        query = "SELECT name, year, score, view, price FROM movie WHERE name LIKE '%" + movies + "%'"
        table = self.tableWidget
        self.loadingData(table, query+" LIMIT "+str(current_table)+",10")
        self.update()

    def selected_movie(self, selected):

        global row
        
        # get row of selected cell
        for ix in selected.indexes():
            row = ix.row()
        
        movie_name = self.tableWidget.item(row,0).text()

        self.stackedWidget.setCurrentWidget(self.page_2)  
        
        query = "SELECT Mid, name, year, price FROM movie WHERE name = '"+movie_name+"'"
        res = database(query)
        self.lineEdit_4.setText(str(res[0][1])) #name
        self.lineEdit_3.setText(str(res[0][2])) #year
        self.lineEdit_11.setText(str(res[0][3])) #price

        query = "SELECT genre FROM genre WHERE Mid = '"+str(res[0][0])+"'"
        res2 = database(query)
        query = "SELECT director FROM director WHERE Mid = '"+str(res[0][0])+"'"
        res3 = database(query)
        
        self.lineEdit_7.setText(str(res2[0][0])) #genre
        self.lineEdit_9.setText(str(res3[0][0])) #director
        
        self.pushButton_3.clicked.connect(lambda: self.edit(str(res[0][0])))
        self.pushButton_6.clicked.connect(lambda: self.delete(str(res[0][0])))

    def new_movie(self):
        
        self.stackedWidget.setCurrentWidget(self.page_2)  
        self.pushButton_2.clicked.connect(lambda: self.create())

    def create(self):
        name = self.lineEdit_4.text()
        year = self.lineEdit_3.text()
        genre1 = self.lineEdit_7.text()
        genre2 = self.lineEdit_9.text()
        genre3 = self.lineEdit_13.text()
        director1 = self.lineEdit_14.text()
        director2 = self.lineEdit_15.text()
        director3 = self.lineEdit_12.text()
        price = self.lineEdit_11.text()

        query = "INSERT INTO `movie` (`Mid`, `name`, `year`, `score`, `view`, `price`) VALUES (NULL, '"+name+"', '"+year+"', '0', '0', '"+price+"')"
        database(query)

        query = "SELECT Mid FROM movie WHERE name = '"+name+"'"
        res = database(query)

        query = "INSERT INTO `director` (`Mid`, `director`) VALUES ('"+str(res[0][0])+"', '"+director1+"')"
        database(query)
        query = "INSERT INTO `director` (`Mid`, `director`) VALUES ('"+str(res[0][0])+"', '"+director2+"')"
        database(query)
        query = "INSERT INTO `director` (`Mid`, `director`) VALUES ('"+str(res[0][0])+"', '"+director3+"')"
        database(query)

        query = "INSERT INTO `genre` (`Mid`, `genre`) VALUES ('"+str(res[0][0])+"', '"+genre1+"')"
        database(query)
        query = "INSERT INTO `genre` (`Mid`, `genre`) VALUES ('"+str(res[0][0])+"', '"+genre2+"')"
        database(query)
        query = "INSERT INTO `genre` (`Mid`, `genre`) VALUES ('"+str(res[0][0])+"', '"+genre3+"')"
        database(query)

    def edit(self,mid):
        name = self.lineEdit_4.text()
        year = self.lineEdit_3.text()
        genre = self.lineEdit_7.text()
        director = self.lineEdit_9.text()
        price = self.lineEdit_11.text()

        query = "UPDATE `movie` SET name = '"+name+"', year = '"+year+"', price = '"+price+"' WHERE Mid = '"+mid+"'"
        database(query)

        query = "UPDATE `director` SET director = '"+director+"' WHERE Mid = '"+mid+"'"
        database(query)

        query = "UPDATE `genre` SET genre = '"+genre+"' WHERE Mid = '"+mid+"'"
        database(query)

    def delete(self,mid):
        query = "DELETE FROM `movie` WHERE `movie`.`Mid` = '"+mid+"'"
        database(query)

    def log_admin(self):
         
        self.stackedWidget.setCurrentWidget(self.page_3)
        query = "SELECT DISTINCT * FROM log"
        table = self.tableWidget_2
        self.loadingData(table, query)

        self.pushButton_4.clicked.connect(lambda: self.next_list(table,query))
        self.pushButton_5.clicked.connect(lambda: self.previous_list(table,query))


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('login.ui',self)
        

        #############################
        #### Buttons actions ########
        #############################

        self.register_Button.clicked.connect(lambda: self.register())
        self.login_Button.clicked.connect(lambda: self.log_in())

    def log_in(self):
        global username
        current_username = self.username_login_lineEdit.text()
        current_password = "('"+self.password_login_lineEdit.text()+"',)"

        #if admin log in
        if(current_username == "abcd"):
            if(self.password_login_lineEdit.text() == "1234"):
                adminwindow = admin()
                widget.addWidget(adminwindow)
                widget.setCurrentIndex(widget.currentIndex()+1)
        else:
        #############################
        #### connect to database ####
        #############################
            try:
                db = mdb.connect('localhost','root','','test')
                cursor = db.cursor()
                cursor.execute("SELECT password FROM user where username = '"+current_username+"'")
                m = cursor.fetchone()
                if(str(m) == current_password):
                    username = current_username

                    mainwindow = Show()
                    widget.addWidget(mainwindow)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                
                elif(str(m) == "None"):
                    error_message("Wrong username")
                else:
                    error_message("Wrong password")
            except:
                error_message("Can't connect to the database.")
            finally:
                db.close()

    def register(self):
        global username

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

        query = "INSERT INTO `user` (`username`, `name`, `email`, `cellphone`, `password`, `Introducer`, `score`, `amount`, `Type`, `remain_time`) VALUES ('"+reg_username+"', '"+reg_name+"', '"+reg_email+"', '"+reg_phone+"', '"+reg_password+"', "+reg_introducer+", '0', '0', 'typical', NULL) ;"
        res = database(query)

        username = reg_username
        admin_log("Registered")
        if(len(res) == 0):
            query = "UPDATE user SET score = score + 1 WHERE username = "+reg_introducer+" "
            database(query)

class Show(QMainWindow):
    def __init__(self):
        super(Show, self).__init__()
        loadUi('main_window.ui',self)
        
        ### loading data to all place
        self.load()

        #############################
        ### Slide Buttons actions ###
        #############################

        #Left Menu toggle button
        self.left_menu_toggle_btn.clicked.connect(lambda: self.slideLeftMenu())
        
        #navigate to Home page
        self.home_button.clicked.connect(lambda: self.homepageclicked())

        #navigate to account page
        self.account_button.clicked.connect(lambda: self.acountpageclicked())

        #navigate to user page
        self.User_button.clicked.connect(lambda: self.userpageclicked())

        #navigate to lists page
        self.Lists_button.clicked.connect(lambda: self.listspageclicked())

        #navigate to My list page
        self.MyList_button.clicked.connect(lambda: self.mylistpageclicked("SELECT Lid FROM viplists WHERE username = '"+username+"'"))

        #navigate to friends page
        self.Friends_button.clicked.connect(lambda: self.friendspageclicked())

        #navigate to Settings page
        self.settings_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.settings_page))   

    #############################
    # loading data to all place #
    #############################

    def load(self):
        #home page
        self.homepageclicked()

        #user page
        self.userpageclicked()

        #account page
        self.acountpageclicked() 

    def loadingData(self, table, query):
        
        res = database(query)
        table.setRowCount(0)
        for row_number, row_data in enumerate(res):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
            
        #Table will fit the screen horizontally
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)        

    def homepageclicked(self):
        global current_table
        global ct
        current_table = 0
        ct = 0

        #home page
        query = "SELECT DISTINCT name, year, score, view, price FROM movie GROUP BY name ORDER BY Mid DESC LIMIT 0,10" # Priority is given to newer ones
        table = self.newest_movies_table
        self.loadingData(table, query)

        self.stackedWidget.setCurrentWidget(self.home_page)

        # select a cell in the tabel
        self.newest_movies_table.selectionModel().selectionChanged.connect(self.selctedMovie)
   
        #navigate to filter page
        self.Filter_Button.clicked.connect(lambda: self.filter())

        # movie name search
        self.Saerch_Button.clicked.connect(lambda: self.search_movie())

        # director search
        self.search_director_Button.clicked.connect(lambda: self.search_director())
     
    def selctedMovie(self, selected):

        global row
        global mvname
        
        # get row of selected cell
        for ix in selected.indexes():
            row = ix.row()
        
        if(ct == 0):
            movie_name = self.newest_movies_table.item(row,0).text()
        elif(ct == 1):
            movie_name = self.filter_movies_table.item(row,0).text()
        elif(ct == 4):
            movie_name = self.filter_director_table.item(row,1).text()
        else:
            movie_name = self.MyList_TableWidget.item(row,0).text()

        mvname = movie_name

        query = "SELECT Mid, name, score, view, price FROM movie WHERE name = '"+movie_name+"'"
        
        res = database(query)
        
        self.name_movie_Button.setText("name: "+str(res[0][1]))        
        self.score_movie_Button.setText("score: "+str(res[0][2]))         
        self.view_movie_Button.setText("view: "+str(res[0][3]))
        self.price_movie_Button.setText("price: "+str(res[0][4]))

        #director
        query = "SELECT DISTINCT director FROM director WHERE Mid = '"+str(res[0][0])+"'"
        res1 = database(query)

        self.director_comboBox.clear()
        for i in range(len(res1)):
            if(i<4):
                self.director_comboBox.addItem(str(res1[i][0]))

        #genre
        query = "SELECT DISTINCT genre FROM genre WHERE Mid = '"+str(res[0][0])+"'"
        res1 = database(query)

        self.genre_comboBox.clear()
        for i in range(len(res1)):
            if(i<4):
                self.genre_comboBox.addItem(str(res1[i][0]))
        
        
        self.stackedWidget.setCurrentWidget(self.Movie_page)
        self.comments_movie_Button.clicked.connect(lambda: self.getcomments(str(res[0][0])))

        self.play_movie_Button.clicked.connect(lambda: self.play(res[0][4]))
        self.name_movie_play_Button.setText(str(res[0][1]))

        self.addToList_movie_Button.clicked.connect(lambda: self.add_to_my_list(str(res[0][0])))

    def play(self,price):

        if(price > 0):
            if(self.UserType_lineEdit.text() == "VIP"):
                self.stackedWidget.setCurrentWidget(self.Buy_Movie_page)
                self.buywithcash_Button.clicked.connect(lambda: self.buy_with_cash(price))
                self.buywithscore_Button.clicked.connect(lambda: self.buy_with_score())
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("You need to get VIP to see this movie")
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            self.stackedWidget.setCurrentWidget(self.Play_page)

        self.verify_vote_Button.clicked.connect(lambda: self.vote())
        # self.verify_vote_Button.clicked.disconnect()

    def buy_with_cash(self,price):
        amount = float(self.Amount_lineEdit.text())
        if(amount > price):
            query = "UPDATE user SET amount = '" + str(amount-price) + "'"
            database(query)
            self.stackedWidget.setCurrentWidget(self.Play_page)
            admin_log("Whached "+mvname)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("You don't have enough money.")
            msg.setWindowTitle("Error")
            msg.exec_()

    def buy_with_score(self):
        score = int(self.Score_lineEdit.text())
        if(score > 1):
            query = "UPDATE user SET score = '" + str(score-1) + "'"
            database(query)
            self.stackedWidget.setCurrentWidget(self.Play_page)
            admin_log("Whached "+mvname)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("You don't have enough score.")
            msg.setWindowTitle("Error")
            msg.exec_()

    def add_to_my_list(self,Mid):
        query = "SELECT Lid FROM viplists WHERE username = '"+username+"'"
        res = database(query)

        if(len(res) != 0):
            query = "INSERT INTO `list` (`Lid`, `Mid`) VALUES ('"+str(res[0][0])+"', '"+Mid+"')"
            database(query)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("You don't have any lists")
            msg.setWindowTitle("Error")
            msg.exec_()

    def getcomments(self,Mid):
        global current_table
        current_table = 0

        query = "SELECT username,comment,score FROM comments WHERE Mid = '"+Mid+"'"
        table = self.comments_table
        self.loadingData(table, query+" LIMIT "+str(current_table)+",10")
        
        self.stackedWidget.setCurrentWidget(self.comments_page)
        self.next_comments_Button.clicked.connect(lambda: self.next_list(table,query))
        self.previous_comments_Button.clicked.connect(lambda: self.previous_list(table,query))

    def vote(self):
        comment = self.leave_comment_play_lineEdit.text()
        score = self.score_play_spinBox.value()

        movie_name = self.name_movie_play_Button.text()
        query = "SELECT Mid FROM movie WHERE name = '"+movie_name+"'"
        Mid = database(query)
        # username = self.UserName_lineEdit.text()

        query = "INSERT INTO `comments` (`Mid`, `username`, `comment`, `score`) VALUES ('"+str(Mid[0][0])+"', '"+username+"', '"+comment+"', '"+str(score)+"')"
        v = database(query)
        if(v == "v"):
            query = "UPDATE comments SET comment = '"+comment+"', score = '"+str(score)+"' WHERE Mid = '"+str(Mid[0][0])+"' and username = '"+username+"'"
            database(query)
        else:
            # score for movie
            query = "SELECT score FROM movie WHERE Mid = '"+str(Mid[0][0])+"'"
            midscore = database(query)

            query = "SELECT view FROM movie WHERE Mid = '"+str(Mid[0][0])+"'"
            view = database(query)

            if(score == 0):
                score = str(midscore[0][0])
            else:
                score = str((midscore[0][0]*view[0][0] + score)/(view[0][0]+1))
            v = view[0][0]+1
            query = "UPDATE movie SET score = '"+score+"', view = '"+str(v)+"' WHERE Mid = '"+str(Mid[0][0])+"'" 
            database(query)

    def search_movie(self):
        movies = self.search_movie_lineEdit.text()
        query = "SELECT DISTINCT name, year,genre, score, view FROM movie Join genre WHERE name LIKE '%" + movies + "%' and movie.Mid = genre.Mid"
        table = self.filter_movies_table
        self.loadingData(table, query+" LIMIT "+str(current_table)+",10")
        self.filter_page_clicked(table, query)

    def search_director(self):
        global ct

        director_name = self.director_lineEdit.text()
        query = "SELECT DISTINCT name FROM movie Join director WHERE movie.Mid = director.Mid and director LIKE '%"+director_name+"%'"
        res = database(query)
        movies = str(res[0][0])
        query = "SELECT DISTINCT director, name, year, score, view FROM movie Join director WHERE name LIKE '%" + movies + "%' and movie.Mid = director.Mid"
        table = self.filter_director_table
        self.loadingData(table, query+" LIMIT "+str(current_table)+",10")
        self.filter_page_clicked(table, query)

        # select a cell in the tabel
        ct = 4
        table.selectionModel().selectionChanged.connect(self.selctedMovie)
        self.stackedWidget.setCurrentWidget(self.director_filter)
        self.next_director_Button.clicked.connect(lambda: self.next_list(table,query))
        self.previous_director_Button.clicked.connect(lambda: self.previous_list(table,query))

    def filter(self):
        genre = str(self.Genere_comboBox.currentText())
        if(genre == "Every Genere"):
            genre = ""
        else:
            genre = "genre = '" + genre + "' and "
        year = str(self.Year_spinBox.value())
        if(year == "1950"):
            year = ""
        else:
            year = "year = '" + year + "' and "
        score = str(self.Score_spinBox.value())
        if(score == "0"):
            score = ""
        else:
            score = "score = '" + score + "' and "
        self.stackedWidget.setCurrentWidget(self.filter_page)
        query = "SELECT DISTINCT name, year, genre, score, view FROM movie Join genre WHERE " + genre + year + score + "movie.Mid = genre.Mid"
        
        table = self.filter_movies_table
        self.loadingData(table, query+" LIMIT "+str(current_table)+",10")

        self.filter_page_clicked(table, query)

    def filter_page_clicked(self,table,query):

        global ct

        self.stackedWidget.setCurrentWidget(self.filter_page)
        
        # select a cell in the tabel
        ct = 1
        table.selectionModel().selectionChanged.connect(self.selctedMovie)

        
        self.orderby_score_Button.clicked.connect(lambda: self.orderby_score(query))
        self.orderby_view_Button.clicked.connect(lambda: self.orderby_view(query))
        self.orderby_year_Byutton.clicked.connect(lambda: self.orderby_year(query))
        
        self.next_filter_Button.clicked.connect(lambda: self.next_list(table,query))
        self.previous_filter_Button.clicked.connect(lambda: self.previous_list(table,query))

    def orderby_score(self,query):
        query += " ORDER BY score DESC"
        table = self.filter_movies_table
        self.loadingData(table, query+" LIMIT "+str(current_table)+",10")
        self.update()

    def orderby_view(self,query):
        query += " ORDER BY view DESC"
        table = self.filter_movies_table
        self.loadingData(table, query+" LIMIT "+str(current_table)+",10")
        self.update()
    
    def orderby_year(self,query):
        query += " ORDER BY year DESC"
        table = self.filter_movies_table
        self.loadingData(table, query+" LIMIT "+str(current_table)+",10")
        self.update()

    def next_list(self,table,query):
        global current_table
        current_table += 5
        self.loadingData(table, query+" LIMIT "+str(current_table)+",10")
        self.update()

    def previous_list(self,table,query):
        global current_table
        if(current_table > 9):
            current_table -= 10
        self.loadingData(table, query+" LIMIT "+str(current_table)+",10")
        self.update()

    def userpageclicked(self):
        global current_table
        current_table = 0

        query = "SELECT username, name, email, cellphone, Introducer, score, amount, Type FROM user WHERE username = '"+username+"'"    
        res = database(query)
            
        #user page
        self.UserName_lineEdit.setText(str(res[0][0]))
        self.Name_lineEdit.setText(str(res[0][1]))
        self.Email_lineEdit.setText(str(res[0][2]))
        self.PhoneNumber_lineEdit.setText(str(res[0][3]))
        self.Introduced_lineEdit.setText(str(res[0][4]))
        self.Score_lineEdit.setText(str(res[0][5]))
        self.Amount_lineEdit.setText(str(res[0][6]))
        self.UserType_lineEdit.setText(str(res[0][7]))
        
        self.stackedWidget.setCurrentWidget(self.User_page)

        self.Edit_User_Button.clicked.connect(lambda: self.edit_user())

        self.Upgradewithamount_User_Button.clicked.connect(lambda: self.upgrade(0))
        self.Upgradewithscor_User_Button.clicked.connect(lambda: self.upgrade(1))
    
    def upgrade(self,x):
        amount = float(self.Amount_lineEdit.text())
        score = int(self.Score_lineEdit.text())
        if(x==0):
            if(amount>500):
                amount -= 500
                query = "UPDATE user SET amount = '"+str(amount)+"', Type = 'VIP' WHERE username = '"+username+"'"
                database(query)
                # query = "SELECT remain_time FROM user WHERE username = '"+username+"'"
                # res = database(query)
                # if(str(res[0][0]) == "None"):
                #     query = "UPDATE user SET remain_time = DATEADD(month,1,GETDATE()) WHERE username = '"+username+"'"
                #     database(query)
                # else:
                query = "UPDATE user SET remain_time = DATE_ADD(remain_time, INTERVAL 1 month ) WHERE username = '"+username+"'"
                database(query)

                admin_log("Upgraded")
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("You have not einough money.")
                msg.setWindowTitle("Error")
                msg.exec_()
        else:
            if(score>3):
                score -= 3
                query = "UPDATE user SET score = '"+str(score)+"', Type = 'VIP'"
                database(query)
                admin_log("Upgraded")
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("You have not einough score.")
                msg.setWindowTitle("Error")
                msg.exec_()

    def edit_user(self):

        query = "SELECT password FROM user WHERE username = '"+username+"'"
        res = database(query)

        text, ok = QInputDialog.getText(None, "Attention", "Password?", QLineEdit.Password)
        if ok and text:
            
            if(str(res[0][0]) == text):

                name = self.Name_lineEdit.text()
                email = self.Email_lineEdit.text()
                phone = self.PhoneNumber_lineEdit.text()
                password = self.new_password_lineEdit.text()
                if(password == ""):
                    password = str(res[0][0])
                query = "UPDATE user SET name = '"+name+"', email = '"+email+"', cellphone = '"+phone+"', password = '"+password+"' WHERE username = '"+username+"'"
                database(query)
                admin_log("Account Edited")
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Your password is incorrect.")
                msg.setWindowTitle("Error")
                msg.exec_()

    def mylistpageclicked(self,query1):
        global current_table
        global ct
        current_table = 0

        # query = "SELECT Lid FROM viplists WHERE username = '"+username+"'"
        res = database(query1)

        if(len(res) != 0):
            query = "SELECT DISTINCT name, score, view FROM movie Join list WHERE movie.Mid = list.Mid and Lid = '"+str(res[0][0])+"'"
            table = self.MyList_TableWidget
            self.loadingData(table, query+" LIMIT "+str(current_table)+",10")

        # select a cell in the tabel
        ct = 2
        self.MyList_TableWidget.selectionModel().selectionChanged.connect(self.selctedMovie)
        
        self.stackedWidget.setCurrentWidget(self.MyList_page)

        self.Create_MyList_Button.clicked.connect(lambda: self.new_list())

        self.Next_MyList_Button.clicked.connect(lambda: self.next_list(table,query))
        self.Previous_MyList_Button.clicked.connect(lambda: self.previous_list(table,query))
        
    def new_list(self):
        query = "SELECT Type FROM user WHERE username = '"+username+"'"
        res = database(query)
        if(str(res[0][0]) == "VIP"):
            query = "SELECT name FROM viplists WHERE username = '"+username+"'"
            res = database(query)
            if(len(res) == 0):
                self.stackedWidget.setCurrentWidget(self.Create_List_page)
        
                self.final_create_list_Button.clicked.connect(lambda: self.make_new_list())
            else:
                error_message("You have a list already")
        else:
            error_message("You are not VIP")

    def make_new_list(self):
        name = self.name_of_your_list.text()
        type_of_list = self.type_of_list.currentText()

        if(name != ""):
            query = "INSERT INTO `viplists` (`Lid`, `username`, `name`, `status`) VALUES (NULL, '"+username+"', '"+name+"', '"+type_of_list+"')"
            database(query)
            admin_log("Made new list")
        else:
            error_message("Please give a name to your list")

    def listspageclicked(self):
        global current_table
        current_table = 0

        query = "SELECT DISTINCT name, username FROM viplists"
        table = self.Lists_TableWidget
        self.loadingData(table, query + " LIMIT "+str(current_table)+",10")

        
        # select a list in the tabel
        table.selectionModel().selectionChanged.connect(self.selctedList)

        self.stackedWidget.setCurrentWidget(self.Lists_page)
        self.next_List_Button.clicked.connect(lambda: self.next_list(table,query))
        self.Previous_List_Button.clicked.connect(lambda: self.previous_list(table,query))
        
    def selctedList(self, selected):
        global row
        
        # get row of selected cell
        for ix in selected.indexes():
            row = ix.row()

        list_name = self.Lists_TableWidget.item(row,0).text()

        query = "SELECT status, username FROM viplists WHERE name = '"+list_name+"'"
        res = database(query)
        status = str(res[0][0])

        if(status == "Public"):
            self.mylistpageclicked("SELECT Lid FROM viplists WHERE username = '"+str(res[0][1])+"'")
        elif(status == "Friends"):
            query = "SELECT status FROM friendship WHERE username2 = '"+username+"' and status = 'accepted'"
            res = database(query)
            if(len(res) == 0):
                error_message("This list is observable just for friends")
            else:
                self.mylistpageclicked("SELECT Lid FROM viplists WHERE username = '"+str(res[0][1])+"'")    
        elif(username == str(res[0][1])):
            self.mylistpageclicked("SELECT Lid FROM viplists WHERE username = '"+str(res[0][1])+"'")
        else:
            error_message("This list is private")          

    def friendspageclicked(self):
        global current_table
        current_table = 0

        query = "SELECT DISTINCT username1, score, status FROM user Join friendship WHERE status = 'accepted' and user.username = friendship.username1"
        table = self.Friends_List_TableWidget
        self.loadingData(table, query + " LIMIT "+str(current_table)+",10")

        self.stackedWidget.setCurrentWidget(self.Friends_page)

        self.NewFriend_Button.clicked.connect(lambda: self.make_new_friend())
        self.friendshipRequest_Button.clicked.connect(lambda: self.friendship_request())
        self.yourRequest_Button.clicked.connect(lambda: self.your_request())

        self.next_friends_Button.clicked.connect(lambda: self.next_list(table,query))
        self.previous_friends_Button.clicked.connect(lambda: self.previous_list(table,query))

    def friendship_request(self):
        table = self.Friends_List_TableWidget
        query = "SELECT distinct username2, score, status FROM friendship Join user WHERE username1 = '"+username+"' and user.username = friendship.username2"
        self.loadingData(table, query)

    def your_request(self):
        table = self.Friends_List_TableWidget
        query = "SELECT distinct username1, score, status FROM friendship Join user WHERE username2 = '"+username+"' and user.username = friendship.username1"
        self.loadingData(table, query)

        # select a list in the tabel
        table.selectionModel().selectionChanged.connect(self.selected_friendship)

    def selected_friendship(self,selected):
        global row
        
        # get row of selected cell
        for ix in selected.indexes():
            row = ix.row()

        username1 = self.Friends_List_TableWidget.item(row,0).text()

        self.stackedWidget.setCurrentWidget(self.friendship_status_page)
        self.accept_Button.clicked.connect(lambda: self.friendship_status(username1, "accept"))
        self.deny_Button.clicked.connect(lambda: self.friendship_status(username1, "deny"))
    
    def friendship_status(self,username1,status):
        if(status == "accept"):
            query = "UPDATE friendship SET status = 'accepted' WHERE username1 = '"+username1+"' and username2 = '"+username+"'"
            admin_log("Accepted "+username1+" friendship request")
        else:
            query = "UPDATE friendship SET status = 'denied' WHERE username1 = '"+username1+"' and username2 = '"+username+"'"
            admin_log("denied "+username1+" friendship request")
        database(query)

    def make_new_friend(self):
        text, ok = QInputDialog.getText(None, "Attention", "your friend username?", QLineEdit.Normal)
        if ok and text:

            username_of_friend = text
            query = "SELECT username , score FROM user WHERE username = '"+username_of_friend+"'"
            res = database(query)
            if(len(res) != 0):
                query = "INSERT INTO friendship VALUES ('"+username+"','"+username_of_friend+"','in progress')"
                database(query)
                admin_log("Send a request friendship to "+username_of_friend+"")
            else:
                error_message("Please enter a correct username")

    def acountpageclicked(self):
        global current_table
        current_table = 0

        query = "SELECT amount FROM user WHERE username = '"+username+"'"
        res = database(query)
        
        #Account page
        self.Amout_LineEdit.setText(str(res[0][0]))   

        self.stackedWidget.setCurrentWidget(self.Account_page)

        self.Increase_Account_Button.clicked.connect(self.increaseAmount)
    
    def increaseAmount(self):
        increase_amount = self.increase_LineEdit.text()
        first_amount = self.Amout_LineEdit.text()
        if(increase_amount != ""):
            final_amount = float(increase_amount) + float(first_amount)
        else: 
            final_amount = float(first_amount)

        query = "UPDATE user SET amount = '"+str(final_amount)+"' WHERE username = '"+username+"'"
        database(query)
        admin_log("Incresed amount to "+str(final_amount)+"")

        self.update() # update right after increase doesn't work

    ########################################################################
    # Slide left menu
    ########################################################################
    def slideLeftMenu(self):
        # Get current left menu width
        width = self.left_side_menu.width()

        # If minimized
        if width == 50:
            # Expand menu
            newWidth = 150
        # If maximized
        else:
            # Restore menu
            newWidth = 50

        # Animate the transition
        self.animation = QPropertyAnimation(self.left_side_menu, b"minimumWidth")#Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)#Start value is the current menu width
        self.animation.setEndValue(newWidth)#end value is the new menu width
        # self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

def database(query):
        try:
            db = mdb.connect('localhost','root','','test')
            db.autocommit = False
            cursor = db.cursor() 
            cursor.execute(query)
            res = cursor.fetchall()
            db.commit()
            return res
        except(db.Error) as e:
            
            print(e)
            error_message("There is a problem")
            db.rollback()
            return "v"
        finally:
            db.close()
    
def admin_log(action):
    # query = "CREATE TRIGGER b_update before update on log for each row begin "
    # query += "INSERT INTO log (username, action) VALUES ('"+username+"', '"+action+"'); END"  
    query = "INSERT INTO log (username, action) VALUES ('"+username+"', '"+action+"')"    
    database(query)

def error_message(err):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(err)
    msg.setWindowTitle("Error")
    msg.exec_()

username = ""
mvname = ""
current_table = 0 # if next button clicked then this variable become 1
ct = 0 # choose between tables for showing movies

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginwindow = Login()
    # mainwindow = Show()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(loginwindow)
    # widget.addWidget(mainwindow)

    widget.show()
    app.exec_()