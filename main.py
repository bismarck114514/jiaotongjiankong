import sys
from PyQt5.QtWidgets import QApplication
from monitor.mainframe import MainApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
