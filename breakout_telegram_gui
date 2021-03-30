from binance.client import Client
import requests, threading
from tkinter import *
from tkinter.ttk import *
import tkinter as tk

binance_api_key = ''  # Enter your own API-key here
binance_api_secret = ''  # Enter your own API-secret here
window = Tk()
cycle_counter = 0
client = Client(api_key=binance_api_key, api_secret=binance_api_secret)


def telegram_bot_sendtext(bot_message, bot_chatID):
    #This is the API Token you get from BotFather on Telegram
    bot_token = ''
    send_message = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_message)

    return response.json()


def send_text(message):
    chat_group = '1678535213'
    text = message
    telegram_bot_sendtext(text, chat_group)

def generate_list():
    ban_list = ['EUR', 'BRL', 'BVND', 'DAI', 'NGN', 'IDRT', 'TRY', 'UAH', 'RUB', 'ZAR', 'USDC', 'UP', 'DOWN', 'AE',
                'LEND',
                'TUSD', 'GBP', 'VAI', 'PAX', 'SUSD', 'BIDR', 'WBTC', 'XZC', 'BKRW', 'DGD', 'WBTC', 'RENBTC', 'TUSDBUSD',
                'TUSDBTC',
                'TUSD', 'BUSDUSDT', 'AUDUSDT', 'USDSBUSDT', 'USDSUSDT', 'BEAR', 'BULL', 'BCCUSDT', 'ERDUSDT',
                'XTZDOWNUSDT',
                'ADADOWNUSDT', 'TRXDOWNUSDT', 'DOTDOWNUSDT', 'YFIDOWNUSDT', 'XLMDOWNUSDT']

    tickers = client.get_orderbook_tickers()

    all_pairs = []

    # Getting all tickers from binance and parsing only the Bitcoin pairs
    for i in tickers:
        if versus.get() in i['symbol']:
            all_pairs.append(i['symbol'])

    for i in ban_list:
        for a in all_pairs:
            if i in a:
                all_pairs.remove(a)

    return all_pairs

def price_pairs():

    all_pairs = generate_list()
    # Getting the latest price for all the pairs
    counter = 1
    breakouts_counter = 0
    while True:
        print(f'Starting a new cycle on {len(all_pairs)} coins...')

        for pair in all_pairs:
            loading_lbl['text'] = f'Scanning {counter}/{len(all_pairs)}'

            # Print a pair and its index number from all pairs


            # Reset the counter
            if counter == len(all_pairs):
                counter = 0
            else:
                counter += 1

            last_candles = client.get_klines(symbol=pair, interval=Client.KLINE_INTERVAL_1MINUTE,
                                             limit=int(minutes_back.get()))
            closing_list = []

            for candle in range(len(last_candles)):
                closing_list.append(last_candles[candle][4])
            closing_list.sort()

            current_price = float(
                client.get_klines(symbol=pair, interval=Client.KLINE_INTERVAL_1MINUTE, limit=1)[0][4])
            biggest_close = float(closing_list[-1])

            print(pair)
            print(f'{counter}/{len(all_pairs)}')
            print(f'{current_price}\n{biggest_close}')

            # Insert the pair, biggest price and biggest close into the GUI text box
            text_insert = f'\n{pair} \nPrice: {current_price} \nClose: {biggest_close}\n----------------'
            text_box.insert(tk.END, text_insert)

            # Asses if a breakout is happening and send an alert if it does
            if current_price > biggest_close:
                print('breakout spotted')
                percent_difference = round((biggest_close * 100) / current_price, 2)
                message = f'Breakout detected on {pair}. With a price of {round(current_price,5)} {versus.get()}, {round((100 - percent_difference),2)}% more than the biggest closing price in the past {minutes_back.get()} minutes.'
                send_text(message)
                breakouts_counter += 1
                breakouts_lbl['text'] = f'Breakouts: {breakouts_counter}'



def caller():
    threading.Thread(target=price_pairs).start()


window.title("Coin Scanner")
window.geometry('200x300')
window.configure(bg='#2FB7FF')

versus_label = Label(window, text='Versus', background='#2FB7FF')
versus_label.grid(column=0, row=0, pady=5, padx=10)

versus = Entry(window, width=12)
versus.grid(column=1, row=0, pady=5, padx=10)

minutes_back_label = Label(window, text='Minutes', background='#2FB7FF')
minutes_back_label.grid(column=0, row=1, pady=5, padx=10)

minutes_back = Entry(window, width=12)
minutes_back.grid(column=1, row=1, pady=5, padx=10)

start_btn = Button(window, text='Start', command=caller)
start_btn.grid(column=1, row=5, pady=5, padx=10)

text_box = Text(window, width=20, height=10)
text_box.grid(column=0, row=6, columnspan=2, pady=5, padx=10)

loading_lbl = Label(window, text='', background='#2FB7FF')
loading_lbl.grid(column=1, row=7, columnspan=1, pady=10, )

breakouts_lbl = Label(window, text='Breakouts: 0', background='#2FB7FF')
breakouts_lbl.grid(column=0, row=7, columnspan=1, pady=10, )

window.mainloop()
