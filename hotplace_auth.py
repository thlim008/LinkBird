# hotplace_auth.py
import streamlit as st
import pandas as pd
import html
from user_manager import UserManager
import folium
from streamlit_folium import st_folium

def show_hotplace_map():
    """핫플레이스 지도 표시"""
    st.header("🗺️ 팔로잉 핫플레이스 맵")
    
    manager = UserManager()
    current_user = st.session_state.get("current_user", {})
    current_uid = current_user.get("user_id", "")
    
    if not current_uid:
        st.warning("🔒 핫플레이스 맵을 보려면 로그인이 필요합니다.")
        return
    
    # 필터 옵션
    col1, col2, col3 = st.columns(3)
    with col1:
        view_option = st.selectbox("보기 옵션", ["팔로잉만", "전체", "내 등록"])
    with col2:
        category_filter = st.selectbox("카테고리", ["전체", "카페/디저트", "음식점", "관광지", "쇼핑", "기타"])
    with col3:
        sort_option = st.selectbox("정렬", ["최신순", "좋아요순", "평점순"])
    
    # 데이터 로드
    try:
        if view_option == "팔로잉만":
            hotplaces_df = manager.get_following_hotplaces(current_uid)
            if hotplaces_df.empty:
                st.info("팔로우한 사용자의 핫플레이스가 없습니다. 다른 사용자를 팔로우해보세요!")
                return
        elif view_option == "내 등록":
            all_hotplaces = manager.get_all_hotplaces_with_stats()
            if all_hotplaces.empty:
                st.info("등록된 핫플레이스가 없습니다. 새로운 핫플레이스를 등록해보세요!")
                return
            hotplaces_df = all_hotplaces[all_hotplaces["user_id"] == current_uid]
            if hotplaces_df.empty:
                st.info("등록한 핫플레이스가 없습니다. 새로운 핫플레이스를 등록해보세요!")
                return
        else:
            hotplaces_df = manager.get_all_hotplaces_with_stats()
            if hotplaces_df.empty:
                st.info("등록된 핫플레이스가 없습니다. 📍 핫플레이스 등록 메뉴에서 첫 번째 핫플레이스를 등록해보세요!")
                return
    except Exception as e:
        st.error(f"데이터 로드 중 오류가 발생했습니다: {str(e)}")
        st.info("📍 핫플레이스 등록 메뉴에서 첫 번째 핫플레이스를 등록해보세요!")
        return
    
    # 카테고리 필터 적용
    if category_filter != "전체":
        hotplaces_df = hotplaces_df[hotplaces_df["category"] == category_filter]
    
    # 정렬 적용
    if sort_option == "좋아요순":
        hotplaces_df = hotplaces_df.sort_values(by="likes_count", ascending=False)
    elif sort_option == "평점순":
        hotplaces_df = hotplaces_df.sort_values(by="avg_rating", ascending=False)
    else:  # 최신순
        hotplaces_df = hotplaces_df.sort_values(by="timestamp", ascending=False)
    
    if hotplaces_df.empty:
        st.info("선택한 조건에 맞는 핫플레이스가 없습니다.")
        return
    
    # 지도 생성 (대전 중심)
    center_lat = 36.3504
    center_lon = 127.3845
    
    # 핫플레이스가 있으면 첫 번째 장소를 중심으로
    if not hotplaces_df.empty:
        center_lat = hotplaces_df.iloc[0]["latitude"]
        center_lon = hotplaces_df.iloc[0]["longitude"]
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    
    # 마커 추가
    for _, place in hotplaces_df.iterrows():
        # 마커 색상 (카테고리별)
        color_map = {
            "카페/디저트": "blue",
            "음식점": "red", 
            "관광지": "green",
            "쇼핑": "purple",
            "기타": "orange"
        }
        color = color_map.get(place["category"], "gray")
        
        # 팝업 내용
        popup_text = f"""
        <b>{place['place_name']}</b><br>
        카테고리: {place['category']}<br>
        등록자: {place['user_id']}<br>
        좋아요: {place.get('likes_count', 0)}개<br>
        평점: {place.get('avg_rating', 0.0)}점<br>
        주소: {place.get('address', '주소 없음')}<br>
        <small>{place['description']}</small>
        """
        
        folium.Marker(
            location=[place["latitude"], place["longitude"]],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=place["place_name"],
            icon=folium.Icon(color=color, icon="map-pin", prefix="fa")
        ).add_to(m)
    
    # 지도 표시
    map_data = st_folium(m, width=700, height=500)
    
    st.divider()
    
    # 핫플레이스 목록
    st.subheader(f"📍 핫플레이스 목록 ({len(hotplaces_df)}개)")
    
    for _, place in hotplaces_df.iterrows():
        place_id = place["place_id"]
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### 📍 {place['place_name']}")
                st.caption(f"🏷️ {place['category']} | 👤 {place['user_id']} | 🕒 {place['timestamp']}")
                st.write(f"📍 **주소:** {place.get('address', '주소 없음')}")
                st.write(f"📝 **설명:** {place['description']}")
                
                # 통계
                likes_count = place.get('likes_count', 0)
                avg_rating = place.get('avg_rating', 0.0)
                st.write(f"👍 좋아요 {likes_count}개 | ⭐ 평점 {avg_rating}점")
            
            with col2:
                # 좋아요 버튼
                likes_df = manager.load_place_likes()
                user_liked = ((likes_df["user_id"] == current_uid) & (likes_df["place_id"] == place_id)).any()
                
                if user_liked:
                    if st.button("💔 좋아요 취소", key=f"unlike_{place_id}"):
                        manager.toggle_like_place(current_uid, place_id)
                        st.rerun()
                else:
                    if st.button("👍 좋아요", key=f"like_{place_id}"):
                        manager.toggle_like_place(current_uid, place_id)
                        st.rerun()
                
                # 리뷰 보기 버튼
                if st.button("💬 리뷰", key=f"review_{place_id}"):
                    st.session_state[f"show_reviews_{place_id}"] = not st.session_state.get(f"show_reviews_{place_id}", False)
            
            # 리뷰 섹션
            if st.session_state.get(f"show_reviews_{place_id}", False):
                st.markdown("**💬 리뷰**")
                
                # 리뷰 작성
                with st.form(f"review_form_{place_id}"):
                    col_rating, col_text = st.columns([1, 3])
                    with col_rating:
                        rating = st.selectbox("평점", [5, 4, 3, 2, 1], key=f"rating_{place_id}")
                    with col_text:
                        review_text = st.text_area("리뷰 내용", key=f"review_text_{place_id}", height=100)
                    
                    if st.form_submit_button("리뷰 등록"):
                        if review_text.strip():
                            manager.add_place_review(current_uid, place_id, rating, review_text)
                            st.success("리뷰가 등록되었습니다!")
                            st.rerun()
                        else:
                            st.warning("리뷰 내용을 입력해주세요.")
                
                # 기존 리뷰들
                reviews = manager.get_place_reviews(place_id)
                if not reviews.empty:
                    st.markdown("**기존 리뷰들:**")
                    for _, review in reviews.iterrows():
                        st.write(f"⭐ {review['rating']}점 | **{review['user_id']}** | {review['timestamp']}")
                        st.write(f"💭 {review['review_text']}")
                        st.markdown("---")
                else:
                    st.caption("아직 리뷰가 없습니다. 첫 번째 리뷰를 남겨보세요!")
            
            st.markdown("---")



