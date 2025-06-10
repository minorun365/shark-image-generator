from strands import Agent, tool
import requests
import base64
from PIL import Image
from io import BytesIO
import os
import time
from config import Config

@tool
def generate_shark_image(prompt: str, width: int = 512, height: int = 512) -> dict:
    """
    AWS Nova Canvasを使用してサメの画像を生成します。
    
    Args:
        prompt: 画像生成用のプロンプト（英語）
        width: 画像の幅（デフォルト: 512）
        height: 画像の高さ（デフォルト: 512）
    
    Returns:
        生成結果を含む辞書
    """
    try:
        import boto3
        import json
        import random
        
        # Bedrock Runtimeクライアントを作成
        client = boto3.client(
            "bedrock-runtime", 
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        
        # モデルIDを設定
        model_id = "amazon.nova-canvas-v1:0"
        
        # ランダムシードを生成
        seed = random.randint(0, 858993460)
        
        # リクエストペイロードを作成
        native_request = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {"text": prompt},
            "imageGenerationConfig": {
                "seed": seed,
                "quality": "standard",
                "height": height,
                "width": width,
                "numberOfImages": 1,
            },
        }
        
        # JSONに変換
        request = json.dumps(native_request)
        
        # モデルを呼び出し
        response = client.invoke_model(modelId=model_id, body=request)
        
        # レスポンスをデコード
        model_response = json.loads(response["body"].read())
        
        # 画像データを抽出
        base64_image_data = model_response["images"][0]
        
        # 画像を保存
        timestamp = int(time.time())
        filename = f"shark_{timestamp}.png"
        
        image_data = base64.b64decode(base64_image_data)
        with open(filename, "wb") as file:
            file.write(image_data)
        
        return {
            "success": True,
            "filename": filename,
            "message": f"画像を {filename} として保存しました"
        }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"画像生成エラー: {str(e)}"
        }

@tool
def create_shark_description(shark_type: str) -> str:
    """
    指定されたサメのタイプから、画像生成用の詳細な説明を作成します。
    
    Args:
        shark_type: サメの種類や特徴（日本語）
    
    Returns:
        画像生成用の英語の詳細説明
    """
    descriptions = {
        "ホホジロザメ": "A majestic great white shark swimming in crystal clear ocean waters, powerful muscular body, sharp triangular teeth visible, dark grey upper body fading to white belly, piercing black eyes",
        "ハンマーヘッドシャーク": "A distinctive hammerhead shark with its iconic T-shaped head, swimming gracefully through tropical waters, bronze-grey coloration, wide-set eyes on the hammer extensions",
        "ジンベエザメ": "A gentle whale shark, the largest fish in the ocean, distinctive spotted pattern across its massive body, wide flat head with small eyes, filter-feeding mouth open",
        "カラフルな": "A vibrant and colorful shark with iridescent scales reflecting rainbow colors, swimming through coral reef waters, bioluminescent patterns along its body"
    }
    
    for key, value in descriptions.items():
        if key in shark_type:
            return value
    
    return f"A realistic {shark_type} shark swimming in natural ocean environment, detailed texture and anatomy, professional wildlife photography style"

shark_agent = Agent(
    tools=[generate_shark_image, create_shark_description],
    system_prompt="""あなたはサメ画像生成の専門家です。
    ユーザーのリクエストに基づいて、以下の手順でサメの画像を生成してください：
    
    1. まず create_shark_description ツールを使って、日本語のサメの説明から英語の詳細な画像生成プロンプトを作成します
    2. 次に generate_shark_image ツールを使って、そのプロンプトからサメの画像を生成します
    3. 生成結果をユーザーに報告します
    
    常に丁寧で分かりやすい日本語で応答してください。"""
)

def create_shark_with_agent(shark_type: str):
    """Strandsエージェントを使ってサメ画像を生成"""
    response = shark_agent(f"{shark_type}のサメ画像を生成してください")
    return response