import gradio as gr
import requests
import uuid

# 生成一个随机的用户ID（取前8位）
my_user_id = str(uuid.uuid4())[:8]

def chat_with_agent(message, history):
    url = "http://127.0.0.1:8000/chat/"
    payload = {
        "user_id": my_user_id,  # <--- 传给后端
        "message": message
    }
    response = requests.post(url, json=payload, stream=True)
    partial_message = ""
    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
        if chunk:
            partial_message += chunk
            yield partial_message

demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="我的赛博导师",
    description=f"当前用户唯一识别码: {my_user_id}" # 把ID显示在页面上
)
demo.launch()