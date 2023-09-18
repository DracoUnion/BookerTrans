import traceback
import sys
import os
from os import path

default_prompt = '请把以下文本翻译成中文，不要保留原文：'

is_html = lambda f: f.endswith('.html') or \
                    f.endswith('.htm') or \
                    f.endswith('.xhtml')

def safe(default=None):
    def wrapper(func):
        def inner(*args, **kw):
            try: return func(*args, **kw)
            except: 
                traceback.print_exc()
                return default
        return inner
    return wrapper

def find_cmd_path(name):
    delim = ';' if sys.platform == 'win32' else ':'
    suff = (
        ['.exe', '.cmd', '.ps1']
        if sys.platform == 'win32'
        else ['', '.sh']
    ) 
    for p in os.environ.get('PATH', '').split(delim):
        if any(path.isfile(path.join(p, name + s)) for s in suff):
            return p
    return ''