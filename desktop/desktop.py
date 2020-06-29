# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!
import calendar
import locale
import platform
import sqlite3
from time import gmtime, strftime, timezone

from uuid import getnode as get_mac

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlRelationalTableModel


def createConnection():
    # Сообщаем, что в качестве БД была выбрана SQLite
    db = QSqlDatabase.addDatabase('QSQLITE')
    # Указываем имя базы данных
    db.setDatabaseName('database.db')
    # Открываем БД
    db.open()
    return db


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        self.tabWidget.setObjectName("tabWidget")

        # TAB 1
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")

        # Admin site integration
        self.webView = QtWebEngineWidgets.QWebEngineView(self.tab)
        self.webView.setUrl(QtCore.QUrl("http://185.188.182.76:8000/admin"))
        self.webView.resize(1200, 800)
        self.webView.setObjectName("webView")

        # TAB 2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        # Desktop Database integration
        self.devices_table = QtWidgets.QTableView(self.tab_2)
        self.devices_table.setGeometry(QtCore.QRect(0, 0, 1200, 800))
        self.devices_table.setObjectName("tableView")

        self.devices_table_UI()

        self.add_record()  # !!!

        last_month_day = calendar.monthrange(int(strftime("%Y", gmtime())), int(strftime("%m", gmtime())))[1]
        today = strftime("%d", gmtime())
        if last_month_day == today:
            self.add_record()

        self.tabWidget.addTab(self.tab_2, "")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setWindowIcon(QtGui.QIcon('label.ico'))

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def devices_table_UI(self):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS devices(id INTEGER PRIMARY KEY AUTOINCREMENT, mac_address TEXT, os_version TEXT, architecture TEXT, locale TEXT, timezone TEXT, last_update TEXT)")
        c.close()

        self.devices_model = QSqlRelationalTableModel(db=createConnection())
        self.devices_model.setTable('devices')
        self.devices_model.select()

        # self.drivers_table.setEditTriggers(QAbstractItemView.CurrentChanged)
        self.devices_table.setModel(self.devices_model)
        self.devices_table.hideColumn(self.devices_model.fieldIndex('id'))

        # Делаем ресайз колонок по содержимому
        self.devices_table.resizeColumnsToContents()

    def add_record(self):
        rec = self.devices_model.record()
        data = [
            get_mac(),  # mac-address
            platform.platform(),
            platform.machine(),
            locale.getdefaultlocale()[0],
            str(timezone / 3600.0),
            strftime("%Y-%m-%d %H:%M:%S", gmtime())
        ]
        for i in range(len(data)):
            rec.setValue(rec.field(i + 1).name(), data[i])
        self.devices_model.insertRecord(-1, rec)
        self.devices_model.submit()
        self.devices_model.select()
        self.devices_table.resizeColumnsToContents()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Polydroid Desktop"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "AdminSite"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Desktop DB"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
