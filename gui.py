#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog, QVBoxLayout, QGraphicsView, QGraphicsScene, QMessageBox
from PyQt5.QtGui import QPixmap
import os
# from TrainedModel import yolo_detection


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Меню')
        self.setStyleSheet(u"background-color: rgb(192, 191, 188);")
        self.setGeometry(0, 0, 1920, 1080)

        layout = QVBoxLayout()

        self.detection_button = QPushButton(self)
        self.detection_button.setFixedSize(200, 50)
        self.detection_button.setText('Детекция')
        self.detection_button.clicked.connect(self.show_detection_window)
        layout.addWidget(self.detection_button)

        self.settings_button = QPushButton(self)
        self.settings_button.setFixedSize(200, 50)
        self.settings_button.setText('Настройки')
        self.settings_button.clicked.connect(self.show_settings_window)
        layout.addWidget(self.settings_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_detection_window(self):
        self.detection_window = DetectionWindow(self)
        self.detection_window.show()
        self.hide()

    def show_settings_window(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()
        self.hide()


class DetectionWindow(QMainWindow):
    def __init__(self, parent):
        super(DetectionWindow, self).__init__()
        self.setWindowTitle('Детекция')
        self.setStyleSheet(u"background-color: rgb(192, 191, 188);")
        self.setGeometry(0, 0, 1920, 1080)

        layout = QVBoxLayout()

        self.choose_folder_button = QPushButton(self)
        self.choose_folder_button.setFixedSize(200, 50)
        self.choose_folder_button.setText('Выберите папку')
        self.choose_folder_button.clicked.connect(self.file_explorer)
        layout.addWidget(self.choose_folder_button)

        self.start_button = QPushButton(self)
        self.start_button.setFixedSize(200, 50)
        self.start_button.setText('Старт')
        self.start_button.clicked.connect(self.start_detection)
        layout.addWidget(self.start_button)

        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)
        layout.addWidget(self.graphics_view)

        self.previous_image = QPushButton(self)
        self.previous_image.setFixedSize(200, 50)
        self.previous_image.setText('-->')
        self.previous_image.clicked.connect(self.show_previous_image)
        layout.addWidget(self.previous_image)

        self.next_image = QPushButton(self)
        self.next_image.setFixedSize(200, 50)
        self.next_image.setText('<--')
        self.next_image.clicked.connect(self.show_next_image)
        layout.addWidget(self.next_image)

        self.back_button = QPushButton(self)
        self.back_button.setFixedSize(200, 50)
        self.back_button.setText('Назад')
        self.back_button.clicked.connect(self.show_menu_window)
        layout.addWidget(self.back_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.image_index = 0
        self.image_paths = []
        self.folder_path = None
        self.parent = parent

    def file_explorer(self):
        self.folder_path = QFileDialog.getExistingDirectory(
            self, 'Выбрать папку', '')
        if self.folder_path:
            self.image_paths = [f"{self.folder_path}/{file}" for file in os.listdir(
                self.folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
            # self.show_image()

    def start_detection(self):
        """
        Добавить модуль (условно yolo_detection), который будет принимать на вход self.folder_path
        и инициализировать внутри метода self.results_path, на который будем ссылаться в методах show_image, show_previous_image и show_next_image
        """
        """
        Запускаем yolo_detection только в том случае, если была нажата кнопка выбора папки (переменная folder_path инициализирована)
        """
        # if self.folder_path:
        #     self.results_path = yolo_detection(self.folder_path)
        """
        Выводим алерт об успехе только в том случае, если функция yolo_detection отработала (переменная resilts_path инициализирована)
        """
        # if self.results_path:
        #     self.show_image()
        #     result_message = f'Детекция завершена, проверьте папку {self.results_path}'
        #     QMessageBox.information(self, 'Детекция завершена', result_message)

    def show_menu_window(self):
        self.parent.show()
        self.close()

    def show_image(self):
        if 0 <= self.image_index < len(self.results_path):
            image_path = self.results_path[self.image_index]
            pixmap = QPixmap(image_path)
            self.graphics_scene.clear()
            self.graphics_scene.addPixmap(pixmap)

    def show_previous_image(self):
        self.image_index -= 1
        if self.image_index < 0:
            self.image_index = len(self.results_path) - 1
        self.show_image()

    def show_next_image(self):
        self.image_index += 1
        if self.image_index >= len(self.results_path):
            self.image_index = 0
        self.show_image()


class SettingsWindow(QMainWindow):
    def __init__(self, parent):
        super(SettingsWindow, self).__init__()
        self.setWindowTitle('Настройки')
        self.setStyleSheet(u"background-color: rgb(192, 191, 188);")
        self.setGeometry(0, 0, 1920, 1080)

        layout = QVBoxLayout()

        self.choose_folder_button = QPushButton(self)
        self.choose_folder_button.setFixedSize(200, 50)
        self.choose_folder_button.setText('Выберите папку')
        self.choose_folder_button.clicked.connect(self.file_explorer)
        layout.addWidget(self.choose_folder_button)

        self.fine_tuning_button = QPushButton(self)
        self.fine_tuning_button.setFixedSize(200, 50)
        self.fine_tuning_button.setText('Дообучить')
        self.fine_tuning_button.clicked.connect(self.start_fine_tuning)
        layout.addWidget(self.fine_tuning_button)

        self.back_button = QPushButton(self)
        self.back_button.setFixedSize(200, 50)
        self.back_button.setText('Назад')
        self.back_button.clicked.connect(self.show_menu_window)
        layout.addWidget(self.back_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.folder_path = None

        self.parent = parent

    def file_explorer(self):
        fname = QFileDialog.getExistingDirectory(
            self, 'Выбрать файл или папку', '')

        if fname:
            self.folder_path = fname
            print(f'Выбранный файл: {self.folder_path}')

    def start_fine_tuning(self):
        """
        Добавить модуль (условно yolo_finetune), который будет принимать на вход self.folder_path
        и инициализировать внутри метода self.results_path, на который будем ссылаться в методах show_image, show_previous_image и show_next_image
        """
        """
        Запускаем yolo_finetune только в том случае, если была нажата кнопка выбора папки (переменная folder_path инициализирована)
        """
        # if self.folder_path:
        #     yolo_finetune(self.folder_path)
        #     result_message = f'Дообучение завершено, запустите детекцию'
        #     QMessageBox.information(self, 'Детекция завершена', result_message)

    def show_menu_window(self):
        self.parent.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu_window = MainWindow()
    menu_window.show()
    sys.exit(app.exec_())
