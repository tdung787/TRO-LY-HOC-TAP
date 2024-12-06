import streamlit as st
import yaml
import hashlib
import os
import json
from src.global_settings import USERS_FILE
from src.conversation_engine import (
    create_new_chat_file
)

# cookie_password = os.getenv("COOKIE_PASSWORD", "12002")

# cookies = EncryptedCookieManager(prefix="aio_mental_health", password=str(cookie_password))

# if not cookies.ready():
#     st.stop()

def ensure_directory_exists():
    directory = os.path.dirname(USERS_FILE)
    if not os.path.exists(directory):
        os.makedirs(directory)

# Đảm bảo USERS_FILE tồn tại
def ensure_file_exists():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as file:
            yaml.safe_dump({"usernames": {}}, file)

# Đọc dữ liệu từ file YAML
def load_users():
    ensure_directory_exists()
    ensure_file_exists()
    with open(USERS_FILE, 'r') as file:
        users = yaml.safe_load(file)
    return users    

# Lưu người dùng vào file YAML
def save_users(users):
    ensure_directory_exists()
    with open(USERS_FILE, 'w') as file:
        yaml.safe_dump(users, file)

# Mã hóa mật khẩu
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Kiểm tra mật khẩu
def verify_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)

# def set_cookie_session(username, user_info):
#     cookies['username'] = username
#     cookies['user_info'] = user_info
#     cookies.save()

# def get_cookie_session():
#     username = cookies.get('username')
#     user_info = cookies.get('user_info')
#     if username:
#         st.session_state.username = username
#         st.session_state.logged_in = True
#         st.session_state.user_info = user_info

# def clear_cookie_session():
#     if "username" in cookies:
#         del cookies["username"]
#     if "user_info" in cookies:
#         del cookies["user_info"]
#     cookies.save()

def load_visit_count():
    """Load visit count from a JSON file."""
    file_path = "data/visit_count.json"
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump({"visit_count": 0}, file)
    with open(file_path, "r") as file:
        return json.load(file)["visit_count"]


def increment_visit_count():
    """Increment the visit count and save to a JSON file."""
    file_path = "data/visit_count.json"
    with open(file_path, "r") as file:
        data = json.load(file)
    data["visit_count"] += 1
    with open(file_path, "w") as file:
        json.dump(data, file)

# Giao diện đăng ký
def register():
    with st.form(key="register"):
        st.subheader('Register')
        username = st.text_input('Tên tài khoản')
        email = st.text_input('Email')
        name = st.text_input('Họ tên')
        age = st.number_input('Tuổi', min_value=5, max_value=100)
        gender = st.selectbox('Giới tính', ['Nam', 'Nữ', 'Khác'])
        job = st.text_input('Nghề nghiệp')
        address = st.text_input('Địa chỉ')
        password = st.text_input('Mật khẩu', type='password')
        confirm_password = st.text_input('Xác nhận mật khẩu', type='password')

        if st.form_submit_button('Đăng ký'):
            users = load_users()
            if len(users['usernames']) >= 10:
                st.error('Số lượng người dùng đã đạt giới hạn tối đa!')
            elif not username or not password:
                st.error('Bạn cần nhập tên tài khoản và mật khẩu!')
            elif password == confirm_password:
                if username in users['usernames']:
                    st.error('Tên tài khoản không hợp lệ!')
                else:
                    hashed_password = hash_password(password)
                    users['usernames'][username] = {
                        'email': email,
                        'name': name,
                        'age': age,
                        'gender': gender,
                        'job': job,
                        'address': address,
                        'password': hashed_password
                    }
                    save_users(users)
                    st.session_state.username = username
                    st.session_state.logged_in = True
                    st.session_state.user_info = f"username:{username}, "
                    for key, value in users['usernames'][username].items():
                        if key != 'password':
                            st.session_state.user_info += f"{key}:{value}, "
                    # set_cookie_session(username, st.session_state.user_info)
                    st.rerun()
            else:
                st.error('Mật khẩu không khớp!')

def login():
    with st.form(key="login"):
        st.subheader('Login')
        username = st.text_input('Tên đăng nhập')
        password = st.text_input('Mật khẩu', type='password')

        if st.form_submit_button('Đăng nhập'):
            users = load_users()
            if username in users['usernames']:
                stored_password = users['usernames'][username]['password']
                if verify_password(stored_password, password):
                    st.session_state.username = username
                    st.session_state.logged_in = True
                    increment_visit_count()
                    st.session_state.user_info = f"username:{username}, "
                    for key, value in users['usernames'][username].items():
                        if key != 'password':
                            st.session_state.user_info += f"{key}:{value}, "
                    # set_cookie_session(username, st.session_state.user_info)
                    st.rerun()
                else:
                    st.error('Mật khẩu không chính xác!')
            else:
                st.error('Tên đăng nhập không đúng!')

def guest_login():
    if st.button('Log in as Guest'):
        st.session_state.logged_in = True
        increment_visit_count()
        st.session_state.username = 'bạn'
        st.session_state.user_info = f"username:{st.session_state.username}, " + "Chưa cung cấp thông tin"
        # set_cookie_session(st.session_state.username, st.session_state.user_info)
        st.rerun()

def logout():
        # clear_cookie_session()
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_info = None
        st.rerun()

if __name__ == '__main__':
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        # get_cookie_session()

    if not st.session_state.logged_in:
        with st.expander('AIO MENTAL HEALTH', expanded=True):
            login_tab, create_tab = st.tabs(
                [
                    "Đăng nhập",
                    "Tạo tài khoản",
                ]
            )
            with create_tab:
                register()
            with login_tab:
                login()
    else:
        st.write(f"Welcome, {st.session_state.username}!")
        st.write(st.session_state.user_info)
