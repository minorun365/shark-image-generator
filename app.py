import streamlit as st
import time
from PIL import Image
import os
from shark_agent import create_shark_with_agent
import re

st.set_page_config(
    page_title="サメ上手 #ssmjp",
    page_icon="🦈",
    layout="centered"
)

def extract_filename_from_response(response):
    """レスポンスからファイル名を抽出"""
    match = re.search(r'shark_\d+\.png', str(response))
    if match:
        return match.group(0)
    return None

def main():
    st.title("🦈 サメ上手 #ssmjp")
    st.write("AWS Strands AgentsとClaude Sonnet 4を使ってサメの説明を生成し、Nova Canvasで画像を作成します")
    
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        shark_type = st.text_input(
            "どんなサメを生成しますか？",
            placeholder="例: カラフルなハンマーヘッドシャーク、ホホジロザメ、ジンベエザメ"
        )
    
    with col2:
        generate_button = st.button("🎨 生成", type="primary", use_container_width=True)
    
    if generate_button and shark_type:
        with st.spinner("Strandsエージェントがサメ画像を生成中..."):
            try:
                response = create_shark_with_agent(shark_type)
                
                
                filename = extract_filename_from_response(str(response))
                if filename and os.path.exists(filename):
                    image = Image.open(filename)
                    
                    st.success("画像生成完了！")
                    st.image(image, caption=shark_type, use_container_width=True)
                    
                    with open(filename, "rb") as file:
                        st.download_button(
                            label="画像をダウンロード",
                            data=file.read(),
                            file_name=filename,
                            mime="image/png"
                        )
                    
                    st.session_state.generated_images.append({
                        'filename': filename,
                        'shark_type': shark_type,
                        'timestamp': time.time()
                    })
                else:
                    st.warning("画像ファイルが見つかりませんでした。AWS認証情報が正しく設定されていることを確認してください。")
                    
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
                st.info("AWS認証情報が正しく設定されていることを確認してください。")
    
    with st.expander("🔧 セットアップ方法"):
        st.write("""
        ### 必要な準備:
        1. **AWS認証情報の設定**
           - `.env`ファイルを作成し、AWS認証情報を設定
           - Bedrock Claude 3.5 Sonnetへのアクセス権限が必要
        
        2. **MCPサーバーの起動**
           ```bash
           uvx mcp-server-aws-nova-canvas
           ```
        
        3. **アプリの起動**
           ```bash
           pip install -r requirements.txt
           streamlit run app.py
           ```
        """)
    
    with st.expander("📚 使い方"):
        st.write("""
        1. テキストボックスに生成したいサメの特徴を入力します
        2. 「生成」ボタンをクリックします
        3. Strands Agentが自動的に：
           - サメの詳細な説明を生成
           - Nova Canvasで画像を生成
        4. 生成された画像はダウンロードできます
        
        ### 入力例:
        - ホホジロザメ
        - カラフルなハンマーヘッドシャーク
        - ジンベエザメ
        - 虹色に光るサメ
        """)
    
    if st.session_state.generated_images:
        with st.expander("📷 生成履歴"):
            for img in reversed(st.session_state.generated_images[-5:]):
                st.write(f"- {img['shark_type']} ({img['filename']})")

if __name__ == "__main__":
    main()