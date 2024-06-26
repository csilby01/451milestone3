import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestone1app.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    def __init__(self):
        super(milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipList.itemSelectionChanged.connect(self.zipChanged)
        self.ui.categoryList.itemSelectionChanged.connect(self.categoryChanged)
        self.ui.clearButton.clicked.connect(self.clearAll)  

    def clearAll(self):
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()
        
        self.ui.cityList.clear()
        self.ui.zipList.clear()
        self.ui.categoryList.clear()

        self.ui.avgIncome.clear()
        self.ui.population.clear()
        self.ui.numBusiness.clear()

        self.clearTable(self.ui.businessTable)
        self.clearTable(self.ui.categoryTable)
        self.clearTable(self.ui.successfulTable)
        self.clearTable(self.ui.popularTable)

    def clearTable(self, table):
        for i in reversed(range(table.rowCount())):
            table.removeRow(i)

    def executeQuery(self, sql_str):
        try: 
            conn = psycopg2.connect("dbname='Milestone2DB' user='postgres' host='localhost' password='password'") #  password='mustafa'
        except:
            print('Unable  to connect to database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("LSL Query Failed!")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        self.ui.zipList.clear()
        self.ui.categoryList.clear()
        state = self.ui.stateList.currentText()
        self.clearTable(self.ui.categoryTable)
        self.clearTable(self.ui.successfulTable)
        self.clearTable(self.ui.popularTable)
        self.clearTable(self.ui.businessTable)

        if (self.ui.stateList.currentIndex() >= 0):
            sql_str = "SELECT DISTINCT city FROM business WHERE state='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("SC Query Failed")

        sql_str ="SELECT name, address, city, stars, review_count, reviewrating, numcheckins FROM business WHERE state= '" + state + "' ORDER BY name;" 
        try:
            results = self.executeQuery(sql_str)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable.setColumnCount(len(results[0]))
            self.ui.businessTable.setRowCount(len(results))
            self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Number of Checkins'])
            self.ui.businessTable.resizeColumnsToContents()
            self.ui.businessTable.setColumnWidth(0,200)
            self.ui.businessTable.setColumnWidth(1,150)
            self.ui.businessTable.setColumnWidth(2,100)
            self.ui.businessTable.setColumnWidth(3,50)
            self.ui.businessTable.setColumnWidth(4,100)
            self.ui.businessTable.setColumnWidth(5,100)
            self.ui.businessTable.setColumnWidth(6,60)
            currentRow = 0
            for row in results:
                for colCount in range(0, len(results[0])):
                    self.ui.businessTable.setItem(currentRow, colCount, QTableWidgetItem(str(row[colCount])))
                currentRow +=1
        except:
            print("SC2 Query Failed")

    def cityChanged(self):
        self.ui.zipList.clear()
        self.ui.categoryList.clear()
        self.clearTable(self.ui.categoryTable)
        self.clearTable(self.ui.successfulTable)
        self.clearTable(self.ui.popularTable)
        if (self.ui.stateList.currentIndex() >=0 ) and (len(self.ui.cityList.selectedItems()) > 0):
            city = self.ui.cityList.selectedItems()[0].text()
            state = self.ui.stateList.currentText()
            sql_str = "SELECT DISTINCT postal_code FROM business WHERE city='" + city + "' ORDER BY postal_code;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.zipList.addItem(str(row[0]))
            except:
                print("zip Query Failed")
            sql_str ="SELECT name, address, city, stars, review_count, reviewrating, numcheckins FROM business WHERE city='" + city + "' AND state='" + state + "' ORDER BY name;" 
            self.clearTable(self.ui.businessTable)
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Number of Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,200)
                self.ui.businessTable.setColumnWidth(1,150)
                self.ui.businessTable.setColumnWidth(2,100)
                self.ui.businessTable.setColumnWidth(3,50)
                self.ui.businessTable.setColumnWidth(4,100)
                self.ui.businessTable.setColumnWidth(5,100)
                self.ui.businessTable.setColumnWidth(6,60)
                currentRow = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRow, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRow +=1
            except:
                print("CC Query Failed")

    def zipChanged(self):
        self.ui.categoryList.clear()
        self.ui.avgIncome.clear()
        self.ui.population.clear()
        self.ui.numBusiness.clear()
        if (len(self.ui.cityList.selectedItems()) > 0) and (len(self.ui.zipList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zip = self.ui.zipList.selectedItems()[0].text()
            sql_str ="SELECT name, address, city, stars, review_count, reviewrating, numcheckins FROM business WHERE city='" + city + "' AND state='" + state + "' AND postal_code=" + zip + " ORDER BY name;" 
            self.clearTable(self.ui.businessTable)
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Number of Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,200)
                self.ui.businessTable.setColumnWidth(1,150)
                self.ui.businessTable.setColumnWidth(2,100)
                self.ui.businessTable.setColumnWidth(3,50)
                self.ui.businessTable.setColumnWidth(4,100)
                self.ui.businessTable.setColumnWidth(5,100)
                self.ui.businessTable.setColumnWidth(6,60)
                currentRow = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRow, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRow +=1
            except:
                print("business Query Failed")

            sql_str = "SELECT DISTINCT category_name FROM Business JOIN Categories ON Business.business_id = Categories.business_id WHERE city = '"+ city + "' AND postal_code = "  + zip + " ORDER BY category_name;"
            print(sql_str)
            results = self.executeQuery(sql_str) 
            for row in results:
                self.ui.categoryList.addItem(str(row[0]))

            sql_str = "SELECT meanincome FROM zipcodedata WHERE zipcode = '" + str(zip) + "';"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.avgIncome.addItem(str(row[0]))
            except:
                print("income Query Failed")

            sql_str = "SELECT population FROM zipcodedata WHERE zipcode = '" + str(zip) + "';"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.population.addItem(str(row[0]))
            except:
                print("population Query Failed")

            sql_str = "SELECT COUNT(business_id) FROM business WHERE postal_code  = " + str(zip) + ";"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.numBusiness.addItem(str(row[0]))
            except:
                print("zip Query Failed")


            sql_str = "SELECT category_name, COUNT(category_name) FROM categories as cat JOIN business as bus ON cat.business_id = bus.business_id WHERE postal_code = " + str(zip) + " GROUP BY category_name ORDER BY COUNT(category_name) DESC"
            self.clearTable(self.ui.categoryTable)
            results = self.executeQuery(sql_str)
            print(sql_str)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.categoryTable.horizontalHeader().setStyleSheet(style)
            self.ui.categoryTable.setColumnCount(len(results[0]))
            self.ui.categoryTable.setRowCount(len(results))
            self.ui.categoryTable.setHorizontalHeaderLabels(['Category Name', '# of Businesses'])
            self.ui.categoryTable.resizeColumnsToContents()
            self.ui.categoryTable.setColumnWidth(0,200)
            self.ui.categoryTable.setColumnWidth(1,155)
            currentRow = 0
            for row in results:
                for colCount in range(0, len(results[0])):
                    self.ui.categoryTable.setItem(currentRow, colCount, QTableWidgetItem(str(row[colCount])))
                currentRow +=1
            
            # Successful Business Table
            sql_str = "SELECT name, city, reviewrating, review_count AS avgReviewCount FROM Business JOIN Categories AS Cat on Business.business_id = Cat.business_id JOIN(SELECT AVG(review_count) AS averageReviews, category_name FROM Business JOIN Categories on Business.business_id = Categories.business_id GROUP BY category_name) AS Average ON Average.category_name = Cat.category_name GROUP BY Business.business_id, business.name HAVING review_count > AVG(averageReviews) AND reviewrating >= 4.0 AND postal_code = " + str(zip) + " ORDER BY reviewrating DESC"
            self.clearTable(self.ui.successfulTable)
            try:
                print(sql_str)
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.successfulTable.horizontalHeader().setStyleSheet(style)
                self.ui.successfulTable.setColumnCount(len(results[0]))
                self.ui.successfulTable.setRowCount(len(results))
                self.ui.successfulTable.setHorizontalHeaderLabels(['Business Name', 'City', 'Average Rating', 'Review Count'])
                self.ui.successfulTable.resizeColumnsToContents()
                self.ui.successfulTable.setColumnWidth(0,150)
                self.ui.successfulTable.setColumnWidth(1,100)
                self.ui.successfulTable.setColumnWidth(2,110)
                self.ui.successfulTable.setColumnWidth(3,50)
                currentRow = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.successfulTable.setItem(currentRow, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRow +=1
            except:
                print("Success table failed")

            # Popular Business Table
            sql_str = "SELECT Business.name, Business.city, Business.stars, numCheckins FROM Business JOIN (SELECT AVG(numCheckins) AS avgCheckins, postal_code FROM Business GROUP BY postal_code) AS Average ON Business.postal_code = Average.postal_code WHERE numCheckins > avgCheckins AND Business.postal_code = " + str(zip) +" ORDER BY Business.reviewrating;"
            self.clearTable(self.ui.popularTable)
            try:
                print(sql_str)
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.popularTable.horizontalHeader().setStyleSheet(style)
                self.ui.popularTable.setColumnCount(len(results[0]))
                self.ui.popularTable.setRowCount(len(results))
                self.ui.popularTable.setHorizontalHeaderLabels(['Business Name', 'City', 'Stars', '# of Checkins'])
                self.ui.popularTable.resizeColumnsToContents()
                self.ui.popularTable.setColumnWidth(0,190)
                self.ui.popularTable.setColumnWidth(1,100)
                self.ui.popularTable.setColumnWidth(2,70)
                self.ui.popularTable.setColumnWidth(3,100)
                currentRow = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.popularTable.setItem(currentRow, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRow +=1
            except:
                print("Popular table failed")

    def categoryChanged(self):
        if (len(self.ui.zipList.selectedItems()) > 0 and len(self.ui.categoryList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zip = self.ui.zipList.selectedItems()[0].text()
            category = self.ui.categoryList.selectedItems()[0].text()
            sql_str ="SELECT name, address, city, stars, review_count, reviewrating, numcheckins FROM business JOIN Categories ON Business.business_id = Categories.business_id WHERE city='" + city + "' AND state='" + state + "' AND postal_code=" + zip + " AND category_name = '" + category  + "' ORDER BY name;" 
            self.clearTable(self.ui.businessTable)
            try:    
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Number of Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,200)
                self.ui.businessTable.setColumnWidth(1,150)
                self.ui.businessTable.setColumnWidth(2,100)
                self.ui.businessTable.setColumnWidth(3,50)
                self.ui.businessTable.setColumnWidth(4,100)
                self.ui.businessTable.setColumnWidth(5,100)
                self.ui.businessTable.setColumnWidth(6,60)
                currentRow = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRow, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRow +=1
            except:
                print("category Query Failed")

#sql query for popular categories - needs to be based on the state, city, zip
# """SELECT category_name, COUNT(category_name)
# FROM categories as cat
# JOIN business as bus ON cat.business_id = bus.business_id
# GROUP BY category_name
# ORDER BY COUNT(category_name) DESC"""
                

#sql query for getting businesses that belong to a specific category
# """SELECT DISTINCT name
# FROM business as bus
# JOIN categories as cat ON bus.business_id = cat.business_id
# WHERE category_name = " + category_name "
# ORDER BY name"""


#sql query for getting population and avg income
# """SELECT meanIncome, population
# FROM zipcodedata
# WHERE zipcode = "+ zip +"
# ORDER BY population DESC"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec_())
