from PySide2 import QtCore, QtGui, QtWidgets
import sys
import psycopg2
import psycopg2.extras
import mm3_add_person

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.db = DB()

        self.statusBar()
        self.menubar = self.menuBar()
        self.menubar.addMenu('Файл')

        personsAction = QtWidgets.QAction(QtGui.QIcon('icon.png'), 'Список сотрудников', self)
        personsAction.setShortcut('Ctrl+Q')
        personsAction.triggered.connect(self.table_person)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(personsAction)

        self.mdiarea1 = QtWidgets.QMdiArea()
        self.mdiarea1.setViewMode(QtWidgets.QMdiArea.TabbedView)
        self.mdiarea1.setTabsClosable(True)
        self.mdiarea1.setTabsMovable(True)

        self.setCentralWidget(self.mdiarea1)
        self.resize(900, 480)
        self.setWindowTitle('БухУчет')
        self.show()


    def table_person(self):
        """открыть Список сотрудников в дочерном окне"""
        self.window_person = QtWidgets.QWidget()
        self.window_person.setWindowTitle("Список сотрудников")
        self.mdiarea1.addSubWindow(self.window_person)
        self.gridLayout_person = QtWidgets.QGridLayout(self.window_person)
        spacerItem = QtWidgets.QSpacerItem(156, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_person.addItem(spacerItem, 0, 0, 1, 1)
        self.btn_add_person = QtWidgets.QPushButton("Добавить",self.window_person)
        self.btn_add_person.setMinimumSize(QtCore.QSize(75, 0))
        self.gridLayout_person.addWidget(self.btn_add_person, 0, 1, 1, 1)
        self.btn_izmenit_person = QtWidgets.QPushButton("Изменить",self.window_person)
        self.btn_izmenit_person.setMinimumSize(QtCore.QSize(75, 0))
        self.gridLayout_person.addWidget(self.btn_izmenit_person, 0, 2, 1, 1)
        self.btn_delete_person = QtWidgets.QPushButton("Загрузить",self.window_person)
        self.btn_delete_person.setMinimumSize(QtCore.QSize(75, 0))
        self.gridLayout_person.addWidget(self.btn_delete_person, 0, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(45, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_person.addItem(spacerItem1, 0, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(44, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_person.addItem(spacerItem2, 0, 5, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(45, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_person.addItem(spacerItem3, 0, 6, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(44, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_person.addItem(spacerItem4, 0, 7, 1, 1)

        self.tableWidget_person = QtWidgets.QTableWidget(self.window_person)
        self.tableWidget_person.setMinimumSize(QtCore.QSize(451, 0))
        self.tableWidget_person.setEditTriggers(QtWidgets.QAbstractItemView.SelectedClicked)
        self.tableWidget_person.setTabKeyNavigation(0)
        self.tableWidget_person.setWordWrap(0)
        self.tableWidget_person.setColumnCount(5)
        self.tableWidget_person.setHorizontalHeaderLabels(["Номер №", "ФИО","Дата рождения", "ИИН", "Организация"])
        self.gridLayout_person.addWidget(self.tableWidget_person, 1, 1, 1, 7)

        self.treeWidget_person = QtWidgets.QTreeWidget(self.window_person)
        self.treeWidget_person.setColumnCount(1)
        self.treeWidget_person.setHeaderLabels(["Список"])
        self.l1 = QtWidgets.QTreeWidgetItem(["Все школы"])
        self.l1_child = QtWidgets.QTreeWidgetItem(["Ангар"])
        self.l1.addChild(self.l1_child)
        self.treeWidget_person.addTopLevelItem(self.l1)
        self.gridLayout_person.addWidget(self.treeWidget_person, 1, 0, 1, 1)

        self.btn_add_person.clicked.connect(self.insert_person_window)
        self.btn_delete_person.clicked.connect(self.update_data_table_person)

        self.window_person.show()

    def insert_person_window(self):
        """Добавление нового сотрудника"""
        addPersonWindow = QtWidgets.QWidget()
        self.u1 = mm3_add_person.Ui_Form()
        self.u1.setupUi(addPersonWindow)
        self.mdiarea1.addSubWindow(addPersonWindow)
        self.u1.btn_save.clicked.connect(self.insert_data_table_person)

        addPersonWindow.show()  # список сотрудников

#-----------------------------------------------------LOGIC------------------------------------------------------------------------

    def insert_data_table_person(self):
        """Добавление нового сотрудника в таблицу базы данных person"""
        uName1 = self.u1.lineEdit_FIO.text()
        uData_burn = self.u1.dateEdit_data_born.text()
        uIin1 = self.u1.lineEdit_IIN.text()
        uOrganizacia1 = self.u1.lineEdit_organiz.text()
        with self.db.con:
            self.db.cur.execute("INSERT INTO person (name, data_burn, iin, organizacia) VALUES (%s, %s, %s, %s)", (uName1, uData_burn, uIin1, uOrganizacia1))
            self.db.con.commit()

    def delete_data_person(self):
        """Удаление данных из таблицы person"""
        r = self.tableWidget_person.currentRow()
        uId = self.tableWidget_person.item(r,0).text()
        with self.db.con:
            self.db.cur.execute("DELETE FROM person WHERE id = %s ", ([uId]))
            self.db.con.commit()

    def update_data_table_person(self):
        """Загрузка данных в таблицу из базы данных person"""
        with self.db.con:
            self.db.cur.execute("SELECT * FROM person")
            rows = self.db.cur.fetchall()
            for i in rows:
                row = self.tableWidget_person.rowCount()
                self.tableWidget_person.setRowCount(row+1)

                self.tableWidget_person.setItem(row,0,QtWidgets.QTableWidgetItem(f"{i[0]}"))
                self.tableWidget_person.setItem(row,1,QtWidgets.QTableWidgetItem(f"{i[1]}"))
                self.tableWidget_person.setItem(row,2,QtWidgets.QTableWidgetItem(f"{i[2]}"))
                self.tableWidget_person.setItem(row,3,QtWidgets.QTableWidgetItem(f"{i[3]}"))
                self.tableWidget_person.setItem(row,4,QtWidgets.QTableWidgetItem(f"{i[4]}"))


class DB():
    def __init__(self):
        self.con = psycopg2.connect(database='postgres', user='postgres', password='1')
        self.cur = self.con.cursor()

        with self.con:
            self.cur.execute("CREATE TABLE IF NOT EXISTS person (id SERIAL PRIMARY KEY,name VARCHAR(255),data_burn VARCHAR(255),iin bigint,organizacia VARCHAR(255) )")



app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec_())
