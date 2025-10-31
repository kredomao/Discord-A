"""
APScheduler を使った定期通知スクリプト
指定した間隔で自動的に Discord に通知を送信します
"""
import os
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from notify_sync import send_message

# 環境変数を読み込む
load_dotenv()

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# スケジューラを初期化
scheduler = BlockingScheduler()


def scheduled_notification():
    """定期実行される通知関数"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"定期通知: 状態正常です ⏰\n時刻: {current_time}"
    
    logger.info(f"定期通知を送信します: {current_time}")
    success = send_message(
        content=message,
        username="ScheduledNotifier"
    )
    
    if success:
        logger.info("定期通知の送信に成功しました")
    else:
        logger.error("定期通知の送信に失敗しました")


def hourly_notification():
    """毎時0分に実行される通知"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"毎時通知: システムは正常に稼働中です 🕐\n時刻: {current_time}"
    
    send_message(
        content=message,
        username="HourlyNotifier"
    )


def daily_report():
    """毎日特定時刻（例: 朝9時）に実行される日次レポート"""
    current_date = datetime.now().strftime("%Y-%m-%d")
    message = f"📊 日次レポート {current_date}\n\nシステムは正常に稼働中です。"
    
    send_message(
        content=message,
        username="DailyReport"
    )


def setup_schedules():
    """スケジュールを設定"""
    # 例1: 毎時0分に実行
    scheduler.add_job(
        hourly_notification,
        CronTrigger(minute=0),  # 毎時0分
        id='hourly_notification',
        name='毎時通知',
        replace_existing=True
    )
    logger.info("毎時通知スケジュールを設定しました（毎時0分）")
    
    # 例2: 毎日朝9時に実行
    scheduler.add_job(
        daily_report,
        CronTrigger(hour=9, minute=0),  # 毎日9時0分
        id='daily_report',
        name='日次レポート',
        replace_existing=True
    )
    logger.info("日次レポートスケジュールを設定しました（毎日9:00）")
    
    # 例3: 5分ごとに実行（テスト用 - 本番環境では削除推奨）
    # scheduler.add_job(
    #     scheduled_notification,
    #     'interval',
    #     minutes=5,
    #     id='test_notification',
    #     name='テスト通知（5分間隔）',
    #     replace_existing=True
    # )
    # logger.info("テスト通知スケジュールを設定しました（5分間隔）")


if __name__ == "__main__":
    if not os.environ.get("DISCORD_WEBHOOK_URL"):
        logger.error("DISCORD_WEBHOOK_URL 環境変数を設定してください")
        exit(1)
    
    logger.info("スケジューラを起動します...")
    
    try:
        setup_schedules()
        logger.info("スケジューラを開始します（Ctrl+C で停止）")
        
        # スケジューラを開始（ブロッキング）
        scheduler.start()
        
    except KeyboardInterrupt:
        logger.info("スケジューラを停止します...")
        scheduler.shutdown()
        logger.info("スケジューラを停止しました")

