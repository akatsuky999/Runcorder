'''
record_window.py

This module defines the RecordWindow class, which provides a graphical interface for users to add training records.
It includes input fields for date, distance, pace, self-assessment, and whether it was a morning run.
Before submitting the record, it validates the input data to ensure its correctness.
If the input is valid, it calls the add_training_record function to save the record.

此模块定义了 RecordWindow 类，它提供了一个图形界面，允许用户添加训练记录。
它包含日期、距离、配速、自我评估以及是否为晨跑的输入字段。
在提交记录之前，它会验证输入数据以确保其正确性。
如果输入有效，它会调用 add_training_record 函数保存记录。
'''

import tkinter as tk
from tkinter import messagebox
from utils.Interaction import add_training_record
from utils.validator import DateValidator


class RecordWindow:
    def __init__(self, master, runner):
        self.master = master
        self.runner = runner

        self.window = tk.Toplevel(master)
        self.window.title("添加训练记录")

        self.create_form()

    def create_form(self):
        form_frame = tk.Frame(self.window, padx=20, pady=20)
        form_frame.pack()

        tk.Label(form_frame, text="日期 (YYYY-MM-DD):").grid(row=0, column=0, sticky='e')
        self.date_entry = tk.Entry(form_frame, width=20)
        self.date_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="距离 (km):").grid(row=1, column=0, sticky='e')
        self.dist_entry = tk.Entry(form_frame, width=20)
        self.dist_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="配速 (e.g. 5/30 or 5):").grid(row=2, column=0, sticky='e')
        self.pace_entry = tk.Entry(form_frame, width=20)
        self.pace_entry.grid(row=2, column=1)

        tk.Label(form_frame, text="自我评估 (e.g. Good/Bad):").grid(row=3, column=0, sticky='e')
        self.assessment_entry = tk.Entry(form_frame, width=20)
        self.assessment_entry.grid(row=3, column=1)

        tk.Label(form_frame, text="晨跑? (Y/N):").grid(row=4, column=0, sticky='e')
        self.morning_run_entry = tk.Entry(form_frame, width=20)
        self.morning_run_entry.grid(row=4, column=1)

        tk.Button(form_frame, text="提交", command=self.submit).grid(row=5, columnspan=2, pady=10)

    def submit(self):
        date = self.date_entry.get()
        distance = self.dist_entry.get()
        pace = self.pace_entry.get()
        assessment = self.assessment_entry.get()
        morning_run = self.morning_run_entry.get().upper()

        if not DateValidator.validate_date(date):
            messagebox.showerror("错误", "日期格式无效！")
            return

        if not distance.replace('.', '', 1).isdigit():
            messagebox.showerror("错误", "距离必须是数字！")
            return

        try:
            from utils.time_parse import parse_pace_input
            pace = parse_pace_input(pace)
        except ValueError as e:
            messagebox.showerror("错误", f"配速格式错误：{str(e)}")
            return

        if morning_run not in ["Y", "N"]:
            messagebox.showerror("错误", "晨跑输入必须是 Y 或 N！")
            return

        try:
            add_training_record(self.runner, date, float(distance), pace, assessment, morning_run)
            messagebox.showinfo("成功", "训练记录添加成功！")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"添加记录失败：{str(e)}")