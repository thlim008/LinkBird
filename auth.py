# auth.py
import streamlit as st
import html
import pandas as pd
from user_manager import UserManager

def show_page():
    """로그인/회원가입 페이지 (탭 UI)"""
    st.title("🐦 LinkBird")
    tab_login, tab_signup = st.tabs(["🔑 로그인", "📝 회원가입"])
    manager = UserManager()

    with tab_login:
        _login_ui(manager)

    with tab_signup:
        _signup_ui(manager)

    # 사이드바에 가입자 수
    try:
        st.sidebar.metric("총 가입자", manager.get_user_count())
    except Exception:
        pass


def _login_ui(manager: UserManager):
    st.subheader("로그인")
    username = st.text_input("아이디", key="login_username")
    password = st.text_input("비밀번호", type="password", key="login_password")
    if st.button("로그인", type="primary", key="btn_login"):
        if not username or not password:
            st.warning("모든 필드를 입력하세요.")
            return
        success, user_info = manager.login_user(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.current_user = user_info
            st.success(f"✅ {username}님 환영합니다!")
            st.rerun()
        else:
            st.error("❌ 아이디 또는 비밀번호가 틀렸습니다.")


def _signup_ui(manager: UserManager):
    st.subheader("회원가입")
    username = st.text_input("아이디", key="signup_username")
    pw1 = st.text_input("비밀번호", type="password", key="signup_pw1")
    pw2 = st.text_input("비밀번호 확인", type="password", key="signup_pw2")
    if st.button("회원가입", type="primary", key="btn_signup"):
        if not username or not pw1 or not pw2:
            st.warning("모든 필드를 입력하세요.")
            return
        if pw1 != pw2:
            st.error("비밀번호가 일치하지 않습니다.")
            return
        ok, msg = manager.create_user(username, pw1)
        if ok:
            st.success(msg + " 이제 로그인 해주세요.")
        else:
            st.error(msg)


def logout_user():
    """로그아웃 처리"""
    st.session_state.logged_in = False
    if "current_user" in st.session_state:
        del st.session_state["current_user"]
    st.success("로그아웃 완료!")
    st.rerun()


# auth.py의 post_fuc() 함수 수정 버전

def post_fuc():
    """게시물 작성 폼 (기존 이름 유지)"""
    st.subheader("✍️ 새 게시물 작성")
    manager = UserManager()
    
    # 성공 메시지 표시 (세션 상태 기반)
    if st.session_state.get("post_success", False):
        st.success("🎉 게시물이 작성되었습니다!")
        st.session_state.post_success = False  # 메시지 표시 후 플래그 리셋
    
    # 해시태그 사용법 안내
    st.info("💡 팁: 제목이나 내용에 #해시태그를 포함하면 자동으로 태그가 생성됩니다!")
    
    title = st.text_input("제목", key="post_title", placeholder="예: #멋쟁이사자")
    content = st.text_area("내용", height=150, key="post_content", placeholder="내용을 입력하세요... #AI #ChatGPT")
    
    # 실시간 해시태그 미리보기
    if title or content:
        hashtags_title = manager.extract_hashtags(title or "")
        hashtags_content = manager.extract_hashtags(content or "")
        all_hashtags = list(set(hashtags_title + hashtags_content))
        
        if all_hashtags:
            st.caption(f"🏷️ 감지된 해시태그: {', '.join(['#' + tag for tag in all_hashtags])}")
    
    if st.button("게시하기", type="primary", key="btn_post"):
        if not st.session_state.get("logged_in", False):
            st.warning("로그인이 필요합니다.")
            return
        if not title or not content:
            st.warning("제목과 내용을 입력하세요.")
            return
        user_id = st.session_state["current_user"]["user_id"]
        ok, msg = manager.create_post(user_id, title, content)
        if ok:
            # 성공 플래그 설정하고 입력 필드 초기화
            st.session_state.post_success = True
            # 입력 필드 초기화를 위해 키 변경
            if "post_title" in st.session_state:
                del st.session_state["post_title"]
            if "post_content" in st.session_state:
                del st.session_state["post_content"]
            st.rerun()
        else:
            st.error("등록 실패")


def _display_posts(posts_df, current_uid, manager, page_type):
    """게시물을 표시하는 공통 함수"""
    # ===== 검색 필터 =====
    with st.expander("🔍 고급 검색"):
        col1, col2 = st.columns(2)
        with col1:
            search_title = st.text_input("제목 검색", key=f"{page_type}_search_title")
            search_content = st.text_input("내용 검색", key=f"{page_type}_search_content")
        with col2:
            search_author = st.text_input("작성자 검색", key=f"{page_type}_search_author")
            search_hashtag = st.text_input("해시태그 검색 (# 없이 입력)", placeholder="예: AI, ChatGPT", key=f"{page_type}_search_hashtag")

    # 필터 적용
    filtered_df = posts_df.copy()
    
    if search_title:
        filtered_df = filtered_df[filtered_df["title"].str.contains(search_title, case=False, na=False)]
    if search_content:
        filtered_df = filtered_df[filtered_df["content"].str.contains(search_content, case=False, na=False)]
    if search_author:
        filtered_df = filtered_df[filtered_df["user_id"].str.contains(search_author, case=False, na=False)]
    if search_hashtag:
        # 해시태그로 검색
        hashtag_posts = manager.search_posts_by_hashtag(search_hashtag)
        if not hashtag_posts.empty:
            filtered_df = filtered_df[filtered_df["post_id"].isin(hashtag_posts["post_id"])]
        else:
            # 검색 결과가 없으면 빈 DataFrame
            filtered_df = pd.DataFrame(columns=filtered_df.columns)

    # ===== 정렬 탭 =====
    tab_latest, tab_likes, tab_comments = st.tabs(["⏱ 최신순", "👍 좋아요순", "💬 댓글순"])
    tab_map = {
        "latest": tab_latest,
        "likes": tab_likes,
        "comments": tab_comments
    }

    for sort_type, tab in tab_map.items():
        with tab:
            # 정렬 기준별 데이터
            if sort_type == "latest":
                sorted_df = filtered_df.sort_values(by="timestamp", ascending=False)
            elif sort_type == "likes":
                sorted_df = filtered_df.copy()
                sorted_df["likes_count"] = sorted_df["post_id"].apply(manager.count_post_likes)
                sorted_df = sorted_df.sort_values(by="likes_count", ascending=False)
            elif sort_type == "comments":
                sorted_df = filtered_df.copy()
                sorted_df["comments_count"] = sorted_df["post_id"].apply(lambda pid: len(manager.get_comments(pid)))
                sorted_df = sorted_df.sort_values(by="comments_count", ascending=False)

            if sorted_df.empty:
                st.info("검색 조건에 맞는 게시물이 없습니다.")
                continue

            # ===== 게시물 표시 =====
            for _, row in sorted_df.iterrows():
                post_id = row["post_id"]
                author_id = row["user_id"]

                title = str(row.get("title", "") or "")
                content = str(row.get("content", "") or "")
                hashtags = str(row.get("hashtags", "") or "")
                safe_content = html.escape(content)

                with st.container():
                    st.markdown(f"### {html.escape(title) if title else '제목없음'}")
                    st.caption(f"📌 작성자: {author_id} | 🕒 {row['timestamp']}")
                    st.markdown(
                        f"""
                        <div style="
                            background:#f8f9fa;
                            border:1px solid #e9ecef;
                            border-radius:8px;
                            padding:12px 14px;
                            margin:8px 0 10px 0;
                            line-height:1.5;
                            white-space:pre-wrap;
                            color:#343a40;
                        ">{safe_content}</div>
                        """,
                        unsafe_allow_html=True,
                    )
                    
                    # 해시태그 표시
                    if hashtags:
                        st.markdown(f"🏷️ **태그:** {hashtags}")

                    likes_cnt = manager.count_post_likes(post_id)
                    rts_cnt = manager.count_post_retweets(post_id)
                    comments_cnt = len(manager.get_comments(post_id))

                    # 현재 유저 상태
                    likes_df = manager.load_likes()
                    user_liked = ((likes_df["user_id"] == current_uid) & (likes_df["post_id"] == post_id)).any()

                    rts_df = manager.load_retweets()
                    user_rt = ((rts_df["user_id"] == current_uid) & (rts_df["post_id"] == post_id)).any()

                    is_own = (current_uid == author_id)
                    is_following = False
                    if current_uid and not is_own:
                        is_following = manager.is_following(current_uid, author_id)

                    # ===== 버튼 영역 =====
                    if page_type == "home":
                        # 홈 페이지: 모든 버튼 표시
                        c1, c2, c3, c4, c5 = st.columns(5)
                        with c5:
                            # 게시물 삭제 버튼 (본인만 보임)
                            if current_uid == author_id:
                                if st.button("🗑️ 게시물 삭제", key=f"{page_type}_{sort_type}_delete_post_{post_id}", type="secondary"):
                                    if st.session_state.get(f"confirm_delete_{post_id}", False):
                                        # 삭제 실행
                                        success, msg = manager.delete_post(current_uid, post_id)
                                        if success:
                                            st.success(msg)
                                            st.rerun()
                                        else:
                                            st.error(msg)
                                    else:
                                        # 삭제 확인
                                        st.session_state[f"confirm_delete_{post_id}"] = True
                                        st.warning("⚠️ 한 번 더 클릭하면 게시물이 삭제됩니다!")
                    else:
                        # 좋아요/리트윗 목록: 4개 컬럼
                        c1, c2, c3, c4 = st.columns(4)

                    # 공통 버튼들
                    with c1:
                        label = f"💔 좋아요 취소 {likes_cnt}" if user_liked else f"👍 좋아요 {likes_cnt}"
                        if st.button(label, key=f"{page_type}_{sort_type}_like_{post_id}"):
                            manager.toggle_like_post(current_uid, post_id)
                            st.rerun()
                    with c2:
                        label = f"❌ 리트윗 취소 {rts_cnt}" if user_rt else f"🔁 리트윗 {rts_cnt}"
                        if st.button(label, key=f"{page_type}_{sort_type}_rt_{post_id}"):
                            manager.toggle_retweet(current_uid, post_id)
                            st.rerun()
                    with c3:
                        if page_type == "following" or (page_type in ["liked", "retweeted"] and current_uid != author_id):
                            # 팔로잉 피드이거나 좋아요/리트윗 목록에서 다른 사람의 게시물인 경우
                            if is_following:
                                if st.button("👋 언팔로우", key=f"{page_type}_{sort_type}_unfollow_{post_id}"):
                                    manager.toggle_follow(current_uid, author_id)
                                    st.success(f"{author_id}님을 언팔로우했습니다.")
                                    st.rerun()
                            else:
                                if st.button("👤 팔로우", key=f"{page_type}_{sort_type}_follow_{post_id}"):
                                    manager.toggle_follow(current_uid, author_id)
                                    st.success(f"{author_id}님을 팔로우했습니다.")
                                    st.rerun()
                        elif page_type == "home" and current_uid and not is_own:
                            # 홈에서 다른 사람 게시물
                            if is_following:
                                if st.button("팔로우 취소", key=f"{page_type}_{sort_type}_unfollow_{post_id}"):
                                    manager.toggle_follow(current_uid, author_id)
                                    st.rerun()
                            else:
                                if st.button("팔로우", key=f"{page_type}_{sort_type}_follow_{post_id}"):
                                    manager.toggle_follow(current_uid, author_id)
                                    st.rerun()
                    with c4:
                        st.caption(f"💬 댓글 {comments_cnt}")

                    # ===== 댓글 섹션 =====
                    st.markdown("**💬 댓글**")
                    comments = manager.get_comments(post_id)
                    if comments.empty:
                        st.caption("아직 댓글이 없습니다.")
                    else:
                        for _, c in comments.iterrows():
                            cid = c["comment_id"]
                            c_user = c["user_id"]
                            c_txt = str(c.get("content", "") or "")
                            c_like_cnt = manager.count_comment_likes(cid)

                            cl_df = manager.load_comment_likes()
                            c_user_liked = ((cl_df["user_id"] == current_uid) & (cl_df["comment_id"] == cid)).any()

                            cc1, cc2, cc3 = st.columns([6, 2, 2])
                            with cc1:
                                st.write(f"**{c_user}**  ·  {c['timestamp']}")
                                st.write(html.escape(c_txt))
                            with cc2:
                                btn_label = f"💔 댓글 좋아요 취소 {c_like_cnt}" if c_user_liked else f"👍 댓글 좋아요 {c_like_cnt}"
                                if st.button(btn_label, key=f"{page_type}_{sort_type}_clike_{cid}"):
                                    manager.toggle_like_comment(current_uid, cid)
                                    st.rerun()
                            with cc3:
                                if current_uid == c_user:
                                    if st.button("🗑 삭제", key=f"{page_type}_{sort_type}_cdelete_{cid}"):
                                        manager.delete_comment(current_uid, cid)
                                        st.success("댓글이 삭제되었습니다.")
                                        st.rerun()

                    # 댓글 작성
                    new_comment = st.text_input("댓글 입력", key=f"{page_type}_{sort_type}_c_input_{post_id}")
                    if st.button("댓글 등록", key=f"{page_type}_{sort_type}_c_add_{post_id}"):
                        if new_comment.strip() == "":
                            st.warning("댓글 내용을 입력하세요.")
                        else:
                            manager.add_comment(current_uid, post_id, new_comment)
                            st.success("댓글 등록!")
                            st.rerun()

                    st.markdown("---")


def show_post():
    """
    타임라인(홈) : 게시물 목록 + (게시물 좋아요/좋아요 취소, 리트윗/취소, 팔로우/취소)
                + 댓글 작성/목록/댓글 좋아요/취소/삭제
                + 검색(제목, 내용, 작성자 분리) + 정렬 탭
                + 해시태그 검색 기능 + 게시물 삭제 기능 추가
    """
    manager = UserManager()
    posts_df = manager.load_posts()

    if posts_df.empty:
        st.info("등록된 게시물이 없습니다.")
        return

    current_user = st.session_state.get("current_user", {})
    current_uid = current_user.get("user_id", "")

    _display_posts(posts_df, current_uid, manager, "home")


def show_following_posts():
    """
    팔로잉 피드: 내가 팔로우한 사용자들의 게시물만 표시
    (홈과 동일한 기능 - 댓글, 좋아요, 리트윗 등 모든 기능 포함)
    """
    manager = UserManager()
    current_user = st.session_state.get("current_user", {})
    current_uid = current_user.get("user_id", "")

    if not current_uid:
        st.warning("🔒 팔로잉 피드를 보려면 로그인이 필요합니다.")
        return

    # 팔로잉 사용자들의 게시물만 가져오기
    posts_df = manager.get_following_posts(current_uid)

    if posts_df.empty:
        st.info("팔로우한 사용자의 게시물이 없거나, 아직 아무도 팔로우하지 않았습니다.")
        st.markdown("### 💡 팁")
        st.markdown("- 🏠 홈에서 다른 사용자를 팔로우해보세요!")
        st.markdown("- 팔로우한 사용자들의 최신 게시물이 여기에 표시됩니다.")
        return

    st.success(f"팔로우 중인 사용자들의 게시물 {len(posts_df)}개")

    _display_posts(posts_df, current_uid, manager, "following")


def show_liked_posts():
    """
    좋아요 목록: 내가 좋아요한 게시물들을 상세하게 표시
    """
    st.header("👍 내가 좋아요한 게시물")
    manager = UserManager()
    current_user = st.session_state.get("current_user", {})
    current_uid = current_user.get("user_id", "")

    if not current_uid:
        st.warning("🔒 좋아요 목록을 보려면 로그인이 필요합니다.")
        return

    liked_posts = manager.list_liked_posts_by_user(current_uid)

    if liked_posts.empty:
        st.info("좋아요한 게시물이 없습니다.")
        st.markdown("### 💡 팁")
        st.markdown("- 🏠 홈에서 게시물에 좋아요를 눌러보세요!")
        st.markdown("- 좋아요한 게시물들이 여기에 표시됩니다.")
        return

    st.success(f"좋아요한 게시물 {len(liked_posts)}개")

    _display_posts(liked_posts, current_uid, manager, "liked")


def show_retweeted_posts():
    """
    리트윗 목록: 내가 리트윗한 게시물들을 상세하게 표시
    """
    st.header("🔁 내가 리트윗한 게시물")
    manager = UserManager()
    current_user = st.session_state.get("current_user", {})
    current_uid = current_user.get("user_id", "")

    if not current_uid:
        st.warning("🔒 리트윗 목록을 보려면 로그인이 필요합니다.")
        return

    retweeted_posts = manager.list_retweeted_posts_by_user(current_uid)

    if retweeted_posts.empty:
        st.info("리트윗한 게시물이 없습니다.")
        st.markdown("### 💡 팁")
        st.markdown("- 🏠 홈에서 게시물을 리트윗해보세요!")
        st.markdown("- 리트윗한 게시물들이 여기에 표시됩니다.")
        return

    st.success(f"리트윗한 게시물 {len(retweeted_posts)}개")

    _display_posts(retweeted_posts, current_uid, manager, "retweeted")

    # auth.py에 추가할 알림 관련 함수들

def show_notifications():
    """알림 목록 페이지 - 전체 삭제 기능 포함"""
    st.header("🔔 알림 센터")
    
    manager = UserManager()
    current_user = st.session_state.get("current_user", {})
    current_uid = current_user.get("user_id", "")
    
    if not current_uid:
        st.warning("🔒 알림을 보려면 로그인이 필요합니다.")
        return
    
    # 알림 가져오기
    notifications = manager.get_user_notifications(current_uid)
    unread_count = manager.get_unread_count(current_uid)
    
    # 상단 요약 (4개 컬럼으로 변경)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📧 전체 알림", len(notifications))
    with col2:
        st.metric("🆕 읽지 않은 알림", unread_count)
    with col3:
        if st.button("✅ 모두 읽음 처리", type="primary"):
            manager.mark_all_notifications_read(current_uid)
            st.success("모든 알림을 읽음 처리했습니다!")
            st.rerun()
    with col4:
        if st.button("🗑️ 전체 삭제", type="secondary"):
            # 확인 플래그 체크
            if st.session_state.get("confirm_delete_all_notifications", False):
                success, msg = manager.delete_all_notifications(current_uid)
                if success:
                    st.success(msg)
                    # 확인 플래그 리셋
                    st.session_state.confirm_delete_all_notifications = False
                    st.rerun()
            else:
                # 삭제 확인
                st.session_state.confirm_delete_all_notifications = True
                st.warning("⚠️ 한 번 더 클릭하면 모든 알림이 삭제됩니다!")
    
    st.divider()
    
    if notifications.empty:
        st.info("📪 받은 알림이 없습니다.")
        st.markdown("### 💡 팁")
        st.markdown("- 다른 사용자가 회원님을 팔로우하면 알림이 옵니다")
        st.markdown("- 회원님의 게시물에 좋아요나 댓글이 달리면 알림이 옵니다")
        st.markdown("- 알림 설정에서 원하는 알림만 받을 수 있습니다")
        return
    
    # 필터 탭
    tab_all, tab_unread, tab_follow, tab_like, tab_comment = st.tabs([
        "📋 전체", "🆕 읽지 않음", "👥 팔로우", "👍 좋아요", "💬 댓글"
    ])
    
    # 각 탭별 필터링
    tabs_data = {
        "all": notifications,
        "unread": notifications[notifications["is_read"] == False],
        "follow": notifications[notifications["type"] == "follow"],
        "like": notifications[notifications["type"].isin(["like", "comment_like"])],
        "comment": notifications[notifications["type"].isin(["comment", "retweet"])]
    }
    
    for tab_key, (tab, filtered_notifications) in zip(
        ["all", "unread", "follow", "like", "comment"],
        [(tab_all, tabs_data["all"]), (tab_unread, tabs_data["unread"]), 
         (tab_follow, tabs_data["follow"]), (tab_like, tabs_data["like"]), 
         (tab_comment, tabs_data["comment"])]
    ):
        with tab:
            if filtered_notifications.empty:
                st.info(f"해당하는 알림이 없습니다.")
                continue
                
            st.caption(f"총 {len(filtered_notifications)}개의 알림")
            
            # 알림 카드 표시
            for idx, noti in filtered_notifications.iterrows():
                noti_id = noti["notification_id"]
                is_read = noti["is_read"]
                noti_type = noti["type"]
                
                # 안읽은 알림은 초록색 배경, 읽은 알림은 검은색 배경
                card_style = "background:#28a745; color:#ffffff; border-left:4px solid #ffffff;" if not is_read else "background:#000000; color:#ffffff; border-left:4px solid #6c757d;"
                
                # 알림 타입별 아이콘
                type_icons = {
                    "follow": "👥",
                    "like": "👍", 
                    "comment": "💬",
                    "comment_like": "👍",
                    "retweet": "🔁"
                }
                
                icon = type_icons.get(noti_type, "🔔")
                
                with st.container():
                    st.markdown(
                        f"""
                        <div style="{card_style} padding:12px; margin:8px 0; border-radius:8px;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div style="flex:1;">
                                    <span style="font-size:16px;">{icon}</span>
                                    <strong style="color:#ffffff;">{noti['message']}</strong>
                                </div>
                                <div style="color:#cccccc; font-size:12px;">
                                    {noti['timestamp']}
                                </div>
                            </div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # 버튼 영역 - 고유 키 생성
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                    
                    with col1:
                        if not is_read:
                            if st.button("✅ 읽음 처리", key=f"read_{tab_key}_{noti_id}_{idx}"):
                                manager.mark_notification_read(noti_id)
                                st.success("읽음 처리했습니다!")
                                st.rerun()
                    
                    with col2:
                        # 관련 게시물로 이동 (추후 구현 가능)
                        post_id = noti.get("post_id", "")
                        if post_id and str(post_id).strip() and str(post_id) != "nan":
                            st.caption(f"📄 관련 게시물: {post_id}")

                    with col3:
                        comment_id = noti.get("comment_id", "")
                        if comment_id and str(comment_id).strip() and str(comment_id) != "nan":
                            st.caption(f"💬 관련 댓글: {comment_id}")
                            
                    with col4:
                        if st.button("🗑️", key=f"delete_{tab_key}_{noti_id}_{idx}", help="알림 삭제"):
                            manager.delete_notification(noti_id, current_uid)
                            st.success("알림을 삭제했습니다!")
                            st.rerun()

def show_notification_settings():
    """알림 설정 페이지"""
    st.header("⚙️ 알림 설정")
    
    manager = UserManager()
    current_user = st.session_state.get("current_user", {})
    current_uid = current_user.get("user_id", "")
    
    if not current_uid:
        st.warning("🔒 알림 설정을 변경하려면 로그인이 필요합니다.")
        return
    
    st.markdown("### 🔔 받고 싶은 알림을 선택하세요")
    st.markdown("알림을 끄면 해당 활동에 대한 알림을 받지 않습니다.")
    
    # 현재 설정 가져오기
    current_settings = manager.get_notification_settings(current_uid)
    
    # 설정 폼
    with st.form("notification_settings"):
        st.markdown("#### 👥 팔로우 알림")
        follow_enabled = st.checkbox(
            "새로운 팔로워가 생겼을 때 알림 받기", 
            value=current_settings.get("follow_notifications", True),
            help="다른 사용자가 회원님을 팔로우할 때 알림을 받습니다"
        )
        
        st.markdown("#### 👍 좋아요 알림")
        like_enabled = st.checkbox(
            "게시물이나 댓글에 좋아요를 받았을 때 알림 받기", 
            value=current_settings.get("like_notifications", True),
            help="회원님의 게시물이나 댓글에 다른 사용자가 좋아요를 누를 때 알림을 받습니다"
        )
        
        st.markdown("#### 💬 댓글 알림")
        comment_enabled = st.checkbox(
            "게시물에 댓글이 달렸을 때 알림 받기", 
            value=current_settings.get("comment_notifications", True),
            help="회원님의 게시물에 댓글이 달릴 때 알림을 받습니다"
        )
        
        st.markdown("#### 🔁 리트윗 알림")
        retweet_enabled = st.checkbox(
            "게시물이 리트윗되었을 때 알림 받기", 
            value=current_settings.get("retweet_notifications", True),
            help="회원님의 게시물이 리트윗될 때 알림을 받습니다"
        )
        
        # 저장 버튼
        if st.form_submit_button("💾 설정 저장", type="primary"):
            manager.update_notification_settings(
                current_uid, 
                follow=follow_enabled,
                like=like_enabled, 
                comment=comment_enabled,
                retweet=retweet_enabled
            )
            st.success("✅ 알림 설정이 저장되었습니다!")
            st.rerun()
    
    # 현재 설정 상태 표시
    st.divider()
    st.markdown("### 📋 현재 설정 상태")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = "🟢 켜짐" if current_settings.get("follow_notifications", True) else "🔴 꺼짐"
        st.metric("👥 팔로우", status)
    
    with col2:
        status = "🟢 켜짐" if current_settings.get("like_notifications", True) else "🔴 꺼짐"
        st.metric("👍 좋아요", status)
    
    with col3:
        status = "🟢 켜짐" if current_settings.get("comment_notifications", True) else "🔴 꺼짐"
        st.metric("💬 댓글", status)
        
    with col4:
        status = "🟢 켜짐" if current_settings.get("retweet_notifications", True) else "🔴 꺼짐"
        st.metric("🔁 리트윗", status)
    
    # 알림 통계
    st.divider()
    st.markdown("### 📊 알림 통계")
    
    notifications = manager.get_user_notifications(current_uid)
    if not notifications.empty:
        total_count = len(notifications)
        unread_count = manager.get_unread_count(current_uid)
        
        # 타입별 통계
        type_counts = notifications["type"].value_counts()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📧 총 받은 알림", total_count)
            st.metric("🆕 읽지 않은 알림", unread_count)
        
        with col2:
            if len(type_counts) > 0:
                st.markdown("**알림 종류별 개수:**")
                for noti_type, count in type_counts.items():
                    type_names = {
                        "follow": "👥 팔로우",
                        "like": "👍 좋아요", 
                        "comment": "💬 댓글",
                        "comment_like": "👍 댓글 좋아요",
                        "retweet": "🔁 리트윗"
                    }
                    type_name = type_names.get(noti_type, noti_type)
                    st.write(f"- {type_name}: {count}개")
    else:
        st.info("아직 받은 알림이 없습니다.")