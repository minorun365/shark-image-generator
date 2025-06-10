import os
import streamlit as st
from dotenv import load_dotenv

# ローカル環境では.envファイルを読み込み
load_dotenv()

class Config:
    # Streamlit CloudではSecretsを使用、ローカルでは環境変数を使用
    if hasattr(st, 'secrets') and 'default' in st.secrets:
        AWS_REGION = st.secrets['default']['AWS_REGION']
        AWS_ACCESS_KEY_ID = st.secrets['default']['AWS_ACCESS_KEY_ID']
        AWS_SECRET_ACCESS_KEY = st.secrets['default']['AWS_SECRET_ACCESS_KEY']
    else:
        AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
        AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')