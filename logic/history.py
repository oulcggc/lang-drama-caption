import os
import json
import datetime
import uuid

# 具体例
example_history = [
    {
        "id": "28540577-7de3-4c30-aec4-ec6b6265afe8",
        "timestamp": "2025-04-28T02:37:59.913343",
        "filepath": "2025_bunkasai"
    },
    {
        "id": "518e87c3-8773-4abb-ad37-7aa103a59f0d",
        "timestamp": "2025-04-28T02:38:08.661569",
        "filepath": "2025_bunkasai2"
    }
]

# 履歴を保存
def save_history(history_data, history_file="history.json"):
  with open(history_file, 'w') as historyfile:
    json.dump(history_data, historyfile, indent=4)
    
# 履歴を追加
def add_history(ppt_name, history_file="history.json"):
  timestamp = datetime.datetime.now().isoformat()
  id = str(uuid.uuid4())
  append_history = {"id": id, "timestamp": timestamp, "filepath": ppt_name}
  history_data = load_history(history_file)
  history_data.append(append_history)
  save_history(history_data)

# 履歴を削除
def delete_history(remove_id, history_file="history.json"):
  history_data = load_history(history_file)
  try:
    updated_data = [item for item in history_data if item.get("id") != remove_id]
  except Exception as e:
    print("特定の履歴が存在しません: " + e)
  save_history(updated_data, history_file)

# 履歴をロード
def load_history(history_file="history.json"):
  history_data = []
  if os.path.exists(history_file):
    try:
      with open(history_file, "r") as historyfile:
        history_data = json.load(historyfile)
    except json.JSONDecodeError as e:
      print("履歴を読み込むことができませんでした:" + e)
      pass
  return history_data


# 削除例(idを指定することで削除)
# id="518e87c3-8773-4abb-ad37-7aa103a59f0d"
# delete_history(id) 

# 作成例
# add_history("2026_ichosai_ch")

# ロード例
# print(load_history())