import webbrowser
import tkinter
from tkinter import messagebox
from selenium import webdriver
import time
import urllib.request
import pandas as pd
import base64
from tqdm import tqdm
import requests
import os
from random import randint

userID = ''
password = ''

stockPriceDownloaded = './tmp/stockprice.csv'
sihyoDownloaded = './tmp/sihyo.csv'
fundDownloaded = './tmp/fund.csv'
sinyoDownloaded = './tmp/sinyo.csv'

stockPriceURL= 'https://csvex.com/kabu.plus/csv/japan-all-stock-prices-2/daily/'
sihyoURL = 'https://csvex.com/kabu.plus/csv/japan-all-stock-data/daily/'
fundURL = 'https://csvex.com/kabu.plus/csv/japan-all-stock-financial-results/monthly/'
sinyoURL = 'https://csvex.com/kabu.plus/csv/japan-all-stock-margin-transactions/weekly/'

stockPricePrefix = 'japan-all-stock-prices-2_'
sihyoPrefix = 'japan-all-stock-data_'
fundPrefix = 'japan-all-stock-financial-results_'
sinyoPrefix = 'japan-all-stock-margin-transactions_'

#elem = driver.find_element_by_class_name("ui-link")

class GuiComponents:
    def __init__(self):
        #ウインドウの作成
        self.root = tkinter.Tk()
        self.root.title("Kabu tool")
        self.root.geometry("360x520")
    
    def addButtons(self, func, x, y, title):
        #ボタンの作成
        button = tkinter.Button(text=title,command=func)
        button.place(x=x, y=y)
    
    def addLabel(self,x, y, text):
        # ラベル
        lbl = tkinter.Label(text=text)
        lbl.place(x=x, y=y)
    
    def popupMessage(self,title, text):
        messagebox.showinfo(title, text)
    
    def popupError(self,title, text):
        messagebox.showerror(title, text)
        
    def start(self):
        #ウインドウの描画
        self.root.mainloop()

#テスト用のスタブ
class Test:
    def func1(self):
        print('func1')
    
    def func2(self):
        print('func2')
    
    def func3(self):
        print('func3')

class DLscript:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='D:\\install\\driver\\chromedriver.exe')
        #ダウンロード済ファイルを記したファイルを読み込む
        with open(stockPriceDownloaded) as f:
            self.SPhistorical = f.readlines()
        with open(sihyoDownloaded) as f:
            self.sihyoHistrical = f.readlines()
        with open(fundDownloaded) as f:
            self.fundHistrical = f.readlines()
        with open(sinyoDownloaded) as f:
            self.sinyoHistrical = f.readlines()

    def DataDL(self,URL, prefix,histrical, DownloadedFileName, dir):
        self.driver.get(URL)
        elems = self.driver.find_elements_by_tag_name('a')
        #リンク先のcsvファイル名取得

        add = ""
        for elem in elems:
            if prefix in elem.text:
                if elem.text+'\n' not in histrical:
                    print('hoge')
                    add = add + elem.text + "\n"
        
        
        self.addFileTail(add,DownloadedFileName)
        print('過去ファイルのダウンロード完了。')

    def setup_basic_auth(self,base_uri, user, password):
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(
                realm=None,
                uri=base_uri,
                user=user,
                passwd=password)
        auth_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(auth_handler)
        urllib.request.install_opener(opener)

    def download_file(self,url, dir):
        filename = dir + os.path.basename(url)
        print('Downloading ... {0} as {1}'.format(url, filename))
        urllib.request.urlretrieve(url, filename)
    
    def addFileTail(self,add,filename):
        with open(filename, mode='a') as f:
            f.write(add)
    
    def histricalDataDL(self):
        self.DataDL(stockPriceURL,stockPricePrefix,self.SPhistorical,stockPriceDownloaded ,'./info/stockprice/')
        #self.DataDL(sihyoURL, sihyoPrefix, self.sihyoHistrical, sihyoDownloaded, './info/sihyo/')
        #self.DataDL(fundURL, fundPrefix, self.fundHistrical, fundDownloaded, './info/fund/')
        #self.DataDL(sinyoURL, sinyoPrefix, self.sinyoHistrical, sinyoDownloaded, './info/sinyo/')

class Analyze:
    def todaysReport(self,latestFilename):
        #load as dataframe
        df = pd.read_csv(latestFilename)

        #市場別売買代金
        
        #





if __name__ == '__main__':
    DLfuc = DLscript()
    test = Test()    
    gui = GuiComponents()
    gui.addButtons(DLfuc.histricalDataDL,20, 70,"過去データダウンロード")
    gui.addLabel(20, 300, "最新データ:")
    gui.addButtons(test.func2,20, 120,"当日データ更新")
    gui.addLabel(20, 300, "最新データ:")
    gui.addButtons(test.func3,20, 170,"ほげ")
    gui.start()