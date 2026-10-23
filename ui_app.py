import gradio as gr
import requests
import json


# 这个函数负责把你的话发给 FastAPI 后端，并把流式结果拿回来
def chat_with_agent(message, history):
    url = "http://127.0.0.1:8000/chat/"
    payload = {"message": message}

    # 开启流式请求
    response = requests.post(url, json=payload, stream=True)

    # 收集碎片
    partial_message = ""
    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        if chunk:
            partial_message += chunk
            yield partial_message  # 交给 Gradio 渲染


# 极简的前端 UI
demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="我的赛博导师",
    description="基于 FastAPI + DeepSeek 的 AI 规划助手"
)

if __name__ == "__main__":
    demo.launch()