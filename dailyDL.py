import webbrowser
import tkinter
from tkinter import messagebox
from selenium import webdriver
import chromedriver_binary


daily = 'https://csvex.com/kabu.plus/csv/japan-all-stock-prices-2/daily/'
sihyo = 'https://kabu.plus/data/statistic1?fn=japan-all-stock-data'
fund = 'https://kabu.plus/data/finance1?fn=japan-all-stock-financial-results'
sinyo = 'https://csvex.com/kabu.plus/csv/japan-all-stock-margin-transactions/weekly/'

def dailyDL():
    print('daily dl')
    #use selenium
    driver = webdriver.Chrome(executable_path='D:\\install\\driver\\chromedriver.exe')
    driver.get('https://www.google.com/')
    

def histricalDL():
    print("histricalDL")

def createNewData():
    print("create new Data table.")

#ウインドウの作成
root = tkinter.Tk()
root.title("Kabu tool")
root.geometry("360x520")

#ボタンの作成
button = tkinter.Button(text="当日データDL",command=dailyDL)
button.place(x=20, y=70)

#ボタンの作成
button = tkinter.Button(text="ヒストリカルデータDL",command=histricalDL)
button.place(x=20, y=120)

#ボタンの作成
button = tkinter.Button(text="株価データ更新",command=createNewData)
button.place(x=20, y=170)

#ウインドウの描画
root.mainloop()