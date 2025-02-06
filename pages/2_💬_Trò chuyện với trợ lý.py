import streamlit as st
import base64
from llama_index.llms.openai import OpenAI
import openai
from src.conversation_engine import (
    initialize_chatbot, chat_interface, load_chat_store, create_new_chat_file, save_chat_history,
)
from llama_index.core import Settings
import src.sidebar as sidebar

# Cài đặt mô hình OpenAI và khóa API
Settings.llm = OpenAI(model="gpt-4o", temperature=0.2)
openai.api_key = st.secrets.openai.OPENAI_API_KEY

hoc_bong = "data/images/hocbong.jpg"
xet_tuyen = "data/images/xettuyen.jpg"

link_hocbong = "https://tuyensinh.girc.edu.vn/"
link_xettuyen = "https://tuyensinh.tuaf.edu.vn/"

def get_base64_hocbong(hoc_bong):
    with open(hoc_bong, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
def get_base64_xettuyen(xet_tuyen):
    with open(xet_tuyen, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

hocbong_base64 = get_base64_hocbong(hoc_bong)
xettuyen_base64 = get_base64_xettuyen(xet_tuyen)

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""  # Đảm bảo có username khi người dùng đăng nhập

    username = st.session_state.username

    # Hiển thị sidebar và load tệp trò chuyện của người dùng
    sidebar.show_sidebar(username)

    # Khởi tạo các biến trạng thái cho lần đầu truy cập
    if 'conversation_file' not in st.session_state:
        st.session_state.conversation_file = create_new_chat_file() 
    if 'selected_chat_file' not in st.session_state:
        st.session_state.selected_chat_file = False
    if 'has_chatted' not in st.session_state:
        st.session_state.has_chatted = False 

    # Kiểm tra nếu đã chọn tệp chat từ sidebar
    if st.session_state.selected_chat_file:
        # Nếu có, thay đổi tệp trò chuyện hiện tại
        st.session_state.conversation_file = st.session_state.selected_chat_file
        chat_store = load_chat_store(st.session_state.selected_chat_file)
        st.session_state.has_chatted = True
    else:
        # Nếu chưa chọn tệp nào, sử dụng tệp mới
        chat_store = load_chat_store(st.session_state.conversation_file)

    if st.session_state.logged_in:
        user_info = st.session_state.user_info
        st.header("💬 AI trợ lý học tập và giảng dạy môn Toán")

        # Tạo hoặc tải chat_store
        col1, col2, col3 = st.columns([1.5, 2, 1.5])
        with col1:
            st.markdown(
                f'<a href="{link_hocbong}" target="_blank">'
                f'<img src="data:image/png;base64,{hocbong_base64}" width="300">'
                '</a>',
                unsafe_allow_html=True
            )

            with col2:
                container = st.container()
                # Khởi tạo chatbot và bắt đầu giao diện trò chuyện
                agent = initialize_chatbot(chat_store, container, username, user_info)
                
                # Cập nhật trạng thái nếu có chat
                if chat_interface(agent, chat_store, container, st.session_state.conversation_file):
                    st.session_state.has_chatted = True  # Đánh dấu đã có chat
                    save_chat_history(chat_store, st.session_state.conversation_file, st.session_state.username)

                # Chỉ hiển thị nút "Kết thúc cuộc trò chuyện" khi đã có ít nhất một tin nhắn
                if st.session_state.has_chatted:
                    if st.button("Tạo cuộc trò chuyện mới"):
                        save_chat_history(chat_store, st.session_state.conversation_file, username)
                        st.session_state.conversation_file = create_new_chat_file()
                        st.session_state.selected_chat_file = False
                        st.session_state.has_chatted = False
                        st.rerun()
            with col3:
                st.markdown(
                    f'<a href="{link_xettuyen}" target="_blank">'
                    f'<img src="data:image/png;base64,{xettuyen_base64}" width="300">'
                    '</a>',
                    unsafe_allow_html=True
                )
                
    else:
        st.markdown('### Đăng nhập để sử dụng tính năng này')

if __name__ == "__main__":
    main()
