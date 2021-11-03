from binance.client import Client
from sqlalchemy import create_engine
from os import environ
import pandas as pd
from time import sleep
import sys

# psycopg2 connection
engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (environ["POSTGRES_USER"], environ["POSTGRES_PASSWORD"], environ["POSTGRES_HOST"], environ["POSTGRES_DB"]))


# binance client
client = Client(environ["BINANCE_API_KEY"], environ["BINANCE_API_SECRET"])

if __name__ == '__main__':
    try:
        while True:
            # update
            SYMBOLS = { "BTCUSDT" : 1196358476445, "ETHUSDT" : 532988896161, "BNBUSDT" : 94580743908 }
            for SYMBOL, MARKETCAP in SYMBOLS.items():
                trades = client.get_recent_trades(symbol= SYMBOL, limit = 100000)
                df = pd.DataFrame(trades)
                df["symbol"] = SYMBOL
                df['time'] = pd.to_datetime(df['time'],unit='ms')
                df.rename(columns={"time": "timestamp"}, inplace=True)
                df["price"] = df["price"].astype(float)
                df["qty"] = df["qty"].astype(float)
                df["quoteQty"] = df["quoteQty"].astype(float)
                df["volume"] = df["qty"] * df["price"]
                df["id"] = df["id"] + df["symbol"]
                df["pctOfMarketcap"] = df["qty"] / MARKETCAP * 1000000000

                # print(df.head())
                print("saving data for %s" % SYMBOL)
                print(df.tail(1))
                df.to_sql(name='binancetrades', con=engine, if_exists='append', index=False)
                # df.to_parquet("testbtc.parquet")
            # sleep until next query
            sleep(90)

    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)



