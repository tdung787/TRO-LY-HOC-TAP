import os
import json
from datetime import datetime
import streamlit as st
import re
from pydantic import ValidationError
from llama_index.core import load_index_from_storage
from llama_index.core import StorageContext
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.tools import FunctionTool, ToolMetadata
from src.global_settings import INDEX_STORAGE, SCORES_FILE
from src.prompts import CUSTORM_AGENT_SYSTEM_TEMPLATE

user_avatar = "data/images/user.png"
firefox_avatar = "data/images/firefox.png"

def generate_chat_title(messages):
    """
    Tạo tiêu đề từ câu hỏi mới nhất của người dùng trong cuộc trò chuyện.
    """
    keywords = []

    # Lấy tin nhắn mới nhất từ người dùng
    if messages:
        for msg in reversed(messages):  # Duyệt ngược để tìm tin nhắn cuối cùng của người dùng
            if msg["role"] == "user":
                keywords = re.findall(r'\b\w+\b', msg["content"])[:8]
                break

    # Kết hợp các từ khóa thành tiêu đề
    title = " ".join(keywords).strip()
    title = re.sub(r'[<>:"/\\|?*]', '', title)  # Loại bỏ các ký tự không hợp lệ

    # Trả về tiêu đề hoặc tên mặc định
    return title[:50] if title else "Chat_History"


def save_chat_history(chat_store, conversation_file, username=None):
    """Lưu toàn bộ nội dung chat store vào tệp JSON với định dạng gốc và đổi tên tệp hiện tại."""
    chat_data = chat_store.dict()
    user_messages = chat_data.get("store", {}).get(username, [])
    if not user_messages:
        print("Không tìm thấy tin nhắn của người dùng.")
        return

    # Lấy timestamp và tạo tiêu đề
    timestamp = datetime.now().strftime("%H%M%S")
    chat_title = generate_chat_title(user_messages)

    # Tạo tên tệp mới với định dạng username_chatTitle_timestamp.json
    new_conversation_file = f"data/cache/{username}_{chat_title}_{timestamp}.json"

    # Lưu toàn bộ nội dung vào tệp đã được đổi tên với định dạng gốc
    with open(new_conversation_file, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=4, ensure_ascii=False)

    # Xóa tệp cũ nếu cần
    if os.path.exists(conversation_file) and conversation_file != new_conversation_file:
        os.remove(conversation_file)

    st.session_state.conversation_file = new_conversation_file


def load_chat_store(conversation_file):
    """Load hoặc tạo mới một chat store dựa trên tệp đã cung cấp."""
    chat_store = SimpleChatStore()

    if os.path.exists(conversation_file) and os.path.getsize(conversation_file) > 0:
        try:
            # Đọc dữ liệu từ tệp JSON trước để xác nhận định dạng
            with open(conversation_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Kiểm tra nếu dữ liệu là một từ điển hợp lệ
            if isinstance(data, dict):
                chat_store = SimpleChatStore.from_persist_path(conversation_file)
            else:
                # Nếu dữ liệu không hợp lệ, tạo một SimpleChatStore trống
                chat_store = SimpleChatStore()
        except (json.JSONDecodeError, ValidationError):
            # Nếu có lỗi trong khi đọc JSON, tạo một SimpleChatStore trống
            chat_store = SimpleChatStore()
        
    return chat_store


def display_messages(chat_store, container, key):
    """Hiển thị các tin nhắn hiện có trong `chat_store`."""
    with container:
        for message in chat_store.get_messages(key=key):
            if message.role == "user":
                with st.chat_message(message.role, avatar=user_avatar):
                    st.markdown(message.content)
            elif message.role == "assistant" and message.content is not None:
                with st.chat_message(message.role, avatar=firefox_avatar):
                    st.markdown(message.content)

def create_new_chat_file():
    """Tạo tên tệp mới mà không có tên người dùng ngay lập tức."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/cache/Chat_History_{timestamp}.json"  # Không có username
    return filename

def get_date_time():
    """
    Trả về thời gian hiện tại dưới dạng chuỗi định dạng "YYYY-MM-DD HH:MM:SS".
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_score(score, content, total_guess, username):
        """Write score and content to a file.
        Args:
            score (string): Score of the user's mental health.
            content (string): Content of the user's mental health.
            total_guess (string): Total guess of the user's mental health.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {
            "username": username,
            "Time": current_time,
            "Score": score,
            "Content": content,
            "Total guess": total_guess
        }
        # Đọc dữ liệu từ file nếu tồn tại
        try:
            with open(SCORES_FILE, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        
        # Thêm dữ liệu mới vào danh sách
        data.append(new_entry)
        
        # Ghi dữ liệu trở lại file
        with open(SCORES_FILE, "w") as f:
            json.dump(data, f, indent=4)

def initialize_chatbot(chat_store, container, username, user_info):
    """Khởi tạo chatbot với bộ nhớ và công cụ cần thiết."""
    memory = ChatMemoryBuffer.from_defaults(
        token_limit=3000, 
        chat_store=chat_store, 
        chat_store_key=username
    )  
    storage_context = StorageContext.from_defaults(
        persist_dir=INDEX_STORAGE
    )
    index = load_index_from_storage(
        storage_context, index_id="vector"
    )
    query_engine = index.as_query_engine(
        similarity_top_k=1,
    )
    query_tool = QueryEngineTool(
        query_engine=query_engine, 
        metadata=ToolMetadata(
            name="query",
            description=(
                "Cung cấp các câu hỏi và câu trả lời hay đáp án của môn sinh học."
            ),
        )
    )
    save_tool = FunctionTool.from_defaults(fn=save_score)
    get_date_time_tool = FunctionTool.from_defaults(fn=get_date_time)
    agent = OpenAIAgent.from_tools(
        tools=[get_date_time_tool, query_tool], 
        memory=memory,
        system_prompt=CUSTORM_AGENT_SYSTEM_TEMPLATE.format(user_info=user_info)
    )
    display_messages(chat_store, container, key=username)
    return agent

def chat_interface(agent, chat_store, container, conversation_file):  
    """Quản lý giao diện trò chuyện và lưu lại khi kết thúc."""
    if not os.path.exists(conversation_file) or os.path.getsize(conversation_file) == 0:
        with container:
            with st.chat_message(name="assistant", avatar=firefox_avatar):
                st.markdown("Hãy hỏi Trợ lý sẽ cho biết Trợ lý AI này hỗ trợ giáo viên và học sinh những gì nhé!")

    prompt = st.chat_input("Chat với AI...")
    if prompt:
        # Người dùng đã gửi tin nhắn, trả về True để cập nhật trạng thái
        with container:
            with st.chat_message(name="user", avatar=user_avatar):
                st.markdown(prompt)
            response = str(agent.chat(prompt))
            with st.chat_message(name="assistant", avatar=firefox_avatar):
                st.markdown(response)
        # Lưu cuộc trò chuyện vào tệp
        chat_store.persist(conversation_file)

        return True  # Trả về True khi có tin nhắn được gửi
    return False  # Trả về False nếu không có tin nhắn nào được gửi