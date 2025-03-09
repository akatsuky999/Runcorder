'''
utils/user_manage.py

This module is responsible for user management in the running training system.
It provides functions to list existing users, create new users, load existing users, delete users, and handle user selection.
The user management system uses a simple JSON file - based database to store user information.

此模块负责跑步训练系统中的用户管理。
它提供了列出现有用户、创建新用户、加载现有用户、删除用户以及处理用户选择的功能。
用户管理系统使用基于简单JSON文件的数据库来存储用户信息。
'''

import os
import json
from core.runner import Runner
import tkinter as tk
from tkinter import simpledialog, messagebox
from .resource_utils import resource_path


root = tk.Tk()
root.withdraw()

def list_existing_users():
    """列出所有已存在的用户"""
    user_dir = resource_path("database/users")
    if not os.path.exists(user_dir):
        return []
    return [f.split('.')[0] for f in os.listdir(user_dir) if f.endswith('.json')]

def create_new_user():
    """创建新用户流程"""
    while True:
        name = simpledialog.askstring("新用户", "🏃️ Enter NEW runner's name (输入新用户名): ")
        if name is None:
            return None

        name = name.strip()
        if not name:
            messagebox.showerror("错误", "⚠️Username cannot be empty! (用户名不能为空)")
            continue

        user_file = resource_path(f"database/users/{name}.json")
        if os.path.exists(user_file):
            messagebox.showerror("错误", "⚠️ User already exists! (用户已存在)")
            continue

        initial_data = {
            "training_records": {},
            "training_modes": {}
        }
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False)
        return Runner(name)

def load_existing_user():
    """加载已有用户流程"""
    users = list_existing_users()
    if not users:
        messagebox.showerror("错误", "⚠️ No existing users found! (未找到现有用户)")
        return None

    user_list = "\n".join([f"{i+1}. {user}" for i, user in enumerate(users)])
    choice = simpledialog.askstring("选择用户", f"现有用户:\n{user_list}\n👉 输入用户名或序号: ")
    if choice is None:
        return None

    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(users):
            return Runner(users[index])
    elif choice in users:
        return Runner(choice)
    messagebox.showerror("错误", "⚠️ Invalid selection! (无效选择)")
    return None

def delete_user():
    """删除用户流程"""
    users = list_existing_users()
    if not users:
        messagebox.showerror("错误", "⚠️ No existing users found! (未找到现有用户)")
        return

    user_list = "\n".join([f"{i+1}. {user}" for i, user in enumerate(users)])
    choice = simpledialog.askstring("删除用户", f"现有用户:\n{user_list}\n👉 输入要删除的用户名或序号: ")
    if choice is None:
        return

    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(users):
            user_to_delete = users[index]
        else:
            messagebox.showerror("错误", "⚠️ Invalid selection! (无效选择)")
            return
    elif choice in users:
        user_to_delete = choice
    else:
        messagebox.showerror("错误", "⚠️ Invalid selection! (无效选择)")
        return

    # 确认删除
    if messagebox.askyesno("确认", f"确定要删除用户 {user_to_delete} 吗？"):
        user_file = resource_path(f"database/users/{user_to_delete}.json")
        os.remove(user_file)
        messagebox.showinfo("成功", f"✅ 用户 {user_to_delete} 已删除！")

def user_selection():
    """用户选择入口"""
    print("\n" + "= " * 40)
    print("👥 User Management System (用户管理系统)")
    print("1. 🆕 Create New User (新建用户)")
    print("2. 📂 Load Existing User (读取用户)")
    print("3. 🗑️ Delete User (删除用户)")
    print("4. 🚪 Exit (退出系统)")

    while True:
        choice = simpledialog.askstring("选择操作", "👉 Select option (1-4) (请选择操作): ")
        if choice == "1":
            runner = create_new_user()
            if runner:
                return runner
        elif choice == "2":
            user = load_existing_user()
            if user:
                return user
        elif choice == "3":
            delete_user()
        elif choice == "4":
            print("👋 Exiting... (正在退出)")
            root.destroy()
            exit()
        else:
            messagebox.showerror("错误", "⚠️ Invalid input! (无效输入)")