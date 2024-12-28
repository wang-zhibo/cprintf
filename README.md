
## cprintf

## Install

`pip install cprintf`

## Usage

```python
import cprintf


cprintf.info("普通字符串")
cprintf.info('{"hello": "world", "list": [1, 2, 3]}')
cprintf.info({"hello": "world", "list": [1, 2, 3]})
cprintf.warn({"warn_key": True})
cprintf.err("这是一条错误信息", format_mode='pprint')
cprintf.fatal("This is a fatal error.")
cprintf.ok('强制使用 pprint 模式', format_mode='pprint')
cprintf.debug('强制使用 raw 模式', format_mode='raw')
cprintf.line()
cprintf.custom("This is a custom color message in cyan!", "\033[96m")
cprintf.line(char='=', length=60, color='OK')

