"""
Runcorder.py

This is the main entry point of the running training management system.
It initializes the Tkinter root window, hides it, and then launches the AuthWindow.
This window serves as the starting point for user management, including creating, loading, and deleting users.

这是跑步训练管理系统的主入口文件。
它初始化 Tkinter 根窗口并将其隐藏，然后启动用户管理窗口（AuthWindow）。
该窗口是用户管理的起始点，包括创建、加载和删除用户等操作。
"""

import tkinter as tk

class AuthWindow:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("用户管理系统")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="🏃 训练管理系统", font=('微软雅黑', 16)).pack(pady=10)

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="新建用户", command=self.create_user, width=15).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="加载用户", command=self.load_user, width=15).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="删除用户", command=self.delete_user, width=15).grid(row=1, column=0, padx=10)
        tk.Button(btn_frame, text="退出系统", command=self.quit_program, width=15).grid(row=1, column=1, pady=10)

    def quit_program(self):
        """退出程序"""
        self.window.destroy()
        self.master.quit()

    def create_user(self):
        from utils.user_manage import create_new_user
        runner = create_new_user()
        if runner:
            self.open_main_window(runner)

    def load_user(self):
        from utils.user_manage import load_existing_user
        user = load_existing_user()
        if user:
            self.open_main_window(user)

    def delete_user(self):
        from utils.user_manage import delete_user
        delete_user()

    def open_main_window(self, runner):
        from .main_window import MainWindow
        self.window.destroy()
        MainWindow(self.master, runner)