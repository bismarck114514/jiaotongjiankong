import sys
import cv2 as cv
import threading
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QTextEdit
from PyQt5.QtCore import QTimer, Qt, QTime, pyqtSignal, QObject
from PyQt5.QtGui import QImage, QPixmap
from monitor.video import vehicle_detect, car_type_detect, person_detect

class Worker(QObject):
    finished = pyqtSignal()
    data_ready = pyqtSignal(str, dict)

    def __init__(self, frame, detect_type):
        super().__init__()
        self.frame = frame
        self.detect_type = detect_type

    def run(self):
        try:
            result_text = ""
            counts = {'vehicle_count': {'total': 0, 'car': 0, 'bus': 0, 'truck': 0}, 'person_count': 0}
            if self.detect_type == 'vehicle':
                vehicles = vehicle_detect(self.frame)
                car_types = car_type_detect(self.frame)
                result_text = "车辆检测结果:\n"
                for vehicle in vehicles:
                    result_text += f"车辆类型: {vehicle['type']}, 置信度: {vehicle.get('score', 0):.2f}\n"
                    counts['vehicle_count']['total'] += 1
                    if vehicle['type'] in counts['vehicle_count']:
                        counts['vehicle_count'][vehicle['type']] += 1
                result_text += "\n车型识别结果:\n"
                for car_type in car_types:
                    result_text += f"车型: {car_type['name']}, 置信度: {car_type['score']:.2f}\n"
            elif self.detect_type == 'person':
                person_num = person_detect(self.frame)
                counts['person_count'] = person_num
                result_text = f"检测到的人数: {person_num}\n"
            self.data_ready.emit(result_text, counts)
        except Exception as e:
            print(f"Error in worker run method: {e}")
        finally:
            self.finished.emit()

class TrafficMonitor(QMainWindow):
    def __init__(self, detect_type, main_app):
        super().__init__()
        self.setWindowTitle('交通监控系统')
        self.setGeometry(100, 100, 1200, 900)

        self.detect_type = detect_type
        self.main_app = main_app

        self.initUI()
        self.video_path = None
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.last_detection_time = QTime.currentTime()
        self.detecting = False
        self.current_frame = None

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.video_label)

        info_layout = QHBoxLayout()

        self.info_textbox = QTextEdit(self)
        self.info_textbox.setReadOnly(True)
        info_layout.addWidget(self.info_textbox)

        self.vehicle_count_label = QLabel('车辆计数信息将显示在这里', self)
        self.person_count_label = QLabel('人流检测信息将显示在这里', self)
        info_layout.addWidget(self.vehicle_count_label)
        info_layout.addWidget(self.person_count_label)

        main_layout.addLayout(info_layout)

        button_layout = QHBoxLayout()
        self.load_button = QPushButton('加载视频', self)
        self.load_button.clicked.connect(self.load_video)
        button_layout.addWidget(self.load_button)

        self.camera_button = QPushButton('使用摄像头', self)
        self.camera_button.clicked.connect(self.use_camera)
        button_layout.addWidget(self.camera_button)

        self.start_button = QPushButton('开始检测', self)
        self.start_button.clicked.connect(self.check_connection)
        button_layout.addWidget(self.start_button)

        self.back_button = QPushButton('返回', self)
        self.back_button.clicked.connect(self.go_back)
        button_layout.addWidget(self.back_button)

        self.load_button.setFixedSize(160, 90)
        self.camera_button.setFixedSize(160, 90)
        self.start_button.setFixedSize(160, 90)
        self.back_button.setFixedSize(160, 90)

        main_layout.addLayout(button_layout)

    def go_back(self):
        self.main_app.show_detection_selection()

    def load_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "视频文件 (*.mp4 *.avi *.mov)")
        if self.video_path:
            self.cap = cv.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                self.info_textbox.setText("无法打开视频文件")
            else:
                self.info_textbox.setText(f"成功加载视频: {self.video_path}")

    def use_camera(self):
        self.cap = cv.VideoCapture(0)  # 打开默认摄像头
        if not self.cap.isOpened():
            self.info_textbox.setText("无法打开摄像头")
        else:
            self.info_textbox.setText("摄像头已开启")
            self.check_connection()  # 开始检测

    def check_connection(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.info_textbox.setText("正在连接云端进行检测，请稍候...")
                self.detecting = True
                worker = Worker(frame, self.detect_type)
                worker.data_ready.connect(self.handle_connection_check)
                worker.finished.connect(lambda: setattr(self, 'detecting', False))
                threading.Thread(target=worker.run).start()
            else:
                self.info_textbox.setText("无法读取视频帧")
        else:
            self.info_textbox.setText("请先加载视频文件或开启摄像头")

    def handle_connection_check(self, result_text, counts):
        self.info_textbox.setText("云端检测连接成功，开始视频播放和检测...")
        self.update_counts(counts)
        self.start_video_detection()

    def start_video_detection(self):
        if self.cap and self.cap.isOpened():
            self.cap.set(cv.CAP_PROP_POS_FRAMES, 0)  # 重置视频到开头
            self.timer.start(1000)  # 每1000毫秒更新一次
            self.info_textbox.setText("开始检测...")
        else:
            self.info_textbox.setText("请先加载视频文件或开启摄像头")

    def perform_detection(self):
        if not self.detecting and self.current_frame is not None:
            self.detecting = True
            worker = Worker(self.current_frame, self.detect_type)
            worker.data_ready.connect(self.update_info_textbox)
            worker.finished.connect(lambda: setattr(self, 'detecting', False))
            threading.Thread(target=worker.run).start()

    def update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame.copy()
                current_time = QTime.currentTime()
                elapsed_time = self.last_detection_time.msecsTo(current_time)
                if elapsed_time >= 1000 and not self.detecting:
                    self.last_detection_time = QTime.currentTime()
                    self.perform_detection()
                self.display_frame(self.current_frame)
            else:
                self.timer.stop()
                self.cap.release()
                self.info_textbox.setText("视频播放结束")
        else:
            self.info_textbox.setText("无法打开视频源")

    def display_frame(self, frame):
        try:
            rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))
        except Exception as e:
            print(f"Error in display_frame: {e}")

    def update_info_textbox(self, result_text, counts):
        self.info_textbox.setText(result_text)
        self.update_counts(counts)

    def update_counts(self, counts):
        vehicle_count = counts.get('vehicle_count', {})
        person_count = counts.get('person_count', 0)
        count_text = f"总车辆数: {vehicle_count.get('total', 0)}\n"
        count_text += f"小汽车: {vehicle_count.get('car', 0)}\n"
        count_text += f"卡车: {vehicle_count.get('truck', 0)}\n"
        count_text += f"公交车: {vehicle_count.get('bus', 0)}\n"
        self.vehicle_count_label.setText(count_text)
        self.person_count_label.setText(f"检测到的人数: {person_count}")
