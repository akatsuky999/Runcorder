'''
utils/plotter.py

This module contains a class `TrainingPlotter` that is used for visualizing and presenting running training data.
It can plot training metrics such as running distance and pace over time, and also display detailed training records in a tabular format.
The module also includes a utility function to convert decimal minutes to a more human - readable minutes - seconds format.

此模块包含一个`TrainingPlotter`类，用于可视化和展示跑步训练数据。
它可以绘制诸如跑步距离和配速随时间变化的训练指标，还可以以表格形式显示详细的训练记录。
该模块还包含一个实用函数，用于将十进制分钟转换为更易读的分秒格式。
'''

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib.ticker import FixedLocator, FixedFormatter
from matplotlib import rcParams
from tabulate import tabulate
from datetime import datetime

plt_font = 'Microsoft YaHei'
rcParams['font.sans-serif'] = [plt_font, 'SimHei']
rcParams['axes.unicode_minus'] = False

def decimal_minutes_to_min_sec(pace_decimal):
    """将十进制分钟转换为分秒格式"""
    total_seconds = round(pace_decimal * 60)
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes}’{seconds:02d}''"

class TrainingPlotter:
    @staticmethod
    def plot_training_metrics(dates, distances, paces, fig, dist_ylim=(1, 7), pace_ylim=(3, 8), modes=None):
        import matplotlib.dates as mdates
        from matplotlib.dates import DayLocator, DateFormatter

        plt.style.use('seaborn-v0_8')
        fig.clear()

        # 创建子图
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        # 将字符串日期转换为 datetime 对象
        date_objs = [mdates.datestr2num(d) for d in dates]

        ax1.plot(date_objs, distances, marker='o', color='#4063D8', label='Distance (km)')
        ax1.set_title("Running Distance Trend", fontweight='bold')
        ax1.set_ylabel("Distance (km)")
        ax1.grid(True, linestyle=':', alpha=0.6)

        ax1.set_ylim(*dist_ylim)

        ax2.plot(date_objs, paces, marker='s', color='#E3624B', label='Pace (min/km)')
        ax2.set_title("Average Pace Trend", fontweight='bold')
        ax2.set_ylabel("Pace (min/km)")
        ax2.grid(True, linestyle=':', alpha=0.6)

        ax2.set_ylim(*pace_ylim)

        # 格式化日期轴
        for ax in [ax1, ax2]:
            ax.xaxis.set_major_locator(DayLocator(interval=4))  # 每4天一个刻度
            ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            ax.tick_params(axis='x', rotation=45)


        if modes:
            for date, mode in modes.items():
                if date in dates:
                    idx = dates.index(date)
                    ax1.annotate(
                        text=mode[:3],
                        xy=(date_objs[idx], distances[idx]),
                        xytext=(0, 10),
                        textcoords="offset points",
                        ha='center',
                        color='#27AE60',
                        fontsize=8,
                        arrowprops=dict(arrowstyle="->", color='#2ECC71', lw=0.5)
                    )

                    ax2.plot(date_objs[idx], paces[idx],
                             marker='*', markersize=8,
                             color='#F1C40F', alpha=0.8)

        fig.tight_layout()

    @staticmethod
    def display_training_details(data, modes=None):
        formatted_data = []
        for date_str, details in sorted(data.items(), key=lambda x: x[0]):
            distance = f"{float(details['distance']):.2f}"
            pace_str = decimal_minutes_to_min_sec(float(details['pace']))
            time_symbol = "晨跑" if details['morning_run'] else "非晨跑"

            mode = modes.get(date_str, "无记录") if modes else "无记录"
            mode = f"{mode[:5]:<5}"

            formatted_data.append([
                date_str,
                distance,
                pace_str,
                details['assessment'].capitalize(),
                time_symbol,
                mode
            ])

        # 更新表头
        table_headers = [
            "Date",
            "Distance(km)",
            "Pace(min/km)",
            "Perception",
            "Running time",
            "Training Mode"
        ]

        # 生成表格
        table = tabulate(
            formatted_data,
            headers=table_headers,
            tablefmt="grid",
            colalign=("left", "right", "left", "left", "center", "left"),
            floatfmt=(".2f",)
        )
        return table