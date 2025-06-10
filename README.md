# 🦈 SAME JAWS - サメ画像生成アプリ

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://same-jaws.streamlit.app)

AWS Strands AgentsとBedrock Claude 3.7 Sonnetを使用してサメの説明を生成し、AWS Nova Canvasで高品質なサメ画像を生成するStreamlitアプリケーションです。

## 🚀 ライブデモ

[**https://same-jaws.streamlit.app**](https://same-jaws.streamlit.app) でアプリを試してみてください！

## 📸 スクリーンショット

日本語でサメの特徴を入力するだけで、AIが自動的に詳細な英語プロンプトを生成し、Nova Canvasで美しいサメ画像を作成します。

## 機能

- 日本語でサメの特徴を入力
- Strands Agentが自動的に英語の詳細な説明を生成
- Nova Canvasで高品質なサメ画像を生成
- 生成した画像のダウンロード機能

## 必要な環境

- Python 3.8以上
- AWS アカウント
- AWS Bedrock Claude 3.7 Sonnetへのアクセス権限
- AWS Bedrock Nova Canvasへのアクセス権限

## 🛠️ ローカルセットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/minorun365/same-jaws.git
cd same-jaws
```

### 2. 仮想環境の作成と有効化

```bash
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

`.env.example`をコピーして`.env`を作成し、AWS認証情報を設定します：

```bash
cp .env.example .env
```

`.env`ファイルを編集：
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
```

### 5. AWS Bedrockの設定

1. AWSコンソールでBedrock > Model accessに移動
2. 以下のモデルへのアクセスを有効化：
   - Claude 3.7 Sonnet (`anthropic.claude-3-5-sonnet-*`)
   - Nova Canvas (`amazon.nova-canvas-v1:0`)
3. IAMユーザーに `bedrock:InvokeModel` 権限を付与

## ☁️ Streamlit Cloudへのデプロイ

1. GitHubにリポジトリをフォーク
2. [Streamlit Cloud](https://streamlit.io/cloud) にアクセス
3. 「New app」をクリックしてリポジトリを選択
4. Settings > Secrets で以下を設定：

```toml
[aws]
AWS_ACCESS_KEY_ID = "AKIA..."
AWS_SECRET_ACCESS_KEY = "your-secret-access-key"
AWS_DEFAULT_REGION = "us-east-1"
```

5. デプロイ完了！

## 使い方

### アプリケーションの起動

```bash
streamlit run app.py
```

ブラウザが自動的に開き、`http://localhost:8501`でアプリケーションにアクセスできます。

### 画像生成の手順

1. テキストボックスにサメの特徴を日本語で入力
   - 例: "カラフルなハンマーヘッドシャーク"
   - 例: "ホホジロザメ"
   - 例: "虹色に光るジンベエザメ"

2. 「生成」ボタンをクリック

3. Strands Agentが以下を自動実行：
   - 入力された日本語から英語の詳細説明を生成
   - Nova Canvasを使用して画像を生成

4. 生成された画像が表示され、ダウンロードボタンから保存可能

## トラブルシューティング

### エラー: "画像生成エラー"
- AWS認証情報が正しいか確認
- Nova Canvasモデルへのアクセス権限があるか確認

### エラー: "AWS認証エラー"
- `.env`ファイル（ローカル）またはStreamlit Secrets（クラウド）の認証情報が正しいか確認
- IAMユーザーに`bedrock:InvokeModel`権限があるか確認
- 使用リージョン（us-east-1）が正しいか確認

### 画像が生成されない
- AWS Nova Canvasへのアクセス権限を確認
- リージョンが正しいか確認（us-east-1）

## 📁 プロジェクト構造

```
same-jaws/
├── app.py                          # Streamlitメインアプリケーション
├── shark_agent.py                  # Strands Agentの定義
├── config.py                       # 設定ファイル（ローカル/クラウド対応）
├── requirements.txt                # Python依存関係
├── .env.example                    # ローカル用環境変数の例
├── .streamlit/
│   └── secrets.toml.example        # Streamlit Cloud用設定例
├── .gitignore                      # Git除外ファイル
└── README.md                       # このファイル
```

## 🔧 技術スタック

- **フロントエンド**: Streamlit
- **AIエージェント**: AWS Strands Agents
- **言語モデル**: Amazon Bedrock Claude 3.7 Sonnet
- **画像生成**: Amazon Bedrock Nova Canvas
- **デプロイ**: Streamlit Cloud

## 🤝 コントリビューション

プルリクエストやイシューを歓迎します！

## 📄 ライセンス

MITライセンス

## ライセンス

このプロジェクトはMITライセンスで公開されています。