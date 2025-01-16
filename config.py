import sys
import os
import datetime
import time

import pyauto
from keyhac import *

#####   ユーザ設定   ##################

USER_NAME = "starg"

######################################


def configure(keymap):
	# windowsのキー配列をあらかじめ変更
	#	1. CapsLockをScancode=194に変更
	# 	2. 無変換キーをLeftCtrlに変更
	# 	3. 変換キーをRightCtrlに変更

	#####   基本設定   ##############################################################
	# 編集のデフォルトエディタをVSCodeに設定
	keymap.editor = f"C:\\Users\\{USER_NAME}\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"

	#####   ユーティリティ   ########################################################
	def delay(sec = 0.05):
		# 遅延
		time.sleep(sec)

	def get_clippedText():
		# クリップボードからテキストを取得
		return (getClipboardText() or "")

	def paste_string(s):
		# 文字列を貼り付け
		setClipboardText(s)
		delay()
		keymap.InputKeyCommand("C-V")()

	def copy_string(sec = 0.05):
		# 文字列をコピー
		keymap.InputKeyCommand("C-C")()
		delay(sec)
		return get_clippedText()

	def send_input(ime_mode, keys, sleep = 0.01):
		# キー入力を送信
		# ime_mode: 0 -> 英語入力, 1 -> 日本語入力
		if ime_mode is not None:
			if keymap.getWindow().getImeStatus() != ime_mode:
				keymap.InputKeyCommand("(243)")()
		# keys: 入力するキーのリスト
		for key in keys:
			delay(sleep)
			try:
				keymap.InputKeyCommand(key)()
			except:
				keymap.InputTextCommand(key)()
	
	#####   カーソル移動・キーリマップ   ########################################################
	# 常に有効になるキーリマップ
	keymap_global = keymap.defineWindowKeymap()
	# capslockをUser1に割り当て
	keymap.defineModifier(194, "User1")

	# caps + (p, b, f, n) -> (up, left, right, down)
	keymap_global["User1-P"] = "Up"
	keymap_global["User1-B"] = "Left"
	keymap_global["User1-F"] = "Right"
	keymap_global["User1-N"] = "Down"

	# caps + (a, e) -> (home, end)
	keymap_global["User1-A"] = "Home"
	keymap_global["User1-E"] = "End"

	# caps + (d, h) -> (delete, backspace)
	keymap_global["User1-D"] = "Delete"
	keymap_global["User1-H"] = "Back"

	# caps + k -> カーソルの後ろを全削除
	keymap_global["User1-K"] = "S-End", "Back"
	# caps + y -> カーソルの前を全削除
	keymap_global["User1-Y"] = "S-Home", "Delete"
	
	# caps + j -> Enter
	keymap_global["User1-J"] = "Enter"

	# caps + u -> _
	keymap_global["User1-U"] = "S-Underscore"
	# caps + i -> -
	keymap_global["User1-I"] = "Minus"
	# caps + o -> =
	keymap_global["User1-O"] = "S-Minus"

	# caps + {i} -> F{i}
	keymap_global[ "User1-1" ] = "F1"
	keymap_global[ "User1-2" ] = "F2"
	keymap_global[ "User1-3" ] = "F3"
	keymap_global[ "User1-4" ] = "F4"
	keymap_global[ "User1-5" ] = "F5"
	keymap_global[ "User1-6" ] = "F6"
	keymap_global[ "User1-7" ] = "F7"
	keymap_global[ "User1-8" ] = "F8"
	keymap_global[ "User1-9" ] = "F9"
	
	#####   記号の直接入力   ########################################################
	def direct_input(key, turnoff_ime_later = False):
		# IMEのオンオフに関係なく直接入力する
		key_list = [key]
		if keymap.getWindow().getImeStatus() == 1:
			key_list.append("C-M")
			if turnoff_ime_later:
				key_list.append("(243)")
		send_input(None, key_list)
	
	# 二つ目の引数がTrueの場合は入力後にIMEをオフにする
	for key in [
		("AtMark"	  , True), # ＠
		("Caret"	   , False), # ～
		("CloseBracket", False), # 」
		("Colon"	   , False), # 。
		("Comma"	   , False), # 、
		("LS-AtMark"   , True), # ‘
		("LS-Caret"	, False), # ～
		("LS-Colon"	, False), # ＊
		("LS-Comma"	, False), # ＜
		("LS-Minus"	, False), # ＝
		("LS-Period"   , False), # ＞
		("LS-SemiColon", False), # ＋
		("LS-Slash"	, False), # ？
		("LS-Yen"	  , True), # ｜
		("OpenBracket" , False), # 「
		("Period"	  , False), # 。
		("SemiColon"   , False), # ；
		("Slash"	   , False), # ・
		("Yen"		 , True), # ￥
	]:
		def _wrapper(k, i):
			return lambda: direct_input(k, i)
		keymap_global[key[0]] = _wrapper(key[0], key[1])

	# シフト+数字キーでの記号
	for n in "123456789":
		def _wrapper(k, i):
			return lambda: direct_input(k, i)
		key = "S-" + n
		if n in ("2", "3", "4"):
			keymap_global[key] = _wrapper(key, True)
		else:
			keymap_global[key] = _wrapper(key, False)

	# シフトで大文字アルファベットを入力した場合は以降の IME をオフにする
	for alphabet in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
		def _wrapper(k):
			return lambda: direct_input(k, True)
		key = "S-" + alphabet
		keymap_global[key] = _wrapper(key)

	#####   IMEの切り替え   ########################################################
	# LeftCtrl -> 英語入力
	keymap_global["O-LCtrl"] = lambda: keymap.getWindow().setImeStatus(0)
	# RightCtrl -> 日本語入力
	keymap_global["O-RCtrl"] = lambda: keymap.getWindow().setImeStatus(1)


	#####   Chromeを開く   ########################################################
	def find_window(arg_exe, arg_class):
		wnd = pyauto.Window.getDesktop().getFirstChild()
		last_found = None
		while wnd:
			if wnd.isVisible() and not wnd.getOwner():
				if wnd.getClassName() == arg_class and wnd.getProcessName() == arg_exe:
					last_found = wnd
			wnd = wnd.getNext()
		return last_found

	def google_search():
		if keymap.getWindow().getProcessName() == "chrome.exe":
			send_input(1, ["C-T", "C-K"])
		else:
			wnd = find_window("chrome.exe", "Chrome_WidgetWin_1")
			if wnd:
				send_input(1, ["C-LWin-1", "C-T", "C-K"], 0.05)
			else:
				send_input(1, ["LWin-1"])
	keymap_global["User1-Q"] = google_search