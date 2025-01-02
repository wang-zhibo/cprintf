import cprintf
from time import sleep

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
