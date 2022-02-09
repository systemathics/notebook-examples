import pandas as pd
import numpy as np
import json
pd.options.mode.chained_assignment = None  # default='warn'
import seaborn as sns
import matplotlib.pyplot as plt
import os
import grpc
from datetime import datetime
import google.type.date_pb2 as date
import google.type.dayofweek_pb2 as dayofweek
import google.type.timeofday_pb2 as timeofday
import google.protobuf.duration_pb2 as duration
import systemathics.apis.type.shared.v1.identifier_pb2 as identifier
import systemathics.apis.services.daily.v1.daily_bars_pb2 as daily_bars
import systemathics.apis.services.daily.v1.daily_bars_pb2_grpc as daily_bars_service
from math import *
import statistics

class PriceData():

    def __init__(self, token):
        self.token = token

    def get_pair_df(self, ticker_1, ticker_2, limit=1000, exchange="XNGS"):
        # create daily bars requests for the pair instruments
        daily_request_1 = daily_bars.DailyBarsRequest(identifier = identifier.Identifier(exchange = exchange, ticker = ticker_1))
        daily_request_2 = daily_bars.DailyBarsRequest(identifier = identifier.Identifier(exchange = exchange, ticker = ticker_2))

        # open a gRPC channel, instantiate the daily bars service and get the reply for the 1st instrument
        with open(os.environ['SSL_CERT_FILE'], 'rb') as f:
            credentials = grpc.ssl_channel_credentials(f.read())
        with grpc.secure_channel(os.environ['GRPC_APIS'], credentials) as channel:
            daily_service = daily_bars_service.DailyBarsServiceStub(channel)
            response_1 = daily_service.DailyBars(request = daily_request_1, metadata = [('authorization', self.token)])
            
        print("Total bars for ticker1 retrieved: ",len(response_1.data))

        # open a gRPC channel, instantiate the daily bars service and get the reply for the 2nd instrument
        with open(os.environ['SSL_CERT_FILE'], 'rb') as f:
            credentials = grpc.ssl_channel_credentials(f.read())
        with grpc.secure_channel(os.environ['GRPC_APIS'], credentials) as channel:
            daily_service = daily_bars_service.DailyBarsServiceStub(channel)
            response_2 = daily_service.DailyBars(request = daily_request_2, metadata = [('authorization', self.token)])
            
        print("Total bars for ticker2 retrieved: ",len(response_2.data))

        # create pandas dataframe to store close prices for the pair instruments
        length = limit # keep last x points
        dates = [datetime(ts.date.year,ts.date.month, ts.date.day ) for ts in response_2.data[-length:]]
        prices1 = [ts.close for ts in response_1.data[-length:]]
        prices2 = [ts.close for ts in response_2.data[-length:]]
        data = {'Date': dates, 'Price_1': prices1, 'Price_2': prices2}
        df = pd.DataFrame(data=data)
        df['Price_1'] = pd.to_numeric(df['Price_1'])
        df['Price_2'] = pd.to_numeric(df['Price_2'])
        df = df.set_index(df['Date'])
        df.index = pd.to_datetime(df.index, unit='ms')
        return df
    
    def get_historical_daily_candles(self, ticker, exchange="XNGS", limit=1000, adjusted=True):
        if adjusted == True:
            request = daily_bars.DailyBarsRequest(
                identifier = identifier.Identifier(exchange = exchange, ticker = ticker),
                adjustment = True
            )
        else:
            request = daily_bars.DailyBarsRequest(
                identifier = identifier.Identifier(exchange = exchange, ticker = ticker)
            )
        # open a gRPC channel
        with open(os.environ['SSL_CERT_FILE'], 'rb') as f:
            credentials = grpc.ssl_channel_credentials(f.read())
        with grpc.secure_channel(os.environ['GRPC_APIS'], credentials) as channel:

            # instantiate the daily prices service
            service = daily_bars_service.DailyBarsServiceStub(channel)

            # process the request
            response = service.DailyBars(
                request = request, 
                metadata = [('authorization', self.token)]
            )

        # print("Total bars retrieved: ",len(response.data))
        #Prepare the data frame content
        length = limit
        dates=[datetime(b.date.year, b.date.month, b.date.day) for b in response.data[-length:]]
        opens = [b.open for b in response.data[-length:]]
        highs = [b.high for b in response.data[-length:]]
        lows = [b.low for b in response.data[-length:]]
        closes = [b.close for b in response.data[-length:]]
        volumes = [b.volume for b in response.data[-length:]]

        d = {'Date': dates, 'Open': opens, 'High': highs, 'Low' : lows,'Close': closes, 'Volume': volumes }
        # create pandas dataframe
        df = pd.DataFrame(data=d)
        df = df.set_index(df['Date'])
        df.index = pd.to_datetime(df.index, unit='ms')
        df['Open'] = pd.to_numeric(df['Open'])
        df['High'] = pd.to_numeric(df['High'])
        df['Low'] = pd.to_numeric(df['Low'])
        df['Close'] = pd.to_numeric(df['Close'])
        df['Volume'] = pd.to_numeric(df['Volume'])
        return df[-limit:]
    
    def get_daily_pair_candles(self, ticker_1, ticker_2, exchange="XNGS", limit=1000):
        df1 = self.get_historical_daily_candles(ticker = ticker_1, exchange = exchange, limit = limit)
        df1.rename(columns={
            'Date': 'Date_1', 
            'Open': 'Open_1', 
            'High': 'High_1', 
            'Low': 'Low_1', 
            'Close': 'Close_1', 
            'Volume': 'Volume_1'
        }, inplace=True)

        df2 = self.get_historical_daily_candles(ticker = ticker_2, exchange = exchange, limit = limit)
        df2.rename(columns={
            'Date': 'Date_2', 
            'Open': 'Open_2', 
            'High': 'High_2', 
            'Low': 'Low_2', 
            'Close': 'Close_2', 
            'Volume': 'Volume_2'
        }, inplace=True)  
        frames = [df1, df2]
        df = pd.concat(frames, axis=1)
        print("Retrieve",len(df),"daily candles from",ticker_1+"/"+ticker_2)
        return df