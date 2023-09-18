import openai
import os

class ChatGptApi():
    def __init__(self, args):
        self.key = None
        self.prompt = '请把以下文本翻译成中文，不要保留原文：'
        self.retry = 10
        self.temperature = 0.5
        self.max_tokens = 4000
        self.model = 'text-davinci-003'
        
    def _get_api_key(self):
        return self._key
        
    def _set_api_key(self, key):
        self._key = key or os.environ.get('OPENAI_API_KEY', '')
        
    key = property(_get_api_key, _set_api_key)
        
    def _get_proxy(self):
        return openai.proxy
        
    def _set_proxy(self, pr):
        openai.proxy = pr
        
    proxy = property(_get_proxy, _set_proxy)
        
    def translate(self, text, src='', dst=''):
        ipt = self.prompt + text
        assert len(ipt) <= 3096
        try: 
            r = openai.Completion.create(
                engine=self.model,
                prompt=ipt,
                max_tokens=self.max_tokens - len(ipt),
                temperature=self.temperature,
            )
        except Exception as ex: 
            raise ex
        if hasattr(r, 'choices'): 
            return r.choices[0].text
        else:
            raise ValueError(f'OpenAI API 调用失败：{r}')