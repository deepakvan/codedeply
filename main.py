import datetime
import time
from time import sleep
import algobot_helper_functions as hf
from binance.um_futures import UMFutures
from binance.error import ClientError
import pandas as pd
import threading
import random
import os

# Replace 'vpn_address' with the address of your free VPN server
proxy_address = "103.38.205.69:5678"
import requests

# Set up proxy settings using environment variables
os.environ['HTTP_PROXY'] = proxy_address
os.environ['HTTPS_PROXY'] = proxy_address


""" kuber """
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
client=UMFutures(key=API_KEY,secret=API_SECRET)
coinpair_list= ['GALAUSDT']

orders = 0
symbol = ''

threading.Thread(target=hf.remove_pending_orders, args=(client,)).start()
while True:
    try:
        minutes = datetime.datetime.now().minute
        seconds = datetime.datetime.now().second
        if minutes % 15 <= 1 and seconds>=5: #minutes%15<=1
            # we need to get balance to check if the connection is good, or you have all the needed permissions
            balance = hf.get_balance_usdt(client)
            sleep(1)
            if balance == None:
                print('Cant connect to API. Check IP, restrictions or wait some time')
            if balance != None:
                print("My balance is: ", balance, " USDT")
                # getting position list:
                pos = hf.get_pos(client)
                print(f'You have {len(pos)} opened positions:\n{pos}')
                if len(pos)==0:
                    ord = hf.check_orders(client)
                    #print("working")
                    #print(ord)
                    # removing stop orders for closed positions
                    for elem in ord:
                        if not elem in pos:
                            hf.close_open_orders(client,elem)
                    random.shuffle(coinpair_list)
                    signal_list=[]
                    for coinpair in coinpair_list:
                        df=hf.fetch_historical_data(client,coinpair,'15m',10)
                        #print(coinpair)
                        signal_data=hf.get_signal(df)
                        #break
                        if signal_data!=None:
                            #print([coinpair,signal_data])
                            signal_list.append([coinpair,signal_data])
                    for sig in signal_list:
                        print(sig)
                    print("calling monitor")
                    #hf.monitor_signal(client,signal_list,coinpair_list)
                    threading.Thread(target=hf.monitor_signal, args=(client,signal_list,coinpair_list)).start()

            #break # break while loop if needed
            time.sleep(3*60)
        elif minutes % 15 > 1:
            if (13 - (minutes % 15)) * 60 > 0:
                print("sleeping for ", (13 - (minutes % 15)) * 60, " seconds (", 13 - (minutes % 15), ") minutes")
                time.sleep((13 - (minutes % 15)) * 60)
                print("awaked at ",datetime.datetime.now())
        time.sleep(5)
    except:
        print("Error in code Main Code")
        pass
