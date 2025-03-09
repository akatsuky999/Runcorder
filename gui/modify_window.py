'''
modify_window.py

This module defines the ModifyWindow class, which provides a graphical interface for users to modify or delete training records.
It displays a list of existing training records, allowing users to select a record and perform modification or deletion operations.
Before performing these operations, it validates user input and prompts for confirmation when necessary.

此模块定义了 ModifyWindow 类，它提供了一个图形界面，允许用户修改或删除训练记录。
它显示一个现有的训练记录列表，允许用户选择一条记录并执行修改或删除操作。
在执行这些操作之前，它会验证用户输入，并在必要时提示确认。
'''

import tkinter as tk
from tkinter import ttk, messagebox
from utils.Interaction import modify_or_delete_records


class ModifyWindow:
    def __init__(self, master, runner):
        self.runner = runner
        self.window = tk.Toplevel(master)
        self.window.title("修改/删除记录")

        self.records = runner._load_data()["training_records"]
        self.listbox = tk.Listbox(self.window, width=40)
        self.listbox.pack(padx=10, pady=10)

        for date in sorted(self.records.keys()):
            self.listbox.insert(tk.END, f"{date} - {self.records[date]['distance']}km")

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="修改", command=self.modify).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="删除", command=self.delete).pack(side=tk.LEFT, padx=5)


    def modify(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("错误", "请先选择记录！")
            return
        date = self.listbox.get(selected[0]).split(" - ")[0]
        modify_or_delete_records(self.runner, date)  # 需要修改原函数支持直接传入日期
        self.window.destroy()

    def delete(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("错误", "请先选择记录！")
            return
        date = self.listbox.get(selected[0]).split(" - ")[0]
        if messagebox.askyesno("确认", "确定要删除这条记录吗？"):
            data = self.runner._load_data()
            del data["training_records"][date]
            self.runner._save_data(data)
            self.window.destroy()