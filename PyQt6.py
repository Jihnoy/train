import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QRect, Qt


class MyButton(QPushButton):
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.color = color
        self.setStyleSheet(
            f"border-radius: 2px; border: 2px solid black; background-color: {self.color}; color: white;")

    def enterEvent(self, event):
        self.setStyleSheet(
            f"border-radius: 2px; border: 2px solid black; background-color: {self.color}; color: white;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(
            f"border-radius: 2px; border: 2px solid black; background-color: {self.color}; color: white;")
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setStyleSheet(f"border-radius: 2px; border: 2px solid red; background-color: {self.color}; color: white;")
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet(
            f"border-radius: 2px; border: 2px solid black; background-color: {self.color}; color: white;")
        super().mouseReleaseEvent(event)


class MyWidget(QWidget):
    def __init__(self, name):
        super().__init__()
        self.setWindowTitle(name)
        self.setMinimumSize(200, 200)  # 设置每个界面的最小大小

        layout = QVBoxLayout(self)  # 创建垂直布局管理器

        self.label = QLabel("This area is active", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: transparent;")  # 设置label背景为透明
        layout.addWidget(self.label)

        self.button = None
        self.is_gray = True  # 记录当前界面是否为灰色

        self.custom_width = 350
        self.custom_height = 700

        self.set_button(name)
        self.setLayout(layout)

    def set_button(self, name):
        if name == 'A':
            self.button = MyButton("A", "#FF0000", self)

        elif name == 'B':
            self.button = MyButton("B", "#0000FF", self)

        elif name == 'X':
            self.button = MyButton("X", "#00FF00", self)

        elif name == 'Y':
            self.button = MyButton("Y", "#FFFF00", self)

        self.update_button_geometry()

        self.button.clicked.connect(self.on_button_clicked)

    def update_button_geometry(self):
        if self.button:
            self.button.setGeometry((self.width() - self.button.width()) // 2,
                                    (self.custom_height - self.button.height()) // 2,
                                    self.button.width(),
                                    self.button.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_button_geometry()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))  # 设置画笔颜色为黑色
        if self.is_gray:
            painter.setBrush(QBrush(QColor(192, 192, 192)))  # 设置填充颜色为灰色
        else:
            painter.setBrush(QBrush(QColor(255, 192, 203)))  # 设置填充颜色为粉色
        rect = QRect((self.width() - self.custom_width) // 2, (self.height() - self.custom_height) // 8,
                     self.custom_width, self.custom_height)  # 调整矩形框的位置和大小
        painter.drawRect(rect)  # 绘制矩形框

    def on_button_clicked(self):
        # 切换界面的背景色
        self.is_gray = not self.is_gray
        self.update()
        self.set_button(self.windowTitle())

        if self.is_gray:
            self.label.setText("This area is active")
        else:
            self.label.setText("This area cannot be chosen")



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("多界面示例")
        self.resize(1920, 1080)  # 设置主窗口的大小
        self.setStyleSheet("background-color: white;")  # 设置主界面的背景为白色

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout(main_widget)  # 使用水平布局

        # 创建并添加四个交互界面
        for name in ['A', 'B', 'X', 'Y']:
            widget = MyWidget(name)
            layout.addWidget(widget)

        main_widget.setLayout(layout)  # 应用布局管理器到主部件

        self.button = QPushButton("重置界面", self)  # 创建按钮
        self.button.setGeometry(20, 20, 100, 30)  # 设置按钮的位置和大小
        self.button.clicked.connect(self.reset_widgets)  # 连接按钮的点击信号到重置界面的槽函数

    def reset_widgets(self):
        # 重置所有交互界面的背景色为灰色
        for widget in self.centralWidget().findChildren(MyWidget):
            widget.is_gray = True
            widget.update()
            widget.set_button(widget.windowTitle())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
