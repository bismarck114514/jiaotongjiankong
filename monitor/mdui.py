from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt

# 定义按钮和输入框的尺寸
INPUT_WIDTH = 320
INPUT_HEIGHT = 60
BUTTON_WIDTH = 160
BUTTON_HEIGHT = 90

user_db = {
    '123456': {'password': '123456', 'email': '123456@example.com'}
}

class LoginDialog(QDialog):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('登录')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('登录', self)
        self.register_button = QPushButton('注册', self)
        self.reset_button = QPushButton('重置密码', self)

        self.login_button.clicked.connect(self.check_credentials)
        self.register_button.clicked.connect(self.register)
        self.reset_button.clicked.connect(self.reset_password)

        layout.addWidget(QLabel('用户名:', self), alignment=Qt.AlignCenter)
        layout.addWidget(self.username, alignment=Qt.AlignCenter)
        layout.addWidget(QLabel('密码:', self), alignment=Qt.AlignCenter)
        layout.addWidget(self.password, alignment=Qt.AlignCenter)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.register_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.reset_button, alignment=Qt.AlignCenter)

        self.username.setFixedSize(INPUT_WIDTH, INPUT_HEIGHT)
        self.password.setFixedSize(INPUT_WIDTH, INPUT_HEIGHT)
        self.login_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.register_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.reset_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)

        self.setLayout(layout)

    def check_credentials(self):
        username = self.username.text()
        password = self.password.text()
        if username in user_db and user_db[username]['password'] == password:
            self.accept()
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, '错误', '用户名或密码错误')

    def register(self):
        reg_dialog = RegisterDialog()
        if reg_dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, '成功', '注册成功，请使用新账号登录')

    def reset_password(self):
        reset_dialog = ResetPasswordDialog()
        if reset_dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, '成功', '密码已重置为123456')


class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('注册')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.email = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.register_button = QPushButton('注册', self)

        self.register_button.clicked.connect(self.register_user)

        layout.addWidget(QLabel('用户名:', self), alignment=Qt.AlignCenter)
        layout.addWidget(self.username, alignment=Qt.AlignCenter)
        layout.addWidget(QLabel('密码:', self), alignment=Qt.AlignCenter)
        layout.addWidget(self.password, alignment=Qt.AlignCenter)
        layout.addWidget(QLabel('邮箱:', self), alignment=Qt.AlignCenter)
        layout.addWidget(self.email, alignment=Qt.AlignCenter)
        layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        self.username.setFixedSize(INPUT_WIDTH, INPUT_HEIGHT)
        self.password.setFixedSize(INPUT_WIDTH, INPUT_HEIGHT)
        self.email.setFixedSize(INPUT_WIDTH, INPUT_HEIGHT)
        self.register_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)

        self.setLayout(layout)

    def register_user(self):
        username = self.username.text()
        password = self.password.text()
        email = self.email.text()

        if username in user_db:
            QMessageBox.warning(self, '错误', '用户名已存在')
        elif not username or not password or not email:
            QMessageBox.warning(self, '错误', '所有字段都是必填的')
        else:
            user_db[username] = {'password': password, 'email': email}
            self.accept()


class ResetPasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('重置密码')
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.username = QLineEdit(self)
        self.email = QLineEdit(self)
        self.reset_button = QPushButton('重置', self)

        self.reset_button.clicked.connect(self.reset_user_password)

        layout.addWidget(QLabel('用户名:', self), alignment=Qt.AlignCenter)
        layout.addWidget(self.username, alignment=Qt.AlignCenter)
        layout.addWidget(QLabel('邮箱:', self), alignment=Qt.AlignCenter)
        layout.addWidget(self.email, alignment=Qt.AlignCenter)
        layout.addWidget(self.reset_button, alignment=Qt.AlignCenter)

        self.username.setFixedSize(INPUT_WIDTH, INPUT_HEIGHT)
        self.email.setFixedSize(INPUT_WIDTH, INPUT_HEIGHT)
        self.reset_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)

        self.setLayout(layout)

    def reset_user_password(self):
        username = self.username.text()
        email = self.email.text()

        if username in user_db and user_db[username]['email'] == email:
            user_db[username]['password'] = '123456'
            self.accept()
        else:
            QMessageBox.warning(self, '错误', '用户名或邮箱不匹配')


class DetectionSelectionDialog(QDialog):
    detection_type_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('选择检测类型')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.vehicle_detect_button = QPushButton('车辆检测', self)
        self.person_detect_button = QPushButton('人流检测', self)
        self.back_button = QPushButton('返回', self)

        self.vehicle_detect_button.clicked.connect(self.select_vehicle_detect)
        self.person_detect_button.clicked.connect(self.select_person_detect)
        self.back_button.clicked.connect(self.go_back)

        layout.addWidget(self.vehicle_detect_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.person_detect_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.vehicle_detect_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.person_detect_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.back_button.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)

        self.setLayout(layout)

    def select_vehicle_detect(self):
        self.detection_type_selected.emit('vehicle')
        self.accept()

    def select_person_detect(self):
        self.detection_type_selected.emit('person')
        self.accept()

    def go_back(self):
        self.reject()
