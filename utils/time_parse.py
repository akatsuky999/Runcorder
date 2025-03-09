'''
utils/time_parse.py

This module provides two utility functions for handling running pace data.
The `parse_pace_input` function is used to parse a user - input pace string in the format of 'minutes/seconds' (e.g., '5/30') or just 'minutes' (e.g., '5') into a decimal representation of minutes. It also includes validation to ensure the input is in the correct format and the values are within a reasonable range.
The `format_pace_decimal` function converts a decimal representation of pace (in minutes) back to a human - readable 'minutes'seconds'' format.

此模块提供了两个实用函数，用于处理跑步配速数据。
`parse_pace_input` 函数用于将用户输入的配速字符串（格式为 '分钟/秒'，如 '5/30'，或仅为 '分钟'，如 '5'）解析为分钟的十进制表示形式。它还包含验证功能，以确保输入格式正确且值在合理范围内。
`format_pace_decimal` 函数将配速的十进制表示形式（以分钟为单位）转换回人类可读的 '分钟'秒'' 格式。
'''

import re

def parse_pace_input(pace_str):
    """支持5/30或5格式输入"""
    # 允许的格式示例：5/30 → 5分30秒 | 5 → 5分0秒
    match = re.match(r'^(\d+)(?:/(\d{1,2}))?$', pace_str)

    if not match:
        raise ValueError("配速格式错误，请使用分钟/秒格式（如5/30）")

    minutes = int(match.group(1))
    seconds = int(match.group(2)) if match.group(2) else 0

    if minutes < 0:
        raise ValueError("分钟数不能为负数")
    if seconds >= 60:
        raise ValueError("秒数不能超过59")

    return minutes + seconds / 60

def format_pace_decimal(pace_decimal):
    """保持分秒显示格式"""
    total_seconds = round(pace_decimal * 60)
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes}’{seconds:02d}’’"