# BuaaaBot

BuaaaBotは、創作を支援する便利なツールとユニークなユーモア機能を搭載したDiscord向けのマルチツールBotです！  
背景切り抜きやYouTube基準でのラウドネスペナルティ測定など、創作活動をサポートする一方、クイズゲームや名前から性別をあてる機能など遊び心満載の機能も楽しめます！

BuaaaBotは、ほとんどの機能をAPIに頼っているので、各自でAPIキーを取得する必要があります！( 詳細は下へ )

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
    git clone https://github.com/yh2237/buaaabot.git
    cd buaaabot
    ```
2. 仮想環境を作って入る:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. 必要なパッケージをインストール！:
    ```bash
    pip install -r requirements.txt
    ```
4. `.env`ファイルを以下に合わせて作成し、Discordなどのトークンを入力してください：
    ```
    DISCORD_TOKEN=""
    BINGKEY=""
    COHERE=""
    REMOVEBG=""
    GEMINI=""
    ```
    なお、このトークンはそれぞれ以下の用途で使用されます。
- DISCORD_TOKEN：Discordボットを動かすために必要
- BINGKEY：画像の検索に使用
- COHERE：精度を求める回答の際に使用
- REMOVEBG：背景の切り抜きに使用
- GEMINI：精度より速度を求める際や、画像の処理をする際に使用
  
5. `config/config.yml`内ののstartNoticeChannelを、起動通知してほしいテキストチャンネルのIDに置き換える

6. あなたのPCに合った、最新のchromedriverをダウンロードし、bot.pyと同じ場所に配置してください！
   [ダウンロード](https://googlechromelabs.github.io/chrome-for-testing/#stable)

## 🚀 使い方

1. Botを起動:
    ```bash
    python bot.py
    ```
2. DiscordサーバーにBotを追加し、スラッシュコマンドより使い方を参照してください！

## 🤝 コントリビュート

フィードバックや改善案は大歓迎です！プルリクエストを送ってください！

## 💛 Special Thanks

#### れいね（環境構築テスト）
Windowsでの環境構築を問題なく行なうためのテストを手伝っていただきました！
ありがとうございます。

## ❓ よくある問題
- 「ファイルが見つかりません」と表示された場合：原因は調査中ですが、その状態でエンターを押すと続行できます。
- moviepy関連のエラーが発生した場合：以下の手順に従ってください（moviepyのバージョン変更をするので慎重に！）
1. `pip uninstall moviepy`でmoviepyを一旦アンインストール
2. `pip install moviepy==2.0.0.dev2`で互換性があるバージョンでインストール

## 📜 ライセンス

このプロジェクトは、[MITライセンス](LICENSE)のもとで公開されています。
