#!/usr/local/bin/python
# -*- coding: latin-1 -*-

#Girl Or Boy Lib Intro

import wx
import AdvancedSplash as AS
from Fader import *
from _Info import *

def INTRO():
	bitmap = wx.Bitmap("images\D!Xwar3.bmp", wx.BITMAP_TYPE_BMP)
	shadow = wx.WHITE
	frame = AS.AdvancedSplash(None,
	 bitmap=bitmap,
	 timeout=3500,
	 extrastyle=AS.AS_TIMEOUT | AS.AS_CENTER_ON_SCREEN | AS.AS_SHADOW_BITMAP,
	 shadowcolour=shadow)
	FADER(frame).FaderOUT()