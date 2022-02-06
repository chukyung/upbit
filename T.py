
import pyupbit
import pandas




df = pyupbit.get_ohlcv("KRW-MANA", count=5)

print(df)
print(max(df.iloc[0]['close'], df.iloc[1]['close'], df.iloc[2]['close'], df.iloc[3]['close'])*1.01)




#print(max(df.high)*1.01)
