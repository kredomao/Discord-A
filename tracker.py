import json
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any

DATA_FILE = "data.json"


def load_data() -> Dict[str, Any]:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"last_push_date": "", "streak": 0, "level": 1, "exp": 0}


def save_data(data: Dict[str, Any]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def update_progress() -> Tuple[Dict[str, Any], bool]:
    """Push/学習進捗を更新し、連続日数・レベル・経験値を管理する。

    Returns:
        (更新後データ, レベルアップしたかどうか)
    """
    data = load_data()
    today = datetime.now().date()
    last_str = data.get("last_push_date") or ""

    last_date = None
    if last_str:
        try:
            last_date = datetime.strptime(last_str, "%Y-%m-%d").date()
        except ValueError:
            last_date = None

    # streak ロジック
    if last_date == today:
        # 同じ日に複数回 push しても streak は増やさない
        pass
    elif last_date == today - timedelta(days=1):
        data["streak"] = int(data.get("streak", 0)) + 1
    else:
        data["streak"] = 1

    data["last_push_date"] = today.strftime("%Y-%m-%d")

    # XP & Level ロジック（MVP: 1 Push = 10 exp, 次レベル必要経験値 = level * 30）
    data["exp"] = int(data.get("exp", 0)) + 10
    data["level"] = int(data.get("level", 1))

    level_up = False
    required = data["level"] * 30
    if data["exp"] >= required:
        data["level"] += 1
        data["exp"] = 0
        level_up = True

    save_data(data)
    return data, level_up


if __name__ == "__main__":
    updated, leveled = update_progress()
    print({"updated": updated, "level_up": leveled})


