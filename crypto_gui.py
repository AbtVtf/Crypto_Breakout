from binance.client import Client
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import tkinter.ttk as ttk
import threading

window = Tk()

binance_api_key = 'l4MTPxt1TfARPXt90dCG8UT8ghpa6Rnj0NL7mDIbsmCPU8KQGbjLN62H4ZY6ldlM'    #Enter your own API-key here
binance_api_secret = '2ztsVWZoTxTbQCxq3W9LL9GBH2gmdqcbq3UuRtC9Oo6IFSe4KziPSrGz176ewa3I' #Enter your own API-secret here


# A list of all banned pairs, some are added because they are not listed
ban_list = ['EUR', 'BRL', 'BVND', 'DAI', 'NGN', 'IDRT', 'TRY', 'UAH', 'RUB', 'ZAR', 'USDC', 'UP', 'DOWN', 'AE', 'LEND',
            'TUSD', 'GBP', 'VAI', 'PAX', 'SUSD', 'BIDR', 'WBTC', 'XZC', 'BKRW', 'DGD', 'WBTC', 'RENBTC', 'TUSDBUSD', 'TUSDBTC',
            'TUSD', 'BUSDUSDT', 'AUDUSDT', 'USDSBUSDT', 'USDSUSDT', 'BEAR', 'BULL', 'BCCUSDT', 'ERDUSDT']


# The client object that's gonna do all the heavy lifting
client = Client(api_key=binance_api_key, api_secret=binance_api_secret)


# With this function we get a list of all the pairs available for a pair. The coin argument is versus, as in BTC, ETH, USDT, BUSD
def generate_all_pairs(client, coin):
    tickers = client.get_orderbook_tickers()

    all_pairs = []
    my_pairs = []

    #Getting all tickers from binance and parsing only the desired pairs
    for i in tickers:
        if coin in i['symbol']:
            all_pairs.append(i['symbol'])

    # Removing all the pairs from the ban list and parsing the list for any potential errors
    for i in ban_list:
        for a in all_pairs:
            if i in a:
                all_pairs.remove(a)

    for i in all_pairs:
        pair = i.split(coin)[0]
        if pair != '':
            my_pairs.append(i)

    return my_pairs

# Function to call the main function, the threading module was acting weird, lagging the entire program, so I found this workaround
def caller():
    threading.Thread(target=get_candles).start()
btn = Button(window, text="Scan", command=caller)
btn.grid(column=1, row=5)

# Main Function
def get_candles():

    # Refresing the window with every call
    my_tree.delete(*my_tree.get_children())
    lbl_load['text']= 'Scanning, please be patient...'



    # tree_index is used to index rows in the tree view table, it needs to be different every time
    # due to some errors that appeared I decided to increase it by 10, instead of 1 with every loop
    counter = 0
    tree_index = 1
    all_pairs = generate_all_pairs(client, pair.get())

    # The maximum percentage allowed between the highest closing price and the lowest closing price
    percent = 1 - (float(percentage_number.get()) / 100)

    for coins in all_pairs:

        # Using the info from the combo-menu we can retrieve the right candles
        if combo.get() == '30M':
            # We start by creating a list of all the closing prices and ordering it in ascending order
            # Repeat the steps for every timeframe
            candles = client.get_klines(symbol=coins, interval=Client.KLINE_INTERVAL_30MINUTE, limit=candles_number.get())
            close_list = []
            for i in range(len(candles)):
                close_list.append(float(candles[i][4]))
            close_list.sort()

        elif combo.get() == '1H':
            candles = client.get_klines(symbol=coins, interval=Client.KLINE_INTERVAL_1HOUR, limit=candles_number.get())
            close_list = []
            for i in range(len(candles)):
                close_list.append(float(candles[i][4]))
            close_list.sort()

        elif combo.get() == '4H':
            candles = client.get_klines(symbol=coins, interval=Client.KLINE_INTERVAL_4HOUR, limit=candles_number.get())
            close_list = []
            for i in range(len(candles)):
                close_list.append(float(candles[i][4]))
            close_list.sort()

        elif combo.get() == '1D':
            candles = client.get_klines(symbol=coins, interval=Client.KLINE_INTERVAL_1DAY, limit=candles_number.get())
            close_list=[]
            for i in range(len(candles)):
                close_list.append(float(candles[i][4]))
            close_list.sort()


        # By multiplying the highest closing price with the percentage we can find the minimun value allowed
        if close_list[0] > close_list[-1] * percent:


            # Enabling this will return only coins with the current price higher than the max closing price, currently it is off
            if breakout.get() == 0:
                # I advise using a try except for this, sometimes the api might cause crashes or errors
                try:
                    # Volume of the current unit, this might be misleading sometimes if the current candle just started or is halfway through
                    volume = round(float(candles[-1][5]), 2)
                    price = round(float(candles[-1][4]), 5)

                    # Getting the percent difference between the last closing price and the current price and for volumes the same
                    price_percent = str(round((float(candles[-1][4]) - float(candles[-2][4]) * 100)/price, 2))
                    volume_percent = str(round((float(candles[-1][5]) - float(candles[-2][5]) * 100)/volume, 2))

                    #Inserting the values into the treeview object, take note of the extra caution on the iid argument
                    my_tree.insert(parent='', index='end', iid=tree_index + 1, text='Parent', values=(coins, volume, volume_percent+ '%',price, price_percent + '%'))
                    print(coins)
                    print(volume)
                    print(volume_percent)
                    print(price)
                    print('-----------------------------')
                except:
                    continue
                tree_index += 10
                counter += 1

                window.update()

            # Breakout scan enabled
            elif breakout.get() == 1:
                print(candles[-1][4])
                print(close_list[-1])
                if close_list[0] > close_list[-1] * percent:
                    if float(client.get_klines(symbol=coins, interval=Client.KLINE_INTERVAL_1DAY, limit=1)[0][4]) > close_list[-1]:
                        try:
                            # Volume of the current unit, this might be misleading sometimes if the current candle just started or is halfway through
                            volume = round(float(candles[-1][5]), 2)
                            price = round(float(candles[-1][4]), 5)

                            # Getting the percent difference between the last closing price and the current price and for volumes the same
                            price_percent = str(round((float(candles[-1][4]) - float(candles[-2][4]) * 100) / price, 2))
                            volume_percent = str(
                                round((float(candles[-1][5]) - float(candles[-2][5]) * 100) / volume, 2))

                            print(coins)
                            print(price)
                            print(close_list[-1])
                            print('-----------------------------')

                            # Inserting the values into the treeview object, take note of the extra caution on the iid argument
                            my_tree.insert(parent='', index='end', iid=tree_index + 1, text='Parent',
                                           values=(coins, volume, volume_percent + '%', price, price_percent + '%'))
                        except:
                            continue
                        tree_index += 10
                        counter += 1

                        window.update()
    # Loading label in the lower right corner
    if counter == 1:
        lbl_load['text'] = f'Scan completed. {counter} breakout found.'
    elif counter == 0:
        lbl_load['text'] = 'No breakouts detected'
    else:
        lbl_load['text'] = f'Scan completed. {counter} breakouts found.'



