#!/usr/bin/python
# --encoding: utf-8

# Author: Dixtosa
# Date started: 2009

import wx
import time
import random
import fractions

class MathQuizFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, -1,
                                  "MathQuiz v1.5",
                                  wx.DefaultPosition,
                                  wx.Size(700, 525))
		self.game_p = None
		self.font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		self.font_gamo = wx.Font(40,wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		self.font50=wx.Font(50,wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		self.MainPanel = wx.Panel(self,-1)
		self.gameDuration=0
		self.count_answer=0
		self.objectSetup()
		self.setMenubar()
		self.binding()
	def objectSetup(self):
		if self.game_p!=None:
			for child in self.game_p.GetChildren():
				child.Destroy()
		dro = wx.StaticText(self.MainPanel,-1, u"დრო:",(25,75))
		dro.SetFont(self.font)
		self.timer_value = wx.TextCtrl(self.MainPanel,-1,"",(125,75),wx.Size(100,100),style = wx.TE_CENTRE)
		self.timer_value.SetFont(self.font50)
		
		wami = wx.StaticText(self.MainPanel,-1, u"წამი",(25,75))
		wami.SetFont(self.font)
		
		
		start = wx.Button(self.MainPanel,1,"Start",(310,350),wx.Size(75,75))
		start.Bind(wx.EVT_BUTTON,self.start)
		
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(dro,1,wx.EXPAND | wx.ALL, 50)
		sizer.Add(self.timer_value,1)
		sizer.Add(wami,1,wx.EXPAND | wx.ALL, 50)
		
		sizer_2=wx.BoxSizer(wx.VERTICAL)
		sizer_2.Add(sizer,1,wx.EXPAND | wx.ALL, 50)
		sizer_2.Add(start,1,wx.EXPAND | wx.LEFT | wx.RIGHT, 150)
		
		self.MainPanel.SetSizer(sizer_2)
		self.MainPanel.Layout()
	def start(self, evt):
		try:
			self.gameDuration = int(self.timer_value.GetValue())
			if self.gameDuration < 10 or self.gameDuration > 60*10:
				wx.MessageBox('Game duration should be no less than 10 seconds and no more than 10 minutes', '!')
				return
		except:
			return
		
		for child in self.MainPanel.GetChildren(): child.Show(False)

		self.game_p = GamePanel(self,self.gameDuration)
	def setMenubar(self):
		menuBar = wx.MenuBar()
		
		FILE_MENU = wx.Menu()
		FILE_MENU.Append(101, "Exit", "")
		menuBar.Append(FILE_MENU, "File")

		ABOUT_MENU = wx.Menu()
		
		self.SetMenuBar(menuBar)
	def binding(self):
		self.Bind(wx.EVT_MENU, self.exit, id=101)
	def exit(self,e):
		self.Close()


class GamePanel(wx.Panel):
	def __init__(self, parent, i):
		self.count_answered=0
		self.gameDuration = i
		self.gameDurationi = i
		self.parent = parent
		self.font = wx.Font(18,wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
		self.font_gamo = wx.Font(40,wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL )
		self.font50=wx.Font(50,wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL )
		
		self.cfg = wx.Config('RESULTS')
		
		wx.Panel.__init__(self,parent,-1,(0,0),wx.Size(1500,1500))
		paneli = wx.Panel(self,-1)
		
		self.expressionLabel = wx.StaticText(paneli,-1, self.generateExpression(),
									style = wx.ALIGN_CENTRE  | wx.ST_NO_AUTORESIZE)
		self.expressionLabel.SetFont(self.font_gamo)
		tmp_sizer = wx.BoxSizer(wx.HORIZONTAL)
		tmp_sizer.Add(self.expressionLabel,1,wx.ALIGN_CENTER)
		paneli.SetSizer(tmp_sizer)
		
		
		self.answer = wx.TextCtrl(self,-1,"",(0,25),style = wx.TE_CENTRE |  wx.TE_MULTILINE)
		self.answer.SetFont(self.font_gamo)
		self.answer.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
		self.answer.SetFocus()
		
		
		ans_p = wx.Panel(self,-1)
		ans_sz = wx.BoxSizer(wx.HORIZONTAL)
		self.answered = wx.StaticText(ans_p,-1,str(self.count_answered),style = wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
		ans_sz.Add(self.answered,1,wx.ALIGN_CENTER)
		self.answered.SetFont(self.font50)
		ans_p.SetSizer(ans_sz)
		
		
		time_p = wx.Panel(self,-1)
		self.TimeCountDown = wx.StaticText(time_p,-1,str(self.gameDuration),style = wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE)
		self.TimeCountDown.SetFont(self.font)
		time_sz = wx.BoxSizer(wx.HORIZONTAL)
		time_sz.Add(self.TimeCountDown,1,wx.ALIGN_CENTER)
		time_p.SetSizer(time_sz)
		
		##### TIMER
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.timerCountdown, self.timer)
		self.timer.Start(1000)
		##### TIMER
		
		
		sizer__=wx.BoxSizer(wx.HORIZONTAL)
		sizer__.Add(ans_p,1,wx.EXPAND)
		sizer__.Add(time_p,1,wx.EXPAND)
		
		
		##   M A I N      S I Z E R
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(paneli,1,wx.EXPAND)
		sizer.Add(self.answer,1,wx.EXPAND | wx.LEFT | wx.RIGHT, 50)
		sizer.Add(sizer__,1,wx.EXPAND)
		
		
		parent.SetSizer(sizer)
		parent.Layout()
	def onKeyDown(self, event):
		keycode = event.GetKeyCode()
		if (keycode == wx.WXK_RETURN) or (keycode==wx.WXK_NUMPAD_ENTER):
			if self.check():
				self.count_answered += 1
				self.answered.SetLabel(str(self.count_answered))
				self.expressionLabel.SetLabel(self.generateExpression())
				self.answer.Clear()
			else:
				self.answer.SetValue("")
		else:
			event.Skip()
	def timerCountdown(self,evt):
		self.gameDuration-=1
		if self.gameDuration!=-1:
			self.answer.SetFocus()
			self.TimeCountDown.SetLabel(str(self.gameDuration))
		else:
			self.timer.Stop()
			for child in self.parent.MainPanel.GetChildren(): child.Show(True)
			self.Show(False)
			
			res=[]
			if self.cfg.Exists('allResults'): # "1/2,5/6,..,45/88"
				res = self.cfg.Read('allResults').split(",")
			else:
				self.cfg.Write("allResults", "")
				
			res.remove("")#I Have no idea why this is in it
			score = "%d/%d"%(self.count_answered, self.gameDurationi)
			res.append(score)
			##fractionize and defractionize in order to sort easily
			
			print res
			res = map(fractions.Fraction, res)
			res.sort()
			res.reverse()
			res = map(str, res)
			#
			self.cfg.Write("allResults", ','.join(res))
			
			res = res[:5]
			
			fr = wx.MiniFrame(None, -1, "results")
			wx.StaticText(fr,-1,"TOP scores - answered/time",(0,0))
			for pos, i in enumerate(res):
				wx.StaticText(fr, -1, "%d)        %s"%(pos+1, i), (0, 25 + pos*25))
			
			
			self.f = fr
			wx.StaticText(fr,-1,'damtavrda.\nshedegi: %s qula\nxangrdzlivoba: %s wami\n\n\n\t\tTavidan?'%(self.count_answered,self.gameDurationi),(150,150))
			wx.Button(fr,11,"close",(150,100),wx.Size(50,25)).Bind(wx.EVT_BUTTON,self.close)
			fr.Centre()
			fr.Show()
	def close(self,e):
		self.f.Close()
	def check(self):
		try:
			ans = int(self.answer.GetValue())
			return ans == eval(self.expressionLabel.GetLabelText())
		except Exception, e:
			return False
	def generateExpression(self):
		a = random.randrange(10)
		op = random.choice("+-/*")
		b = random.randrange(10)
		if op=="/" and (b==0 or a%b!=0):
			return self.generateExpression()
		else:
			return "%d %s %d" % (a, op, b)
		
app = wx.App(0)
frame = MathQuizFrame()
frame.Centre()
frame.Show(True)
app.MainLoop()