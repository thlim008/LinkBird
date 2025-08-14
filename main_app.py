# main_app.py
import streamlit as st
import html
from auth import show_page, logout_user, post_fuc, show_post, show_following_posts, show_liked_posts, show_retweeted_posts, show_notifications, show_notification_settings
from user_manager import UserManager
from hotplace_auth import show_hotplace_map, show_add_hotplace
# 🔥 이 부분을 추가하세요
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="프롬프트 트위터", page_icon="🐦", layout="wide")

# 초기 세션
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 비로그인: 로그인/회원가입 페이지
if not st.session_state.logged_in:
    show_page()
else:
    # 로그인된 상태
    current_user = st.session_state.get("current_user", {})
    user_id = current_user.get("user_id", "")
    username = current_user.get("username", "")

    # 헤더
    left, center, right = st.columns([2, 1, 1])
    with left:
        st.title("🐦 프롬프트 트위터")
        st.markdown(f"**{username}님 환영합니다!**")

    with center:
        # 알림 카운터
        um = UserManager()
        unread_count = um.get_unread_count(user_id)
        if unread_count > 0:
            st.markdown(f"### 🔔 알림 {unread_count}개")
        else:
            st.markdown("### 🔔 알림")

    with right:
        if st.button("🚪 로그아웃"):
            logout_user()

    # 사이드바
    st.sidebar.title("📋 메뉴")
    st.sidebar.markdown(f"👤 **{username}**")
    st.sidebar.markdown(f"🆔 {user_id}")

    # 인기 해시태그 표시
    st.sidebar.markdown("### 🔥 인기 해시태그")
    try:
        um = UserManager()
        popular_hashtags = um.get_popular_hashtags(limit=10)
        if popular_hashtags:
            for tag, count in popular_hashtags:
                st.sidebar.markdown(f"#{tag} ({count})")
        else:
            st.sidebar.caption("아직 해시태그가 없습니다.")
    except Exception:
        st.sidebar.caption("해시태그 로딩 중...")

    menu = st.sidebar.selectbox(
    "페이지 선택",
    ["🏠 홈", "✍️ 게시물 작성", "👥 팔로잉 피드", "👍 좋아요 목록", "🔁 리트윗 목록", "🔔 알림", "⚙️ 알림 설정",  "🗺️ 핫플레이스 맵", "📍 핫플레이스 등록", "👤 프로필","📊 데이터 확인"]
    )

    # --- 라우팅 ---
    if menu == "🏠 홈":
        show_post()

    elif menu == "✍️ 게시물 작성":
        post_fuc()

    elif menu == "👍 좋아요 목록":
        show_liked_posts()

    elif menu == "🔁 리트윗 목록":
        show_retweeted_posts()
    
    # 라우팅 부분에 추가
    elif menu == "👥 팔로잉 피드":
        show_following_posts()
    elif menu == "🔔 알림":
        show_notifications()

    elif menu == "⚙️ 알림 설정":
        show_notification_settings()    
        
    elif menu == "🗺️ 핫플레이스 맵":
        show_hotplace_map()

    elif menu == "📍 핫플레이스 등록":
        show_add_hotplace()

    elif menu == "👤 프로필":
        st.header("👤 내 프로필")
        um = UserManager()

        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face", width=100)
        with col2:
            st.markdown(f"### {username}")
            st.markdown(f"**사용자 ID:** {user_id}")
            st.markdown(f"**가입일:** {current_user.get('created_at','-')}")

        st.divider()
        post_count = um.count_user_posts(user_id)
        like_recv  = um.count_received_likes(user_id)  
        following  = um.count_following(user_id)
        followers  = um.count_followers(user_id)

        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("작성 글 수", post_count)
        with m2: st.metric("받은 좋아요", like_recv)
        with m3: st.metric("팔로잉", following)
        with m4: st.metric("팔로워", followers)
    
    elif menu == "📊 데이터 확인":
        st.header("📊 저장 데이터 (CSV)")
        um = UserManager()

        st.subheader("👥 사용자")
        users = um.load_users().copy()
        if not users.empty:
            users_disp = users.copy()
            if "password" in users_disp.columns:
                users_disp["password"] = "***"
            st.dataframe(users_disp, use_container_width=True)
            st.caption(f"총 사용자: {len(users)}")
        else:
            st.info("사용자가 없습니다.")

        st.subheader("📝 게시물")
        st.dataframe(um.load_posts(), use_container_width=True)

        st.subheader("👍 게시물 좋아요")
        st.dataframe(um.load_likes(), use_container_width=True)

        st.subheader("🔁 리트윗")
        st.dataframe(um.load_retweets(), use_container_width=True)

        st.subheader("👥 팔로우")
        st.dataframe(um.load_follows(), use_container_width=True)

        st.subheader("💬 댓글")
        st.dataframe(um.load_comments(), use_container_width=True)

        st.subheader("👍 댓글 좋아요")
        st.dataframe(um.load_comment_likes(), use_container_width=True)

        st.subheader("🏷️ 해시태그")
        st.dataframe(um.load_hashtags(), use_container_width=True)
