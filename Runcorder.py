'''
Runcorder.py

This is the main entry point of the running training management system.
It initializes the root window, hides it, and then launches the AuthWindow.
This window serves as the starting point for user management, including creating, loading, and deleting users.

这是跑步训练管理系统的主入口文件。
它初始化根窗口并将其隐藏，然后启动用户管理窗口。
该窗口是用户管理的起始点，包括创建、加载和删除用户等操作。
'''

import tkinter as tk
from gui.auth_window import AuthWindow

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = AuthWindow(root)
    root.mainloop()