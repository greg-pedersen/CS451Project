# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 13:28:05 2021

@author: dana.kenney
"""
import psycopg2
import PyQt5
import sys
from PyQt5.QtWidgets import QHeaderView, QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap


qtCreatorfile = "milestone3user.ui"


Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorfile)

# Application

class milestone3user(QMainWindow):
    def __init__(self):
        super(milestone3user, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.displaylatesttips.setColumnCount(5)
        self.ui.displaylatesttips.setHorizontalHeaderLabels(('Friend','Business','City','Date','Review'))
        self.ui.displaylatesttips.verticalHeader().setVisible(False)
        
        self.ui.displayfriends.setColumnCount(5)
        self.ui.displayfriends.setHorizontalHeaderLabels(('Name','Stars','Fans','# Tips','Yelping Since'))
        self.ui.displayfriends.verticalHeader().setVisible(False)
        
        self.ui.displayfriendsoffriends.setColumnCount(6)
        self.ui.displayfriendsoffriends.setHorizontalHeaderLabels(('Degree','Name','Stars','Fans','# Tips','Yelping Since'))
        self.ui.displayfriendsoffriends.verticalHeader().setVisible(False)
        
        self.ui.displayrecommendedfriends.setColumnCount(6)
        self.ui.displayrecommendedfriends.setHorizontalHeaderLabels(('Mutual Friends','Name','Stars','Fans','# Tips','Yelping Since'))
        self.ui.displayrecommendedfriends.verticalHeader().setVisible(False)

        self.ui.displayname.setReadOnly(True)
        self.ui.displaystars.setReadOnly(True)
        self.ui.displayfans.setReadOnly(True)
        self.ui.displayyelpingsince.setReadOnly(True)
        self.ui.displayfunnyvotes.setReadOnly(True)
        self.ui.displaycoolvotes.setReadOnly(True)
        self.ui.displayusefulvotes.setReadOnly(True)
        
        self.ui.name.editingFinished.connect(self.nameChanged)
        self.ui.userid.activated.connect(self.userIdChanged)

    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect(host='localhost',dbname='term project',user='postgres',password='danak2000',)
        except:
            print('Unable to connect to database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result
    
    def executeQueryNoValue(self, sql_str):
        try:
            conn = psycopg2.connect(host='localhost',dbname='term project',user='postgres',password='danak2000',)
        except:
            print('Unable to connect to database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        conn.close()
    
    
    def nameChanged(self):
        self.ui.userid.clearEditText()
        self.ui.displaylatesttips.setRowCount(0)
        self.ui.displayfriends.setRowCount(0)
        self.ui.displayfriendsoffriends.setRowCount(0)
        self.ui.displayrecommendedfriends.setRowCount(0)
        
        name = self.ui.name.text()
        sql_str = "SELECT userid FROM users WHERE username = '" + name + "' ORDER by username;"
        self.ui.userid.clear()

        try:
            results = self.executeQuery(sql_str)
            i=1
            for row in results:
                self.ui.userid.insertItem(i, row[0])
                i = i+1
        except:
            print("Query failed!")
        
        self.ui.userid.setCurrentIndex(-1)
    
    def userIdChanged(self):
        if self.ui.userid.currentIndex() >= 0:
            self.ui.userid.clearEditText()
            self.ui.displaylatesttips.setRowCount(0)
            self.ui.displayfriends.setRowCount(0)
            self.ui.displayfriendsoffriends.setRowCount(0)
            self.ui.displayrecommendedfriends.setRowCount(0)
            
            userid = self.ui.userid.currentText()
            name = self.ui.name.text()
    
            querystars = "SELECT average_stars FROM users WHERE userid ='" + userid + "';"
            queryfans = "SELECT fans FROM users WHERE userid ='" + userid + "';"        
            queryyelpingsince = "SELECT yelping_since FROM users WHERE userid ='" + userid + "';"
            queryfunny = "SELECT funnyvotes FROM users WHERE userid ='" + userid + "';"
            querycool = "SELECT coolvotes FROM users WHERE userid ='" + userid + "';"
            queryuseful = "SELECT usefulvotes FROM users WHERE userid ='" + userid + "';"
            
            querylatest = "SELECT t1.userid, username, recent INTO temp1 FROM \
                		(SELECT userid, max(tipdate) as recent \
                    		FROM tip \
                    		GROUP BY userid) as t1 \
                    	INNER JOIN ( \
                    		SELECT userid, username FROM users \
                    	 	WHERE users.userid in \
                     		(SELECT friendid \
                     		FROM friend \
                     		WHERE friend.userid = '" + userid + "')) as t2 \
                    	ON t1.userid = t2.userid;\
                        SELECT username, business_name, city, recent, tiptext FROM \
                        (temp1 INNER JOIN tip on temp1.recent = tip.tipdate and temp1.userid = tip.userid) \
                        INNER JOIN business on businessid = business.business_id \
                        ORDER BY recent DESC"
                        
            queryfriends = "SELECT username, average_stars, fans, tipcount, yelping_since \
                            FROM users \
                            WHERE users.userid in \
		        			(Select friendid\
    				    	FROM friend\
            	    		WHERE friend.userid = '" + userid + "') ORDER BY username"
                                
            queryfriendsoffriends = "WITH RECURSIVE friendsoffriends (userid,friendid,currentlevel) AS (\
	                                 SELECT distinct f.userid, f.friendid, 1 as currentlevel\
	                                 FROM friend join friend as f\
	                                 ON friend.friendid = f.userid\
	                                 WHERE friend.userid = '" + userid + "'\
                                UNION ALL\
                                	SELECT distinct friend.userid, friend.friendid, currentlevel+1\
                                	FROM friendsoffriends join friend\
                                	ON friendsoffriends.friendid = friend.userid\
                                	WHERE currentlevel < 2)\
                                    SELECT distinct currentlevel as degree, username, average_stars, fans, tipcount, yelping_since\
                                    FROM friendsoffriends inner join users ON friendsoffriends.friendid = users.userid\
                                    WHERE friendsoffriends.friendid !='" + userid + "' and friendsoffriends.friendid not in\
                                    (SELECT friendid FROM friend WHERE userid = '" + userid + "')\
                                    ORDER BY degree,username;"
                                    
            queryrecommendedfriends = "SELECT mutuals, username, average_stars, fans, tipcount, yelping_since\
                                        FROM\
                                        	(SELECT count(t1.userid) as mutuals, friendid\
                                        		FROM\
                                        			(SELECT f.userid,f.friendid FROM\
                                        			friend INNER JOIN friend as f\
                                        			ON friend.friendid = f.userid\
                                        			WHERE friend.userid = '" + userid + "') as t1\
                                        	GROUP BY friendid) as t2\
                                        INNER JOIN\
                                        	users\
                                        ON t2.friendid = users.userid\
                                        WHERE friendid != '" + userid + "' and mutuals >=3\
                                        ORDER BY mutuals DESC"
                                                
            self.ui.displayname.clear()
            self.ui.displaystars.clear()
            self.ui.displayfans.clear()
            self.ui.displayyelpingsince.clear()
            self.ui.displayfunnyvotes.clear()
            self.ui.displaycoolvotes.clear()
            self.ui.displayusefulvotes.clear()
            
            try:
                #USER INFORMATION
                self.ui.displayname.setText(name)
            
                stars = self.executeQuery(querystars)
                self.ui.displaystars.setText(str(stars[0][0]))
                
                fans = self.executeQuery(queryfans)
                self.ui.displayfans.setText(str(fans[0][0]))
    
                yelpingsince = self.executeQuery(queryyelpingsince)
                self.ui.displayyelpingsince.setText(str(yelpingsince[0][0]))
                
                funny = self.executeQuery(queryfunny)
                self.ui.displayfunnyvotes.setText(str(funny[0][0]))
                cool = self.executeQuery(querycool)
                self.ui.displaycoolvotes.setText(str(cool[0][0]))
                useful = self.executeQuery(queryuseful)
                self.ui.displayusefulvotes.setText(str(useful[0][0]))
                
                #RECENT TIPS OF FRIENDS
                recenttips = self.executeQuery(querylatest)
                self.executeQueryNoValue("DROP TABLE temp1")
                
                for rownum, rowcontent in enumerate(recenttips):
                    self.ui.displaylatesttips.insertRow(rownum)
                    for colnum, colcontent in enumerate(rowcontent):
                        self.ui.displaylatesttips.setItem(rownum,colnum, QTableWidgetItem(str(colcontent)))
                self.ui.displaylatesttips.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
                self.ui.displaylatesttips.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
                self.ui.displaylatesttips.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
                self.ui.displaylatesttips.setHorizontalHeaderLabels(('Friend','Business','City','Date','Review'))
                
                #MY FRIENDS
                friends = self.executeQuery(queryfriends)
                
                for rownum, rowcontent in enumerate(friends):
                    self.ui.displayfriends.insertRow(rownum)
                    for colnum, colcontent in enumerate(rowcontent):
                        self.ui.displayfriends.setItem(rownum,colnum, QTableWidgetItem(str(colcontent)))
                self.ui.displayfriends.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
                self.ui.displayfriends.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
                self.ui.displayfriends.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
                self.ui.displayfriends.setHorizontalHeaderLabels(('Name','Stars','Fans','# Tips','Yelping Since'))
                
                #MY FRIENDS OF FRIENDS
                friendsoffriends = self.executeQuery(queryfriendsoffriends)
                
                for rownum, rowcontent in enumerate(friendsoffriends):
                    self.ui.displayfriendsoffriends.insertRow(rownum)
                    for colnum, colcontent in enumerate(rowcontent):
                        self.ui.displayfriendsoffriends.setItem(rownum,colnum, QTableWidgetItem(str(colcontent)))
                self.ui.displayfriendsoffriends.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
                self.ui.displayfriendsoffriends.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
                self.ui.displayfriendsoffriends.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
                self.ui.displayfriendsoffriends.setHorizontalHeaderLabels(('Degree','Name','Stars','Fans','# Tips','Yelping Since'))
                
                #MY RECOMMENDED FRIENDS
                recommendedfriends = self.executeQuery(queryrecommendedfriends)
                
                for rownum, rowcontent in enumerate(recommendedfriends):
                    self.ui.displayrecommendedfriends.insertRow(rownum)
                    for colnum, colcontent in enumerate(rowcontent):
                        self.ui.displayrecommendedfriends.setItem(rownum,colnum, QTableWidgetItem(str(colcontent)))
                self.ui.displayrecommendedfriends.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
                self.ui.displayrecommendedfriends.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
                self.ui.displayrecommendedfriends.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
                self.ui.displayrecommendedfriends.setHorizontalHeaderLabels(('Mutual Friends','Name','Stars','Fans','# Tips','Yelping Since'))
                
            except:
                print("Query failed!")
    
       
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = milestone3user()
    window.show()
    sys.exit(app.exec_())