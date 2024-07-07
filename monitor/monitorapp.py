from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from monitor.mfui import LoginDialog, DetectionSelectionDialog
from monitor.monitorframe import TrafficMonitor

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('交通监控系统')
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_dialog = LoginDialog()
        self.detection_selection_dialog = DetectionSelectionDialog()
        self.traffic_monitor = None

        self.stacked_widget.addWidget(self.login_dialog)
        self.stacked_widget.addWidget(self.detection_selection_dialog)

        self.login_dialog.login_successful.connect(self.show_detection_selection)
        self.detection_selection_dialog.detection_type_selected.connect(self.start_traffic_monitor)

        self.show_login()

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_dialog)

    def show_detection_selection(self):
        self.stacked_widget.setCurrentWidget(self.detection_selection_dialog)

    def start_traffic_monitor(self, detect_type):
        self.traffic_monitor = TrafficMonitor(detect_type, self)
        self.stacked_widget.addWidget(self.traffic_monitor)
        self.stacked_widget.setCurrentWidget(self.traffic_monitor)

    def return_to_login(self):
        self.stacked_widget.setCurrentWidget(self.login_dialog)

if __name__ == '__main__':
    app = QApplication([])
    main_app = MainApp()
    main_app.show()
    app.exec_()
