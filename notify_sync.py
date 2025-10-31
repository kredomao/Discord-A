"""
Discord Webhook を使った同期版通知スクリプト
リトライ機能、ログ出力、エラーハンドリング付き
"""
import os
import json
import time
import logging
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")


def send_message(
    content: str,
    username: str = "Notifier",
    embeds: Optional[list] = None,
    max_retries: int = 3,
    retry_delay: float = 1.0
) -> bool:
    """
    Discord Webhook にメッセージを送信（同期版）
    
    Args:
        content: 送信するメッセージ本文
        username: Webhook の表示名
        embeds: Embed オブジェクトのリスト（オプション）
        max_retries: 最大リトライ回数
        retry_delay: リトライ間の待機時間（秒）
    
    Returns:
        成功時 True、失敗時 False
    """
    if not WEBHOOK_URL:
        logger.error("DISCORD_WEBHOOK_URL が設定されていません")
        raise RuntimeError("DISCORD_WEBHOOK_URL 環境変数を設定してください")
    
    payload: Dict[str, Any] = {
        "username": username,
        "content": content,
    }
    
    if embeds:
        payload["embeds"] = embeds
    
    for attempt in range(max_retries):
        try:
            logger.info(f"メッセージ送信を試みます（試行 {attempt + 1}/{max_retries}）")
            resp = requests.post(
                WEBHOOK_URL,
                json=payload,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
            
            # レート制限チェック
            if resp.status_code == 429:
                retry_after = float(resp.headers.get("Retry-After", retry_delay * 2))
                logger.warning(f"レート制限に達しました。{retry_after}秒待機します")
                if attempt < max_retries - 1:
                    time.sleep(retry_after)
                    continue
            
            resp.raise_for_status()
            logger.info(f"メッセージ送信成功（ステータス: {resp.status_code}）")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"送信エラー（試行 {attempt + 1}/{max_retries}）: {e}")
            if attempt < max_retries - 1:
                logger.info(f"{retry_delay}秒後にリトライします...")
                time.sleep(retry_delay)
            else:
                logger.error("最大リトライ回数に達しました。送信に失敗しました。")
                return False
    
    return False


def send_simple_notification(message: str):
    """
    シンプルな通知送信（クイックスタート用）
    """
    return send_message(content=message)


if __name__ == "__main__":
    # テスト送信
    success = send_simple_notification(
        "こんにちは — Cursor からの自動通知テストです 🚀"
    )
    
    if success:
        print("✅ 通知送信に成功しました")
    else:
        print("❌ 通知送信に失敗しました")

