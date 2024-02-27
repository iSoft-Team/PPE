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

class SettingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.curr_value_enzim = None
        self.curr_status_machine = None
        self.curr_is_wrong_open_door = None
        self.curr_interlock_status = False
        self.curr_system_status = True
        self.timer = QTimer(self)

        # self.collect_window = CollectWindow(start_yn=False)
        # self.collect_window.close()

        # Tạo hai side bar
        input_side = QWidget(self)
        self.create_left_buttons(input_side)  # Thêm button vào bên trái

        self.input_header = QLabel("INPUT", self)
        self.input_header.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2874A6, stop:1 #85C1E9); color: white; border: none")
        self.input_header.setFixedWidth(1920/2)
        self.input_header.setAlignment(Qt.AlignCenter)
        
        font = self.input_header.font()
        font.setPointSize(60)  # You can change the size as needed
        self.input_header.setFont(font)

        output_side = QWidget(self)
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

        # Tạo nút quit mới
        self.quit_btn = QPushButton("", self)
        self.quit_btn.setFixedSize(30, 30)
        self.quit_btn.setStyleSheet(c.CLOSE_PATH)  # Bạn cần thêm stylesheet cho nút này nếu cần
        self.quit_btn.clicked.connect(self.close_setting)
        self.quit_btn.setFocusPolicy(Qt.NoFocus)

        # Thêm nút quit vào layout của phần dưới
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)  # Thêm một khoảng trống linh hoạt giữa nút close và nút quit
        bottom_layout.addWidget(self.quit_btn, alignment=Qt.AlignTop | Qt.AlignRight)
        bottom_layout.setContentsMargins(0, 0, 25, 0)
        # Thêm bottom_layout vào container_layout trước top_layout
        container_layout.addLayout(bottom_layout, 0)  # Đặt index là 0 để thêm vào đầu tiên

        container_layout.addLayout(header_layout, 1)  # Thêm header vào layout chính
        container_layout.addWidget(splitter, 6)  # Thêm QSplitter vào layout chính

        self.setCentralWidget(container_widget)

        self.init_main_window()
        self.update_button_styles()
        self.start_timer()
        self.enzyme_btn.clicked.connect(lambda: self.handle_button_click(self.enzyme_btn))
        self.machine_run_btn.clicked.connect(lambda: self.handle_button_click(self.machine_run_btn))
        self.door_status_btn.clicked.connect(lambda: self.handle_button_click(self.door_status_btn))
        self.interlock_btn.clicked.connect(lambda: self.handle_button_click(self.interlock_btn))
        self.setup_gpio()
    def start_timer(self):
        time.sleep(1)
        self.timer.start(33)  

    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup([cf.GPIO_RESULT, cf.GPIO_SOUND, cf.GPIO_READY], GPIO.OUT)
        GPIO.setup([cf.GPIO_ENZIM, cf.GPIO_MACHINE_RUN, cf.GPIO_OPEN_DOOR], GPIO.IN)
        GPIO.output(cf.GPIO_SOUND, not cf.STATE_BUZER)

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
        interlock_status = c.INTERLOCK_OFF_PATH if self.curr_interlock_status == cf.STATE_INTERLOCK else c.INTERLOCK_ON_PATH
        
        self.interlock_btn.setStyleSheet(interlock_status)
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
        
    def handle_button_click(self, button):
        # if button == self.enzyme_btn:
            #         self.curr_value_enzim = not self.curr_value_enzim
        # elif button == self.machine_run_btn:
        #     self.curr_status_machine = not self.curr_status_machine
        # elif button == self.door_status_btn:
        #     self.curr_is_wrong_open_door = not self.curr_is_wrong_open_door
        if button == self.interlock_btn:
            self.curr_interlock_status = not self.curr_interlock_status
        if self.curr_interlock_status == False:
            GPIO.output(cf.GPIO_SOUND, GPIO.LOW)
        else:
            GPIO.output(cf.GPIO_SOUND, GPIO.HIGH)
        self.update_button_styles()

    def create_right_buttons(self, widget):
        self.interlock_btn = QPushButton("", widget)

        self.interlock_btn.setFixedHeight(130)
        self.interlock_btn.setFixedWidth(175)

        layout = QHBoxLayout(widget)
        layout.addWidget(self.interlock_btn)

        # self.interlock_label = QLabel("ON", widget)
        # self.interlock_label.setFixedHeight(100)
        # self.interlock_label.setFixedWidth(100)

        # layout.addWidget(self.interlock_label)

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
        # self.update_button_by_enzim()
        # self.update_status_machine()
        # self.update_status_error_door()
        self.update_status_instalock()
        self.update_button_styles()
        
    def close_setting(self):
        print("show_collect_screen")
    
        # self.collect_window.show()
        # self.collect_window.raise_()
        # self.collect_window.showFullScreen()
        # self.collect_window.init_camera()
        # self.collect_window.start_timer()
        # self.flash_window.close()
        self.hide()
        sys.exit()

    def show_collect_window(self):
        try:
            self.collect_window.show()
            self.collect_window.raise_()

        except Exception as e:
            print(f"An error occurred: {e}")

    
    def closeEvent(self, event):
        super().closeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            sys.exit()
                