# user_manager.py
import pandas as pd
import os
from datetime import datetime

class UserManager:
    def __init__(self):
        self.csv_path = 'data/users.csv'
        self.ensure_csv_exists()

    def ensure_csv_exists(self):
        """CSV 파일이 없으면 생성"""
        if not os.path.exists(self.csv_path):
            os.makedirs('data', exist_ok=True)
            empty_df = pd.DataFrame(columns=['user_id', 'username', 'password', 'created_at'])
            empty_df.to_csv(self.cs