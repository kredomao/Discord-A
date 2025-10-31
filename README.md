# Study Motivation Bot (GitHub Push → Discord 通知)

毎日の Push を習慣化するための最小構成（MVP）。
GitHub Webhook で Push を検知 → 連続日数/レベルを更新 → Discord に通知します。

## 📋 機能

- ✅ **同期版** (`notify_sync.py`) - シンプルで確実な送信
- ⚡ **非同期版** (`notify_async.py`) - 高頻度送信や並列処理に適している
- 🎨 **Embed版** (`notify_embed.py`) - リッチなメッセージ（色付き、フィールド付き）
- ⏰ **定期送信** (`scheduled_notify.py`) - APScheduler を使った自動通知

## 構成

```
study-motivation-bot/
 ├─ tracker.py        # 連続日数 & レベル/EXP 管理
 ├─ data.json         # 保存データ
 └─ webhook_server.py # GitHub Webhook 受信（Flask）
```

## 🚀 セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env` を作成して Discord Webhook URL を設定（`.env.example` をコピー）

```bash
# .env ファイル
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
```

**⚠️ 重要**: `.env` ファイルは Git にコミットしないでください（`.gitignore` に含まれています）

### 3. Discord Webhook の作成方法

1. Discord を開き、通知を送りたいサーバーを選ぶ
2. **サーバー設定** → **統合** → **Webhook** → **新しいWebhookを作成**
3. チャンネルを選択し、Webhook URL をコピー
4. `.env` ファイルに貼り付け

## 📝 使い方

### 同期版（シンプル）

```python
from notify_sync import send_message

# シンプルなメッセージ送信
send_message("こんにちは！通知テストです")

# カスタムユーザー名付き
send_message("メッセージ", username="MyBot")
```

実行:
```bash
python notify_sync.py
```

### 非同期版

```python
import asyncio
from notify_async import send_message
from aiohttp import ClientSession

async def main():
    async with ClientSession() as session:
        await send_message(session, "非同期通知テスト")

asyncio.run(main())
```

実行:
```bash
python notify_async.py
```

### Embed版（リッチなメッセージ）

```python
from notify_embed import create_success_embed, send_message

embed = create_success_embed(
    title="✅ ジョブ完了",
    description="処理が正常に完了しました",
    fields=[
        {"name": "処理時間", "value": "12分34秒", "inline": True},
        {"name": "ステータス", "value": "成功", "inline": True},
    ]
)

send_message(content="", embeds=[embed], username="JobBot")
```

実行:
```bash
python notify_embed.py
```

### 定期送信（別テンプレート）

```bash
python scheduled_notify.py
```

スケジュール例:
- **毎時0分**: システム状態通知
- **毎日9:00**: 日次レポート

カスタマイズは `scheduled_notify.py` の `setup_schedules()` を編集してください。

## GitHub 側設定（Webhook）

Repository → Settings → Webhooks → Add webhook で以下を設定：
- Payload URL: `http://<あなたのIPまたはドメイン>:8000/github`
- Content type: `application/json`
- Events: `Just the push event`

ローカル開発なら `ngrok` を使って公開 URL を作成できます：
```bash
ngrok http 8000
```

## 🔧 カスタマイズ

### リトライ設定

`notify_sync.py` の `send_message()` 関数でリトライ回数や待機時間を変更できます：

```python
send_message(
    "メッセージ",
    max_retries=5,      # 最大リトライ回数
    retry_delay=2.0     # リトライ間の待機時間（秒）
)
```

### スケジュール設定

` APScheduler` の Cron 形式で自由に設定可能：

```python
# 毎時30分
CronTrigger(minute=30)

# 毎日の午後3時
CronTrigger(hour=15, minute=0)

# 毎週月曜日の朝9時
CronTrigger(day_of_week='mon', hour=9, minute=0)
```

## ⚠️ 注意点

### セキュリティ

- **Webhook URL は機密情報**です。公開リポジトリにコミットしないでください
- Webhook URL が漏洩した場合は、Discord で削除して新規作成してください

### レート制限

- Discord のレート制限に注意してください
- コードには自動リトライ機能が実装されています（`Retry-After` ヘッダーを確認）
- 大量送信時は適切な間隔を空けてください

### エラーハンドリング

すべてのスクリプトにはエラーハンドリングとログ出力が実装されています。
送信に失敗した場合は、ログを確認してください。

## 📚 参考リンク

- [Intro to Webhooks（Discord Support）](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks?utm_source=chatgpt.com)
- [Webhook Resource | Documentation（Discord）](https://discord.com/developers/docs/resources/webhook?utm_source=chatgpt.com)
- [API Reference（Discord Developer Portal）](https://discord.com/developers/docs/reference?utm_source=chatgpt.com)

## 📄 ライセンス

このプロジェクトは自由に使用・改変できます。

