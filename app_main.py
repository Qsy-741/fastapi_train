# coding: utf-8
import io
import os
import sys
import esptool
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QSize, Qt, QRectF, pyqtSignal, QPoint, QTimer, QEvent, QAbstractItemModel, pyqtProperty, \
    QThread
from PyQt5.QtGui import QPainter, QPainterPath, QIcon, QCursor, QTextCursor, QPixmap
from PyQt5.QtWidgets import (QApplication, QAction, QHBoxLayout, QLineEdit, QToolButton, QTextEdit,
                             QPlainTextEdit, QCompleter, QStyle, QWidget, QFileDialog)
from qfluentwidgets import FluentIconBase, FluentStyleSheet, isDarkTheme, drawIcon, setFont, FluentIcon as FIF, \
    LineEditMenu, themeColor, RoundMenu, IndicatorMenuItemDelegate, MenuAnimationType, SmoothScrollDelegate, InfoBar, \
    InfoBarPosition, Action, DropDownPushButton
from qfluentwidgets.components.widgets.menu import TextEditMenu
import warnings
from ui import Ui_MainWindow, basedir


class EmittingStringIO(io.StringIO):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def write(self, s):
        super().write(s)
        self.signal.emit(s)


class EsptoolThread(QThread):
    output_updated = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, port, ol_path):
        super().__init__()
        self.port = port
        self.ol_path = ol_path

    def run(self):
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = EmittingStringIO(self.output_updated)
        sys.stderr = EmittingStringIO(self.output_updated)
        try:
            print(f"Starting esptool with port: {self.port} and ol_path: {self.ol_path}")
            esptool.main(['--chip', 'auto', '--port', self.port, '--baud', '921600', '--before', 'default_reset', '--after', 'hard_reset', 'write_flash', '-z', '--flash_mode', 'dio', '--flash_freq', '40m', '--flash_size', '4MB', '0x0', self.ol_path])
        except Exception as e:
            print(e)
        finally:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        self.finished.emit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.AvatarWidget.setRadius(80)
        self.ui.PushButton.clicked.connect(self.selectFile)
        self.ui.PushButton_2.clicked.connect(self.downloadFirmware)
        self.ui.dropDownPushButton.clicked.connect(self.scanfSerial)
        self.ui.menu.triggered.connect(self.menuItemSelected)
        self.selected_port = None
        self.ports = []

    # 日志输出
    def append_output(self, text):
        cursor = self.ui.BodyLabel.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.ui.BodyLabel.setTextCursor(cursor)
        self.ui.BodyLabel.ensureCursorVisible()

    def downloadFirmware(self):
        if self.ui.LineEdit.text() == "":
            self.createInfoBar("请先选择要下载的程序文件!")
            return 0
        if self.ui.dropDownPushButton.text() == "串口连接断开":
            self.createInfoBar("请先选择端口连接!")
            return 0

        self.esptool_thread = EsptoolThread(self.selected_port, self.ui.LineEdit.text())
        self.esptool_thread.output_updated.connect(self.updateDebugText)
        self.esptool_thread.finished.connect(self.downloadFinish)
        self.esptool_thread.start()

    def updateDebugText(self, output):
        self.append_output(output)

    def downloadFinish(self):
        self.createInfoBar("下载结束!")

    def selectFile(self):
        fileDialog = QFileDialog()
        path = fileDialog.getOpenFileName(filter='*bin', initialFilter='*bin')
        if path[0] is not None:
            self.ui.LineEdit.setText(path[0])

    def scanfSerial(self):
        self.ui.menu.clear()
        self.ports = list(serial.tools.list_ports.comports())
        for port in self.ports:
            if "CH" in port.description:
                # 将串口名添加到列表控件
                self.ui.menu.addAction(Action(QIcon(os.path.join(basedir, "chuankou.svg")), port.description))
        self.ui.menu.addAction(Action(QIcon(os.path.join(basedir, "chuankou.svg")), '串口连接断开'))

    def menuItemSelected(self, action):
        # 更新按钮文本
        self.ui.dropDownPushButton.setText(action.text())
        temp = self.ui.dropDownPushButton.text()
        for port in list(serial.tools.list_ports.comports()):
            if temp == port.description:
                self.selected_port = port.device
                return 0
        self.ui.dropDownPushButton.setText("串口连接断开")

    def createInfoBar(self, str):
        InfoBar.info(
            title=self.tr('提示'),
            content=str,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=1000,
            parent=self
        )


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
