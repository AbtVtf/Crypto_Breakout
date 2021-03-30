# Crypto_Breakout

This is a collection of scripts that manipulate data extracted from the Binance API. 
I am trying to always add a GUI so if you are not that into Python you could just run the script and use the GUI.
In the near future I will add fundamental analysis and sentiment analysis scripts, as soon as I finish them.

# Script Usage

crypto_gui.py

This script finds either consolidations or breakouts from consolidations. In order for the pattern to be valid it
needs to form inside a given percentage.
Since it operates with candle-stick data you need to select a timeframe for each candle and a number of candles.

The script works by generating a list of all closing prices for the number of candles you selected. 
If the difference between the highest and the lowest price is smaller than the percent selected, that means that
the coin is consolidating inside the selected time period.

In case Breakout Scan is selected, the script will first check if all the candles except the last one are consoidating.
If the candles are consolidating, the script will check it the closing price of the last candle (the current ptice) is
higher than the highest closing price inside the consolidation. If it is, that means that the coin is exiting a 
consolidation period.

telegram_custom_alert.py

This script will take all the 1 minute cadles for the selected time period and compare the closing price of each.
if the current price of the coin is higher than the highest high of the selected period, the script will send a
telegram alert through the telegram api with the name of the coin, the price, and the percentage in increase.
