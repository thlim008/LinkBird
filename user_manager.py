# user_manager.py
import os
import pandas as pd
from datetime import datetime
import re

DATA_DIR = "data"

class UserManager:
    def __init__(self):
        self.users_csv = os.path.join(DATA_DIR, "users.csv")
        self.posts_csv = os.path.join(DATA_DIR, "posts.csv")
        self.likes_csv = os.path.join(DATA_DIR, "likes.csv")  
        self.retweets_csv = os.path.join(DATA_DIR, "retweets.csv")
        self.follows_csv = os.path.join(DATA_DIR, "follows.csv")
        self.comments_csv = os.path.join(DATA_DIR, "comments.csv")
        self.comment_likes_csv = os.path.join(DATA_DIR, "comment_likes.csv")
        self.hashtags_csv = os.path.join(DATA_DIR, "hashtags.csv")  
        self.notifications_csv = os.path.join(DATA_DIR, "notifications.csv")
        self.notification_settings_csv = os.path.join(DATA_DIR, "notification_settings.csv")
        self.hotplaces_csv = os.path.join(DATA_DIR, "hotplaces.csv")
        self.place_likes_csv = os.path.join(DATA_DIR, "place_likes.csv")
        self.place_reviews_csv = os.path.join(DATA_DIR, "place_reviews.csv")
        self._ensure_csv()

    # -------------------- init & IO --------------------
    def _ensure_csv(self):
        os.makedirs(DATA_DIR, exist_ok=True)

        if not os.path.exists(self.users_csv):
            pd.DataFrame(columns=["user_id", "username", "password", "created_at"]).to_csv(self.users_csv, index=False, encoding="utf-8")

        if not os.path.exists(self.posts_csv):
            pd.DataFrame(columns=["post_id", "user_id", "title", "content", "hashtags", "timestamp"]).to_csv(self.posts_csv, index=False, encoding="utf-8")

        if not os.path.exists(self.likes_csv):
            pd.DataFrame(columns=["user_id", "post_id", "timestamp"]).to_csv(self.likes_csv, index=False, encoding="utf-8")

        if not os.path.exists(self.retweets_csv):
            pd.DataFrame(columns=["user_id", "post_id", "timestamp"]).to_csv(self.retweets_csv, index=False, encoding="utf-8")

        if not os.path.exists(self.follows_csv):
            pd.DataFrame(columns=["follower_id", "followed_id", "timestamp"]).to_csv(self.follows_csv, index=False, encoding="utf-8")

        if not os.path.exists(self.comments_csv):
            pd.DataFrame(columns=["comment_id", "post_id", "user_id", "content", "timestamp"]).to_csv(self.comments_csv, index=False, encoding="utf-8")

        if not os.path.exists(self.comment_likes_csv):
            pd.DataFrame(columns=["user_id", "comment_id", "timestamp"]).to_csv(self.comment_likes_csv, index=False, encoding="utf-8")

        if not os.path.exists(self.hashtags_csv):
            pd.DataFrame(columns=["post_id", "hashtag", "timestamp"]).to_csv(self.hashtags_csv, index=False, encoding="utf-8")

        if not os.path.exists(self.notifications_csv):
            pd.DataFrame(columns=[
                "notification_id", "user_id", "type", "from_user_id", 
                "post_id", "comment_id", "message", "is_read", "timestamp"
            ]).to_csv(self.notifications_csv, index=False, encoding="utf-8")

        if not os.path.exists(self.notification_settings_csv):
            pd.DataFrame(columns=[
                "user_id", "follow_notifications", "like_notifications", 
                "comment_notifications", "retweet_notifications"
            ]).to_csv(self.notification_settings_csv, index=False, encoding="utf-8")
        if not os.path.exists(self.hotplaces_csv):
            pd.DataFrame(columns=[
                "place_id", "user_id", "place_name", "latitude", "longitude", 
                "category", "address", "description", "timestamp"
            ]).to_csv(self.hotplaces_csv, index=False, encoding="utf-8")

        if not os.path.exists(self.place_likes_csv):
            pd.DataFrame(columns=[
                "user_id", "place_id", "timestamp"
            ]).to_csv(self.place_likes_csv, index=False, encoding="utf-8")

        if not os.path.exists(self.place_reviews_csv):
            pd.DataFrame(columns=[
                "review_id", "place_id", "user_id", "rating", "review_text", "timestamp"
            ]).to_csv(self.place_reviews_csv, index=False, encoding="utf-8")


    # load
    def load_users(self): return pd.read_csv(self.users_csv, encoding="utf-8")
    def load_posts(self): return pd.read_csv(self.posts_csv, encoding="utf-8")
    def load_likes(self): return pd.read_csv(self.likes_csv, encoding="utf-8")
    def load_retweets(self): return pd.read_csv(self.retweets_csv, encoding="utf-8")
    def load_follows(self): return pd.read_csv(self.follows_csv, encoding="utf-8")
    def load_comments(self): return pd.read_csv(self.comments_csv, encoding="utf-8")
    def load_comment_likes(self): return pd.read_csv(self.comment_likes_csv, encoding="utf-8")
    def load_hashtags(self): return pd.read_csv(self.hashtags_csv, encoding="utf-8")
    def load_notifications(self):return pd.read_csv(self.notifications_csv, encoding="utf-8")
    def load_notification_settings(self):return pd.read_csv(self.notification_settings_csv, encoding="utf-8")
    def load_place_likes(self): 
        return pd.read_csv(self.place_likes_csv, encoding="utf-8")
    def load_hotplaces(self): 
        return pd.read_csv(self.hotplaces_csv, encoding="utf-8")
    def load_place_reviews(self): 
        return pd.read_csv(self.place_reviews_csv, encoding="utf-8")
    # save
    def save_users(self, df): df.to_csv(self.users_csv, index=False, encoding="utf-8")
    def save_posts(self, df): df.to_csv(self.posts_csv, index=False, encoding="utf-8")
    def save_likes(self, df): df.to_csv(self.likes_csv, index=False, encoding="utf-8")
    def save_retweets(self, df): df.to_csv(self.retweets_csv, index=False, encoding="utf-8")
    def save_follows(self, df): df.to_csv(self.follows_csv, index=False, encoding="utf-8")
    def save_comments(self, df): df.to_csv(self.comments_csv, index=False, encoding="utf-8")
    def save_comment_likes(self, df): df.to_csv(self.comment_likes_csv, index=False, encoding="utf-8")
    def save_hashtags(self, df): df.to_csv(self.hashtags_csv, index=False, encoding="utf-8")
    def save_notifications(self, df):df.to_csv(self.notifications_csv, index=False, encoding="utf-8")
    def save_notification_settings(self, df):df.to_csv(self.notification_settings_csv, index=False, encoding="utf-8")
    def save_hotplaces(self, df): 
        df.to_csv(self.hotplaces_csv, index=False, encoding="utf-8")
    def save_place_likes(self, df): 
        df.to_csv(self.place_likes_csv, index=False, encoding="utf-8")
    def save_place_reviews(self, df): 
        df.to_csv(self.place_reviews_csv, index=False, encoding="utf-8")

    
    # -------------------- Hashtag Functions --------------------
    def extract_hashtags(self, text):
        """텍스트에서 해시태그 추출 (#태그)"""
        if not text:
            return []
        hashtags = re.findall(r'#(\w+)', text)
        return hashtags

    def save_post_hashtags(self, post_id, hashtags, timestamp):
        """게시물 해시태그 저장"""
        if not hashtags:
            return
        
        hashtag_df = self.load_hashtags()
        
        # 해당 게시물의 기존 해시태그 삭제
        hashtag_df = hashtag_df[hashtag_df["post_id"] != post_id]
        
        # 새 해시태그 추가
        new_rows = []
        for hashtag in hashtags:
            new_rows.append({
                "post_id": post_id,
                "hashtag": hashtag,
                "timestamp": timestamp
            })
        
        if new_rows:
            if hashtag_df.empty:
                hashtag_df = pd.DataFrame(new_rows)
            else:
                hashtag_df = pd.concat([hashtag_df, pd.DataFrame(new_rows)], ignore_index=True)
            self.save_hashtags(hashtag_df)

    def get_popular_hashtags(self, limit=10):
        """인기 해시태그 반환"""
        try:
            hashtag_df = self.load_hashtags()
            if hashtag_df.empty:
                return []
            
            hashtag_counts = hashtag_df["hashtag"].value_counts()
            return [(tag, count) for tag, count in hashtag_counts.head(limit).items()]
        except Exception:
            return []

    def search_posts_by_hashtag(self, hashtag):
        """해시태그로 게시물 검색"""
        hashtag_df = self.load_hashtags()
        posts_df = self.load_posts()
        
        if hashtag_df.empty:
            return pd.DataFrame()
        
        # 해시태그에 해당하는 post_id 찾기
        post_ids = hashtag_df[hashtag_df["hashtag"].str.contains(hashtag, case=False, na=False)]["post_id"].tolist()
        
        if not post_ids:
            return pd.DataFrame()
        
        # 해당 게시물들 반환
        return posts_df[posts_df["post_id"].isin(post_ids)].sort_values(by="timestamp", ascending=False)

    # -------------------- Users --------------------
    def get_user_count(self):
        return len(self.load_users())

    def create_user(self, username, password):
        users = self.load_users()
        if username.strip() == "" or password.strip() == "":
            return False, "아이디/비밀번호를 입력하세요."
        if (users["username"].astype(str) == username).any():
            return False, "이미 존재하는 사용자명입니다."
        new_id = f"user_{len(users) + 1:03d}"
        row = {
            "user_id": new_id,
            "username": username,
            "password": password,
            "created_at": datetime.now().strftime("%Y-%m-%d"),
        }
        if users.empty:
            users = pd.DataFrame([row])
        else:
            users = pd.concat([users, pd.DataFrame([row])], ignore_index=True)
        self.save_users(users)
        return True, "회원가입 완료!"

    def login_user(self, username, password):
        users = self.load_users()
        m = users[(users["username"].astype(str) == str(username)) & (users["password"].astype(str) == str(password))]
        if len(m) == 1:
            return True, m.iloc[0].to_dict()
        return False, None

    # -------------------- Posts --------------------
    def _next_post_id(self, posts: pd.DataFrame):
        if posts.empty: return "post_001"
        mx = posts["post_id"].str.replace("post_", "", regex=False).astype(int).max()
        return f"post_{mx+1:03d}"

    def create_post(self, user_id, title, content):
        posts = self.load_posts()
        post_id = self._next_post_id(posts)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 제목과 내용에서 해시태그 추출
        hashtags_title = self.extract_hashtags(title)
        hashtags_content = self.extract_hashtags(content)
        all_hashtags = list(set(hashtags_title + hashtags_content))  
        hashtags_str = " ".join([f"#{tag}" for tag in all_hashtags])
        
        row = {
            "post_id": post_id,
            "user_id": user_id,
            "title": str(title or "").strip(),
            "content": str(content or "").strip(),
            "hashtags": hashtags_str,
            "timestamp": timestamp,
        }
        if posts.empty:
            posts = pd.DataFrame([row])
        else:
            posts = pd.concat([posts, pd.DataFrame([row])], ignore_index=True)
        self.save_posts(posts)
        # 해시태그 별도 저장
        self.save_post_hashtags(post_id, all_hashtags, timestamp)
        
        return True, "게시물 등록!"

    def delete_post(self, user_id, post_id):
        """게시물 삭제 (본인만 가능)"""
        posts = self.load_posts()
        post = posts[posts["post_id"] == post_id]

        if post.empty:
            return False, "게시물이 존재하지 않습니다."

        # 본인 게시물만 삭제 가능
        if post.iloc[0]["user_id"] != user_id:
            return False, "본인 게시물만 삭제할 수 있습니다."

        # 게시물 삭제
        posts = posts[posts["post_id"] != post_id]
        self.save_posts(posts)

        # 관련 데이터 삭제 - 좋아요
        likes = self.load_likes()
        likes = likes[likes["post_id"] != post_id]
        self.save_likes(likes)

        # 관련 데이터 삭제 - 리트윗
        retweets = self.load_retweets()
        retweets = retweets[retweets["post_id"] != post_id]
        self.save_retweets(retweets)

        # 관련 데이터 삭제 - 댓글
        comments = self.load_comments()
        deleted_comment_ids = comments[comments["post_id"] == post_id]["comment_id"].tolist()
        comments = comments[comments["post_id"] != post_id]
        self.save_comments(comments)

        # 관련 데이터 삭제 - 댓글 좋아요
        comment_likes = self.load_comment_likes()
        comment_likes = comment_likes[~comment_likes["comment_id"].isin(deleted_comment_ids)]
        self.save_comment_likes(comment_likes)

        # 관련 데이터 삭제 - 해시태그
        hashtags = self.load_hashtags()
        hashtags = hashtags[hashtags["post_id"] != post_id]
        self.save_hashtags(hashtags)

        return True, "게시물 삭제 완료!"

    def count_user_posts(self, user_id):
        posts = self.load_posts()
        return int((posts["user_id"] == user_id).sum())

    # -------------------- Post Likes --------------------
    def count_post_likes(self, post_id):
        """게시물 좋아요 수 - 안전한 처리"""
        try:
            likes = self.load_likes()
            if likes.empty:
                return 0
            return int((likes["post_id"].astype(str) == str(post_id)).sum())
        except Exception:
            return 0

    def toggle_like_post(self, user_id, post_id):
        """게시물 좋아요 토글 + 알림 생성"""
        likes = self.load_likes()
        mask = (likes["user_id"] == user_id) & (likes["post_id"] == post_id)

        if mask.any():
            likes = likes[~mask]
            self.save_likes(likes)
            return False, "좋아요 취소"
        else:
            row = {"user_id": user_id, "post_id": post_id, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
            if likes.empty:
                likes = pd.DataFrame([row])
            else:
                likes = pd.concat([likes, pd.DataFrame([row])], ignore_index=True)
            self.save_likes(likes)
    
            # 게시물 작성자에게 알림 (안전한 처리)
            posts = self.load_posts()
            post = posts[posts["post_id"] == post_id]
            if not post.empty:
                post_author = post.iloc[0]["user_id"]
                # 본인에게는 알림 보내지 않음
                if post_author != user_id:
                    self.create_notification(post_author, "like", user_id, post_id=post_id)
    
            return True, "좋아요!"

    # -------------------- Retweets --------------------
    def count_post_retweets(self, post_id):
        """리트윗 수 - 안전한 처리"""
        try:
            rts = self.load_retweets()
            if rts.empty:
                return 0
            return int((rts["post_id"].astype(str) == str(post_id)).sum())
        except Exception:
            return 0

    def toggle_retweet(self, user_id, post_id):
        """리트윗 토글 + 알림 생성"""
        rts = self.load_retweets()
        mask = (rts["user_id"] == user_id) & (rts["post_id"] == post_id)
    
        if mask.any():
            rts = rts[~mask]
            self.save_retweets(rts)
            return False, "리트윗 취소"
        else:
            row = {"user_id": user_id, "post_id": post_id, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            if rts.empty:
                rts = pd.DataFrame([row])
            else:
                rts = pd.concat([rts, pd.DataFrame([row])], ignore_index=True)
            self.save_retweets(rts)
        
            # 게시물 작성자에게 알림
            posts = self.load_posts()
            post = posts[posts["post_id"] == post_id]
            if not post.empty:
                post_author = post.iloc[0]["user_id"]
                if post_author != user_id:  
                    self.create_notification(post_author, "retweet", user_id, post_id=post_id)
        
            return True, "리트윗!"

    # -------------------- Follows --------------------
    def is_following(self, follower_id, followed_id):
        follows = self.load_follows()
        return ((follows["follower_id"] == follower_id) & (follows["followed_id"] == followed_id)).any()

    def toggle_follow(self, follower_id, followed_id):
        """팔로우 토글 + 알림 생성"""
        if follower_id == followed_id:
            return False, "자기 자신을 팔로우할 수 없습니다."
    
        follows = self.load_follows()
        mask = (follows["follower_id"] == follower_id) & (follows["followed_id"] == followed_id)
    
        if mask.any():
            # 언팔로우
            follows = follows[~mask]
            self.save_follows(follows)
            return False, "팔로우 취소"
        else:
            # 팔로우
            row = {
                "follower_id": follower_id,
                "followed_id": followed_id,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            if follows.empty:
                follows = pd.DataFrame([row])
            else:
                follows = pd.concat([follows, pd.DataFrame([row])], ignore_index=True)
            self.save_follows(follows)
        
            # 팔로우 당한 사용자에게 알림 생성
            self.create_notification(followed_id, "follow", follower_id)
        
            return True, "팔로우!"

    def count_following(self, user_id):
        follows = self.load_follows()
        return int((follows["follower_id"] == user_id).sum())

    def count_followers(self, user_id):
        follows = self.load_follows()
        return int((follows["followed_id"] == user_id).sum())

    # -------------------- Comments & Likes on comments --------------------
    def _next_comment_id(self, comments: pd.DataFrame):
        if comments.empty: return "comment_001"
        mx = comments["comment_id"].str.replace("comment_", "", regex=False).astype(int).max()
        return f"comment_{mx+1:03d}"

    def add_comment(self, user_id, post_id, content):
        """댓글 추가 + 알림 생성"""
        comments = self.load_comments()
        cid = self._next_comment_id(comments)
        row = {
            "comment_id": cid,
            "post_id": post_id,
            "user_id": user_id,
            "content": str(content or "").strip(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        if comments.empty:
            comments = pd.DataFrame([row])
        else:
            comments = pd.concat([comments, pd.DataFrame([row])], ignore_index=True)
        self.save_comments(comments)
    
        # 게시물 작성자에게 알림
        posts = self.load_posts()
        post = posts[posts["post_id"] == post_id]
        if not post.empty:
            post_author = post.iloc[0]["user_id"]
            self.create_notification(post_author, "comment", user_id, post_id=post_id, comment_id=cid)
    
        return True, "댓글 등록!"

    def get_comments(self, post_id):
        df = self.load_comments()
        return df[df["post_id"] == post_id].sort_values(by="timestamp", ascending=True)

    def count_comment_likes(self, comment_id):
        cl = self.load_comment_likes()
        return int((cl["comment_id"] == comment_id).sum())

    def toggle_like_comment(self, user_id, comment_id):
        """댓글 좋아요 토글 + 알림 생성"""
        cl = self.load_comment_likes()
        mask = (cl["user_id"] == user_id) & (cl["comment_id"] == comment_id)
    
        if mask.any():
            cl = cl[~mask]
            self.save_comment_likes(cl)
            return False, "댓글 좋아요 취소"
        else:
            row = {"user_id": user_id, "comment_id": comment_id, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            if cl.empty:
                cl = pd.DataFrame([row])
            else:
                cl = pd.concat([cl, pd.DataFrame([row])], ignore_index=True)
            self.save_comment_likes(cl)
        
            # 댓글 작성자에게 알림
            comments = self.load_comments()
            comment = comments[comments["comment_id"] == comment_id]
            if not comment.empty:
                comment_author = comment.iloc[0]["user_id"]
                if comment_author != user_id:  
                    self.create_notification(comment_author, "comment_like", user_id, comment_id=comment_id)
        
            return True, "댓글 좋아요!"

    # -------------------- Aggregations for Profile & Lists --------------------
    def count_received_likes(self, user_id):
        """내가 쓴 게시글 + 내가 쓴 댓글에 받은 좋아요 합계"""
        posts = self.load_posts()
        likes = self.load_likes()
        my_posts = posts[posts["user_id"] == user_id]["post_id"].tolist()
        post_like_cnt = int(likes[likes["post_id"].isin(my_posts)].shape[0])

        comments = self.load_comments()
        my_comments = comments[comments["user_id"] == user_id]["comment_id"].tolist()
        cl = self.load_comment_likes()
        comment_like_cnt = int(cl[cl["comment_id"].isin(my_comments)].shape[0])
        return post_like_cnt + comment_like_cnt

    def list_liked_posts_by_user(self, user_id):
        likes = self.load_likes()
        posts = self.load_posts()
        ids = likes[likes["user_id"] == user_id]["post_id"].tolist()
        return posts[posts["post_id"].isin(ids)].sort_values(by="timestamp", ascending=False)

    def list_retweeted_posts_by_user(self, user_id):
        rts = self.load_retweets()
        posts = self.load_posts()
        ids = rts[rts["user_id"] == user_id]["post_id"].tolist()
        return posts[posts["post_id"].isin(ids)].sort_values(by="timestamp", ascending=False)
    
    def delete_comment(self, user_id, comment_id):
        comments = self.load_comments()
        comment = comments[comments["comment_id"] == comment_id]

        if comment.empty:
            return False, "댓글이 존재하지 않습니다."

        # 본인 댓글만 삭제 가능
        if comment.iloc[0]["user_id"] != user_id:
            return False, "본인 댓글만 삭제할 수 있습니다."

        # 해당 댓글 삭제
        comments = comments[comments["comment_id"] != comment_id]
        self.save_comments(comments)

        # 해당 댓글의 좋아요도 삭제
        comment_likes = self.load_comment_likes()
        comment_likes = comment_likes[comment_likes["comment_id"] != comment_id]
        self.save_comment_likes(comment_likes)

        return True, "댓글 삭제 완료!"
    
    def get_following_posts(self, user_id):
        """내가 팔로우한 사용자들의 게시물만 가져오기"""
        follows_df = self.load_follows()
        posts_df = self.load_posts()
    
        if follows_df.empty or posts_df.empty:
            return pd.DataFrame()
    
        # 내가 팔로우한 사용자들의 ID 목록
        following_ids = follows_df[follows_df["follower_id"] == user_id]["followed_id"].tolist()
    
        if not following_ids:
            return pd.DataFrame()
    
        # 팔로우한 사용자들의 게시물만 필터링
        following_posts = posts_df[posts_df["user_id"].isin(following_ids)]
        return following_posts.sort_values(by="timestamp", ascending=False)
    
    # -------------------- 알림 시스템 --------------------
    def _next_notification_id(self, notifications: pd.DataFrame):
        if notifications.empty: 
            return "noti_001"
        mx = notifications["notification_id"].str.replace("noti_", "", regex=False).astype(int).max()
        return f"noti_{mx+1:03d}"

    # 2. create_notification 함수 안전성 강화
    def create_notification(self, user_id, notification_type, from_user_id, post_id=None, comment_id=None, custom_message=None):
        """알림 생성"""
        notifications = self.load_notifications()

        # 본인에게는 알림을 보내지 않음
        if user_id == from_user_id:
            return

        # 사용자 알림 설정 확인
        if not self.is_notification_enabled(user_id, notification_type):
            return

        # 알림 메시지 생성 - 안전한 사용자명 가져오기
        users = self.load_users()
        from_user_data = users[users["user_id"] == from_user_id]
    
        # ✅ 안전한 사용자명 처리
        if not from_user_data.empty:
            from_username = from_user_data.iloc[0]["username"]
        else:
            from_username = from_user_id  # 사용자가 없으면 ID로 대체

        messages = {
            "follow": f"🫵 {from_username}님이 당신을 팔로우했습니다",
            "like": f"👍 {from_username}님이 회원님의 게시물을 좋아합니다",
            "comment": f"💬 {from_username}님이 회원님의 게시물에 댓글을 달았습니다",
            "comment_like": f"👍 {from_username}님이 회원님의 댓글을 좋아합니다",
            "retweet": f"🔁 {from_username}님이 회원님의 게시물을 리트윗했습니다"
        }

        message = custom_message or messages.get(notification_type, "새로운 알림이 있습니다")

        notification_id = self._next_notification_id(notifications)
        row = {
            "notification_id": notification_id,
            "user_id": user_id,
            "type": notification_type,
            "from_user_id": from_user_id,
            "post_id": post_id or "",
            "comment_id": comment_id or "",
            "message": message,
            "is_read": False,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if notifications.empty:
            notifications = pd.DataFrame([row])
        else:
            notifications = pd.concat([notifications, pd.DataFrame([row])], ignore_index=True)
        self.save_notifications(notifications)


    def get_user_notifications(self, user_id, limit=50):
        """사용자 알림 목록 가져오기"""
        notifications = self.load_notifications()
        user_notifications = notifications[notifications["user_id"] == user_id]
        return user_notifications.sort_values(by="timestamp", ascending=False).head(limit)

    def get_unread_count(self, user_id):
        """읽지 않은 알림 개수"""
        try:
            notifications = self.load_notifications()
            if notifications.empty:
                return 0
        
            # 조건 확인
            mask = (notifications["user_id"] == user_id) & (notifications["is_read"] == False)
            count = mask.sum()
            return int(count)
        except Exception as e:
            print(f"알림 개수 계산 에러: {e}")
            return 0

    def mark_notification_read(self, notification_id):
        """알림 읽음 처리"""
        notifications = self.load_notifications()
        notifications.loc[notifications["notification_id"] == notification_id, "is_read"] = True
        self.save_notifications(notifications)

    def mark_all_notifications_read(self, user_id):
        """모든 알림 읽음 처리"""
        notifications = self.load_notifications()
        notifications.loc[notifications["user_id"] == user_id, "is_read"] = True
        self.save_notifications(notifications)

    def delete_notification(self, notification_id, user_id):
        """알림 삭제 (본인만 가능)"""
        notifications = self.load_notifications()
        notifications = notifications[~((notifications["notification_id"] == notification_id) & (notifications["user_id"] == user_id))]
        self.save_notifications(notifications)

    def get_notification_settings(self, user_id):
        """사용자 알림 설정 가져오기"""
        settings = self.load_notification_settings()
        user_settings = settings[settings["user_id"] == user_id]
    
        if user_settings.empty:
            # 기본 설정 생성
            default_settings = {
                "user_id": user_id,
                "follow_notifications": True,
                "like_notifications": True,
                "comment_notifications": True,
                "retweet_notifications": True
            }
            settings = pd.concat([settings, pd.DataFrame([default_settings])], ignore_index=True)
            self.save_notification_settings(settings)
            return default_settings
    
        return user_settings.iloc[0].to_dict()

    def update_notification_settings(self, user_id, follow=True, like=True, comment=True, retweet=True):
        """알림 설정 업데이트"""
        settings = self.load_notification_settings()
    
        # 기존 설정 제거
        settings = settings[settings["user_id"] != user_id]
    
        # 새 설정 추가
        new_settings = {
            "user_id": user_id,
            "follow_notifications": follow,
            "like_notifications": like,
            "comment_notifications": comment,
            "retweet_notifications": retweet
        }
    
        if settings.empty:
            settings = pd.DataFrame([new_settings])
        else:
            settings = pd.concat([settings, pd.DataFrame([new_settings])], ignore_index=True)
        self.save_notification_settings(settings)

    def is_notification_enabled(self, user_id, notification_type):
        """특정 알림 타입이 활성화되어 있는지 확인"""
        settings = self.get_notification_settings(user_id)
        type_mapping = {
            "follow": "follow_notifications",
            "like": "like_notifications", 
            "comment": "comment_notifications",
            "comment_like": "like_notifications",  
            "retweet": "retweet_notifications"
        }
    
        setting_key = type_mapping.get(notification_type, "follow_notifications")
        return bool(settings.get(setting_key, True))
    
    def delete_all_notifications(self, user_id):
        """사용자의 모든 알림 삭제"""
        notifications = self.load_notifications()
        # 해당 사용자의 알림만 제거
        notifications = notifications[notifications["user_id"] != user_id]
        self.save_notifications(notifications)
        return True, "모든 알림이 삭제되었습니다!"
    
    # 핫플레이스 등록
    def create_hotplace(self, user_id, place_name, latitude, longitude, category, address, description):
        """핫플레이스 등록"""
        hotplaces = self.load_hotplaces()
        place_id = f"place_{len(hotplaces) + 1:03d}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        row = {
            "place_id": place_id,
            "user_id": user_id,
            "place_name": place_name,
            "latitude": latitude,
            "longitude": longitude,
            "category": category,
            "address": address,
            "description": description,
            "timestamp": timestamp
        }
        if hotplaces.empty:
            hotplaces = pd.DataFrame([row])
        else:
            hotplaces = pd.concat([hotplaces, pd.DataFrame([row])], ignore_index=True)
        self.save_hotplaces(hotplaces)
        return True, "핫플레이스 등록 완료!"

    # 팔로잉 사용자들의 핫플레이스 조회
    def get_following_hotplaces(self, user_id):
        """내가 팔로우한 사용자들의 핫플레이스"""
        follows_df = self.load_follows()
        hotplaces_df = self.load_hotplaces()
    
        if follows_df.empty or hotplaces_df.empty:
            return pd.DataFrame()
    
        # 내가 팔로우한 사용자들의 ID 목록
        following_ids = follows_df[follows_df["follower_id"] == user_id]["followed_id"].tolist()
    
        if not following_ids:
            return pd.DataFrame()
    
        # 팔로우한 사용자들의 핫플레이스만 필터링
        following_hotplaces = hotplaces_df[hotplaces_df["user_id"].isin(following_ids)]
        return following_hotplaces.sort_values(by="timestamp", ascending=False)

    # 핫플레이스 좋아요 토글
    def toggle_like_place(self, user_id, place_id):
        """핫플레이스 좋아요 토글"""
        likes = self.load_place_likes()
        mask = (likes["user_id"] == user_id) & (likes["place_id"] == place_id)
    
        if mask.any():
            likes = likes[~mask]
            self.save_place_likes(likes)
            return False, "좋아요 취소"
        else:
            row = {"user_id": user_id, "place_id": place_id, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            if likes.empty:
                likes = pd.DataFrame([row])
            else:
                likes = pd.concat([likes, pd.DataFrame([row])], ignore_index=True)
            self.save_place_likes(likes)
            return True, "좋아요!"

    # 핫플레이스 좋아요 수
    def count_place_likes(self, place_id):
        """핫플레이스 좋아요 수"""
        likes = self.load_place_likes()
        return int((likes["place_id"] == place_id).sum())

    # 리뷰 추가
    def add_place_review(self, user_id, place_id, rating, review_text):
        """핫플레이스 리뷰 추가"""
        reviews = self.load_place_reviews()
        review_id = f"review_{len(reviews) + 1:03d}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        row = {
            "review_id": review_id,
            "place_id": place_id,
            "user_id": user_id,
            "rating": rating,
            "review_text": review_text,
            "timestamp": timestamp
        }
        if reviews.empty:
            reviews = pd.DataFrame([row])
        else:
            reviews = pd.concat([reviews, pd.DataFrame([row])], ignore_index=True)
        self.save_place_reviews(reviews)
        return True, "리뷰 등록 완료!"

    # 특정 장소 리뷰 조회
    def get_place_reviews(self, place_id):
        """특정 핫플레이스의 리뷰들"""
        reviews = self.load_place_reviews()
        return reviews[reviews["place_id"] == place_id].sort_values(by="timestamp", ascending=False)

    # 평균 평점 계산
    def get_place_average_rating(self, place_id):
        """핫플레이스 평균 평점"""
        reviews = self.load_place_reviews()
        place_reviews = reviews[reviews["place_id"] == place_id]
    
        if place_reviews.empty:
            return 0.0
    
        return round(place_reviews["rating"].mean(), 1)

    # 모든 핫플레이스 조회 (검색 포함)
    def get_all_hotplaces_with_stats(self):
        """모든 핫플레이스를 통계와 함께 조회"""
        hotplaces = self.load_hotplaces()
    
        if hotplaces.empty:
            return pd.DataFrame()
    
        # 각 핫플레이스의 좋아요 수와 평균 평점 추가
        hotplaces_with_stats = hotplaces.copy()
        hotplaces_with_stats["likes_count"] = hotplaces_with_stats["place_id"].apply(self.count_place_likes)
        hotplaces_with_stats["avg_rating"] = hotplaces_with_stats["place_id"].apply(self.get_place_average_rating)
    
        return hotplaces_with_stats.sort_values(by="timestamp", ascending=False)
    
    # user_manager.py의 UserManager 클래스에 추가
    def delete_hotplace(self, user_id, place_id):
        """핫플레이스 삭제 (본인만 가능)"""
        hotplaces = self.load_hotplaces()
        place = hotplaces[hotplaces["place_id"] == place_id]
    
        if place.empty:
            return False, "핫플레이스가 존재하지 않습니다."
    
        # 본인 핫플레이스만 삭제 가능
        if place.iloc[0]["user_id"] != user_id:
            return False, "본인 핫플레이스만 삭제할 수 있습니다."
    
        # 핫플레이스 삭제
        hotplaces = hotplaces[hotplaces["place_id"] != place_id]
        self.save_hotplaces(hotplaces)
    
        # 관련 좋아요 삭제
        likes = self.load_place_likes()
        likes = likes[likes["place_id"] != place_id]
        self.save_place_likes(likes)
    
        # 관련 리뷰 삭제
        reviews = self.load_place_reviews()
        reviews = reviews[reviews["place_id"] != place_id]
        self.save_place_reviews(reviews)
    
        return True, "핫플레이스 삭제 완료!"