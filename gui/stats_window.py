'''
stats_window.py

This module is expected to define a window for displaying training statistics.
Extract relevant data from the user's training records and present them in the form of graphs or tables.

此模块预计定义一个用于显示训练统计数据的窗口。
从用户的训练记录中提取相关数据，并以图形或表格的形式呈现。
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from utils.plotter import TrainingPlotter


class StatsWindow:
    def __init__(self, master, runner):
        self.runner = runner
        self.window = tk.Toplevel(master)
        self.window.title("训练统计")

        self.dist_ylim = (1, 7)
        self.pace_ylim = (3, 8)

        self.create_tabs()

    def create_tabs(self):
        tab_control = ttk.Notebook(self.window)

        chart_frame = ttk.Frame(tab_control)
        self.plot_charts(chart_frame)
        tab_control.add(chart_frame, text='统计图')

        table_frame = ttk.Frame(tab_control)
        self.show_table(table_frame)
        tab_control.add(table_frame, text='数据表')

        tab_control.pack(expand=1, fill="both")

    def plot_charts(self, parent):
        control_frame = tk.Frame(parent)
        control_frame.pack(pady=10, fill=tk.X)

        tk.Label(control_frame, text="距离范围 (km):").grid(row=0, column=0, padx=5)
        self.dist_min = tk.Entry(control_frame, width=6)
        self.dist_min.insert(0, str(self.dist_ylim[0]))
        self.dist_min.grid(row=0, column=1)
        tk.Label(control_frame, text="-").grid(row=0, column=2)
        self.dist_max = tk.Entry(control_frame, width=6)
        self.dist_max.insert(0, str(self.dist_ylim[1]))
        self.dist_max.grid(row=0, column=3, padx=5)

        tk.Label(control_frame, text="配速范围 (min):").grid(row=0, column=4, padx=5)
        self.pace_min = tk.Entry(control_frame, width=6)
        self.pace_min.insert(0, str(self.pace_ylim[0]))
        self.pace_min.grid(row=0, column=5)
        tk.Label(control_frame, text="-").grid(row=0, column=6)
        self.pace_max = tk.Entry(control_frame, width=6)
        self.pace_max.insert(0, str(self.pace_ylim[1]))
        self.pace_max.grid(row=0, column=7, padx=5)

        tk.Button(control_frame, text="应用范围", command=self.update_chart).grid(row=0, column=8, padx=9)

        chart_container = tk.Frame(parent)
        chart_container.pack(fill=tk.BOTH, expand=True)

        self.create_figure(chart_container)

    def create_figure(self, parent):
        data = self.runner._load_data()
        records = data["training_records"]

        if not records:
            tk.Label(parent, text="⚠️ 没有训练记录！").pack()
            return

        dates = sorted(records.keys())
        distances = [records[date]["distance"] for date in dates]
        paces = [records[date]["pace"] for date in dates]

        self.fig = Figure(figsize=(8, 6))
        TrainingPlotter.plot_training_metrics(
            dates, distances, paces, self.fig,
            dist_ylim=self.dist_ylim,
            pace_ylim=self.pace_ylim
        )

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_chart(self):
        try:
            dist_min = float(self.dist_min.get())
            dist_max = float(self.dist_max.get())
            pace_min = float(self.pace_min.get())
            pace_max = float(self.pace_max.get())

            if dist_min >= dist_max or pace_min >= pace_max:
                raise ValueError("最小值必须小于最大值")

            self.dist_ylim = (dist_min, dist_max)
            self.pace_ylim = (pace_min, pace_max)

            self.canvas.get_tk_widget().destroy()
            self.create_figure(self.canvas.get_tk_widget().master)
        except ValueError as e:
            tk.messagebox.showerror("输入错误", f"无效的数值范围: {str(e)}")

    def show_table(self, parent):
        """统计表格"""
        data = self.runner._load_data()
        records = data["training_records"]
        modes = data.get("training_modes", {})

        table = TrainingPlotter.display_training_details(records, modes)

        text_frame = tk.Frame(parent)
        text_frame.pack(fill="both", expand=True)

        text = tk.Text(text_frame, wrap="none", font=("Consolas", 10))
        vsb = tk.Scrollbar(text_frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        text.pack(side="left", fill="both", expand=True)

        text.insert("1.0", table)
        text.configure(state="disabled")