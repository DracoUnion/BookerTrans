import re
from os import path
import yaml
import json
import os

PREF_IND = r'\x20{2}'
PREF_OL = r'\d+\.\x20{2}'
PREF_UL = r'[\*\+\-]\x20'
PREF_H1 = r'#\x20+'
PREF_H2 = r'#{2}\x20+'
PREF_H3 = r'#{3}\x20+'
PREF_H4 = r'#{4}\x20+'
PREF_H5 = r'#{5}\x20+'
PREF_H6 = r'#{6}\x20+'
PREF_BQ = r'>\x20'
TYPE_TB = r'^\|\x20.*?\x20\|$'
TYPE_PRE = r'^\[PRE\d+\]$'
TYPE_IMG = r'^!\[.*?\]\(.*?\)$'

PREF_MAP = {
    'PREF_IND': PREF_IND, 
    'PREF_OL': PREF_OL, 
    'PREF_UL': PREF_UL, 
    'PREF_H1': PREF_H1, 
    'PREF_H2': PREF_H2, 
    'PREF_H3': PREF_H3, 
    'PREF_H4': PREF_H4, 
    'PREF_H5': PREF_H5, 
    'PREF_H6': PREF_H6, 
    'PREF_BQ': PREF_BQ
}

TYPE_MAP = {
    'TYPE_TB': TYPE_TB,
    'TYPE_PRE': TYPE_PRE,
    'TYPE_IMG': TYPE_IMG,
}


RE_PRE = r'(`{3,})[\s\S]+?\1'

def match_one_pref(line):
    for tp, rgx in PREF_MAP.items():
        # print(tp, rgx, line)
        m = re.search('^' + rgx, line, re.M)
        if not m: continue
        l = len(m.group())
        line = line[l:]
        return tp, line
    return None, line
        
def match_type(line):
    for tp, rgx in TYPE_MAP.items():
        m = re.search(rgx, line)
        if m: return tp
    return 'TYPE_NORMAL'
        

def parse_block(line):
    prefs = []
    while True:
        pref, line = match_one_pref(line)
        if not pref: break
        prefs.append(pref)
    line = line.strip()
    return {
        'prefs': prefs,
        'line': line,
        'type': match_type(line)
    }

def md2blocks(md):
    lines = md.replace('\t', '\x20' * 4).split('\n')
    lines = [l.strip() for l in lines]
    lines = list(filter(None, lines))
    
    res = [parse_block(l) for l in lines]
    return res
    
def match_block(b1, b2):
    return b1['prefs'] == b2['prefs'] and \
           b1['type'] == b2['type']
    
def find_next_pref(r, st, b):
    for i in range(st, len(r)):
        if match_block(r[i], b):
            return i
    return len(r)
    
def make_align(md1, md2):
    r1, r2 = md2blocks(md1), md2blocks(md2)
    idx1, idx2 = 0, 0
    res = []
    while idx1 < len(r1) and idx2 < len(r2):
        b1, b2 = r1[idx1], r2[idx2]
        if match_block(b1, b2):
            res.append(b1 | b2)
            idx1 += 1
            idx2 += 1
            continue
        idx1n = find_next_pref(r1, idx1 + 1, b2)
        idx2n = find_next_pref(r2, idx2 + 1, b1)
        if idx1n - idx1 < idx2n - idx2:
            while idx1 < idx1n:
                res.append(r1['idx1'] | {'zh': ''})
                idx1 += 1
        else:
            while idx2 < idx2n:
                res.append(r2[idx2] | {'en': ''})
                idx2 += 1
            
    while idx1 < len(r1):
        res.append(r1['idx1'] | {'zh': ''})
        idx1 += 1
    while idx2 < len(r2):
        res.append(r2[idx2] | {'en': ''})
        idx2 += 1
    return res
    
    
def align_handler(args):
    fname1 = args.en
    fname2 = args.zh
    if not fname1.endswith('.md') or \
       not fname2.endswith('.md'):
       raise ValueError('请提供两个 MD 文件！')
    md1 = open(fname1, encoding='utf8').read()
    md2 = open(fname2, encoding='utf8').read()
    res = make_align(md1, md2)
    ofname = path.basename(fname1) + '_' + path.basename(fname2) + '.yaml'
    open(ofname, 'w', encoding='utf8').write(
        yaml.safe_dump(res, allow_unicode=True))
    
def align_dir_handler(args):
    dir1 = args.en
    dir2 = args.zh
    if not path.isdir(dir1) or \
        not path.isdir(dir2):
        raise ValueError('请提供两个目录！')
    fnames = [f for f in os.listdir(dir1) if f.endswith('.md')]
    for f in fnames:
        fen = path.join(dir1, f)
        fzh = path.join(dir2, f)
        if not path.isfile(fzh):
            continue
        args.en = fen
        args.zh = fzh
        align_handler(args)


def make_totrans_handler(args):
    fname = args.fname
    if not fname.endswith('.md'):
       raise ValueError('请提供 MD 文件！')
    md = open(fname, encoding='utf8').read()
    res = md2blocks(md)
    res = [{
        'en': r['line'], 
        'prefs': r['prefs'],
    } for r in res]
    ofname = re.sub(r'\.\w+$', '', fname) + '.yaml'
    open(ofname, 'w', encoding='utf8').write(
        yaml.safe_dump(res, allow_unicode=True))



