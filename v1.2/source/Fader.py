#!/usr/local/bin/python
# -*- coding: latin-1 -*-

#Girl Or Boy Lib Fader

import wx
from _Info import *

class FADER(wx.Frame):
    def __init__(self,parent):
        ## ------- Fader Timer -------- ##
        self.timer = wx.Timer(parent, wx.ID_ANY)
        self.timer.Start(60)
        ## ---------------------------- ##
        self.parent=parent
        self.delta=15
    def FaderIN(self):
        self.amount = 0
        self.parent.SetTransparent(self.amount)
        wx.EVT_TIMER(self.parent, wx.ID_ANY, self.AlphaCycleIN)
    def FaderOUT(self):
        self.amount = 255
        self.parent.SetTransparent(self.amount)
        wx.EVT_TIMER(self.parent, wx.ID_ANY, self.AlphaCycleOUT)
    def AlphaCycleIN(self, evt):
        self.amount += self.delta
        if self.amount >= 250:
            self.timer.Stop()
            self.amount = 255
        self.parent.SetTransparent(self.amount)
    def AlphaCycleOUT(self, evt):
        self.amount -= self.delta
        if self.amount <=5:
            self.timer.Stop()
            self.amount = 0
        self.parent.SetTransparent(self.amount)