# -*- coding: utf-8 -*-

__author__ = 'HE Yuanhang'

import ttk
import json
import urllib2
import threading
from Tkinter import *

dataListTmp = []
def writeDataToFile():
    with open(u'排行榜.html','w') as f:
        f.write(r'<meta charset="utf8"/><table><tr><th>排名</th><th>名称</th><th>图标</th><th>简介</th><th>下载链接</th></tr>')
        for x in xrange(len(dataListTmp)):
            f.write(r'<tr>')
            f.write(r'<td>%s</td>'%(x + 1))
            f.write(r'<td>%s</td>'%dataListTmp[x]['title'].encode('utf8'))
            f.write(ur'<td><img src="%s" alt="ICON" height=80 width=80/></td>'%dataListTmp[x]['icon'])
            f.write(r'<td>%s</td>'%dataListTmp[x]['description'].encode('utf8'))
            f.write(r'<td><a href="%s">download</a></td>'%dataListTmp[x]['detail']['appDetail']['apk'][0]['downloadUrl']['url'])
            f.write(r'</tr>')
        f.write(r'</table>')

def downLoadApp(url,name):
    def __saveApp(data,name):
        with open('%s.apk'%name,'wb') as f:f.write(data)
    iHeaders = {"User-Agent": "Dalvik/1.6.0 (Linux; U; Android 4.2.2; Droid4X-WIN Build/JDQ39E)"}
    req = urllib2.Request(url , headers=iHeaders)
    __saveApp(urllib2.urlopen(req).read(),name)

def downAll():
    def __downAll():
        count = len(dataListTmp)
        for x in xrange(count):
            downLoadApp(dataListTmp[x]['detail']['appDetail']['apk'][0]['downloadUrl']['url'],dataListTmp[x]['title'])
            progressbar1['value'] = int(float(x + 1) / count * 100)
    t = threading.Thread(target=__downAll)
    t.setDaemon(True)
    t.start()

def getUrl(startCount = 0,maxCount = 15):
    topListType = {
                    u'应用周排行':r'apps/tops/weeklytopapp',
                    u'应用好评榜':r'apps/tops/likemosttopapp',
                    u'应用飙升榜':r'apps/tops/raisemosttopapp',
                    u'单机周榜':r'games/tops/TOP_WEEKLY_DOWNLOAD_CONSOLE_GAME',
                    u'网游周榜':r'games/tops/TOP_WEEKLY_DOWNLOAD_ONLINE_GAME',
                    u'游戏口碑榜':r'games/tops/TOP_OPERATION_GAME/436',
                    u'本周上架新游戏':r'games/tops/TOP_OPERATION_GAME/434',
                    }
    return r'http://apis.wandoujia.com/five/v2/%s?start=%s&max=%s'%(topListType[combox1.get()],startCount,maxCount)

def getHTMLStr(startCount = 0,maxCount = 15):
    data = urllib2.urlopen(url = getUrl(startCount,maxCount),timeout = 20).read()
    return data

def getAppNameList():
    global dataListTmp
    dataListTmp = []
    appNameList = []
    appNeedCount = int(entry1.get())
    startCount = 0
    while appNeedCount > 0:
        maxCount = 15 if appNeedCount >= 15 else appNeedCount
        data = json.loads(getHTMLStr(startCount,maxCount))
        if str(data['hasMore']).lower() == 'false':
            break
        dataListTmp += data['entity']
        appNameList += [data['entity'][x]['title'] for x in xrange(len(data['entity']))]
        appNeedCount -= 15
        startCount += 15
    return appNameList

def showTopList():
    listBox1.delete(0,END)
    i = 0
    for appName in getAppNameList():
        listBox1.insert(i,appName)
        i += 1

def getApps():
    if entry1.get().isdigit():
        showTopList()
    else:
        pass

def testDef():
    pass

root = Tk()
root.title(u"豌豆荚排行榜抓取")
label1Frame = Frame(root)
label2Frame = Frame(root)
buttonFrame = Frame(root)
bottomFrame = Frame(root)
searchFrame = Frame(root)
label1 = Label(label1Frame,text = u'选择排行类型').pack(side = LEFT)
combox1 = ttk.Combobox(label1Frame,values=[u'应用周排行',u'应用好评榜',u'应用飙升榜',u'单机周榜',u'网游周榜',u'游戏口碑榜',u'本周上架新游戏'])
combox1.set(u'应用周排行')
combox1.pack(side = RIGHT)
label2 = Label(label2Frame,text = u'输入获取数量:').pack(side = LEFT)
entry1 = Entry(label2Frame)
entry1.insert(0,u'15')
entry1.pack(side = RIGHT)
button1 = Button(buttonFrame,text = u'抓取',command = getApps).pack(side = LEFT)
button2 = Button(buttonFrame,text = u'存储为HTML',command = writeDataToFile).pack(side = RIGHT)
scrollbar = Scrollbar(bottomFrame)
scrollbar.pack(side=RIGHT, fill=Y)
listBox1 = Listbox(bottomFrame,yscrollcommand=scrollbar.set)
listBox1.pack()
scrollbar.config(command=listBox1.yview)
progressbar1 = ttk.Progressbar(searchFrame)
progressbar1.pack(side = LEFT)
button3 = Button(searchFrame,text = u'全部下载到本地',command = downAll).pack(side = RIGHT)
label1Frame.pack()
label2Frame.pack()
buttonFrame.pack()
bottomFrame.pack()
searchFrame.pack()
root.mainloop()