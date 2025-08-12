# auth.py
import streamlit as st
from user_manager import UserManager

def show_page():
    """로그인/회원가입 페이지"""
    st.title("🐦 프롬프트 트위터")
    st.markdown("**로그인이 필요합니다**")

    # 탭으로 로그인/회원가입 구분
    select_tab = st.radio("", ["🔑 로그인", "📝 회원가입"], horizontal=True)

    management = UserManager()
    login_fuc(select_tab, management)
    st.sidebar.metric("📊 총 가입자 수", management.get_user_count())

def login_fuc(select_tab, management):
    if(select_tab == "🔑 로그인"):
        login_or_signup = "로그인"
        login_or_signup_name = "login_username"
        login_or_signup_password = "login_password"
    elif(select_tab == "📝 회원가입"):
        login_or_signup = "회원가입"
        login_or_signup_name = "signup_username"
        login_or_signup_password = "signup_password"

    st.subheader(login_or_signup)
    
    username = st.text_input("사용자명", key=login_or_signup_name)
    password = st.text_input("비밀번호", type="password", key=login_or_signup_password)
    if(login_or_signup == "회원가입"):
        confirm_password = st.text_input("비밀번호 확인", type="password")       

    if st.button(login_or_signup, type="primary"):
        if login_or_signup == "로그인" and username and password:
            success, user_info = management.login_user(username, password)
            if success:
                # Session State에 로그인 정보 저장
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_info
                    st.success(f"✅ {username}님 환영합니다!")
                    st.rerun()
            else:
                    st.error("❌ 사용자명 또는 비밀번호가 틀렸습니다.")
        else:
            st.warning("⚠️ 모든 필드를 입력해주세요.")
        if username and password and confirm_password:
            if password == confirm_password:
                success, message = management.create_user(username, password)

                if success:
                    st.success("🎉 " + message)
                    st.info("💡 이제 로그인 탭에서 로그인해보세요!")
                else:
                    st.error("❌ " + message)
            else:
                st.error("❌ 비밀번호가 일치하지 않습니다.")
        else:
            st.warning("⚠️ 모든 필드를 입력해주세요.")
            
def signup_fuc(management):
    st.subheader("회원가입")

    new_username = st.text_input("사용자명", key="signup_username")
    new_password = st.text_input("비밀번호", type="password", key="signup_password")
    confirm_password = st.text_input("비밀번호 확인", type="password")

    if st.button("회원가입", type="primary"):
        



def logout_user():
    """로그아웃 처리"""
    st.session_state.logged_in = False
    if 'current_user' in st.session_state:
        del st.session_state.current_user
    st.rerun()

