'''
utils/Interaction.py

This module provides several functions for interacting with the running training records.
It includes functions to add training records, view training statistics, modify or delete existing records, and log training modes.
These functions ensure that user inputs are validated and stored correctly in the database.

此模块提供了几个用于与跑步训练记录进行交互的函数。
它包括添加训练记录、查看训练统计数据、修改或删除现有记录以及记录训练模式的功能。
这些函数确保用户输入经过验证并正确存储在数据库中。
'''

# -*- coding: utf-8 -*-
from core.runner import Runner
from core.database_handler import DatabaseHandler
from utils.plotter import TrainingPlotter
from utils.validator import DateValidator
import os
from utils.time_parse import parse_pace_input, format_pace_decimal
from utils.user_manage import user_selection
import tkinter as tk
from tkinter import simpledialog, messagebox

# 初始化Tkinter并隐藏主窗口
root = tk.Tk()
root.withdraw()


def add_training_record(runner, date=None, distance=None, pace=None, assessment=None, morning_run=None):
    """添加训练记录"""
    print("\n📝 Add Training Record (添加训练记录)")

    if date is None:
        while True:
            date = simpledialog.askstring("输入日期", "📅 Enter date (YYYY-MM-DD) (输入日期): ")
            if date is None: return  # 用户取消
            if DateValidator.validate_date(date):
                break
            messagebox.showerror("错误", "⚠️ Invalid date format! (日期格式无效)")

    if distance is None:
        while True:
            distance = simpledialog.askstring("输入距离", "🏃 Enter running distance (km) (输入跑步距离): ")
            if distance is None: return
            if distance.replace('.', '', 1).isdigit():
                distance = float(distance)
                break
            messagebox.showerror("错误", "⚠️ Distance must be a number! (距离必须是数字)")

    if pace is None:
        while True:
            pace_input = simpledialog.askstring("输入配速", "⏱ Enter average pace (e.g. 5/30 or 5) (输入配速): ")
            if pace_input is None: return
            try:
                pace = parse_pace_input(pace_input)
                break
            except ValueError as e:
                messagebox.showerror("错误", f"⚠️{str(e)} (输入错误)")

    if assessment is None:
        assessment = simpledialog.askstring("自我评估", "💬 Self-assessment (e.g. Good/Bad) (自我评估): ")
        if assessment is None: return

    if morning_run is None:
        while True:
            morning_run = simpledialog.askstring("晨跑", "🌅 Morning run? (Y/N) (是否晨跑？): ")
            if morning_run is None: return
            morning_run = morning_run.upper()
            if morning_run in ["Y", "N"]:
                break
            messagebox.showerror("错误", "⚠️ Please enter Y or N! (请输入Y或N)")

    # 添加记录到数据库
    DatabaseHandler.add_training_record(runner, date, distance, pace, assessment, morning_run)


def show_statistics(runner):
    """查看训练统计数据"""
    print("\n📊 View Training Statistics (查看训练统计)")
    data = runner._load_data()
    records = data["training_records"]
    modes = data["training_modes"]

    if not records:
        print("⚠️ No training records found! (未找到训练记录)")
        return

    sorted_dates = DatabaseHandler.get_sorted_dates(records)
    distances = [records[d]["distance"] for d in sorted_dates]
    paces = [records[d]["pace"] for d in sorted_dates]

    TrainingPlotter.plot_training_metrics(sorted_dates, distances, paces)

    TrainingPlotter.display_training_details(records)

    if modes:
        print("\n🏋️ Training Modes: (训练模式)")
        for date, mode in modes.items():
            print(f"{date}: {mode}")
    else:
        print("\n⚠️ No training modes logged yet. (尚未记录训练模式)")


