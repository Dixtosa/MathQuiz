#!/usr/local/bin/python
# -*- coding: latin-1 -*-

#Girl Or Boy Lib Update
import wx
import urllib2
import sys
import os
import urllib,time
from Language import *
from _Info import *

URLs=["http://dixtosa.site.ge"]

class UPDATE:
	def __init__(self,parent,Mode):
		self.Ldata=LANGUAGE().Lang_Data()
		self.your=float(Version)
		self.parent=parent
		if Mode=="NonBack":
			self.ALL()
		if Mode=="Back":
			pass
		self.Bind(wx.EVT_CLOSE,self.cl)
	def cl(self,evt):
		os.remove("tmpData/tmp")
	def ALL(self):
		if self.CheckIsAvail()!="InetError":
			print "No InetError"
			url_,ver_=self.check_Higher(self.CheckIsAvail())
			if self.check_IsNewer(url_,ver_)=="Available":
				print "Available"
				if self.AskDown()=="YES":
					print "YES"
					self.parent.Close()
					self.Download()
				else:
					pass
	def CheckIsAvail(self):
		self.NEW={}
		for i in URLs:
			try:
				try_url=i+"/update.php?v=%s&n=%s"%(self.your,Name)
				source=urllib2.urlopen(try_url).read()
				NVI=source.find("New Version Is: ")+len("New Version Is: ")
				new=source[NVI:NVI+3]
				self.new=new
				self.NEW[i]=float(self.new)
				self.URL=try_url
			except:
				print "eror"
		if len(self.NEW)==0:
			return "InetError"
			wx.MessageBox(self.Ldata[15], self.Ldata[16])
		else:
			return self.NEW
	def check_Higher(self,Dict):
		rezult=[]
		for u in Dict:
			gio=[]
			for u_ in Dict:
				if Dict[u]>=Dict[u_]:
					gio.append(u)
				if len(gio)==len(Dict):
					rezult.append(gio[0])
		return rezult[0],Dict[rezult[0]]
	def check_IsNewer(self,url,Ver):
		if Ver>self.your:
			return "Available"
		else:
			wx.MessageBox("No Update Available", "!")
	def AskDown(self):
		Download_Q=wx.MessageDialog(None,self.Ldata[40]+"\n"+self.Ldata[41], "?",wx.YES_NO | wx.ICON_QUESTION)
		answer=Download_Q.ShowModal()
		if answer==wx.ID_YES:
			return "YES"
		else:
			return "NO"
	def Download(self):
		F=wx.Frame(None,-1,"Downloading",(0,0),wx.Size(600,400),style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		panel=wx.Panel(F,-1)
		self.gauge = wx.Gauge(panel, 57, 350,(0,100), size=(594, 40))
		self.text=wx.StaticText(panel,-1,"Download May Take Some Minutes And Clush CPU slightly",pos=(0,0))
		b=wx.Button(panel,-1,"DownLoad",(0,150),wx.Size(594,200))
		b.Bind(wx.EVT_BUTTON,self.Down)
		F.Show()
		F.Centre()
		self.f=F
	def SetValue_(self,e):
		pr=None
		try:
			pr=int(open("tmpData/tmp").read())
		except:
			pr=""
		while type(pr)!=type(1):
			try:
				pr=int(open("tmpData/tmp").read())
			except:
				pass
		self.pr=pr
		if pr==100:
			self.text.SetLabel("completed")
			os.system(Name+"_v_"+self.new+".exe")
			self.f.Close()
		self.gauge.SetValue(pr)
	def Down(self,event):
		self.timer = wx.Timer(self.f, wx.ID_ANY)
		self.timer.Start(160)
		wx.EVT_TIMER(self.f, wx.ID_ANY, self.SetValue_)
		print "Down Clicked"
		f=open("tmpData/link","w")
		f.write("http://dixtosa.site.ge/GoB_v_1.4.exe:::ggg.exe")
		f.close()
		import subprocess as SP
		child_process = SP.Popen(["python", "get.py"])
