from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                            QVBoxLayout, QHBoxLayout, QPushButton, QDialog,
                            QTextEdit, QLabel, QSplitter)
from PyQt5.QtCore import Qt, QTimer
from utils.constant import constant as c
from utils.project_config import project_config as cf
from utils.project_config import cons

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
        self.curr_spare_1 = None
        self.curr_spare_2 = None
        self.curr_spare_3 = None

        self.curr_spare_4 = True
        self.curr_spare_5 = True
        self.curr_interlock_status = True
        self.curr_system_status = True
        self.curr_buzer_status = False

        self.timer = QTimer(self)
        # self.setup_gpio()
        GPIO.output(cf.GPIO_RESULT, GPIO.HIGH)
        GPIO.output(cf.GPIO_READY, GPIO.HIGH)

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
        self.start_timer()
        self.update_button_styles()
        self.interlock_btn.clicked.connect(lambda: self.handle_button_click(self.interlock_btn))
        self.system_status_btn.clicked.connect(lambda: self.handle_button_click(self.system_status_btn))
        self.buzer_btn.clicked.connect(lambda: self.handle_button_click(self.buzer_btn))

        
        self.spare_4_btn.clicked.connect(lambda: self.handle_button_click(self.spare_4_btn))
        self.spare_5_btn.clicked.connect(lambda: self.handle_button_click(self.spare_5_btn))


    def start_timer(self):
        time.sleep(1)
        self.timer.start(33)  

    def setup_gpio(self):
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup([cf.GPIO_RESULT,cf.GPIO_READY], GPIO.OUT,initial=GPIO.HIGH)
        # GPIO.setup([cf.GPIO_ENZIM, cf.GPIO_MACHINE_RUN, cf.GPIO_OPEN_DOOR], GPIO.IN)
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
        interlock_status = c.INTERLOCK_ON_PATH if self.curr_interlock_status == cf.STATE_INTERLOCK else c.INTERLOCK_OFF_PATH
        system_status = c.SYSTEM_NOT_READY_PATH if self.curr_system_status == cf.STATE_READY else c.SYSTEM_READY_PATH
        buzer_status = c.BUZER_OFF_PATH if self.curr_buzer_status == cf.STATE_BUZER else c.BUZER_ON_PATH

        spare1 = c.SPARE1_ON_PATH if self.curr_spare_1 == cf.STATE_SPEARE1 else c.SPARE1_OFF_PATH
        spare2 = c.SPARE2_ON_PATH if self.curr_spare_2 == cf.STATE_SPEARE2 else c.SPARE2_OFF_PATH
        spare3 = c.SPARE3_ON_PATH if self.curr_spare_3 == cf.STATE_SPEARE3 else c.SPARE3_OFF_PATH
        spare4 = c.SPARE4_ON_PATH if self.curr_spare_4 == cf.STATE_SPEARE4 else c.SPARE4_OFF_PATH
        spare5 = c.SPARE5_ON_PATH if self.curr_spare_5 == cf.STATE_SPEARE5 else c.SPARE5_OFF_PATH


        self.machine_run_btn.setStyleSheet(machine_status)
        self.door_status_btn.setStyleSheet(door_status)
        self.enzyme_btn.setStyleSheet(enzim_style)
        self.interlock_btn.setStyleSheet(interlock_status)
        self.system_status_btn.setStyleSheet(system_status)
        self.buzer_btn.setStyleSheet(buzer_status)


        self.spare_1_btn.setStyleSheet(spare1)
        self.spare_2_btn.setStyleSheet(spare2)
        self.spare_3_btn.setStyleSheet(spare3)
        self.spare_4_btn.setStyleSheet(spare4)
        self.spare_5_btn.setStyleSheet(spare5)


    def create_left_buttons(self, widget):
        self.enzyme_btn = QPushButton("", widget)
        self.machine_run_btn = QPushButton("", widget)
        self.door_status_btn = QPushButton("", widget)
        self.spare_1_btn = QPushButton("", widget)
        self.spare_2_btn = QPushButton("", widget)
        self.spare_3_btn = QPushButton("", widget)

        self.enzyme_btn.setFixedHeight(150)
        self.enzyme_btn.setFixedWidth(180)

        self.machine_run_btn.setFixedHeight(150)
        self.machine_run_btn.setFixedWidth(195)

        self.door_status_btn.setFixedHeight(150)
        self.door_status_btn.setFixedWidth(150)


        self.spare_1_btn.setFixedHeight(165)
        self.spare_1_btn.setFixedWidth(150)

        self.spare_2_btn.setFixedHeight(165)
        self.spare_2_btn.setFixedWidth(150)

        self.spare_3_btn.setFixedHeight(165)
        self.spare_3_btn.setFixedWidth(150)

        layout_button = QVBoxLayout(widget)
        layout_group_button_top = QHBoxLayout()
        layout_group_button_top.addWidget(self.enzyme_btn)
        layout_group_button_top.addWidget(self.machine_run_btn)
        layout_group_button_top.addWidget(self.door_status_btn)
        layout_button.addLayout(layout_group_button_top)

        layout_group_button_bot = QHBoxLayout()
        layout_group_button_bot.addWidget(self.spare_1_btn)
        layout_group_button_bot.addWidget(self.spare_2_btn)
        layout_group_button_bot.addWidget(self.spare_3_btn)
        layout_button.addLayout(layout_group_button_bot)
        
    def handle_button_click(self, button):
        if button == self.interlock_btn:
            self.curr_interlock_status = not self.curr_interlock_status
            GPIO.output(cf.GPIO_RESULT, self.curr_interlock_status)

        elif button == self.system_status_btn:
            self.curr_system_status = not self.curr_system_status
            GPIO.output(cf.GPIO_READY, self.curr_system_status)

        elif button == self.buzer_btn:
            self.curr_buzer_status = not self.curr_buzer_status
            GPIO.output(cf.GPIO_SOUND, self.curr_buzer_status)
        
        elif button == self.spare_4_btn:
            self.curr_spare_4 = not self.curr_spare_4
            GPIO.output(cf.GPIO_SPARE_4, self.curr_spare_4)

        elif button == self.spare_5_btn:
            self.curr_spare_5 = not self.curr_spare_5
            GPIO.output(cf.GPIO_SPARE_5, self.curr_spare_5)

        self.update_button_styles()

    def create_right_buttons(self, widget):
        self.interlock_btn = QPushButton("", widget)
        self.system_status_btn = QPushButton("", widget)
        self.buzer_btn = QPushButton("", widget)

        self.spare_4_btn = QPushButton("", widget)
        self.spare_5_btn = QPushButton("", widget)
        
        self.spare_4_btn.setFixedHeight(165)
        self.spare_4_btn.setFixedWidth(150)

        self.spare_5_btn.setFixedHeight(165)
        self.spare_5_btn.setFixedWidth(150)

        self.interlock_btn.setFixedHeight(165)
        self.interlock_btn.setFixedWidth(150)

        self.system_status_btn.setFixedHeight(165)
        self.system_status_btn.setFixedWidth(150)

        self.buzer_btn.setFixedHeight(165)
        self.buzer_btn.setFixedWidth(150)

        layout_button = QVBoxLayout(widget)

        layout_group_button_top = QHBoxLayout()
        layout_group_button_top.addWidget(self.interlock_btn)
        layout_group_button_top.addWidget(self.system_status_btn)
        layout_group_button_top.addWidget(self.buzer_btn)
        layout_button.addLayout(layout_group_button_top)

        layout_group_button_bot = QHBoxLayout()
        layout_group_button_bot.addWidget(self.spare_4_btn)
        layout_group_button_bot.addWidget(self.spare_5_btn)
        layout_button.addLayout(layout_group_button_bot)


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
    
                
    def update_status_spare_1(self):
        value = GPIO.input(cf.GPIO_SPARE_1)
        if value != self.curr_spare_1:
            print(f"curr_spare_1: {value}")
            self.curr_spare_1 = value

    def update_status_spare_2(self):
        value = GPIO.input(cf.GPIO_SPARE_2)
        if value != self.curr_spare_2:
            print(f"curr_spare_2: {value}")
            self.curr_spare_2 = value
    
    def update_status_spare_3(self):
        value = GPIO.input(cf.GPIO_SPARE_3)
        if value != self.curr_spare_3:
            print(f"curr_spare_1: {value}")
            self.curr_spare_3 = value

    def update_logic(self):
        self.update_button_by_enzim()
        self.update_status_machine()
        self.update_status_error_door()
        self.update_status_spare_1()
        self.update_status_spare_2()
        self.update_status_spare_3()
        self.update_button_styles()
        
    def close_setting(self):
        self.close()
        # GPIO.cleanup()
        cons.check_show_collect = True
        print("Close setting")

    def closeEvent(self, event):
        print("Close")
        super().closeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            sys.exit()
                