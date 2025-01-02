
#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:
# E-mail: gm.zhibo.wang@gmail.com
# Date  :
# Desc  :



from __future__ import print_function, unicode_literals
import sys
import json
import pprint
from datetime import datetime


class ColorPrint:
    """
    一个增强版的彩色打印工具类
    """
    # 添加日志级别
    LOG_LEVELS = {
        'DEBUG': 10,
        'INFO': 20,
        'WARNING': 30,
        'ERROR': 40,
        'FATAL': 50
    }
    
    # 扩展颜色配置
    colors = {
        'NONE':    '\033[0m',
        'DEBUG':   '\033[95m',  # 紫色
        'OK':      '\033[94m',  # 蓝色
        'INFO':    '\033[92m',  # 绿色
        'WARNING': '\033[93m',  # 黄色
        'ERR':     '\033[91m',  # 亮红
        'FATAL':   '\033[31m',  # 红色
        'ENDC':    '\033[0m',   # 结束符
        'CYAN':    '\033[96m',  # 青色
        'GRAY':    '\033[90m',  # 灰色
    }

    # 添加日志级别控制
    log_level = LOG_LEVELS['INFO']

    @classmethod
    def set_log_level(cls, level):
        """
        设置日志级别
        """
        if level.upper() in cls.LOG_LEVELS:
            cls.log_level = cls.LOG_LEVELS[level.upper()]

    @classmethod
    def _auto_format(cls, message):
        """
        根据 message 的类型或内容做自动格式化输出
        """
        if isinstance(message, (dict, list)):
            try:
                return json.dumps(message, indent=4, ensure_ascii=False)
            except (TypeError, ValueError):
                return pprint.pformat(message)

        if isinstance(message, str):
            try:
                parsed = json.loads(message)
                return json.dumps(parsed, indent=4, ensure_ascii=False)
            except (json.JSONDecodeError, TypeError, ValueError):
                return message

        return pprint.pformat(message)

    @classmethod
    def _get_repr(cls, message, format_mode='auto'):
        """
        将非字符串转化为字符串或其美观形式
        """
        if format_mode == 'raw':
            return str(message) if isinstance(message, str) else repr(message)
        elif format_mode == 'json':
            try:
                return json.dumps(message, indent=4, ensure_ascii=False)
            except (TypeError, ValueError):
                return pprint.pformat(message)
        elif format_mode == 'pprint':
            return pprint.pformat(message)
        else:
            return cls._auto_format(message)

    @classmethod
    def _print_in_color(cls, message, color='NONE', file=sys.stdout, prefix='', suffix='', format_mode='auto', timestamp=False, **kwargs):
        """
        增强版打印方法，添加时间戳
        """
        if cls.LOG_LEVELS.get(color, 0) < cls.log_level:
            return
            
        timestamp_str = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " if timestamp else ''
        text = cls._get_repr(message, format_mode=format_mode)
        print(
            cls.colors[color] + timestamp_str + prefix + text + suffix + cls.colors['ENDC'],
            file=file,
            **kwargs
        )

    @classmethod
    def get_colored_string(cls, message, color='NONE', prefix='', suffix='', format_mode='auto'):
        """
        返回带 ANSI 颜色控制符的字符串，但不打印
        """
        text = cls._get_repr(message, format_mode=format_mode)
        return cls.colors[color] + prefix + text + suffix + cls.colors['ENDC']

    @classmethod
    def debug(cls, message, prefix='', suffix='', format_mode='auto', **kwargs):
        """
        打印调试信息(紫色)到 stdout
        """
        cls._print_in_color(message, color='DEBUG', prefix=prefix, suffix=suffix, format_mode=format_mode, file=sys.stdout, **kwargs)

    @classmethod
    def ok(cls, message, prefix='', suffix='', format_mode='auto', **kwargs):
        """
        打印普通成功或确认信息(蓝色)到 stdout
        """
        cls._print_in_color(message, color='OK', prefix=prefix, suffix=suffix, format_mode=format_mode, file=sys.stdout, **kwargs)

    @classmethod
    def info(cls, message, prefix='', suffix='', format_mode='auto', **kwargs):
        """
        打印普通信息(绿色)到 stdout
        """
        cls._print_in_color(message, color='INFO', prefix=prefix, suffix=suffix, format_mode=format_mode, file=sys.stdout, **kwargs)

    @classmethod
    def warn(cls, message, prefix='', suffix='', format_mode='auto', **kwargs):
        """
        打印警告信息(黄色)到 stderr
        """
        cls._print_in_color(message, color='WARNING', prefix=prefix, suffix=suffix, format_mode=format_mode, file=sys.stderr, **kwargs)

    @classmethod
    def err(cls, message, interrupt=False, fatal_message="Fatal error: Program stopped.",
            prefix='', suffix='', format_mode='auto', **kwargs):
        """
        打印错误信息(亮红)到 stderr
        """
        cls._print_in_color(message, color='ERR', prefix=prefix, suffix=suffix, format_mode=format_mode, file=sys.stderr, **kwargs)
        if interrupt:
            cls._print_in_color(fatal_message, color='ERR', file=sys.stderr)
            sys.exit(1)

    @classmethod
    def fatal(cls, message, interrupt=False, fatal_message="Fatal error: Program stopped.",
              prefix='', suffix='', format_mode='auto', **kwargs):
        """
        打印致命错误信息(红色)到 stderr
        """
        cls._print_in_color(message, color='FATAL', prefix=prefix, suffix=suffix, format_mode=format_mode, file=sys.stderr, **kwargs)
        if interrupt:
            cls._print_in_color(fatal_message, color='FATAL', file=sys.stderr)
            sys.exit(1)

    @classmethod
    def custom(cls, message, color_code, prefix='', suffix='', format_mode='auto', file=sys.stdout, **kwargs):
        """
        自定义颜色输出
        """
        text = cls._get_repr(message, format_mode=format_mode)
        print(
            color_code + prefix + text + suffix + cls.colors['ENDC'],
            file=file,
            **kwargs
        )

    @classmethod
    def line(cls, length=50, char='-', color='INFO', file=sys.stdout, **kwargs):
        """
        打印一条分割线
        """
        cls._print_in_color(char * length, color=color, file=file, **kwargs)

    @classmethod
    def progress_bar(cls, iteration, total, prefix='', suffix='', length=50, fill='█', color='INFO'):
        """
        打印进度条
        """
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{cls.colors[color]}{prefix} |{bar}| {percent}% {suffix}{cls.colors["ENDC"]}', end='\r')
        if iteration == total: 
            print()

    @classmethod
    def print_table(cls, data, headers=None, color='INFO', align='left'):
        """
        打印表格
        """
        if not data:
            return
            
        # 计算列宽
        col_widths = [max(len(str(x)) for x in col) for col in zip(*data)]
        if headers:
            col_widths = [max(col_widths[i], len(str(headers[i]))) for i in range(len(headers))]
            
        # 打印表头
        if headers:
            header = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
            cls._print_in_color(header, color=color)
            cls.line(length=sum(col_widths) + len(col_widths)*3 - 1, color=color)
            
        # 打印数据
        for row in data:
            row_str = " | ".join(str(x).ljust(col_widths[i]) if align=='left' else str(x).rjust(col_widths[i]) 
                               for i, x in enumerate(row))
            cls._print_in_color(row_str, color=color)

