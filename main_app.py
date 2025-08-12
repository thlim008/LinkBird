# app.py (완전히 새로운 버전)
import streamlit as st
from auth import show_auth_page, logout_user
from user_manager import UserManager

# 페이지 설정
st.set_page_config(
    page_title="프롬프트 트위터",
    page_icon="🐦",
    layout="wide"
)

# Session State 초기화 (새 접속시 자동 로그아웃)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 로그인 체크
if not st.session_state.logged_in:
    # 로그인하지 않은 경우
    show_auth_page()

else:
    # 로그인한 경우 - 메인 앱
    current_user = st.session_state.current_user

    # 헤더
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🐦 프롬프트 트위터")
        st.markdown(f"**{current_user['username']}님 환영합니다!** ✨")
    with col2:
        if st.button("🚪 로그아웃"):
            logout_user()

    # 사이드바 메뉴
    st.sidebar.title("📋 메뉴")
    st.sidebar.markdown(f"👤 **{current_user['username']}**")
    st.sidebar.markdown(f"🆔 {current_user['user_id']}")

    menu = st.sidebar.selectbox(
        "페이지 선택",
        ["🏠 홈", "✍️ 글쓰기", "👤 프로필", "📊 데이터 확인"]
    )

    # 메인 콘텐츠
    if menu == "🏠 홈":
        st.header("📝 최근 프롬프트")

        # 샘플 게시글 (3단계에서 실제 데이터로 교체)
        st.info("💡 3단계에서 실제 게시글 기능이 구현됩니다!")

        with st.container():
            col1, col2 = st.columns([1, 10])
            with col1:
                st.image("https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=50&h=50&fit=crop&crop=face", width=50)
            with col2:
                st.markdown(f"**{current_user['username']}** • 방금 전")
                st.markdown("로그인 시스템이 완성되었습니다! 🎉")
                st.button("❤️ 0", key="sample_like")

    elif menu == "✍️ 글쓰기":
        st.header("✍️ 새 프롬프트 작성")
        st.info("💡 3단계에서 실제 글쓰기 기능이 구현됩니다!")

        content = st.text_area("프롬프트 내용", height=150)
        if st.button("게시하기", type="primary"):
            if content:
                st.success("3단계에서 실제 저장 기능이 추가됩니다! 🎉")
            else:
                st.error("내용을 입력해주세요.")

    elif menu == "👤 프로필":
        st.header("👤 내 프로필")

        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face", width=100)

        with col2:
            st.markdown(f"### {current_user['username']}")
            st.markdown(f"**사용자 ID:** {current_user['user_id']}")
            st.markdown(f"**가입일:** {current_user['created_at']}")

        st.divider()

        # 활동 통계 (더미 데이터)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("작성한 글", "0")
        with col2:
            st.metric("받은 좋아요", "0")
        with col3:
            st.metric("활동일", "1")

    elif menu == "📊 데이터 확인":
        st.header("📊 저장된 데이터 확인")

        user_mgr = UserManager()
        users_df = user_mgr.load_users()

        st.subheader("👥 사용자 목록")

        if len(users_df) > 0:
            # 비밀번호 숨기기
            display_df = users_df.copy()
            display_df['password'] = '***'
            st.dataframe(display_df, use_container_width=True)

            # 간단한 통계
            col1, col2 = st.columns(2)
            with col1:
                st.metric("총 사용자 수", len(users_df))
            with col2:
                today_users = len(users_df[users_df['created_at'] == current_user['created_at']])
                st.metric("오늘 가입자", today_users)
        else:
            st.warning("등록된 사용자가 없습니다.")

