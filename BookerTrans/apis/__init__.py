from .ChatGptApi import ChatGptApi
from .ChatGLMApi import ChatGLMApi

apis = {
    'chatgpt': ChatGptApi,
    'chatglm': ChatGLMApi,
}