from ..util import *
import re
import subprocess as subp

class ChatGLMApi():

    def __init__(self, args):
        self.glm_path = find_cmd_path('chatglm')
        if not self.glm_path:
            raise RuntimeError('未找到 chatglm.cpp，请下载并将目录添加到 $PATH')
        self.model_path = args.model
        if re.search(r'^[\w\-]+$', self.model_path):
            self.model_path = path.join(self.glm_path, 'models', self.model_path + '.bin')
        self.prompt = args.prompt
        self.limit = args.limit

    def translate(self, text, src='', dst=''):
        assert len(text) <= self.limit - len(self.prompt)
        cmd = [
            'chatglm', '-m', self.model_path,
            '-p', self.prompt + text,
        ]
        print(f'cmd: {cmd}')
        res = subp.Popen(
            cmd, 
            stdout=subp.PIPE, 
            stderr=subp.PIPE,
            shell=True,
        ).communicate()[0].decode('utf8')
        if not res:
            raise('chatglm 调用失败，未返回任务内容')
        return res