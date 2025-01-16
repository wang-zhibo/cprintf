
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
from typing import Any, Dict, List, Optional, Union


class ColorPrint:
    """Enhanced color printing utility with logging capabilities.
    
    Features:
    - Colored output with ANSI escape codes
    - Log level control
    - JSON/pretty print formatting
    - Progress bars
    - Table printing
    - Custom color support
    """
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
    def set_log_level(cls, level: str) -> None:
        """设置日志级别
        
        Args:
            level: 日志级别字符串，支持 DEBUG/INFO/WARNING/ERROR/FATAL
        """
        level = level.upper()
        if level not in cls.LOG_LEVELS:
            raise ValueError(f"Invalid log level: {level}. Valid levels are: {list(cls.LOG_LEVELS.keys())}")
        cls.log_level = cls.LOG_LEVELS[level]

    @classmethod
    def _auto_format(cls, message: Any) -> str:
        """根据 message 的类型或内容做自动格式化输出
        
        Args:
            message: 要格式化的内容，可以是任意类型
            
        Returns:
            格式化后的字符串
        """
        if isinstance(message, (dict, list)):
            try:
                return json.dumps(message, indent=4, ensure_ascii=False)
            except (TypeError, ValueError) as e:
                cls.warn(f"Failed to format as JSON: {str(e)}")
                return pprint.pformat(message)

        if isinstance(message, str):
            try:
                parsed = json.loads(message)
                return json.dumps(parsed, indent=4, ensure_ascii=False)
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                cls.debug(f"Input is not valid JSON: {str(e)}")
                return message

        return pprint.pformat(message)

    @classmethod
    def _get_repr(cls, message: Any, format_mode: str = 'auto') -> str:
        """将非字符串转化为字符串或其美观形式
        
        Args:
            message: 要转换的内容
            format_mode: 格式化模式，支持 'auto'/'raw'/'json'/'pprint'
            
        Returns:
            转换后的字符串表示
            
        Raises:
            ValueError: 如果 format_mode 参数无效
        """
        if format_mode not in ('auto', 'raw', 'json', 'pprint'):
            raise ValueError(f"Invalid format_mode: {format_mode}. "
                           "Valid modes are: auto, raw, json, pprint")

        if format_mode == 'raw':
            return str(message) if isinstance(message, str) else repr(message)
        elif format_mode == 'json':
            try:
                return json.dumps(message, indent=4, ensure_ascii=False)
            except (TypeError, ValueError) as e:
                cls.warn(f"Failed to format as JSON: {str(e)}")
                return pprint.pformat(message)
        elif format_mode == 'pprint':
            return pprint.pformat(message)
        return cls._auto_format(message)

    @classmethod
    def _print_in_color(
        cls,
        message: Any,
        color: str = 'NONE',
        file: Any = sys.stdout,
        prefix: str = '',
        suffix: str = '',
        format_mode: str = 'auto',
        timestamp: bool = False,
        **kwargs: Any
    ) -> None:
        """增强版打印方法，添加时间戳
        
        Args:
            message: 要打印的内容
            color: 颜色名称，默认为'NONE'
            file: 输出文件对象，默认为sys.stdout
            prefix: 前缀字符串
            suffix: 后缀字符串
            format_mode: 格式化模式，支持 'auto'/'raw'/'json'/'pprint'
            timestamp: 是否添加时间戳
            **kwargs: 传递给print()的其他参数
        """
        if color not in cls.colors:
            cls.warn(f"Invalid color: {color}. Using default color.")
            color = 'NONE'

        if cls.LOG_LEVELS.get(color, 0) < cls.log_level:
            return

        timestamp_str = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " if timestamp else ''
        text = cls._get_repr(message, format_mode=format_mode)
        
        try:
            print(
                cls.colors[color] + timestamp_str + prefix + text + suffix + cls.colors['ENDC'],
                file=file,
                **kwargs
            )
        except (IOError, OSError) as e:
            cls.err(f"Failed to print message: {str(e)}")

    @classmethod
    def get_colored_string(
        cls,
        message: Any,
        color: str = 'NONE',
        prefix: str = '',
        suffix: str = '',
        format_mode: str = 'auto'
    ) -> str:
        """返回带 ANSI 颜色控制符的字符串，但不打印
        
        Args:
            message: 要格式化的内容
            color: 颜色名称，默认为'NONE'
            prefix: 前缀字符串
            suffix: 后缀字符串
            format_mode: 格式化模式，支持 'auto'/'raw'/'json'/'pprint'
            
        Returns:
            带颜色控制符的字符串
            
        Raises:
            ValueError: 如果 color 参数无效
        """
        if color not in cls.colors:
            raise ValueError(f"Invalid color: {color}. Valid colors are: {list(cls.colors.keys())}")
            
        text = cls._get_repr(message, format_mode=format_mode)
        return cls.colors[color] + prefix + text + suffix + cls.colors['ENDC']

    @classmethod
    def debug(
        cls,
        message: Any,
        prefix: str = '',
        suffix: str = '',
        format_mode: str = 'auto',
        **kwargs: Any
    ) -> None:
        """打印调试信息(紫色)到 stdout
        
        Args:
            message: 要打印的消息内容
            prefix: 消息前缀
            suffix: 消息后缀
            format_mode: 格式化模式 ('auto'|'raw'|'json'|'pprint')
            **kwargs: 传递给print()的其他参数
            
        Example:
            >>> ColorPrint.debug("This is a debug message")
            \033[95mThis is a debug message\033[0m
        """
        cls._print_in_color(
            message,
            color='DEBUG',
            prefix=prefix,
            suffix=suffix,
            format_mode=format_mode,
            file=sys.stdout,
            **kwargs
        )

    @classmethod
    def ok(
        cls,
        message: Any,
        prefix: str = '',
        suffix: str = '',
        format_mode: str = 'auto',
        **kwargs: Any
    ) -> None:
        """打印普通成功或确认信息(蓝色)到 stdout
        
        Args:
            message: 要打印的消息内容
            prefix: 消息前缀
            suffix: 消息后缀
            format_mode: 格式化模式 ('auto'|'raw'|'json'|'pprint')
            **kwargs: 传递给print()的其他参数
            
        Example:
            >>> ColorPrint.ok("Operation completed successfully")
            \033[94mOperation completed successfully\033[0m
            
            >>> ColorPrint.ok({"status": "ok"}, prefix="[INFO] ")
            \033[94m[INFO] {
                "status": "ok"
            }\033[0m
        """
        cls._print_in_color(
            message,
            color='OK',
            prefix=prefix,
            suffix=suffix,
            format_mode=format_mode,
            file=sys.stdout,
            **kwargs
        )

    @classmethod
    def info(
        cls,
        message: Any,
        prefix: str = '',
        suffix: str = '',
        format_mode: str = 'auto',
        **kwargs: Any
    ) -> None:
        """打印普通信息(绿色)到 stdout
        
        Args:
            message: 要打印的消息内容
            prefix: 消息前缀
            suffix: 消息后缀
            format_mode: 格式化模式 ('auto'|'raw'|'json'|'pprint')
            **kwargs: 传递给print()的其他参数
            
        Example:
            >>> ColorPrint.info("System is running normally")
            \033[92mSystem is running normally\033[0m
            
            >>> ColorPrint.info({"users": 10}, prefix="[STATUS] ")
            \033[92m[STATUS] {
                "users": 10
            }\033[0m
        """
        cls._print_in_color(
            message,
            color='INFO',
            prefix=prefix,
            suffix=suffix,
            format_mode=format_mode,
            file=sys.stdout,
            **kwargs
        )

    @classmethod
    def warn(cls, message: Any, prefix: str = '', suffix: str = '', 
             format_mode: str = 'auto', **kwargs: Any) -> None:
        """打印警告信息(黄色)到 stderr
        
        Args:
            message: 要打印的消息内容
            prefix: 消息前缀
            suffix: 消息后缀
            format_mode: 格式化模式 ('auto'|'raw'|'json'|'pprint')
            **kwargs: 传递给print()的其他参数
            
        Example:
            >>> ColorPrint.warn("This is a warning message")
            \033[93mThis is a warning message\033[0m
        """
        cls._print_in_color(message, color='WARNING', prefix=prefix, suffix=suffix, 
                          format_mode=format_mode, file=sys.stderr, **kwargs)

    @classmethod
    def err(cls, message: Any, interrupt: bool = False, 
            fatal_message: str = "Fatal error: Program stopped.",
            prefix: str = '', suffix: str = '', format_mode: str = 'auto', 
            **kwargs: Any) -> None:
        """打印错误信息(亮红)到 stderr
        
        Args:
            message: 要打印的消息内容
            interrupt: 是否中断程序
            fatal_message: 中断时显示的消息
            prefix: 消息前缀
            suffix: 消息后缀
            format_mode: 格式化模式 ('auto'|'raw'|'json'|'pprint')
            **kwargs: 传递给print()的其他参数
            
        Example:
            >>> ColorPrint.err("An error occurred")
            \033[91mAn error occurred\033[0m
            
            >>> ColorPrint.err("Critical error", interrupt=True)
            \033[91mCritical error\033[0m
            \033[91mFatal error: Program stopped.\033[0m
            [程序退出]
        """
        cls._print_in_color(message, color='ERR', prefix=prefix, suffix=suffix, 
                          format_mode=format_mode, file=sys.stderr, **kwargs)
        if interrupt:
            cls._print_in_color(fatal_message, color='ERR', file=sys.stderr)
            sys.exit(1)

    @classmethod
    def fatal(cls, message: Any, interrupt: bool = False,
              fatal_message: str = "Fatal error: Program stopped.",
              prefix: str = '', suffix: str = '', format_mode: str = 'auto',
              **kwargs: Any) -> None:
        """打印致命错误信息(红色)到 stderr
        
        Args:
            message: 要打印的消息内容
            interrupt: 是否中断程序
            fatal_message: 中断时显示的消息
            prefix: 消息前缀
            suffix: 消息后缀
            format_mode: 格式化模式 ('auto'|'raw'|'json'|'pprint')
            **kwargs: 传递给print()的其他参数
            
        Example:
            >>> ColorPrint.fatal("System failure")
            \033[31mSystem failure\033[0m
            
            >>> ColorPrint.fatal("Critical failure", interrupt=True)
            \033[31mCritical failure\033[0m
            \033[31mFatal error: Program stopped.\033[0m
            [程序退出]
        """
        cls._print_in_color(message, color='FATAL', prefix=prefix, suffix=suffix,
                          format_mode=format_mode, file=sys.stderr, **kwargs)
        if interrupt:
            cls._print_in_color(fatal_message, color='FATAL', file=sys.stderr)
            sys.exit(1)

    @classmethod
    def custom(cls, message: Any, color_code: str, prefix: str = '', 
               suffix: str = '', format_mode: str = 'auto', 
               file: Any = sys.stdout, **kwargs: Any) -> None:
        """自定义颜色输出
        
        Args:
            message: 要打印的消息内容
            color_code: ANSI颜色代码
            prefix: 消息前缀
            suffix: 消息后缀
            format_mode: 格式化模式 ('auto'|'raw'|'json'|'pprint')
            file: 输出文件对象
            **kwargs: 传递给print()的其他参数
            
        Example:
            >>> ColorPrint.custom("Custom message", "\033[95m")
            \033[95mCustom message\033[0m
        """
        text = cls._get_repr(message, format_mode=format_mode)
        print(
            color_code + prefix + text + suffix + cls.colors['ENDC'],
            file=file,
            **kwargs
        )

    @classmethod
    def line(cls, length: int = 50, char: str = '-', color: str = 'INFO', 
             file: Any = sys.stdout, **kwargs: Any) -> None:
        """打印一条分割线
        
        Args:
            length: 分割线长度
            char: 分割线字符
            color: 颜色名称
            file: 输出文件对象
            **kwargs: 传递给print()的其他参数
            
        Example:
            >>> ColorPrint.line(length=30, char='=', color='WARNING')
            \033[93m==============================\033[0m
        """
        color_code = cls.colors.get(color, cls.colors['INFO'])
        line_str = char * length
        print(
            color_code + line_str + cls.colors['ENDC'],
            file=file,
            **kwargs
        )

    @classmethod
    def progress_bar(cls, iteration: int, total: int, prefix: str = '', 
                     suffix: str = '', length: int = 50, fill: str = '█', 
                     color: str = 'INFO') -> None:
        """打印进度条
        
        Args:
            iteration: 当前迭代次数
            total: 总迭代次数
            prefix: 进度条前缀
            suffix: 进度条后缀
            length: 进度条长度
            fill: 进度条填充字符
            color: 颜色名称
            
        Example:
            >>> for i in range(101):
                    ColorPrint.progress_bar(i, 100)
            \r\033[92m |██████████████████████████████████████████████████| 100.0% \033[0m
        """
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{cls.colors[color]}{prefix} |{bar}| {percent}% {suffix}{cls.colors["ENDC"]}', end='\r')
        if iteration == total:
            print()

    @classmethod
    def print_table(cls, data: List[List[Any]], headers: Optional[List[str]] = None,
                    color: str = 'INFO', align: str = 'left') -> None:
        """打印表格
        
        Args:
            data: 表格数据，二维列表
            headers: 表头列表
            color: 颜色名称
            align: 对齐方式 ('left'|'right')
            
        Example:
            >>> data = [["Alice", 25], ["Bob", 30]]
            >>> ColorPrint.print_table(data, headers=["Name", "Age"])
            \033[92mName  | Age\033[0m
            \033[92m------|----\033[0m
            \033[92mAlice | 25 \033[0m
            \033[92mBob   | 30 \033[0m
        """
        if not data:
            return

        col_widths = [max(len(str(x)) for x in col) for col in zip(*data)]
        if headers:
            col_widths = [max(col_widths[i], len(str(headers[i]))) for i in range(len(headers))]
            
        if headers:
            header = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
            cls._print_in_color(header, color=color)
            cls.line(length=sum(col_widths) + len(col_widths)*3 - 1, color=color)

        for row in data:
            row_str = " | ".join(str(x).ljust(col_widths[i]) if align=='left' else str(x).rjust(col_widths[i])
                               for i, x in enumerate(row))
            cls._print_in_color(row_str, color=color)



