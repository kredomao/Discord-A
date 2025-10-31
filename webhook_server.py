from flask import Flask, request
import os
import requests
from dotenv import load_dotenv
from tracker import update_progress

load_dotenv()

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET")  # MVPでは未検証でOK

app = Flask(__name__)


@app.route("/github", methods=["POST"])
def github_webhook():
    # イベント種別
    event = request.headers.get("X-GitHub-Event")

    # MVP: push のみ処理
    if event == "push":
        data, level_up = update_progress()

        msg = (
            f"📚 **学習ログ更新**\n"
            f"🔥 連続日数: `{data['streak']}日`\n"
            f"⭐ Level: `{data['level']}`\n"
            f"✨ EXP: `{data['exp']}` / `{data['level']*30}`"
        )

        if level_up:
            msg += "\n\n🆙 **レベルアップ!!**\n頑張ってる！続けよう🔥"

        if not DISCORD_WEBHOOK:
            return ("DISCORD_WEBHOOK_URL is not set", 500)

        try:
            resp = requests.post(DISCORD_WEBHOOK, json={"content": msg}, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            return (f"Failed to notify Discord: {e}", 500)

        return ("OK", 200)

    return ("Ignored", 200)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)


