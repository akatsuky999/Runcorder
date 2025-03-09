# resource_utils.py
import sys
import os

def resource_path(relative_path):
    """ 获取资源的绝对路径（兼容开发环境和PyInstaller打包环境）"""
    if hasattr(sys, '_MEIPASS'):  # PyInstaller打包环境
        base_path = sys._MEIPASS
    else:  # 开发环境
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)