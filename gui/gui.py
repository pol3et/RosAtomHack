#!/usr/bin/python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog
from PyQt5.QtCore import QRect


class ScanWindow(QWidget):
    def __init__(self):
        super(ScanWindow, self).__init__()
        self.setWindowTitle('Scan')

        self.setGeometry(800, 600, 800, 600)

        self.choose_file_button = QPushButton(self)
        self.choose_file_button.setGeometry(QRect(310, 200, 180, 60))
        self.choose_file_button.setText('Choose file')
        self.choose_file_button.show()

        self.scan_button = QPushButton(self)
        self.scan_button.setGeometry(QRect(310, 280, 180, 60))
        self.scan_button.setText('Scan')
        self.scan_button.show()

        self.choose_file_action()
        self.scan_action()

    def choose_file_action(self):
        self.choose_file_button.clicked.connect(self.file_explorer)

    def scan_action(self):
        self.scan_button.clicked.connect(self.scanning)

    def file_explorer(self):
        fname = QFileDialog.getExistingDirectory(
            self, 'Выбрать файл или папку', '')

        if fname:
            self.file_path = fname
            print(f'Выбранный файл: {self.file_path}')

    def scanning(self):
        if self.file_path:
            print(f'Сканирую выбранный файл: {self.file_path}')


class SettingsWindow(QWidget):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.setWindowTitle('Settings')

        self.setGeometry(800, 600, 800, 600)

        self.choose_file_button = QPushButton(self)
        self.choose_file_button.setGeometry(QRect(310, 200, 180, 60))
        self.choose_file_button.setText('Choose file')
        self.choose_file_button.show()

        self.train_button = QPushButton(self)
        self.train_button.setGeometry(QRect(310, 280, 180, 60))
        self.train_button.setText('Train')
        self.train_button.show()

        self.choose_file_action()
        self.train_action()

    def choose_file_action(self):
        self.choose_file_button.clicked.connect(self.file_explorer)

    def train_action(self):
        self.train_button.clicked.connect(self.training)

    def file_explorer(self):
        fname = QFileDialog.getExistingDirectory(
            self, 'Выбрать файл или папку', '')

        if fname:
            self.file_path = fname
            print(f'Выбранный файл: {self.file_path}')

    def training(self):
        if self.file_path:
            print(f'Дообучаю на выбранном файле: {self.file_path}')


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.scanButton = QtWidgets.QPushButton(self.centralwidget)
        self.scanButton.setGeometry(QtCore.QRect(310, 200, 181, 61))
        self.scanButton.setObjectName("scanButton")

        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setGeometry(QtCore.QRect(310, 280, 181, 61))
        self.settingsButton.setObjectName("settingsButton")

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.scan_action()
        self.settings_action()

    def scan_action(self):
        self.scanButton.clicked.connect(self.show_scan_window)

    def settings_action(self):
        self.settingsButton.clicked.connect(self.show_settings_window)

    def show_scan_window(self):
        self.scan_w = ScanWindow()
        self.scan_w.show()

    def show_settings_window(self):
        self.settings_w = SettingsWindow()
        self.settings_w.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Anomaly Scaner"))
        self.scanButton.setText(_translate("MainWindow", "Scan"))
        self.settingsButton.setText(_translate("MainWindow", "Settings"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
