import openai
import os

class ChatGptApi():
    def __init__(self):
        self.key = os.environ.get('OPENAI_API_KEY', '')
        self.prompt = '请把以下文本翻译成中文，不要保留原文：'
        self.retry = 10
        self.temperature = 0.5
        self.max_tokens = 4000
        self.model = 'text-davinci-003'
        
    def _get_proxy(self):
        return openai.proxy
        
    def _set_proxy(self, pr)
        openai.proxy = pr
        
    proxy = property(_get_proxy, _set_proxy)
        
    def translate(text):
        ipt = self.prompt + text
        assert len(ipt) <= 3096
        for i in range(self.retry):
            try: 
                r = openai.Completion.create(
                    engine=self.model,
                    prompt=ipt,
                    max_tokens=self.max_tokens - len(ipt),
                    temperature=self.temperature,
                )
                if hasattr(r, 'choices'): break
                raise ValueError(f'OpenAI API 调用失败：{r}')
            except Exception as ex: 
                if i == self.retry - 1: raise ex
        return r.choices[0].text