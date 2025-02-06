import streamlit as st
from src.authenticate import login, register, guest_login, logout, load_visit_count
import src.sidebar as sidebar

def main():
    # username = st.session_state.username
    
    # sidebar.tutorial()

    # Phần còn lại của mã Streamlit
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
            st.sidebar.markdown('***Hãy đăng nhập để sử dụng các tính năng này nhé!***')
            with st.expander('AI TRỢ LÝ HỌC TẬP', expanded=True):
                login_tab, create_tab, guest_tab = st.tabs(["Đăng nhập", "Tạo tài khoản", "Khách"])
                with create_tab:
                    register()
                with login_tab:
                    login()
                with guest_tab:
                    guest_login()
    else:
        sidebar.main_tutorial()
        col1, col2, col3 = st.columns(3)
        with col1:  
            if st.button("💬 Trò chuyện với trợ lý"):
                    st.switch_page("pages/2_💬_Trò chuyện với trợ lý.py")
        with col2:
            if st.button("📊 Thông tin sức khỏe"):
                    st.switch_page("pages/1_ 📈_Thông tin sức khỏe.py")       
        with col3:
                # st.session_state.conversation_file = create_new_chat_file(username)
            if st.button('🔴 Đăng xuất'):
                logout()
        st.success(f'Chào mừng {st.session_state.username}, Hãy bắt đầu trải nghiệm trợ lý AI và khám phá tiềm năng học tập đột phá ngay hôm nay!', icon="🎉")

        visit_count = load_visit_count()
        st.sidebar.info(f"👥 Tổng lượt truy cập: {visit_count}")

if __name__ == "__main__":
    main()
