# -*- coding: utf-8 -*-
#.split(',')

import wx
#import tweepy
import mastodon
tag_array1=[]
tag_array2=[]
import sys, codecs
import oath
import os
import os.path
from PIL import Image
import json


# SOMEDAY 使用している場所を見て適切なファイル名に変更する
otaku1exist=os.path.exists("./subjects.txt")
otaku2exist=os.path.exists("./channels.txt")

if not otaku1exist:
    #無ければ、(ほぼ)空のファイルを作成する
    f=open('subjects.txt','w',encoding='UTF-8')
    f.write('\n')
    f.close()
    
f = open("subjects.txt","r",encoding='UTF-8')

for row in f:
    #row=row.encode('utf-8')
    tag_array1.append(row)
    tag_array1.sort()

f.close()

if not otaku2exist:
    #無ければ、(ほぼ)空のファイルを作成する
    g = open('channels.txt','w',encoding='UTF-8')
    g.write('\n')
    g.close()
    
g = open("channels.txt","r",encoding='UTF-8')

for row in g:
    #row=row.encode('utf-8')
    tag_array2.append(row)

g.close()


# ユーザー情報を読み込む
FilePointer=open('user.json','r')

Setting=json.load(FilePointer)
#print(Setting)
FilePointer.close()


# mastodon をする準備
mstdn_handler=mastodon.Mastodon(
    client_id='client_cred.txt',
    access_token='user_cred.txt',
    api_base_url=Setting['url']
)

# old twitter
# create API                                                                
#api = tweepy.API(auth_handler=auth)

if __name__ == "__main__":
    #---------------使うもの諸々定義----------------------------------------

    application = wx.App()

    #---------------レイアウト定義--------------------------------------------
    layout_toukou=wx.BoxSizer(wx.VERTICAL)
    
    post_sizer=wx.GridSizer(1,1,gap=wx.Size(0,0))
    #add1_sizer=wx.GridSizer(1,1)
    #add2_sizer=wx.GridSizer(1,1)

    #frame = wx.Frame(None,wx.ID_ANY,u"テストフレーム")
    frame = wx.Frame(None,wx.ID_ANY,u"グローバル理工丼",
                     style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
                     #デフォは横400、たて220ちょい
                     | wx.CLIP_CHILDREN,size=(400,250)
    )

    # Hint:mastodonは暗めの背景が多めなのでそれ系の背景色にするかも
    frame.SetBackgroundColour("#e8e8e8")
    frame.CreateStatusBar()
    frame.SetStatusText(u"ready")

#--------------------------関数群定義-------------------------------
def post_event(event):
    # toot する
    bun=toukou.GetValue()
    # tag1:番組名を入れる欄
    tag1=combobox_1.GetValue().rstrip()
    # tag2:テレビ局名を入れる欄
    tag2=combobox_2.GetValue().rstrip()

    #print('tag1:'+tag1)
    #print('tag1.length:'+str(len(tag1)))
    #print('tag2.length:'+str(len(tag2)))

    if len(tag1) != 0:
        if tag1[0] != "#":
            tag1="#"+tag1
        tag1=' '+tag1

    if len(tag2) != 0:
        if tag2[0] != "#":
            tag2="#"+tag2
        tag2=' '+tag2

    try:        
        mstdn_handler.toot(bun+tag1+tag2)
    except:
        frame.SetStatusText(u"投稿失敗:"+bun+tag1+tag2)
    else:
        #上手くいったら
        #テキストボックスを空にして次の投稿に備える
        toukou.Clear()

        
def OnKeyChar(event):
    #キーを押す毎に呼び出される?
    key = event.GetKeyCode()
    #実況性を高めるために、Enter キー押下で投稿
    #("Enterキーで投稿する" のチェックが付いているときのみ)
    if key  ==  wx.WXK_RETURN and checkbox.GetValue():
        post_event(event)
    else: event.Skip()

def OnCheckbox(event):
    #print(front_checkbox.GetValue())
    if front_checkbox.GetValue() :
        frame.SetWindowStyleFlag(style= frame.GetWindowStyleFlag() |
                                 wx.STAY_ON_TOP)
    else:
        frame.SetWindowStyleFlag(style= frame.GetWindowStyleFlag() &
                                 (~ wx.STAY_ON_TOP))

def add1(event):
    #タグ1(番組名)に現在入力してある文字列をプリセットに追加

    NewTag=combobox_1.GetValue()#.GetValue()で現在のcomboboxの値を取得可
    #能
    if NewTag[0] != "#":
        NewTag='#'+NewTag
        
    print(NewTag)
    if NewTag in tag_array1:
        return
    
    #ファイル書き込み
    f = open( "subjects.txt", "a",encoding='UTF-8' )
    try:
        
        # 文字列を追記
        f.write( (u"\n"+NewTag) )
          
    finally:
        f.close()


    #UIへ追加
    tag_array1.append(NewTag)
    combobox_1.Append(NewTag)
    #print "add"

