import pandas as pd
import numpy as np
import json
pd.options.mode.chained_assignment = None  # default='warn'
import seaborn as sns
import matplotlib.pyplot as plt
import os
import grpc
import datetime
import google.type.date_pb2 as date
import google.type.dayofweek_pb2 as dayofweek
import google.type.timeofday_pb2 as timeofday
import google.protobuf.duration_pb2 as duration
import systemathics.apis.type.shared.v1.identifier_pb2 as identifier
import systemathics.apis.services.daily.v1.daily_bars_pb2 as daily_bars
import systemathics.apis.services.daily.v1.daily_bars_pb2_grpc as daily_bars_service
from math import *
import statistics

class Backtesting():
    def complete_multi_backtest(self, dfTrades, dfDays, pairList):
        dfTradesCopy = dfTrades.copy()

        dfTradesCopy['tradeIs'] = ''
        dfTradesCopy.loc[dfTradesCopy['tradeResult']>0,'tradeIs'] = 'Good'
        dfTradesCopy.loc[dfTradesCopy['tradeResult']<=0,'tradeIs'] = 'Bad'
        dfTradesCopy['tradeResult'] = dfTradesCopy['tradeResult'] * 100  

        dfTradesCopy['tradeResult'] = pd.to_numeric(dfTradesCopy['tradeResult'])

        dfTradesCopy['highValue'] = dfTradesCopy['wallet'].cummax()

        dfTradesCopy['drawdown'] = (dfTradesCopy['wallet'] - dfTradesCopy['highValue'])/dfTradesCopy['highValue']
        dfTradesCopy['drawdown'] = pd.to_numeric(dfTradesCopy['drawdown'])
        
        initialWallet = dfTradesCopy.iloc[0]['wallet']
        finalWallet = dfTradesCopy.iloc[-1]['wallet']
        strategyFinalResult = (finalWallet - initialWallet)/initialWallet

        try:
            tradesPerformance = round(dfTradesCopy.loc[(dfTradesCopy['tradeIs'] == 'Good') | (dfTradesCopy['tradeIs'] == 'Bad'), 'tradeResult'].sum()
                    / dfTradesCopy.loc[(dfTradesCopy['tradeIs'] == 'Good') | (dfTradesCopy['tradeIs'] == 'Bad'), 'tradeResult'].count(), 2)
        except:
            tradesPerformance = 0
            print("/!\ There is no Good or Bad Trades in your BackTest, maybe a problem...")

        try:
            totalGoodfTradesCopyrades = dfTradesCopy.groupby('tradeIs')['date'].nunique()['Good']
            AveragePercentagePositivTrades = round(dfTradesCopy.loc[dfTradesCopy['tradeIs'] == 'Good', 'tradeResult'].sum()
                                                   / dfTradesCopy.loc[dfTradesCopy['tradeIs'] == 'Good', 'tradeResult'].count(), 2)
            idbest = dfTradesCopy.loc[dfTradesCopy['tradeIs'] == 'Good', 'tradeResult'].idxmax()
            bestTrade = str(
                round(dfTradesCopy.loc[dfTradesCopy['tradeIs'] == 'Good', 'tradeResult'].max(), 2))
        except:
            totalGoodfTradesCopyrades = 0
            AveragePercentagePositivTrades = 0
            idbest = ''
            bestTrade = 0
            print("/!\ There is no Good Trades in your BackTest, maybe a problem...")

        try:
            totalBadfTradesCopyrades = dfTradesCopy.groupby('tradeIs')['date'].nunique()['Bad']
            AveragePercentageNegativTrades = round(dfTradesCopy.loc[dfTradesCopy['tradeIs'] == 'Bad', 'tradeResult'].sum()
                                                   / dfTradesCopy.loc[dfTradesCopy['tradeIs'] == 'Bad', 'tradeResult'].count(), 2)
            idworst = dfTradesCopy.loc[dfTradesCopy['tradeIs'] == 'Bad', 'tradeResult'].idxmin()
            worstTrade = round(dfTradesCopy.loc[dfTradesCopy['tradeIs'] == 'Bad', 'tradeResult'].min(), 2)
        except:
            totalBadfTradesCopyrades = 0
            AveragePercentageNegativTrades = 0
            idworst = ''
            worstTrade = 0
            print("/!\ There is no Bad Trades in your BackTest, maybe a problem...")

        totalTrades = totalBadfTradesCopyrades + totalGoodfTradesCopyrades

        try:
            TotalLongTrades = len(dfTradesCopy.loc[(dfTradesCopy['position'] == 'LONG') & (dfTradesCopy['openOrClose'] == 'Close')])
            AverageLongTrades = round((dfTradesCopy.loc[(dfTradesCopy['position'] == 'LONG') & (dfTradesCopy['openOrClose'] == 'Close'), 'tradeResult'].sum() / TotalLongTrades),2)
            idBestLong = dfTradesCopy.loc[dfTradesCopy['position'] == 'LONG', 'tradeResult'].idxmax()
            bestLongTrade = str(
                round(dfTradesCopy.loc[dfTradesCopy['position'] == 'LONG', 'tradeResult'].max(), 2))
            idWorstLong = dfTradesCopy.loc[dfTradesCopy['position'] == 'LONG', 'tradeResult'].idxmin()
            worstLongTrade = str(
                round(dfTradesCopy.loc[dfTradesCopy['position'] == 'LONG', 'tradeResult'].min(), 2))
        except:
            AverageLongTrades = 0
            TotalLongTrades = 0
            bestLongTrade = ''
            idBestLong = ''
            idWorstLong = ''
            worstLongTrade = ''
            print("/!\ There is no LONG Trades in your BackTest, maybe a problem...")

        try:
            TotalShortTrades = len(dfTradesCopy.loc[(dfTradesCopy['position'] == 'SHORT') & (dfTradesCopy['openOrClose'] == 'Close')])
            AverageShortTrades = round(dfTradesCopy.loc[dfTradesCopy['position'] == 'SHORT', 'tradeResult'].sum()
                                       / dfTradesCopy.loc[dfTradesCopy['position'] == 'SHORT', 'tradeResult'].count(), 2)
            idBestShort = dfTradesCopy.loc[dfTradesCopy['position'] == 'SHORT', 'tradeResult'].idxmax()
            bestShortTrade = str(
                round(dfTradesCopy.loc[dfTradesCopy['position'] == 'SHORT', 'tradeResult'].max(), 2))
            idWorstShort = dfTradesCopy.loc[dfTradesCopy['position'] == 'SHORT', 'tradeResult'].idxmin()
            worstShortTrade = str(
                round(dfTradesCopy.loc[dfTradesCopy['position'] == 'SHORT', 'tradeResult'].min(), 2))
        except:
            AverageShortTrades = 0
            TotalShortTrades = 0
            bestShortTrade = ''
            idBestShort = ''
            idWorstShort = ''
            worstShortTrade = ''
            print("/!\ There is no SHORT Trades in your BackTest, maybe a problem...")

        try:
            totalGoodLongTrade = dfTradesCopy.groupby(['position', 'tradeIs']).size()['LONG']['Good']
        except:
            totalGoodLongTrade = 0
            print("/!\ There is no good LONG Trades in your BackTest, maybe a problem...")

        try:
            totalBadLongTrade = dfTradesCopy.groupby(['position', 'tradeIs']).size()['LONG']['Bad']
        except:
            totalBadLongTrade = 0
            print("/!\ There is no bad LONG Trades in your BackTest, maybe a problem...")

        try:
            totalGoodShortTrade = dfTradesCopy.groupby(['position', 'tradeIs']).size()['SHORT']['Good']
        except:
            totalGoodShortTrade = 0
            print("/!\ There is no good SHORT Trades in your BackTest, maybe a problem...")

        try:
            totalBadShortTrade = dfTradesCopy.groupby(['position', 'tradeIs']).size()['SHORT']['Bad']
        except:
            totalBadShortTrade = 0
            print("/!\ There is no bad SHORT Trades in your BackTest, maybe a problem...")
            
        dfDays['evolution'] = dfDays['wallet'].diff()
        dfDays['daily_return'] = dfDays['evolution']/dfDays['wallet'].shift(1)
        sharpe_ratio = (252**0.5)*(dfDays['daily_return'].mean()/dfDays['daily_return'].std())

        winRateRatio = (totalGoodfTradesCopyrades/totalTrades) * 100

        maxDrawdown = dfTradesCopy['drawdown'].min()
        maxDrawdownId = dfTradesCopy['drawdown'].idxmin()

        print("Multi Pair Strategy")
        print("Period : [" + str(dfTradesCopy.iloc[0]['date']) + "] -> [" +
              str(str(dfTradesCopy.iloc[-1]['date']) + "]"))

        print("\n----- General Informations -----")
        print("Performance :", round(strategyFinalResult*100, 2), "%")
        print("Sharpe ratio :", round(sharpe_ratio,2))
        print("Best trade : +"+bestTrade, "%, the", dfTradesCopy.iloc[idbest]['date'])
        print("Worst trade :", worstTrade, "%, the", dfTradesCopy.iloc[idworst]['date'])
        print("Max DrawDown :", str(round(100*maxDrawdown, 2)), "%, the", dfTradesCopy.iloc[maxDrawdownId]['date'])

        print("\n----- Trades Informations -----")
        print("Total trades on period :",totalTrades)
        print("Number of positive trades :", totalGoodfTradesCopyrades)
        print("Number of negative trades : ", totalBadfTradesCopyrades)
        print("Trades win rate ratio :", round(winRateRatio, 2), '%')
        print("Average trades performance :",tradesPerformance,"%")
        print("Average positive trades :", AveragePercentagePositivTrades, "%")
        print("Average negative trades :", AveragePercentageNegativTrades, "%")

        print("\n----- LONG Trades Informations -----")
        print("Number of LONG trades :",TotalLongTrades)
        print("Average LONG trades performance :",AverageLongTrades, "%")
        print("Best  LONG trade +"+bestLongTrade, "%, the ", dfTradesCopy.iloc[idBestLong]['date'])
        print("Worst LONG trade", worstLongTrade, "%, the ", dfTradesCopy.iloc[idWorstLong]['date'])
        print("Number of positive LONG trades :",totalGoodLongTrade)
        print("Number of negative LONG trades :",totalBadLongTrade)
        print("LONG trade win rate ratio :", round(totalGoodLongTrade/TotalLongTrades*100, 2), '%')

        print("\n----- SHORT Trades Informations -----")
        print("Number of SHORT trades :",TotalShortTrades)
        print("Average SHORT trades performance :",AverageShortTrades, "%")
        print("Best  SHORT trade +"+bestShortTrade, "%, the ", dfTradesCopy.iloc[idBestShort]['date'])
        print("Worst SHORT trade", worstShortTrade, "%, the ", dfTradesCopy.iloc[idWorstShort]['date'])
        print("Number of positive SHORT trades :",totalGoodShortTrade)
        print("Number of negative SHORT trades :",totalBadShortTrade)
        print("SHORT trade win rate ratio :", round(totalGoodShortTrade/TotalShortTrades*100, 2), '%')

        print("\n----- Trades Reasons -----")
        print(dfTradesCopy['reason'].value_counts())

        print("\n----- Pair Result -----")
        dash = '-' * 95
        print(dash)
        print('{:<6s}{:>10s}{:>15s}{:>15s}{:>15s}{:>15s}{:>15s}'.format(
            "Trades","Pair","Sum-result","Mean-trade","Worst-trade","Best-trade","Win-rate"
            ))
        print(dash)
        for pair in pairList:
            try:
                # pair = pairArray[0] + "/" + pairArray[1]
                dfPairLoc = dfTradesCopy.loc[dfTradesCopy['pair'] == pair, 'tradeResult']
                pairGoodTrade = len(dfTradesCopy.loc[(dfTradesCopy['pair'] == pair) & (dfTradesCopy['tradeResult'] > 0)])
                pairTotalTrade = int(len(dfPairLoc)/2)
                pairResult = str(round(dfPairLoc.sum(),2))+' %'
                pairAverage = str(round(dfPairLoc.mean(),2))+' %'
                pairMin = str(round(dfPairLoc.min(),2))+' %'
                pairMax = str(round(dfPairLoc.max(),2))+' %'
                pairWinRate = str(round(100*(pairGoodTrade/pairTotalTrade),2))+' %'
                print('{:<6d}{:>10s}{:>15s}{:>15s}{:>15s}{:>15s}{:>15s}'.format(
                    pairTotalTrade,pair,pairResult,pairAverage,pairMin,pairMax,pairWinRate
                ))
            except:
                pass

        return dfTradesCopy

    def plot_wallet_evolution(self, dfTrades):
        dfTradesCopy = dfTrades.copy()
        dfTradesCopy = dfTradesCopy.set_index(dfTradesCopy['date'])
        dfTradesCopy.index = pd.to_datetime(dfTradesCopy.index)
        dfTradesCopy['wallet'].plot(figsize=(20, 10))
        print("\n----- Plot -----")
        
    def plot_wallet_vs_asset(self, dfTrades, dfAsset):
        fig, axes = plt.subplots(figsize=(20, 10), nrows=2, ncols=1)

        dfSPCopy = dfAsset.copy()
        dfSPCopy = dfSPCopy.set_index(dfSPCopy['time'])
        dfSPCopy.index = pd.to_datetime(dfSPCopy.index, unit='s')
        dfSPCopy = dfSPCopy['2016':]
        dfSPCopy['close'].plot(ax=axes[1])

        dfTradesCopy = dfTrades.copy()
        dfTradesCopy = dfTradesCopy.set_index(dfTradesCopy['date'])
        dfTradesCopy.index = pd.to_datetime(dfTradesCopy.index)
        dfTradesCopy['wallet'].plot(ax=axes[0])
        print("\n----- Plot -----")
        
    def plot_bar_by_month(self, dfTrades):
        sns.set(rc={'figure.figsize':(11.7,8.27)})
        lastMonth = int(dfTrades.iloc[-1]['date'].month)
        lastYear = int(dfTrades.iloc[-1]['date'].year)
        dfTrades = dfTrades.set_index(dfTrades['date'])
        dfTrades.index = pd.to_datetime(dfTrades.index)
        myMonth = int(dfTrades.iloc[0]['date'].month)
        myYear = int(dfTrades.iloc[0]['date'].year)
        custom_palette = {}
        dfTemp = pd.DataFrame([])
        sharpeArr = []
        while myYear != lastYear or myMonth != lastMonth:
            myString = str(myYear) + "-" + str(myMonth)
            try:
                myResult = (dfTrades.loc[myString].iloc[-1]['wallet'] -
                            dfTrades.loc[myString].iloc[0]['wallet'])/dfTrades.loc[myString].iloc[0]['wallet']
            except:
                myResult = 0
            myrow = {
                'date': str(datetime.date(1900, myMonth, 1).strftime('%B')),
                'result': round(myResult*100)
            }
            dfTemp = dfTemp.append(myrow, ignore_index=True)
            if myResult >= 0:
                custom_palette[str(datetime.date(1900, myMonth, 1).strftime('%B'))] = 'g'
            else:
                custom_palette[str(datetime.date(1900, myMonth, 1).strftime('%B'))] = 'r'
            # print(myYear, myMonth, round(myResult*100, 2), "%")
            if myMonth < 12:
                myMonth += 1
            else:
                g = sns.barplot(data=dfTemp,x='date',y='result', palette=custom_palette)
                for index, row in dfTemp.iterrows():
                    if row.result >= 0:
                        g.text(row.name,row.result, '+'+str(round(row.result))+'%', color='black', ha="center", va="bottom")
                    else:
                        g.text(row.name,row.result, '-'+str(round(row.result))+'%', color='black', ha="center", va="top")
                g.set_title(str(myYear) + ' performance in %')
                g.set(xlabel=myYear, ylabel='performance %')
                yearResult = (dfTrades.loc[str(myYear)].iloc[-1]['wallet'] -
                            dfTrades.loc[str(myYear)].iloc[0]['wallet'])/dfTrades.loc[str(myYear)].iloc[0]['wallet']
                
                
                dfSharpe = dfTrades.loc[str(myYear)]
                dfSharpe['highWallet'] = dfSharpe['wallet'].cummax()
                dfSharpe['drawdown'] = (dfSharpe['wallet'] - dfSharpe['highWallet'])/dfSharpe['highWallet']
                print("Max DD",str(round(dfSharpe['drawdown'].min()*100,2)))
                sharpeArr.append((yearResult/(-dfSharpe['drawdown'].min())))
                
                print("----- " + str(myYear) +" Performances: " + str(round(yearResult*100,2)) + "% -----")
                plt.show()
                dfTemp = pd.DataFrame([])
                myMonth = 1
                myYear += 1

        myString = str(lastYear) + "-" + str(lastMonth)
        try:
            myResult = (dfTrades.loc[myString].iloc[-1]['wallet'] -
                        dfTrades.loc[myString].iloc[0]['wallet'])/dfTrades.loc[myString].iloc[0]['wallet']
        except:
            myResult = 0
        g = sns.barplot(data=dfTemp,x='date',y='result', palette=custom_palette)
        for index, row in dfTemp.iterrows():
            if row.result >= 0:
                g.text(row.name,row.result, '+'+str(round(row.result))+'%', color='black', ha="center", va="bottom")
            else:
                g.text(row.name,row.result, '-'+str(round(row.result))+'%', color='black', ha="center", va="top")
        g.set_title(str(myYear) + ' performance in %')
        g.set(xlabel=myYear, ylabel='performance %')
        yearResult = (dfTrades.loc[str(myYear)].iloc[-1]['wallet'] -
                dfTrades.loc[str(myYear)].iloc[0]['wallet'])/dfTrades.loc[str(myYear)].iloc[0]['wallet']
        dfSharpe = dfTrades.loc[str(myYear)]
        dfSharpe['highWallet'] = dfSharpe['wallet'].cummax()
        dfSharpe['drawdown'] = (dfSharpe['wallet'] - dfSharpe['highWallet'])/dfSharpe['highWallet']
        print("Max DD",str(round(dfSharpe['drawdown'].min()*100,2)),'%')
        sharpeArr.append((yearResult/(-dfSharpe['drawdown'].min())))
        print("----- " + str(myYear) +" Performances: " + str(round(yearResult*100,2)) + "% -----")
        print("Annualized mean of",statistics.mean(sharpeArr))
        plt.show()