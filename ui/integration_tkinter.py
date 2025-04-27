from pytk import tk
from pytk import ttk
import os
import sys
import check_display as check_display
from config.color_def import Color

check_display.check_display()

app_name = "字幕整形アプリ（仮）"
# --- メインウィンドウの設定 ---
root = tk.Tk()
root.title("字幕整形アプリ (UIモック)")
root.geometry("800x600")
root.configure(bg=Color.BACKGROUND)

app_container = tk.Frame(root, bg=Color.PANEL_BACKGROUND)
app_container.pack(fill="both", expand=True)

# ボタンのスタイルを統一
def create_control_button(parent, text):
    # 通常のボタン
    btn = tk.Button(parent, text=text, width=3, height=1, bd=0, bg=Color.HEADER_FOOTER, fg="#333",
                    activebackground="#c0c0c0", activeforeground="#333", relief="flat", cursor="hand2")
    # 閉じるボタンはホバーで赤
    if text == '✕':
         btn.config(activebackground="#e81123", activeforeground="white")

    btn.pack(side="left", padx=1, pady=0) # わずかな隙間

# --- メインコンテンツエリア (左右分割) ---
main_content_frame = tk.Frame(app_container, bg=Color.PANEL_BACKGROUND)
main_content_frame.pack(fill="both", expand=True)

# 左側
settings_panel_frame = tk.Frame(main_content_frame, bg=Color.PANEL_BACKGROUND, padx=15, pady=15)
settings_panel_frame.pack(side="left", fill="both", expand=True, ipadx=5) # 左側が伸縮

# 右側（履歴/設定）
right_panel_frame = tk.Frame(main_content_frame, bg=Color.PANEL_BACKGROUND, width=300)
right_panel_frame.pack(side="right", fill="both")
right_panel_frame.pack_propagate(False) # Frameが内部ウィジェットのサイズから独立
right_panel_frame.config(bd=0, highlightbackground=Color.DIVIDER, highlightthickness=1) # 左との区切り線


# --- 左側の設定項目 ---
# 設定項目のテンプレートフレームを作成
def create_setting_item_frame(parent, label_text, show_setting_button=False):
    item_frame = tk.Frame(parent, bg=Color.PANEL_BACKGROUND)
    item_frame.pack(fill='x', pady=7) # 縦方向に隙間
    item_frame.columnconfigure(0, weight=1) # 入力エリアの列は伸縮可能に

    label = tk.Label(item_frame, text=label_text, bg=Color.LABEL_BACKGROUND, fg="#333", font=('Segoe UI', 9, 'bold'), anchor="w", padx=5, pady=3)
    label.grid(row=0, column=0, columnspan=3, sticky='ewns') # 1行目全体に配置

    input_group_frame = tk.Frame(item_frame, bg=Color.PANEL_BACKGROUND)
    input_group_frame.grid(row=1, column=0, columnspan=3, sticky='ew') # 2行目全体に配置
    input_group_frame.columnconfigure(0, weight=1) # ファイル保存場所入力エリア部分は伸縮可能に

    # 入力フィールド
    file_path_entry = tk.Entry(input_group_frame, state='readonly', relief='solid', roforeground="#555", readonlybackground="#ffffff", bd=1, font=('Segoe UI', 9), cursor="arrow") # readonly時はcursor="arrow"が適切か
    file_path_entry.insert(0, "デフォルトのパスが表示されます")
    file_path_entry.grid(row=0, column=0, sticky='ew', padx=(0, 5)) # 左側に配置、右に少し隙間

    # 設定ボタン（デフォルトを設定可能に）
    if show_setting_button:
        setting_button = tk.Button(input_group_frame, text="設定", bg=Color.BUTTON_GRAY, fg="#333", bd=0, padx=10, pady=3, relief="flat", cursor="hand2", activebackground="#b0b0b0")
        setting_button.grid(row=0, column=1, sticky='e', padx=(0, 5)) # 参照ボタンの左に配置
        input_group_frame.columnconfigure(1, weight=0) # 設定ボタンの列は伸縮しない

    # 参照ボタン
    browse_button = tk.Button(input_group_frame, text="参照", bg=Color.BUTTON_BLUE, fg="white", bd=0, padx=10, pady=3, relief="flat", cursor="hand2", activebackground="#005a9e")
    browse_button.grid(row=0, column=2, sticky='e') # 右側に配置
    input_group_frame.columnconfigure(2, weight=0) # 参照ボタンの列は伸縮しない

    return item_frame, file_path_entry # 必要ならウィジェットを返す

# 実行ボタン
execute_button = tk.Button(settings_panel_frame, text="実行", bg=Color.BUTTON_BLUE, fg="white", bd=0, padx=20, pady=8, relief="flat", font=('Segoe UI', 10, 'bold'), cursor="hand2", activebackground="#005a9e")

settings_panel_frame.columnconfigure(0, weight=1) # 左パネルの列を伸縮可能に（設定項目用）
settings_panel_frame.rowconfigure(3, weight=1) # 実行ボタンの上の行（3行目）を伸縮可能にしてボタンを下に追いやる

