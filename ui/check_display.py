import os
import sys

def check_display():
  set_display = os.environ.get("DISPLAY")
  if(set_display==None):
    print("No Display. ディスプレイを接続してください.", file=sys.stderr)
    return 1
  else:
    print("Display is set.")