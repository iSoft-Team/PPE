from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                            QVBoxLayout, QHBoxLayout, QPushButton, QDialog,
                            QTextEdit, QLabel, QSplitter)
from PyQt5.QtCore import Qt, QTimer
from utils.constant import constant as c
from utils.project_config import project_config as cf
from PyQt5 import QtCore
import time
import threading
import Jetson.GPIO as GPIO
import sys
from core.gpio_handler import GPIOHandler


class SettingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.curr_value_enzim = None
        self.curr_status_machine = None
        self.curr_is_wrong_open_door = None
        self.timer = QTimer(self)
        # Tạo hai side bar
        input_side = QWidget(self)
        # input_side.setStyleSheet("background-color: lightblue;")  # Thay đổi màu sắc nếu cần
        self.create_left_buttons(input_side)  # Thêm button vào bên trái
        self.input_header = QLabel("INPUT", self)
        self.input_header.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2874A6, stop:1 #85C1E9); color: white; border: none")
        self.input_header.setFixedWidth(1920/2)
        self.input_header.setAlignment(Qt.AlignCenter)
        
        font = self.input_header.font()
        font.setPointSize(60)  # You can change the size as needed
        self.input_header.setFont(font)

        output_side = QWidget(self)
        # output_side.setStyleSheet("background-color: lightcoral;")  # Thay đổi màu sắc nếu cần
        self.create_right_buttons(output_side)  # Thêm button vào bên phải
        self.output_header = QLabel("OUTPUT", self)
        self.output_header.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #17A589, stop:1 #A3E4D7); color: white; border: none")
        self.output_header.setFixedWidth(1920/2)
        self.output_header.setAlignment(Qt.AlignCenter)


        font = self.output_header.font()
        font.setPointSize(60)  # You can change the size as needed
        self.output_header.setFont(font)
        input_side.setFixedWidth(1920/2)
        # Đặt các side bar và header vào layout ngang
        side_bar_layout = QHBoxLayout()
        side_bar_layout.addWidget(input_side)
        side_bar_layout.addWidget(output_side)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.input_header, alignment=Qt.AlignCenter)
        header_layout.addWidget(self.output_header, alignment=Qt.AlignCenter)

        # Sử dụng QSplitter để chia đôi màn hình
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(input_side)
        splitter.addWidget(output_side)

        container_widget = QWidget(self)
        container_layout = QVBoxLayout(container_widget)
        container_layout.addLayout(header_layout, 1)  # Thêm header vào layout chính
        container_layout.addWidget(splitter, 6)  # Thêm QSplitter vào layout chính
        self.setCentralWidget(container_widget)

        self.init_main_window()
        self.update_button_styles()
        self.start_timer()

    def start_timer(self):
        time.sleep(1)
        self.timer.start(66)  

    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup([cf.GPIO_RESULT, cf.GPIO_SOUND, cf.GPIO_READY], GPIO.OUT)
        GPIO.setup([cf.GPIO_ENZIM, cf.GPIO_MACHINE_RUN, cf.GPIO_OPEN_DOOR], GPIO.IN)
        self.timer.timeout.connect(self.update_logic)

    def init_main_window(self):
        width = 1920
        aspect_ratio = 9 / 16  # 9:16
        height = int(width * aspect_ratio)
        self.setGeometry(0, 0, width, height)
        self.setStyleSheet(c.BACKGROUND_PATH)  # Thay đổi màu sắc nền nếu cần
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

    def update_button_styles(self):
        machine_status = c.MACHINE_ON_PATH if self.curr_status_machine == cf.STATE_MACHINE else c.MACHINE_OFF_PATH
        door_status = c.DOOR_CLOSE_PATH if self.curr_is_wrong_open_door == cf.STATE_DOOR else c.DOOR_OPEN_PATH
        enzim_style = c.ENZIN_LABEL_NO_ENZIM_PATH if self.curr_value_enzim == cf.STATE_ENZYME else c.ENZIN_LABEL_ENZIM_PATH
        
        self.machine_run_btn.setStyleSheet(machine_status)
        self.door_status_btn.setStyleSheet(door_status)
        self.enzyme_btn.setStyleSheet(enzim_style)

    def create_left_buttons(self, widget):
        self.enzyme_btn = QPushButton("", widget)
        self.machine_run_btn = QPushButton("", widget)
        self.door_status_btn = QPushButton("", widget)

        self.enzyme_btn.setFixedHeight(150)
        self.enzyme_btn.setFixedWidth(180)

        self.machine_run_btn.setFixedHeight(150)
        self.machine_run_btn.setFixedWidth(200)

        self.door_status_btn.setFixedHeight(150)
        self.door_status_btn.setFixedWidth(148)

        layout = QHBoxLayout(widget)
        layout.addWidget(self.enzyme_btn)
        layout.addWidget(self.machine_run_btn)
        layout.addWidget(self.door_status_btn)
        

    def create_right_buttons(self, widget):
        self.interlock_label = QLabel("ON", widget)
        self.interlock_label.setFixedHeight(100)
        self.interlock_label.setFixedWidth(100)

        layout = QVBoxLayout(widget)
        layout.addWidget(self.interlock_label)

    def update_button_by_enzim(self):
        value = GPIO.input(cf.GPIO_ENZIM)
        if value != self.curr_value_enzim:
            print(f"curr_value_enzim: {value}")
            self.curr_value_enzim = value


    def update_status_machine(self):
        value = GPIO.input(cf.GPIO_MACHINE_RUN)
        if value != self.curr_status_machine:
            print(f"curr_status_machine: {value}")
            self.curr_status_machine = value
            
    def update_status_error_door(self):
        value = GPIO.input(cf.GPIO_OPEN_DOOR)
        if value != self.curr_is_wrong_open_door:
            print(f"curr_is_wrong_open_door: {value}")
            self.curr_is_wrong_open_door = value

    def update_logic(self):
        self.update_button_by_enzim()
        self.update_status_machine()
        self.update_status_error_door()
        self.update_button_styles()
        

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            sys.exit()
                