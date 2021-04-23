# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 13:28:05 2021

@author: dana.kenney
"""
import psycopg2
import PyQt5
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
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
        
        self.ui.displayname.setReadOnly(True)
        self.ui.displaystars.setReadOnly(True)
        self.ui.displayfans.setReadOnly(True)
        self.ui.displayyelpingsince.setReadOnly(True)
        self.ui.displayfunnyvotes.setReadOnly(True)
        self.ui.displaycoolvotes.setReadOnly(True)
        self.ui.displayusefulvotes.setReadOnly(True)
        
        self.ui.name.editingFinished.connect(self.nameChanged)
        self.ui.userid.currentTextChanged.connect(self.userIdChanged)
        #self.loadStateList()
        #self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        #self.ui.cityList.itemSelectionChanged.connect(self.zipcodeChanged)
        #self.ui.zipCodeList.itemSelectionChanged.connect(self.businessCategoriesChanged)
        #self.ui.businessCategories.itemSelectionChanged.connect(self.businessFilter)
        #self.ui.zipCodeList.itemSelectionChanged.connect(self.GetZipCodeStats)
        #self.ui.zipCodeList.itemSelectionChanged.connect(self.GetZipCodeStats1)
        #self.ui.zname.textChanged.connect(self.getBusinessNames)
        #self.ui.businesses.itemSelectionChanged.connect(self.DisplayBusinessZipcode)

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
    
    
    def nameChanged(self):
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
        self.ui.userid.clearEditText()
    
    def userIdChanged(self):
        userid = self.ui.userid.currentText()
        name = self.ui.name.text()

        sql_str1 = "SELECT average_stars FROM users WHERE userid ='" + userid + "';"
        sql_str2 = "SELECT fans FROM users WHERE userid ='" + userid + "';"        
        sql_str3 = "SELECT yelping_since FROM users WHERE userid ='" + userid + "';"
        
        self.ui.displayname.clear()
        self.ui.displaystars.clear()
        self.ui.displayfans.clear()
        self.ui.displayyelpingsince.clear()
        
        if (self.ui.userid.currentIndex()>=0):
            try:
                self.ui.displayname.setText(name)
            
                stars = self.executeQuery(sql_str1)
                self.ui.displaystars.setText(str(stars[0][0]))
                
                fans = self.executeQuery(sql_str2)
                self.ui.displayfans.setText(str(fans[0][0]))

                yelpingsince = self.executeQuery(sql_str3)
                self.ui.displayyelpingsince.setText(str(yelpingsince[0][0]))
                
            except:
                print("Query failed!")
            
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = milestone3user()
    window.show()
    sys.exit(app.exec_())