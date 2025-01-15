import sys
import os
import datetime

import pyauto
from keyhac import *


def configure(keymap):
	keymap.editor = "C:\\Users\\starg\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"

	keymap_global = keymap.defineWindowKeymap()

	keymap.defineModifier(194, "User1")

	# keymap_global["O-LShift"] = "O-Tab"
	keymap_global["User1-P"] = "Up"
	keymap_global["User1-B"] = "Left"
	keymap_global["User1-F"] = "Right"
	keymap_global["User1-N"] = "Down"

	keymap_global["User1-A"] = "Home"
	keymap_global["User1-E"] = "End"

	keymap_global["User1-D"] = "Delete"
	keymap_global["User1-H"] = "Back"

	keymap_global["O-LCtrl"] = lambda: keymap.getWindow().setImeStatus(0)
	keymap_global["O-RCtrl"] = lambda: keymap.getWindow().setImeStatus(1)