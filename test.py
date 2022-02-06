import time
import pyupbit
import datetime
import requests
import pprint


access = "xxx"
secret = "xxx"
myToken = "xxx"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text})

        


def get_ma5(ticker):
    """5일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_ma20(ticker):
    """20일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

upbit = pyupbit.Upbit(access, secret)
post_message(myToken,"#stock", "Start")


op_mode = False
hold = False


while True:
    try:
        now = datetime.datetime.now()
        
        if op_mode is True and hold is True:
            
            if now.minute == 6 and 10 <= now.second <= 19:
                ma5 = get_ma5("KRW-MANA")            
                current_price = get_current_price("KRW-MANA")
                
                if current_price < ma5 * 0.98:
                    balance = upbit.get_balance("KRW-MANA")
                    upbit.sell_market_order("KRW-MANA",balance)
                    hold = False
                    op_mode = False
                    time.sleep(10)
            
            if now.hour == 8 and now.minute == 59 and 50 <=now.second <= 59:
                if op_mode is True and hold is True:
                    ma5 = get_ma5("KRW-MANA")
                    current_price = get_current_price("KRW-MANA")
                    
                    if current_price < get_ma5:            
                        balance = upbit.get_balance("KRW-MANA")
                        upbit.sell_market_order("KRW-MANA",balance)
                        hold = False
                        op_mode = False
                        time.sleep(10)
                    
        if now.hour == 9 and 0 <= now.minute <=5:
            op_mode = True
            ma5 = get_ma5("KRW-MANA")
            ma20 = get_ma20("KRW-MANA")
            df = pyupbit.get_ohlcv("KRW-MANA", count=5)
            df_high = max(df.iloc[0]['high'], df.iloc[1]['high'], df.iloc[2]['high'], df.iloc[3]['high'])*1.01
            current_price = get_current_price("KRW-MANA")
            if op_mode is True and hold is False and current_price > ma5 and current_price > ma20 and current_price > df_high:
                krw = upbit.get_balance("KRW")
    #           upbit.buy_market_order("KRW-MANA", krw*0.1)
                hold =True

    except Exception as e:
        print(e)
        post_message(myToken,"#stock", e)
        time.sleep(1)




