import psycopg2
import PyQt5
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap


qtCreatorfile = "milestone1.ui"


Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorfile)

# Application

class milestone1practice(QMainWindow):
    def __init__(self):
        super(milestone1practice, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.zipcodeChanged)
        self.ui.zipCodeList.itemSelectionChanged.connect(self.businessCategoriesChanged)
        self.ui.businessCategories.itemSelectionChanged.connect(self.businessFilter)
        self.ui.zipCodeList.itemSelectionChanged.connect(self.GetZipCodeStats)
        self.ui.zipCodeList.itemSelectionChanged.connect(self.GetZipCodeStats1)
        self.ui.zname.textChanged.connect(self.getBusinessNames)
        self.ui.businesses.itemSelectionChanged.connect(self.DisplayBusinessZipcode)

    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect(host='localhost',dbname='milestone1datab',user='postgres',password='Patriots12!',)
        except:
            print('Unable to connect to database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM business ORDER by state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex()>=0):
            sql_str = "SELECT distinct city FROM business WHERE state = '" + state + "' ORDER by city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed!")


    def zipcodeChanged(self):
        self.ui.zipCodeList.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT distinct zipcode, state, city FROM business WHERE state = '" + state + "' AND city = '" + city + "'ORDER BY zipcode;"
            results = self.executeQuery(sql_str)
            print(results)
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.zipCodeList.addItem(row[0])
            except:
                print("Query failed!")

    def businessCategoriesChanged(self):
        self.ui.businessCategories.clear()
        if (len(self.ui.zipCodeList.selectedItems()) > 0):
            zipcodes = self.ui.zipCodeList.selectedItems()[0].text()
            sql_str = "SELECT distinct category_name FROM business, categories WHERE zipcode = '" + zipcodes + "' AND categories.business_id=business.business_id ORDER BY category_name;"
            results = self.executeQuery(sql_str)
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.businessCategories.addItem(row[0])
            except:
                print("Query failed!")

    def businessFilter(self):
        self.ui.businessCategories2.clear()
        if (len(self.ui.businessCategories.selectedItems()) > 0):
            category1 = self.ui.businessCategories.selectedItems()[0].text()
            zipcodes = self.ui.zipCodeList.selectedItems()[0].text()
            sql_str = "SELECT distinct business_name FROM business, categories WHERE category_name = '" + category1 + "' AND zipcode = '" + zipcodes + "' AND categories.business_id=business.business_id ORDER BY business_name;"
            results = self.executeQuery(sql_str)
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.businessCategories2.addItem(row[0])
            except:
                print("Query failed!")


    def getBusinessNames(self):
        self.ui.businesses.clear()
        zipcodename = self.ui.zname.text()
        sql_str = "SELECT distinct zipcode from business WHERE zipcode LIKE '%"+zipcodename+"%' ORDER BY zipcode;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.businesses.addItem(row[0])
        except:
            print("Query failed!")


    def getZipCodesNames(self):
        self.ui.businesses.clear()
        zipcodename = self.ui.zname.text()
        sql_str = "SELECT distinct zipcode from business WHERE zipcode LIKE '%"+zipcodename+"%' ORDER BY zipcode;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.businesses.addItem(row[0])
        except:
            print("Query failed!")

    def DisplayBusinessZipcode(self):
        self.ui.zBusinessTable.clear()
        if (len(self.ui.businesses.selectedItems()) > 0):
            zipcode1 = self.ui.businesses.selectedItems()[0].text()
            # sql_str = "SELECT distinct category_name FROM business, categories WHERE zipcode = '" + zipcodes + "' AND categories.business_id=business.business_id ORDER BY category_name;"
            # results = self.executeQuery(sql_str)

            for i in reversed(range(self.ui.zBusinessTable.rowCount())):
                self.ui.zBusinessTable.removeRow(i)
            sql_str = "SELECT business_name, city, state FROM business WHERE zipcode = '" + zipcode1 + "' ORDER by business_name;"
            try:
                results = self.executeQuery(sql_str)
                style = "::section (""background-color: #f3f3f3; )"
                self.ui.zBusinessTable.setColumnCount(len(results[0]))
                self.ui.zBusinessTable.setRowCount(len(results))
                self.ui.zBusinessTable.setHorizontalHeaderLabels([' Business Name ', 'City', 'State'])
                self.ui.zBusinessTable.resizeColumnsToContents()
                self.ui.zBusinessTable.setColumnWidth(0, 120)
                self.ui.zBusinessTable.setColumnWidth(1, 120)
                self.ui.zBusinessTable.setColumnWidth(2, 120)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.zBusinessTable.setItem(currentRowCount,colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed!")

    def GetZipCodeStats(self):
        self.ui.ZipcodeBusinessTable.clear()
        if (len(self.ui.zipCodeList.selectedItems()) > 0):
            zipcode1 = self.ui.zipCodeList.selectedItems()[0].text()
            ## dont know how to do the top categories
            # sql_str = "SELECT distinct business_name, category_name FROM business full join categories on categories.business_id=business.business_id WHERE zipcode = '" + zipcode1 + "'  ORDER by business_name;"
            sql_str = "SELECT distinct business_name FROM business WHERE zipcode = '" + zipcode1 + "' ORDER by business_name ;"
            results = (str(self.executeQuery(sql_str)))
            try:
                results = self.executeQuery(sql_str)
                style = "::section (""background-color: #f3f3f3; )"
                self.ui.ZipcodeBusinessTable.setColumnCount(len(results[0]))
                self.ui.ZipcodeBusinessTable.setRowCount(len(results))
                self.ui.ZipcodeBusinessTable.setHorizontalHeaderLabels([' Number of Businesses '])
                self.ui.ZipcodeBusinessTable.resizeColumnsToContents()
                self.ui.ZipcodeBusinessTable.setColumnWidth(0, 150)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.ZipcodeBusinessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed!")

    def GetZipCodeStats1(self):
        self.ui.ZipcodeBusinessTable_2.clear()
        if (len(self.ui.zipCodeList.selectedItems()) > 0):
            zipcode1 = self.ui.zipCodeList.selectedItems()[0].text()

            sql_str = "SELECT category_name FROM categories, business WHERE zipcode = '" + zipcode1 + "' AND categories.business_id=business.business_id  ORDER by category_name ;"
            results = (str(self.executeQuery(sql_str)))
            try:
                results = self.executeQuery(sql_str)
                style = "::section (""background-color: #f3f3f3; )"
                self.ui.ZipcodeBusinessTable_2.setColumnCount(len(results[0]))
                self.ui.ZipcodeBusinessTable_2.setRowCount(len(results))
                self.ui.ZipcodeBusinessTable_2.setHorizontalHeaderLabels([' Top Categories '])
                self.ui.ZipcodeBusinessTable_2.resizeColumnsToContents()
                self.ui.ZipcodeBusinessTable_2.setColumnWidth(0, 150)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.ZipcodeBusinessTable_2.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query failed!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = milestone1practice()
    window.show()
    sys.exit(app.exec_())









