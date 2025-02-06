import os
import streamlit as st

def show_sidebar(username):
    if username:  # Kiểm tra xem người dùng đã đăng nhập hay chưa
        st.sidebar.markdown("### Lịch sử trò chuyện")
        
        # Thư mục chứa các tệp chat history
        cache_dir = "data/cache"
        
        # Lọc các tệp chat history chỉ thuộc về người dùng hiện tại
        chat_files = [f for f in os.listdir(cache_dir) if f.startswith(username) and f.endswith(".json")]
        
        if chat_files:  # Kiểm tra nếu có lịch sử trò chuyện
            for idx, file in enumerate(chat_files):
                # Dạng tệp: username_chatTitle_timestamp.json
                try:
                    parts = file.split("_")
                    chat_title = "_".join(parts[1:-1])  # Lấy phần giữa (bỏ username và timestamp)
                except IndexError:
                    chat_title = "Untitled Chat"
                
                # Thêm key duy nhất cho mỗi nút
                if st.sidebar.button(chat_title.strip(), key=f"chat_{idx}"):
                    st.session_state.selected_chat_file = os.path.join(cache_dir, file)
        else:
            st.sidebar.write("Không có lịch sử trò chuyện nào.")

def tutorial():
    st.sidebar.markdown('### 🧠 Trợ lý học tập AI')
    st.sidebar.markdown('***Hướng dẫn sử dụng:***')
    st.sidebar.markdown('1. 🟢 **Đăng nhập tài khoản để lưu lịch sử trò chuyện sau mỗi lần sử dụng.**')
    st.sidebar.markdown('2. 💬 **Sử dụng chức năng chat - "Nói chuyện với chuyên gia hỗ trợ học tập AI" để trình bày vướng mắc trong các môn học tự nhiên hay ngoại ngữ của bạn.**')
    st.sidebar.markdown('3. 📈 **Khi có đủ dữ liệu hoặc bạn kết thúc cuộc trò chuyện. Chuyên gia AI sẽ dựa vào thông tin người dùng khai báo, từ đó đưa ra giải pháp giải quyết bài toán.**')
    st.sidebar.markdown('4. 📊 **Lịch sử trò chuyện của bạn sẽ được lưu lại.**')

def main_tutorial():
    st.markdown('### 🧠Khám phá AI trợ lý học tập và giảng dạy môn Toán theo chương trình GDPT 2018 ###')
    st.markdown('***Hướng dẫn sử dụng giúp giáo viên và học sinh nâng cao hiệu quả học tập và giảng dạy:***')
    st.markdown('1. 🟢 **Cá nhân hóa: Đăng nhập để lưu lịch sử trò chuyện, giúp bạn dễ dàng theo dõi tiến trình học tập.**')
    st.markdown('2. 🍀 **Tương tác thông minh: Sử dụng chức năng chat để nhận hỗ trợ từ AI khi gặp khó khăn trong học tập hoặc giảng dạy Toán.**')
    st.markdown('3. 📊 **Phân tích và giải pháp: AI dựa vào thông tin bạn cung cấp để đưa ra các phương pháp giải quyết bài tập và vấn đề giảng dạy.**')
    st.markdown('4. 💾 **Lưu trữ tiện lợi: Lịch sử trò chuyện được lưu lại, giúp bạn dễ dàng ôn tập và xem lại nội dung quan trọng.**')