'''---------------GUI---------------'''
# For the GUI I decided to use grid instead of pack, in this case it does the job right
window.title("Coin Scanner")
window.geometry('700x260')
window.minsize(width='700', height='260')
window.configure(bg= '#2FB7FF')

timeframe_label = Label(window, background='#2FB7FF', text='Timeframe ')
timeframe_label.grid(column=0, row= 0)

combo = Combobox(window, width=9)
combo['values']= ("30M", '1H', '4H', '1D')
combo.current(3)
combo.grid(column=1, row=0)

candles_label = Label(window, text='Candles no. ',background= '#2FB7FF')
candles_label.grid(column=0, row= 1)

candles_number = Entry(window, width=12)
candles_number.grid(column=1, row=1)

percentage_label = Label(window, text='Percentage ',background= '#2FB7FF')
percentage_label.grid(column=0, row= 2)

percentage_number = Entry(window, width=12)
percentage_number.grid(column=1, row=2)

versus_label = Label(window, text='Versus ',background= '#2FB7FF')
versus_label.grid(column=0, row= 3)

pair = Entry(window,width=12)
pair.grid(column=1, row=3)

breakout = IntVar()
c2 = tk.Checkbutton(window, text='Breakout Scan', anchor=W, onvalue=1, offvalue=0, variable= breakout, background='#2FB7FF')
c2.grid(column=0, row=5)


# Declaring the tree object and its columns. Take note of the fact that I declare 6 columns but handle 7
# That is because by default an indexing column is autogenerated, but I am hiding it here
my_tree= ttk.Treeview(window)
my_tree['columns']=('Coin', 'Volume','Volume Chg', 'Price', 'Price Chg')

# First we address the column itself
my_tree.column('#0', width=0, minwidth = 0)
my_tree.column('Coin', anchor=W, width=100 , minwidth = 100)
my_tree.column('Volume', anchor=CENTER, width=100, minwidth = 100)
my_tree.column('Volume Chg', anchor=CENTER, width=100, minwidth = 100)
my_tree.column('Price', anchor=E, width=100, minwidth = 100)
my_tree.column('Price Chg', anchor=E, width=100, minwidth = 100)

# Afterwards we can address the actual heading text, the first argument must be the same as the first argument for the column
my_tree.heading('#0', text = '', anchor = W)
my_tree.heading('Coin', text = 'Coin', anchor = W)
my_tree.heading('Volume', text = 'Volume', anchor = W)
my_tree.heading('Volume Chg', text = 'Volume Chg', anchor = CENTER)
my_tree.heading('Price', text = 'Price', anchor = CENTER)
my_tree.heading('Price Chg', text = 'Price Chg', anchor = CENTER)

my_tree.grid(column = 3, row = 0, rowspan = 10, padx=10, pady=5)

lbl_load = Label(window, text='', background='#2FB7FF')
lbl_load.grid(row=11, column=3, sticky=E, padx = 10)

window.mainloop()
#Happy scanning