cprintf = ColorPrint()

# 设置日志级别
cprintf.set_log_level('DEBUG')  # 可选: DEBUG, INFO, WARNING, ERROR, FATAL

# 基本打印功能
cprintf.info("普通字符串")
cprintf.info('{"hello": "world", "list": [1, 2, 3]}')
cprintf.info({"hello": "world", "list": [1, 2, 3]})
cprintf.warn({"warn_key": True})
cprintf.err("这是一条错误信息", format_mode='pprint')
cprintf.fatal("This is a fatal error.")
cprintf.ok('强制使用 pprint 模式', format_mode='pprint')
cprintf.debug('强制使用 raw 模式', format_mode='raw')

# 带时间戳的日志
cprintf.info("这是一条带时间戳的信息", timestamp=True)

# 分割线
cprintf.line()
cprintf.line(char='=', length=60, color='OK')

# 自定义颜色
cprintf.custom("This is a custom color message in cyan!", "\033[96m")

# 进度条
for i in range(100):
    sleep(0.1)
    cprintf.progress_bar(i + 1, 100, prefix='进度:', suffix='完成', length=50)

# 打印表格
data = [
    [1, "Alice", 25],
    [2, "Bob", 30],
    [3, "Charlie", 35]
]
cprintf.print_table(data, headers=["ID", "Name", "Age"], color='INFO')

# 获取带颜色的字符串（不打印）
colored_str = cprintf.get_colored_string("这是一个带颜色的字符串", color='WARNING')
print(colored_str)
