"""
Discord Embed を使ったリッチなメッセージ通知の例
見栄えの良い通知を送信するためのテンプレート集
"""
import os
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from notify_sync import send_message

load_dotenv()


def create_success_embed(
    title: str,
    description: str,
    fields: Optional[list] = None,
    timestamp: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    成功メッセージ用の Embed を作成（緑色）
    """
    embed = {
        "title": title,
        "description": description,
        "color": 0x00ff00,  # 緑色
        "timestamp": (timestamp or datetime.utcnow()).isoformat(),
    }
    
    if fields:
        embed["fields"] = fields
    
    return embed


def create_error_embed(
    title: str,
    description: str,
    fields: Optional[list] = None
) -> Dict[str, Any]:
    """
    エラーメッセージ用の Embed を作成（赤色）
    """
    embed = {
        "title": title,
        "description": description,
        "color": 0xff0000,  # 赤色
        "timestamp": datetime.utcnow().isoformat(),
    }
    
    if fields:
        embed["fields"] = fields
    
    return embed


def create_info_embed(
    title: str,
    description: str,
    fields: Optional[list] = None
) -> Dict[str, Any]:
    """
    情報メッセージ用の Embed を作成（青色）
    """
    embed = {
        "title": title,
        "description": description,
        "color": 0x0099ff,  # 青色
        "timestamp": datetime.utcnow().isoformat(),
    }
    
    if fields:
        embed["fields"] = fields
    
    return embed


def create_job_completion_embed(
    job_name: str,
    status: str,
    start_time: str,
    duration: str,
    details: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    ジョブ完了通知用の Embed
    """
    color = 0x00ff00 if status == "成功" else 0xff0000
    
    fields = [
        {"name": "開始時刻", "value": start_time, "inline": True},
        {"name": "所要時間", "value": duration, "inline": True},
        {"name": "ステータス", "value": status, "inline": True},
    ]
    
    if details:
        for key, value in details.items():
            fields.append({"name": key, "value": value, "inline": False})
    
    return {
        "title": f"ジョブ完了: {job_name}",
        "description": f"ジョブ '{job_name}' が {status} しました",
        "color": color,
        "fields": fields,
        "timestamp": datetime.utcnow().isoformat(),
    }


if __name__ == "__main__":
    # 例1: シンプルな成功通知
    print("例1: 成功通知を送信中...")
    success_embed = create_success_embed(
        title="✅ バックアップ完了",
        description="データベースのバックアップが正常に完了しました",
        fields=[
            {"name": "ファイルサイズ", "value": "1.2 GB", "inline": True},
            {"name": "保存先", "value": "/backups/2025-01-29.db", "inline": True},
        ]
    )
    send_message(content="", embeds=[success_embed], username="BackupBot")
    
    # 例2: ジョブ完了通知
    print("\n例2: ジョブ完了通知を送信中...")
    job_embed = create_job_completion_embed(
        job_name="日次レポート生成",
        status="成功",
        start_time="2025-01-29 06:00:00",
        duration="12m 34s",
        details={
            "処理レコード数": "15,234 件",
            "出力ファイル": "report_2025-01-29.pdf"
        }
    )
    send_message(content="", embeds=[job_embed], username="JobScheduler")
    
    # 例3: エラー通知
    print("\n例3: エラー通知を送信中...")
    error_embed = create_error_embed(
        title="❌ エラーが発生しました",
        description="処理中にエラーが発生しました",
        fields=[
            {"name": "エラーコード", "value": "ERR_001", "inline": True},
            {"name": "発生箇所", "value": "データベース接続", "inline": True},
        ]
    )
    send_message(content="", embeds=[error_embed], username="ErrorMonitor")
    
    print("\n✅ すべてのテスト送信が完了しました")

