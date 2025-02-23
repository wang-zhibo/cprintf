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

# 新增示例：不同日志级别
cprintf.set_log_level('INFO')
cprintf.debug("这条调试信息不会显示")  # 日志级别高于DEBUG，不会显示
cprintf.info("这条信息会显示")

# 新增示例：带前缀和后缀的输出
cprintf.info("带前缀和后缀的信息", prefix="[前缀] ", suffix=" [后缀]")

# 新增示例：复杂表格
complex_data = [
    ["项目", "进度", "状态"],
    ["项目A", "75%", "进行中"],
    ["项目B", "100%", "已完成"],
    ["项目C", "50%", "延迟"]
]
cprintf.print_table(complex_data, color='WARNING', align='center')

# 新增示例：不同颜色的进度条
for i in range(100):
    sleep(0.05)
    color = 'OK' if i < 50 else 'WARNING' if i < 80 else 'ERR'
    cprintf.progress_bar(i + 1, 100, prefix='处理中:', suffix=f'阶段 {i//20 + 1}', color=color)

# 新增示例：自定义格式的JSON输出
complex_json = {
    "name": "测试数据",
    "values": [1, 2, 3],
    "metadata": {
        "created_at": "2025-02-23",
        "author": "测试用户"
    }
}
cprintf.info(complex_json, format_mode='json')

# 新增示例：错误处理
try:
    1 / 0
except Exception as e:
    cprintf.err(f"发生错误: {str(e)}", interrupt=False)
    cprintf.fatal("严重错误！", interrupt=True)
