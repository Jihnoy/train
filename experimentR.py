import os
import re
import sys

import numpy
import pandas as pd
import numpy as np
from pygame.locals import *
import pygame
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton, QLabel, QVBoxLayout, \
    QMessageBox, QComboBox, QTableView, QSizePolicy, QHeaderView
from PyQt5.QtGui import QPainter, QColor, QBrush, QStandardItemModel, QStandardItem, QFont
from PyQt5.QtCore import QRect, Qt, QThread, pyqtSignal, QTimer, QDateTime


class MyButton(QPushButton):
    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.color = color
        self.setStyleSheet(
            f"border-radius: 2px; border: 2px solid black; background-color: {self.color}; color: black; "
            f"font-size:25px")
        self.resize(200, 100)

    def enterEvent(self, event):
        self.setStyleSheet(
            f"border-radius: 2px; border: 2px solid black; background-color: {self.color}; color: white;font-size:25px")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(
            f"border-radius: 2px; border: 2px solid black; background-color: {self.color}; color: black; font-size:25px")
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setStyleSheet(f"border-radius: 2px; border: 2px solid red; background-color: {self.color}; color: white;"
                           f"font-size:25px")
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet(
            f"border-radius: 2px; border: 2px solid black; background-color: {self.color}; color: black;"
            f"font-size:25px")
        super().mouseReleaseEvent(event)


