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

downloaded_fileName = './downloaded.txt'

daily = 'https://csvex.com/kabu.plus/csv/japan-all-stock-prices-2/daily/'
sihyo = 'https://kabu.plus/data/statistic1?fn=japan-all-stock-data'
fund = 'https://kabu.plus/data/finance1?fn=japan-all-stock-financial-results'
sinyo = 'https://csvex.com/kabu.plus/csv/japan-all-stock-margin-transactions/weekly/'



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
    
    def popupMessage(self, text):
        messagebox.showinfo(text)
        
    def start(self):
        #ウインドウの描画
        self.root.mainloop()

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
        self.driver.get(daily)
        self.historicalData = pd.read_csv(downloaded_fileName)
        print(self.historicalData)

    def dailyDataDL(self):
        self.elems = self.driver.find_elements_by_tag_name('a')
        self.links = []
        #リンク先のcsvファイル名取得

        add = ""
        for elem in self.elems:
            if 'japan-all-stock-prices-2_' in elem.text:
                if elem.text not in self.historicalData:
                    # Basic認証用の文字列を作成.
                    basic_user_and_pasword = base64.b64encode('{}:{}'.format(userID, password).encode('utf-8'))
                    url = daily + elem.text
                    print('◇◆'*30)
                    print(elem.text + 'をダウンロードします。')

                    # Basic認証付きの、GETリクエストを作成する.
                    self.setup_basic_auth(url, userID, password)
                    
                    self.download_file(url)
                    print(elem.text + 'のダウンロード完了')
                    add = add + elem.text + ","
                    time.sleep(20 + randint(5,30))
            
        self.addFileTail(add)
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

    def download_file(self,url):
        filename = "info/" + os.path.basename(url)
        print('Downloading ... {0} as {1}'.format(url, filename))
        urllib.request.urlretrieve(url, filename)
    
    def addFileTail(self,add):
        tmp = self.historicalData + add
        tmp.to_csv(downloaded_fileName)

if __name__ == '__main__':
    test = Test()
    gui = GuiComponents()
    gui.addButtons(test.func1,20, 70,"過去データダウンロード")
    gui.addButtons(test.func2,20, 120,"当日データ更新")
    gui.addButtons(test.func3,20, 170,"ほげ")
    gui.start()