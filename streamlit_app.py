import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

#   - st.set_page_config() — 配置网页基本信息
#   - page_title — 浏览器标签页显示的标题
#   - page_icon — 标签页的小图标（emoji）
#   - 注意：这行必须是第一个 Streamlit 命令，放后面会报错
st.set_page_config(
    page_title="我的 Chatbot",
    page_icon="🤖"
)

# 初始化会话状态
# session_state 是 Streamlit 的"记忆"，页面刷新前数据不会丢失
if "messages" not in st.session_state: #只有第一次访问时才初始化，避免覆盖已有数据
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

def get_ai_response(prompt, model):
    """
    调用 API 获取回复
    参数:
        prompt: 用户输入（当前没用到，但留着以后扩展）
        model: 选择的模型
    返回:
        str: AI 的回复
    """
    # 创建客户端
    client = OpenAI(
        api_key=st.secrets["CODINGPLAN_API_KEY"],
        base_url=st.secrets["CODINGPLAN_BASE_URL"]
    )
    # 调用 API
    response = client.chat.completions.create(
        model=model,
        messages=st.session_state.messages
    )
    # 返回回复内容
    return response.choices[0].message.content

# 侧边栏
with st.sidebar:
    st.title("⚙️ 设置")
    # 模型选择下拉框
    model = st.selectbox(
        "选择模型",
        ["GLM-5","gpt-3.5-turbo"],
        index=0
    )
    # 清空对话按钮
    if st.button("清空对话"):
        st.session_state.messages = []
        st.session_state.total_tokens = 0
        st.rerun()  # 重新运行页面，刷新显示

#   - st.title() — 大标题，显示在页面中央
#   - st.chat_message() — 聊天气泡组件，role="user" 显示用户样式，role="assistant"
#   显示 AI 样式
#   - st.markdown() — 显示文本内容（支持 Markdown 格式）
#   - 循环遍历 messages，把历史对话一条条显示出来      

# 主界面标题
st.title("🤖 AI Chatbot")
# 显示历史消息
for message in st.session_state.messages:
    # 根据角色显示不同样式的消息气泡
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入框
if prompt := st.chat_input("说点什么..."):
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)        
    # 保存用户消息到历史
    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })
    # 获取 AI 回复
    with st.chat_message("assistant"):
        # 创建一个加载动画    
        with st.spinner("思考中..."):
            response = get_ai_response(prompt,model)
            st.markdown(response)
    # 保存 AI 回复到历史    
    st.session_state.messages.append({
        "role":"assistant",
        "content":response
    })