def show_add_hotplace():
    """핫플레이스 등록 페이지"""
    st.header("📍 새로운 핫플레이스 등록")
    
    manager = UserManager()
    current_user = st.session_state.get("current_user", {})
    current_uid = current_user.get("user_id", "")
    
    if not current_uid:
        st.warning("🔒 핫플레이스 등록을 하려면 로그인이 필요합니다.")
        return
    
    # 성공 메시지 표시
    if st.session_state.get("hotplace_success", False):
        st.success("🎉 핫플레이스가 등록되었습니다!")
        st.session_state.hotplace_success = False
    
    st.info("💡 팁: 정확한 위치 정보를 입력하면 지도에서 더 쉽게 찾을 수 있어요!")
    
    with st.form("add_hotplace_form"):
        # 기본 정보
        col1, col2 = st.columns(2)
        with col1:
            place_name = st.text_input("장소명*", placeholder="예: 성심당 본점")
            category = st.selectbox("카테고리*", ["카페/디저트", "음식점", "관광지", "쇼핑", "기타"])
        
        with col2:
            address = st.text_input("주소", placeholder="예: 대전광역시 중구 은행동")
        
        # 위치 정보
        st.markdown("### 📍 위치 정보")
        col3, col4 = st.columns(2)
        with col3:
            latitude = st.number_input("위도*", min_value=-90.0, max_value=90.0, value=36.3504, format="%.6f")
        with col4:
            longitude = st.number_input("경도*", min_value=-180.0, max_value=180.0, value=127.3845, format="%.6f")
        
        # 위치 도움말
        with st.expander("🤔 위도/경도를 모르겠어요"):
            st.markdown("""
            **위도/경도 찾는 방법:**
            1. 구글맵에서 장소를 검색하세요
            2. 해당 위치를 우클릭하세요
            3. 나오는 숫자(위도, 경도)를 복사해서 입력하세요
            
            **대전 주요 지역 참고:**
            - 대전역: 36.3312, 127.4341
            - 서대전네거리역: 36.3540, 127.3776
            - 유성온천역: 36.3623, 127.3431
            """)
        
        # 설명
        description = st.text_area("장소 설명*", height=100, 
                                 placeholder="이 장소만의 특별한 점, 추천 이유 등을 자유롭게 작성해주세요!")
        
        # 등록 버튼
        submitted = st.form_submit_button("🚀 핫플레이스 등록", type="primary")
        
        if submitted:
            if not place_name or not description:
                st.error("❌ 장소명과 설명은 필수 입력 항목입니다.")
            elif not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                st.error("❌ 올바른 위도/경도를 입력해주세요.")
            else:
                success, message = manager.create_hotplace(
                    current_uid, place_name, latitude, longitude, 
                    category, address, description
                )
                if success:
                    st.session_state.hotplace_success = True
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    # 미리보기 지도
    st.divider()
    st.markdown("### 🗺️ 위치 미리보기")
    
    try:
        preview_map = folium.Map(location=[latitude, longitude], zoom_start=15)
        folium.Marker(
            location=[latitude, longitude],
            popup="등록할 위치",
            tooltip="등록할 위치",
            icon=folium.Icon(color="red", icon="map-pin", prefix="fa")
        ).add_to(preview_map)
        
        st_folium(preview_map, width=700, height=300)
    except:
        st.caption("위도/경도를 입력하면 미리보기가 표시됩니다.")
    
    # 내가 등록한 핫플레이스 목록
    st.divider()
    st.markdown("### 📋 내가 등록한 핫플레이스")
    
    my_hotplaces = manager.get_all_hotplaces_with_stats()
    if not my_hotplaces.empty:
        my_hotplaces = my_hotplaces[my_hotplaces["user_id"] == current_uid]
        
        if not my_hotplaces.empty:
            for _, place in my_hotplaces.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"📍 **{place['place_name']}** ({place['category']})")
                    st.caption(f"👍 {place.get('likes_count', 0)}개 | ⭐ {place.get('avg_rating', 0.0)}점 | 🕒 {place['timestamp']}")
                with col2:
                    st.caption(f"📍 {place['latitude']:.4f}, {place['longitude']:.4f}")
                with col3:
                    if st.button("🗑️ 삭제", key=f"del_{place['place_id']}", help="핫플레이스 삭제"):
                        success, message = manager.delete_hotplace(current_uid, place['place_id'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("아직 등록한 핫플레이스가 없습니다.")
    else:
        st.info("아직 등록한 핫플레이스가 없습니다.")