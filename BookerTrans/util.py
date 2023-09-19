import traceback
import sys
import os
import re
from os import path

RE_MD_PRE = r'^(\x20*)(`{3,})([\s\S]+?)^\1\2'

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
    
def ext_md_pre(md):
    pres = []
    def replace_func(g):
        pre = g.group(2) + g.group(3) + g.group(1) + g.group(2)
        pres.append(pre)
        rep = g.group(1) + f'[PRE{len(pres)-1}]'
        return rep
    md = re.sub(RE_MD_PRE, replace_func, md, flags=re.M)
    return md, pres

def rec_md_pre(md, pres):
    for i, pre in enumerate(pres):
        md = md.replace(f'[PRE{i}]', pre)
    return md