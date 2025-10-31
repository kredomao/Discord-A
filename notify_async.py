"""
Discord Webhook を使った非同期版通知スクリプト
高頻度送信や他の async 処理との統合に適しています
"""
import os
import asyncio
import logging
from typing import Optional, Dict, Any, List
from aiohttp import ClientSession, ClientError, ClientTimeout
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


async def send_message(
    session: ClientSession,
    content: str,
    username: str = "AsyncNotifier",
    embeds: Optional[List[Dict[str, Any]]] = None,
    max_retries: int = 3,
    retry_delay: float = 1.0
) -> bool:
    """
    Discord Webhook にメッセージを非同期送信
    
    Args:
        session: aiohttp の ClientSession インスタンス
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
            
            timeout = ClientTimeout(total=10)
            async with session.post(
                WEBHOOK_URL,
                json=payload,
                timeout=timeout,
                headers={"Content-Type": "application/json"}
            ) as resp:
                # レート制限チェック
                if resp.status == 429:
                    retry_after = float(resp.headers.get("Retry-After", retry_delay * 2))
                    logger.warning(f"レート制限に達しました。{retry_after}秒待機します")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_after)
                        continue
                
                resp.raise_for_status()
                logger.info(f"メッセージ送信成功（ステータス: {resp.status}）")
                return True
                
        except ClientError as e:
            logger.error(f"送信エラー（試行 {attempt + 1}/{max_retries}）: {e}")
            if attempt < max_retries - 1:
                logger.info(f"{retry_delay}秒後にリトライします...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error("最大リトライ回数に達しました。送信に失敗しました。")
                return False
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
            return False
    
    return False


async def send_multiple_messages(contents: List[str], username: str = "AsyncNotifier"):
    """
    複数のメッセージを非同期で送信（並列処理）
    """
    if not WEBHOOK_URL:
        raise RuntimeError("DISCORD_WEBHOOK_URL 環境変数を設定してください")
    
    async with ClientSession() as session:
        tasks = [
            send_message(session, content, username)
            for content in contents
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results


async def main():
    """テスト実行用"""
    if not WEBHOOK_URL:
        logger.error("DISCORD_WEBHOOK_URL が設定されていません")
        return
    
    async with ClientSession() as session:
        success = await send_message(
            session,
            "非同期通知テスト from Cursor + aiohttp ⚡",
            username="AsyncTest"
        )
        
        if success:
            print("✅ 非同期通知送信に成功しました")
        else:
            print("❌ 非同期通知送信に失敗しました")
        
        # 複数メッセージ送信の例
        print("\n複数メッセージの送信テスト...")
        results = await send_multiple_messages([
            "メッセージ 1",
            "メッセージ 2",
            "メッセージ 3"
        ])
        print(f"送信結果: {results}")


if __name__ == "__main__":
    asyncio.run(main())

