from tkinter import messagebox
from selenium import webdriver
import time,base64,requests,os,threading,tkinter
import urllib.request
import pandas as pd
from tqdm import tqdm
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
        self.root.geometry("1000x720")
    
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

class DLscript(GuiComponents):
    def __init__(self):
        super().__init__()
        
        #ダウンロード済ファイルを記したファイルを読み込む
        with open(stockPriceDownloaded) as f:
            self.SPhistorical = f.readlines()
        with open(sihyoDownloaded) as f:
            self.sihyoHistrical = f.readlines()
        with open(fundDownloaded) as f:
            self.fundHistrical = f.readlines()
        with open(sinyoDownloaded) as f:
            self.sinyoHistrical = f.readlines()

    def DataDL(self,URL, prefix,histrical, DownloadedFileName, dir, lock):
        
        #スレッドごとにタブを開く
        driver = webdriver.Chrome(executable_path='D:\\install\\driver\\chromedriver.exe')
        driver.get(URL)

        # ②ロック実行
        lock.acquire()
        elems = driver.find_elements_by_tag_name('a')
        #リンク先のcsvファイル名取得

        add = ""
        for elem in elems:
            if prefix in elem.text:
                if elem.text+'\n' not in histrical:
                    # Basic認証用の文字列を作成.
                    basic_user_and_pasword = base64.b64encode('{}:{}'.format(userID, password).encode('utf-8'))
                    
                    print('◇◆'*30)
                    print(elem.text + 'をダウンロードします。')

                    url = URL + elem.text
                    # Basic認証付きの、GETリクエストを作成する.
                    self.setup_basic_auth(url, userID, password)
                    
                    self.download_file(url,dir)
                    print(elem.text + 'のダウンロード完了')
                    add = add + elem.text + "\n"
                    time.sleep(randint(5,30))
            
        self.addFileTail(add,DownloadedFileName)
        self.update()

        #タブを閉じる
        driver.close()

        # ③アンロック
        lock.release()
        print('{}のダウンロード完了。'.format(prefix))
    
    #ダウンロード済データの更新
    def update(self):
        with open(stockPriceDownloaded) as f:
            self.SPhistorical = f.readlines()
        with open(sihyoDownloaded) as f:
            self.sihyoHistrical = f.readlines()
        with open(fundDownloaded) as f:
            self.fundHistrical = f.readlines()
        with open(sinyoDownloaded) as f:
            self.sinyoHistrical = f.readlines()

    #basic認証の設定
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

    #ファイルをDlする
    def download_file(self,url, dir):
        filename = dir + os.path.basename(url)
        print('Downloading ... \n{0} as {1}'.format(url, filename))
        urllib.request.urlretrieve(url, filename)
    
    #ファイルにDLしたファイル名を追記する関数
    def addFileTail(self, add,filename):
        #ファイルにダウンロード済ファイルを書き込む
        with open(filename, mode='a') as f:
            f.write(add)
    
    #DLを実行する。スレッドに分割する
    def AllDataDL(self):
        #ロックの作成
        lock = threading.Lock()

        thread1 = threading.Thread(target=self.DataDL, args=(stockPriceURL,stockPricePrefix,self.SPhistorical,stockPriceDownloaded ,'./info/stockprice/',lock))
        thread2 = threading.Thread(target=self.DataDL, args=(sihyoURL, sihyoPrefix, self.sihyoHistrical, sihyoDownloaded, './info/sihyo/',lock))
        thread3 = threading.Thread(target=self.DataDL, args=(fundURL, fundPrefix, self.fundHistrical, fundDownloaded, './info/fund/',lock))
        thread4 = threading.Thread(target=self.DataDL, args=(sinyoURL, sinyoPrefix, self.sinyoHistrical, sinyoDownloaded, './info/sinyo/',lock))

        #スレッドをスタートさせる
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()

    def latestDay(self):
        with open(stockPriceDownloaded) as f:
            return f.readlines()[-1]
    

def main():
    scripts = DLscript()
    test = Test()
    scripts.addButtons(scripts.AllDataDL,20, 70,"データ一括ダウンロード")
    scripts.addLabel(200, 70, "最新データ:{}".format(scripts.latestDay()))
    scripts.addButtons(test.func3,20, 170,"今日のレポート")
    scripts.start()

if __name__ == '__main__':
    main()