def add2(event):
    #タグ2(テレビ局名)に現在入力してある文字列をプリセットに追加
    NewTag=combobox_2.GetValue()#.GetValue()で現在のcomboboxの値を取得
    #可能
    if Newtag[0]!='#':
        NewTag='#'+NewTag
        
    print(NewTag)

    if NewTag in tag_array2:
        return
    
    #ファイル書き込み
    f = open( "channels.txt", "a",encoding='UTF-8' )
    #print type(add_)
    try:
        
        # 文字列を追記
        f.write( (u"\n"+NewTag) )
          
    finally:
        f.close()


    #UIへ追加
    tag_array2.append(NewTag)
    combobox_2.Append(NewTag)
    #print "add"
    
def geticon():
    #発言者のアイコンを取得し、保存する
    
    
    me=mstdn_handler.account_verify_credentials()
    iconurl=me['avatar']
    
    
    # 付属の oath.py でダウンロードする
    # iconname 拡張子無しで保存される
    # Hint:例外処理をした方が良いかも
    iconname=oath.download(iconurl)

    
    hyo=iconurl.split('?')
    CleanUrl=hyo[0]
    # 保存したファイルに合せた拡張子に変名する
    # hoge.png.gif の様なファイル名にされている可能性があるので、
    # ライブラリに頼った方が良い
    root, ext = os.path.splitext(CleanUrl)
    #print ext
    SaveName='icon'+ext

    #既にファイルがある場合は削除する
    if os.path.exists('./'+SaveName):
        os.remove(SaveName)
        
    #リサイズ
    gazo=Image.open(iconname,'r')
    mini_gazo=gazo.resize((80,80),resample=1)
    mini_gazo.save(SaveName)

    #後始末
    os.remove(iconname)
    return SaveName





if __name__ == "__main__":

    def ExitHandler(self):
        frame.Destroy()
        #os.remove("./icon.png")
        
        sys.exit()
        
    frame.Bind(wx.EVT_CLOSE, ExitHandler)

    #iconname='test.png'
    iconname=geticon()

    #--------------------------panel------------------------------------------------------
    write_panel = wx.Panel(frame,wx.ID_ANY,pos=(10,10),size=(250,80))
    post_panel = wx.Panel(frame,wx.ID_ANY,pos=(260,100),size=(80,20))
    add1_panel = wx.Panel(frame,wx.ID_ANY,pos=(15,160),size=(160,20))
    add2_panel = wx.Panel(frame,wx.ID_ANY,pos=(180,160),size=(160,20))
    
    check_panel = wx.Panel(frame,wx.ID_ANY,pos=(20,100),size=(120,20))
    front_check_panel = wx.Panel(frame,wx.ID_ANY,pos=(150,100),size=(150,20))
    
    choice_1_panel = wx.Panel(frame,wx.ID_ANY,pos=(15,130),size=(160,26))
    choice_2_panel = wx.Panel(frame,wx.ID_ANY,pos=(180,130),size=(160,26))
    add1_panel.SetBackgroundColour("#FF0000")
    add2_panel.SetBackgroundColour("#FF0000")
    #-------------------------------button他パーツ--------------------------------------------------
    button_post = wx.Button(post_panel,wx.ID_ANY,"post",size=(80,20))
    button_add1 = wx.Button(add1_panel,wx.ID_ANY,u"タグ1追加",size=(160,20))
    button_add2 = wx.Button(add2_panel,wx.ID_ANY,u"タグ2追加",size=(160,20))
    toukou = wx.TextCtrl(write_panel,wx.ID_ANY,style=wx.TE_MULTILINE,size=(250,80))
    checkbox = wx.CheckBox(check_panel,wx.ID_ANY,u"Enterキーで投稿する")
    checkbox.SetValue(True)
    front_checkbox = wx.CheckBox(front_check_panel,wx.ID_ANY,
                                 u"常に手前に表示")
    front_checkbox.SetValue(False)
    combobox_1 = wx.ComboBox(choice_1_panel,wx.ID_ANY,u"タグ1",choices=tag_array1,style=wx.CB_DROPDOWN,size=(160,26))
    combobox_2 = wx.ComboBox(choice_2_panel,wx.ID_ANY,u"タグ2",choices=tag_array2,style=wx.CB_DROPDOWN,size=(160,26))
    image = wx.Image(iconname, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    button_account = wx.StaticBitmap(frame, -1, image, pos=(278, 10),size=(80,80))
    #-------------------------------layoutに追加---------------------------------------------------
    layout_toukou.Add(toukou,flag=wx.EXPAND)
    post_sizer.Add(button_post,flag=wx.GROW)

    #----------------------------------イベント----------------------------------
    button_post.Bind(wx.EVT_BUTTON,post_event)
    button_add1.Bind(wx.EVT_BUTTON,add1)
    button_add2.Bind(wx.EVT_BUTTON,add2)
    toukou.Bind(wx.EVT_KEY_DOWN, OnKeyChar)

    front_checkbox.Bind(wx.EVT_CHECKBOX,OnCheckbox)
    #write_panel.SetSizer(layout_toukou)
    

    #g_panel = wx.Panel(frame,wx.ID_ANY,pos=(270,0),size=(80,220))
    #g_panel.SetBackgroundColour("#00FF00")

    #b_panel = wx.Panel(frame,wx.ID_ANY,pos=(160,0),size=(80,300))
    #b_panel.SetBackgroundColour("#0000FF")

    frame.Show()
    
    application.MainLoop()
   
    
