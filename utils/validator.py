'''
utils/validator.py

This module provides a utility class `DateValidator` for validating date strings.
The `validate_date` static method checks if a given date string is in the 'YYYY-MM-DD' format.
If the date string can be parsed according to the specified format, it returns True; otherwise, it returns False.

此模块提供了一个实用类 `DateValidator`，用于验证日期字符串。
`validate_date` 静态方法会检查给定的日期字符串是否为 'YYYY-MM-DD' 格式。
如果日期字符串可以按照指定格式进行解析，则返回 True；否则返回 False。
'''


from datetime import datetime

class DateValidator:
    @staticmethod
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False