def modify_or_delete_records(runner, pre_selected_date=None):
    """修改或删除记录"""
    data = runner._load_data()
    records = data["training_records"]

    if not records:
        messagebox.showerror("错误", "⚠️No records found to modify or delete! (未找到可修改或删除的记录)")
        return

    if pre_selected_date is None:
        record_list = "\n".join([f"- {date}" for date in records])
        date = simpledialog.askstring("选择记录", f"现有记录:\n{record_list}\n📅 输入要修改/删除的日期 (YYYY-MM-DD):")
        if date is None:
            return
    else:
        date = pre_selected_date

    if not DateValidator.validate_date(date) or date not in records:
        messagebox.showerror("错误", "⚠️Invalid date or no record found! (日期无效或未找到记录)")
        return

    action = simpledialog.askinteger("选择操作",
                                     "1. Modify Record (修改记录)\n2. Delete Record (删除记录)\n👉 选择操作 (1-2):")
    if action not in [1, 2]:
        messagebox.showerror("错误", "⚠️ Invalid action! (无效操作)")
        return

    if action == 1:
        current = records[date]
        current_pace = format_pace_decimal(current['pace'])

        new_distance = simpledialog.askstring("修改距离",
                                              f"当前距离: {current['distance']}km\n🏃 新跑步距离:")
        if new_distance:
            while not new_distance.replace('.', '', 1).isdigit():
                messagebox.showerror("错误", "⚠️ Distance must be a number! (距离必须是数字)")
                new_distance = simpledialog.askstring("修改距离", "🏃 新跑步距离:")
            records[date]["distance"] = float(new_distance)

        new_pace = simpledialog.askstring("修改配速",
                                          f"当前配速: {current_pace}\n⏱️ 新配速 (如5/30):")
        if new_pace:
            while True:
                try:
                    records[date]["pace"] = parse_pace_input(new_pace)
                    break
                except (ValueError, AttributeError) as e:
                    messagebox.showerror("错误", f"⚠️ Invalid pace format! {str(e)} (配速格式错误)")
                    new_pace = simpledialog.askstring("修改配速", "⏱️ 请重新输入新配速 (格式示例：5/30):")

        new_assessment = simpledialog.askstring("修改评估",
                                                f"当前评估: {current['assessment']}\n💬 新自我评估:")
        if new_assessment:
            records[date]["assessment"] = new_assessment

        new_morning = simpledialog.askstring("修改晨跑",
                                             f"当前: {'Y' if current['morning_run'] else 'N'}\n🌅 新晨跑? (Y/N):")
        if new_morning:
            records[date]["morning_run"] = new_morning.upper() == "Y"

        runner._save_data(data)
        messagebox.showinfo("成功", "✅ Record modified successfully! (记录修改成功)")

    elif action == 2:
        if messagebox.askyesno("确认", "确定要删除这条记录吗？"):
            del records[date]
            runner._save_data(data)
            messagebox.showinfo("成功", "✅ Record deleted successfully! (记录删除成功)")


def add_training_mode(runner, date=None, mode=None):
    """记录训练模式"""
    print("\n🏋️ Log Training Mode (记录训练模式)")

    if date is None:
        while True:
            date = simpledialog.askstring("输入日期", "📅 Enter date (YYYY-MM-DD) (输入日期): ")
            if date is None:
                return
            if DateValidator.validate_date(date):
                break
            messagebox.showerror("错误", "⚠️ Invalid date format! (日期格式无效)")

    if mode is None:
        mode_choice = simpledialog.askinteger("选择模式",
                                              "Select Training Mode: (选择训练模式)\n"
                                              "1. Aerobic Run (有氧跑)\n"
                                              "2. Anaerobic Run (无氧跑)\n"
                                              "3. Badminton Anaerobic Training (羽毛球无氧训练)\n"
                                              "👉 Select mode (1-3): ")
        if mode_choice is None:
            return

        mode_map = {
            1: "Aerobic Run (有氧跑)",
            2: "Anaerobic Run (无氧跑)",
            3: "Badminton Anaerobic Training (羽毛球)"
        }

        if mode_choice not in mode_map:
            messagebox.showerror("错误", "⚠️ Invalid choice! (无效选择)")
            return

        mode = mode_map[mode_choice]

    DatabaseHandler.add_training_mode(runner, date, mode)
    messagebox.showinfo("成功", "✅ Training mode logged successfully! (训练模式记录成功)")