# 設定項目をgridで再配置
row_index = 0
for label_text, show_setting in [("字幕ファイルの場所を選択", False), ("画像フォルダの場所を選択", False), ("出力ファイルを保存する場所を選択", True)]:
    item_frame = tk.Frame(settings_panel_frame, bg=Color.PANEL_BACKGROUND)
    item_frame.grid(row=row_index, column=0, sticky='ew', pady=7)
    item_frame.columnconfigure(0, weight=1) # 入力エリアの列を伸縮可能にする

    label = tk.Label(item_frame, text=label_text, bg=Color.LABEL_BACKGROUND, fg="#333", font=('Segoe UI', 9, 'bold'), anchor="w", padx=5, pady=3)
    label.grid(row=0, column=0, columnspan=3, sticky='ewns')

    input_group_frame = tk.Frame(item_frame, bg=Color.PANEL_BACKGROUND)
    input_group_frame.grid(row=1, column=0, columnspan=3, sticky='ew')
    input_group_frame.columnconfigure(0, weight=1)

    file_path_entry = tk.Entry(input_group_frame, state='readonly', relief='solid', readonlybackground="#ffffff", bd=1, font=('Segoe UI', 9), cursor="arrow")
    file_path_entry.insert(0, f"C:\\path\\to\\{label_text.split('の場所')[0]}...")
    file_path_entry.grid(row=0, column=0, sticky='ew', padx=(0, 5))

    if show_setting:
        setting_button = tk.Button(input_group_frame, text="設定", bg=Color.BUTTON_GRAY, fg="#333", bd=0, padx=10, pady=3, relief="flat", cursor="hand2", activebackground="#b0b0b0")
        setting_button.grid(row=0, column=1, sticky='e', padx=(0, 5))
        input_group_frame.columnconfigure(1, weight=0)
        browse_column = 2 # 設定ボタンがある場合は参照ボタンは3列目
    else:
        browse_column = 1 # 設定ボタンがない場合は参照ボタンは2列目

    browse_button = tk.Button(input_group_frame, text="参照", bg=Color.BUTTON_BLUE, fg="white", bd=0, padx=10, pady=3, relief="flat", cursor="hand2", activebackground="#005a9e")
    browse_button.grid(row=0, column=browse_column, sticky='e')
    input_group_frame.columnconfigure(browse_column, weight=0)

    row_index += 1

# 実行ボタンを最終行に配置
execute_button = tk.Button(settings_panel_frame, text="実行", bg=Color.BUTTON_BLUE, fg="white", bd=0, padx=20, pady=8, relief="flat", font=('Segoe UI', 10, 'bold'), cursor="hand2", activebackground="#005a9e")
execute_button.grid(row=row_index, column=0, sticky='s', pady=(20, 0)) # 最終行、下に寄せる、上部に余白


# --- 右側のタブとコンテンツ ---
notebook = ttk.Notebook(right_panel_frame)
notebook.pack(fill="both", expand=True, padx=10, pady=10) # 右パネル内で伸縮

# スタイル設定 (タブの色など)
style = ttk.Style()
# デフォルトのスタイルを取得し、必要な部分を変更
style.configure("TNotebook", background=Color.PANEL_BACKGROUND, borderwidth=0)
style.configure("TNotebook.Tab", background=Color.LABEL_BACKGROUND, foreground="#555", padding=[10, 5]) # [左右パディング, 上下パディング]
style.map("TNotebook.Tab", background=[("selected", Color.LABEL_BACKGROUND)], foreground=[("selected", "#333")])


# 履歴タブ
history_frame = tk.Frame(notebook, bg=Color.PANEL_BACKGROUND)
notebook.add(history_frame, text="履歴")

# 履歴アイテムの例を作成
def create_history_item(parent, file_name):
    item_frame = tk.Frame(parent, bg=Color.HISTORY_ITEM, padx=8, pady=5)
    item_frame.pack(fill="x", pady=3) # 縦方向に隙間を持って並べる
    item_frame.columnconfigure(0, weight=1) # ファイル名表示部分を伸縮可能に

    file_name_label = tk.Label(item_frame, text=file_name, bg=Color.HISTORY_ITEM, fg="white", anchor="w", font=('Segoe UI', 9))
    file_name_label.grid(row=0, column=0, sticky='ew')

    delete_button = tk.Button(item_frame, text="履歴削除", bg=Color.BUTTON_GRAY, fg="#333", bd=0, padx=5, pady=1, relief="flat", cursor="hand2", activebackground="#b0b0b0")
    delete_button.grid(row=0, column=1, sticky='e')
    item_frame.columnconfigure(1, weight=0) # ボタンの列は伸縮しない

# 履歴アイテムを追加
create_history_item(history_frame, "ファイル名 例 1.srt")
create_history_item(history_frame, "別の字幕ファイル.srt")
create_history_item(history_frame, "非常に長いファイル名の例eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee.srt")
# 履歴アイテムが多くなった場合にスクロールできるように、history_frame自体をCanvasなどに入れることも検討したい

# 設定タブ
settings_frame = tk.Frame(notebook, bg=Color.PANEL_BACKGROUND)
notebook.add(settings_frame, text="設定")

# 設定タブの内容
settings_label = tk.Label(settings_frame, text="ここに設定内容が表示されます\n", bg=Color.PANEL_BACKGROUND, fg="#333")
settings_label.pack(padx=10, pady=10)


# --- フッター（クレジット表記）
footer_frame = tk.Frame(app_container, bg=Color.HEADER_FOOTER)
footer_frame.pack(fill="x")

credits_label = tk.Label(footer_frame, text="GGC", bg=Color.HEADER_FOOTER, fg="#555", font=('Segoe UI', 8), anchor="e")
credits_label.pack(side="right", padx=5, pady=2)

# --- メインループの開始 ---
root.mainloop()