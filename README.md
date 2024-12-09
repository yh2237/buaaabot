# BuaaaBot

BuaaaBotは、創作を支援する便利なツールとユニークなユーモア機能を搭載したDiscord向けのマルチツールBotです！  
背景切り抜きやYouTube基準でのラウドネスペナルティ測定など、創作活動をサポートする一方、クイズゲームや名前から性別をあてる機能など遊び心満載の機能も楽しめます！

BuaaaBotは、ほとんどの機能をAPIに頼っているので、各自でAPIキーを取得する必要があります！

## 🌟 主な機能

### 創作支援ツール
- **画像の背景切り抜き**：簡単に背景を切り抜けます！
- **YouTube基準でのラウドネスペナルティ測定**：音楽や音MAD制作などに活用できます！
- **画像からアニメの場面を特定**：アニメシーンの逆引き検索に対応！
- **Webページのスクリーンショット**：指定URLの見た目をそのままフルページキャプチャ！

### その他
- **Google Geminiと対話**：AIとのやり取りが可能！
- **画像検索機能**：検索ワードからさっと検索！
- **クイズゲーム**：問題生成と答え合わせが可能なクイズ機能！
- **名前から性別を判定**：名前から性別を推測します！

## 📦 インストール

1. リポジトリをクローン！:
    ```bash
    git clone https://github.com/buachigithub/buaaabot.git
    cd BuaaaBot
    ```
2. 必要なパッケージをインストール！:
    ```bash
    pip install -r requirements.txt
    ```
3. `.env`ファイルを以下に合わせて作成し、Discordなどのトークンを入力してください：
    ```
    DISCORD_TOKEN=""
    BINGKEY=""
    OPENAI=""
    COHERE=""
    REMOVEBG=""
    GEMINI=""
    ```
4. `bot.py`内の116行目を指定の通りに書き換える
   ただ単に実装がだるかっただけですごめんなさい。

5. あなたのPCにあったchromedriverをダウンロードする
   [ダウンロード](https://googlechromelabs.github.io/chrome-for-testing/#stable)

## 🚀 使い方

1. Botを起動:
    ```bash
    python bot.py
    ```
2. DiscordサーバーにBotを追加し、スラッシュコマンドから使い方を参照してください！

## 🤝 コントリビュート

フィードバックや改善案は大歓迎です！以下の手順でご協力ください：
1. このリポジトリをフォークします
2. ブランチを作成します (`git checkout -b feature/YourFeature`)
3. 変更をコミットします (`git commit -m 'Add YourFeature'`)
4. プッシュします (`git push origin feature/YourFeature`)
5. プルリクエストを作成しましょう！

## 💛 Special Thanks

れいね

## 📜 ライセンス

このプロジェクトは、[MITライセンス](LICENSE)のもとで公開されています。