class MyWidget(QWidget):

    def __init__(self, name):
        super().__init__()
        self.custom_width = 350
        self.custom_height = 700

        self.setWindowTitle(name)
        self.setMinimumSize(200, 200)  # 设置每个界面的最小大小

        layout = QVBoxLayout(self)  # 创建垂直布局管理器

        self.label = QLabel("区域可选择\nエリアは選択可能です\nArea can be selected\n", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: transparent;")  # 设置label背景为透明
        self.label.setGeometry((self.custom_width - self.label.width()) // 2,
                               (self.custom_height - self.label.height()) // 2 + 200,
                               self.label.width(), self.label.height())

        font = QFont()  # 创建字体对象
        font.setPointSize(14)  # 设置字体大小为20
        self.label.setFont(font)  # 将字体应用到标签

        self.nameLabel = QLabel(name, self)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setStyleSheet("background-color: transparent;")  # 设置label背景为透明

        self.button = None
        self.is_gray = True  # 记录当前界面是否为灰色

        self.setLayout(layout)
        self.set_button(name)

        self.choose_time = 0
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.label)

    def update(self):
        super().update()
        self.label_button()

    def create_button(self, name):
        if name == 'A':
            self.button = MyButton("A", "transparent", self)  # 红FF0000

        elif name == 'B':
            self.button = MyButton("B", "transparent", self)  # 蓝0000FF

        elif name == 'X':
            self.button = MyButton("X", "transparent", self)  # 绿00FF00

        elif name == 'Y':
            self.button = MyButton("Y", "transparent", self)  # 黄FFFF00

        self.button.clicked.connect(self.on_button_clicked)
        self.update_button_geometry()

    def set_button(self, name):
        self.create_button(name)

    def reset_button(self):
        self.create_button(self.windowTitle())
        self.label_button()

    def update_button_geometry(self):
        if self.button:
            self.button.setGeometry((self.width() - self.button.width()) // 2,
                                    (self.custom_height - self.button.height()) // 2 + 200,
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
        rect = QRect((self.width() - self.custom_width) // 2, (self.height() - self.custom_height) // 2,
                     self.custom_width, self.custom_height)  # 调整矩形框的位置和大小
        painter.drawRect(rect)  # 绘制矩形框

    def on_button_clicked(self):
        # 切换界面的背景色
        self.choose_time += 1
        if self.choose_time == 1:
            self.label.setText(f"再次点击按钮{self.windowTitle()}以选择\n確もう一度選択して確認します"
                               f"\nSelect{self.windowTitle()}again to confirm")
        elif self.choose_time == 2:
            self.is_gray = not self.is_gray
            self.update()
            self.set_button(self.windowTitle())
        elif self.choose_time > 2:
            pass

    def cancel(self, force):
        if force:
            self.choose_time = 0
            self.label.setText("区域可选择\nエリアは選択可能です\nArea can be selected\n")
            self.is_gray = not self.is_gray
            self.update()
            self.set_button(self.windowTitle())
        else:
            if self.is_gray:
                self.choose_time = 0
                self.label.setText("区域可选择\nエリアは選択可能です\nArea can be selected\n")
            else:
                pass

    def label_button(self):  # 改变label和button的状态
        if self.is_gray:
            self.label.setText("区域可选择\nエリアは選択可能です\nArea can be selected\n")
            self.button.setEnabled(True)
            self.nameLabel.setText(self.windowTitle())
        else:
            self.label.setText("区域不可选择\nエリアは選択できません\nArea cannot be chosen")
            self.button.setEnabled(False)
            self.nameLabel.setText("")


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Collection")
        self.resize(1920, 1080)  # 设置主窗口的大小
        # self.showFullScreen()  # 自动全屏
        self.setStyleSheet("background-color: white;")  # 设置主界面的背景为白色

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout(main_widget)  # 使用水平布局
        self.widgets = []  # 存储子窗口的列表
        self.reset_count = 0  # 重置计数器

        self.create_widgets(layout)  # 创建初始的子窗口并添加到布局

        main_widget.setLayout(layout)  # 应用布局管理器到主部件

        self.button = QPushButton("Next Ex", self)  # 创建按钮
        self.button.setGeometry(20, 20, 100, 30)  # 设置按钮的位置和大小
        self.button.clicked.connect(self.reset_widgets)  # 连接按钮的点击信号到重置界面的槽函数

        self.experiment_results = pd.DataFrame(columns=['Participant zone', 'L0R1', 'A', 'B', 'X', 'Y'])
        # 导出数据
        self.export_button = QPushButton("导出数据", self)
        self.export_button.setGeometry(1800, 20, 100, 30)
        self.export_button.clicked.connect(self.export_experiment_results)

        self.data_table = QTableView(self)  # 创建 QTableView 用于显示数据
        self.data_table.setGeometry(500, 0, 1000, 150)  # 设置 QTableView 的位置和大小
        # 设置表格视图的行和列大小策略
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.data_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 设置水平和垂直滚动条策略
        self.data_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.data_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.data_model = QStandardItemModel()  # 创建数据模型

        # 删除错误数据
        self.add_data_button = QPushButton("Delete data", self)
        self.add_data_button.setGeometry(150, 20, 100, 30)
        self.add_data_button.clicked.connect(self.delete_last_data)
        # 记录选择区域
        self.selected = None
        self.ex_data = np.zeros(4, dtype=numpy.int8)  # 区域选择情况，-1代表已经选择过，0代表未选择，1代表当前选择，初始化为全0
        self.btn_time = 0
        # 记录实验者所在距离区域和
        self.zone_lr = np.zeros(2, dtype=numpy.int8)  # 实验者所在区域zone：1、2、3，实验者从左侧进入0，右侧进入1
        self.zone = [1, 2, 3]  # 区域1，2，3, 4, 5, 6
        self.lr = [1, 1, 1]  # 位于左侧右侧
        self.ex_timer = QTimer()
        self.start_time = None
        # self.ex_timer.timeout.connect(self.update_timer)
        # 手柄线程
        self.joystick = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_joystick_events)

        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

            self.timer.start(10)  # 设置定时器的间隔时间，单位为毫秒

    def process_joystick_events(self):
        operate = [0, 1, 2, 3]
        name = ['A', 'B', 'X', 'Y']
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button not in operate:
                    self.btn_time = 0
                    # if self.selected is not None:
                    #     self.cancel_operate(self.selected, False)
                    # else:
                    #     pass
                else:
                    self.selected = name[event.button]
                    self.select_widget(self.selected)
            elif event.type == pygame.JOYBUTTONUP:
                print("释放手柄按钮:", event.button)

    def select_widget(self, name):
        for i, widget in enumerate(self.widgets):
            if not widget.is_gray:
                self.ex_data[i] = -1
            if widget.windowTitle() == name:
                if widget.is_gray:
                    widget.on_button_clicked()
                    self.btn_time += 1
                    if self.btn_time == 1:
                        self.toggle_timer()
                    if self.btn_time == 2:
                        self.btn_time = 0

                        if self.ex_data[i] == 0:
                            self.ex_data[i] = 1
                        else:
                            pass
                        self.add_data_to_experiment()
                        self.show_experiment_results()
                        break

    def cancel_operate(self, name, force):
        for widget in self.centralWidget().findChildren(MyWidget):
            if widget.windowTitle() == name:
                widget.cancel(force)
                self.btn_time = 0
                break

    def create_widgets(self, layout):
        # 创建并添加四个交互界面
        for name in ['A', 'B', 'X', 'Y']:
            widget = MyWidget(name)
            layout.addWidget(widget)
            self.widgets.append(widget)

    def reset_widgets(self):
        self.reset_count += 1  # 增加重置计数器的值(实验次数)
        if self.reset_count < len(self.zone):  # 移除并销毁当前的子窗口
            for widget in self.widgets:
                widget.setParent(None)
                widget.deleteLater()

            self.widgets = []  # 清空子窗口列表

            layout = self.centralWidget().layout()  # 获取当前布局
            self.create_widgets(layout)  # 创建新的子窗口并添加到布局

            self.update()  # 更新主窗口
            self.zone_lr = np.zeros(2)
            self.ex_data = np.zeros(4)

            # 输出重置信息
            print(f"实验次数/：{self.reset_count}，子窗口个数：{len(self.widgets)}")
        else:
            result = QMessageBox.question(self, "确认选择", "Yes is export file, No to continue",
                                          QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                self.export_experiment_results()
            if result == QMessageBox.No:
                self.reset_count = 0
                for widget in self.widgets:
                    widget.setParent(None)
                    widget.deleteLater()

                self.widgets = []  # 清空子窗口列表

                layout = self.centralWidget().layout()  # 获取当前布局
                self.create_widgets(layout)  # 创建新的子窗口并添加到布局

                self.update()  # 更新主窗口
                self.zone_lr = np.zeros(2)
                self.ex_data = np.zeros(4)

                # 输出重置信息
                print(f"实验次数/：{self.reset_count}，窗口重置成功，可进行下一位实验者")

    def add_data_to_experiment(self):
        # 将当前实验数据添加到总实验结果中
        self.zone_lr[0] = self.zone[self.reset_count]
        self.zone_lr[1] = 1
        data = np.concatenate((self.zone_lr, self.ex_data))
        print(data)
        self.experiment_results = self.experiment_results.append(
            pd.Series(data, index=self.experiment_results.columns),
            ignore_index=True
        )
        print("数据已添加到总实验结果。")

    def select_start_area(self, index):
        start_area = index
        print(f"实验者将从区域{start_area}开始进行实验。")
        self.zone_lr[0] = start_area

    def export_experiment_results(self):
        if not os.path.exists("result"):
            os.makedirs("result")

            # 获取结果文件夹中已有的结果文件名列表
        result_files = os.listdir("result")

        # 提取文件名中的数字部分
        numbers = [re.findall(r'\d+', filename) for filename in result_files]
        numbers = [int(num[0]) for num in numbers if num]  # 过滤出包含数字的文件名

        # 确定下一个文件名
        if numbers:
            next_number = max(numbers) + 1
        else:
            next_number = 1

        # 生成新的结果文件名
        filename = f"resultR{next_number}.csv"

        # 导出实验结果到CSV文件
        self.experiment_results.to_csv(os.path.join("result", filename), index=False)

        print(f"实验结果已导出为{filename}文件，保存在result文件夹中。")

    def delete_last_data(self):
        if not self.experiment_results.empty:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Confirm Operate")
            msgBox.setText("Last row has been remove")
            msgBox.setStandardButtons(QMessageBox.Ok)
            result = msgBox.exec_()
            if result == QMessageBox.Ok:
                for index, data in enumerate(self.ex_data):
                    if data == 1:
                        print(self.widgets[index].windowTitle())
                        self.cancel_operate(self.widgets[index].windowTitle(), True)
                self.experiment_results = self.experiment_results.iloc[:-1]
                # 删除数据模型的最后一行
                self.data_model.removeRow(self.data_model.rowCount() - 1)
                self.show_experiment_results()

    def show_experiment_results(self):
        column_names = list(self.experiment_results.columns)
        for col, name in enumerate(column_names):
            item = QStandardItem(name)
            self.data_model.setHorizontalHeaderItem(col, item)

        # 将 Pandas 数据添加到数据模型
        for row in range(len(self.experiment_results)):
            for col in range(len(column_names)):
                item = QStandardItem(str(self.experiment_results.iloc[row, col]))
                self.data_model.setItem(row, col, item)

        self.data_table.setModel(self.data_model)  # 将数据模型设置到 QTableView 中

    def update_timer(self):
        if self.start_time is not None:
            current_time = QDateTime.currentDateTime()
            elapsed = self.start_time.msecsTo(current_time)
            print("Elapsed time:", elapsed)

    def toggle_timer(self):
        if self.start_time is None:
            self.start_time = QDateTime.currentDateTime()
            self.ex_timer.start(1)
        else:
            self.ex_timer.stop()
            if self.start_time is not None:
                end_time = QDateTime.currentDateTime()
                elapsed = self.start_time.msecsTo(end_time)
                print("Elapsed time:", elapsed)
                self.start_time = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
