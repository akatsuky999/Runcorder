'''
training_mode_window.py

This module defines a window for recording training modes.
Provides an interface for users to enter or select different training modes for each training.

此模块定义一个用于记录训练模式的窗口。
提供一个界面，让用户为每次训练输入或选择不同的训练模式。
'''

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from utils.Interaction import add_training_mode

class TrainingModeWindow:
    def __init__(self, master, runner):
        self.runner = runner
        self.window = tk.Toplevel(master)
        self.window.title("记录训练模式")

        tk.Label(self.window, text="日期 (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.window)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.window, text="训练模式:").grid(row=1, column=0, padx=5, pady=5)
        self.mode_var = tk.StringVar()
        ttk.Combobox(self.window, textvariable=self.mode_var,
                     values=["有氧跑", "无氧跑", "🏸&有氧跑", "🏸&无氧跑"]).grid(row=1, column=1)

        tk.Button(self.window, text="提交", command=self.submit).grid(row=2, columnspan=2, pady=10)


    def submit(self):
        date = self.date_entry.get()
        mode = self.mode_var.get()
        if not date or not mode:
            tk.messagebox.showerror("错误", "所有字段必须填写！")
            return
        add_training_mode(self.runner, date, mode)
        self.window.destroy()