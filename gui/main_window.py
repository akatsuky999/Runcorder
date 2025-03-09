'''
main_window.py

This module defines the MainWindow class, which is the main interface for the running training management system.
It provides a menu with various functions such as adding training records, viewing statistics, recording training modes,
modifying or deleting records, and returning to the user management system.
The main window also displays the current user and the latest training record.

此模块定义了 MainWindow 类，它是跑步训练管理系统的主界面。
它提供了一个菜单，包含多种功能，如添加训练记录、查看统计数据、记录训练模式、修改或删除记录，以及返回用户管理系统。
主窗口还会显示当前用户和最近的训练记录。
'''

import tkinter as tk
from .stats_window import StatsWindow
from .record_window import RecordWindow
from .training_mode_window import TrainingModeWindow
from .modify_window import ModifyWindow


class MainWindow:
    def __init__(self, master, runner):
        self.master = master
        self.runner = runner

        self.window = tk.Toplevel(master)
        self.window.title(f"{runner.name}的训练管理系统")

        self.create_menu()
        self.create_main_frame()

    def create_menu(self):
        """创建主菜单"""
        menu_bar = tk.Menu(self.window)

        # 功能菜单
        func_menu = tk.Menu(menu_bar, tearoff=0)
        func_menu.add_command(label="添加训练记录", command=self.open_add_record)
        func_menu.add_command(label="查看统计数据", command=self.open_stats)
        func_menu.add_command(label="记录训练模式", command=self.open_training_mode)  # 新增：训练模式
        func_menu.add_command(label="修改/删除记录", command=self.open_modify_records)  # 新增：修改/删除
        func_menu.add_separator()
        func_menu.add_command(label="退出系统", command=self.return_to_auth)  # 修改退出逻辑
        menu_bar.add_cascade(label="功能", menu=func_menu)

        self.window.config(menu=menu_bar)

    def create_main_frame(self):
        """创建主界面"""
        main_frame = tk.Frame(self.window, padx=60, pady=60)
        main_frame.pack(expand=True)

        # 显示当前用户
        tk.Label(main_frame,
                 text=f"👤 当前用户：{self.runner.name}",
                 font=('微软雅黑', 14)).pack(pady=30)

        # 显示最近训练记录
        records = self.runner._load_data()["training_records"]
        if records:
            last_date = max(records.keys())
            last_dist = records[last_date]["distance"]
            tk.Label(main_frame,
                     text=f"最近训练：{last_date} | 距离：{last_dist}km",
                     font=('微软雅黑', 10)).pack()
        else:
            tk.Label(main_frame,
                     text="⚠️ 暂无训练记录",
                     font=('微软雅黑', 10)).pack()

    def return_to_auth(self):
        """返回到用户管理系统界面"""
        self.window.destroy()
        from .auth_window import AuthWindow
        AuthWindow(self.master)

    def open_add_record(self):
        """打开添加训练记录窗口"""
        RecordWindow(self.master, self.runner)

    def open_stats(self):
        """打开统计数据窗口"""
        StatsWindow(self.master, self.runner)

    def open_training_mode(self):
        """打开记录训练模式窗口"""
        TrainingModeWindow(self.master, self.runner)

    def open_modify_records(self):
        """打开修改/删除记录窗口"""
        ModifyWindow(self.master, self.runner)