import configparser
import os

default_config = {
  'General':{
    'Save_Location': '.'
  }
}

def save_config(config_data=None, config_file="config.ini"):
  config = configparser.ConfigParser()
  save_config_data = config_data if config_data is not None else default_config
  for section, data in save_config_data.items():
    config[section] = data
  try:
    with open(config_file, 'w') as configfile:
      config.write(configfile)
    return 0
  # 以下各エラー処理
  except IOError as e:
      print(f"ファイル書き込みエラー: {e}")
      return 1
  except PermissionError as e:
      print(f"書き込み権限エラー: {e}")
      return 1
  except Exception as e:
      print(f"予期せぬエラー: {e}")
      return 1


def load_config(config_file="config.ini"):
  config = configparser.ConfigParser()
  if not os.path.exists(config_file):
    error_msg = f"設定ファイルが見つかりませんでした: {config_file}"
    config.read(default_config)
    config_data = {
      section: dict(config[section]) for section in config.sections()
    }
    print(error_msg + ". デフォルト設定を使用します。")
    return config_data, error_msg
  
  else:
    try:
      config.read(config_file)
      config_data = {
        section: dict(config[section]) for section in config.sections()
      }
      return config_data, None
    except Exception as e:
      error_msg = f"予期せぬエラーが発生しました: {e}"
      print(error_msg)
      return None, error_msg