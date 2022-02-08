import os
import grpc
import json
import itertools
import numpy as np
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from statsmodels.tsa.stattools import adfuller, kpss, zivot_andrews
import systemathics.apis.type.shared.v1.identifier_pb2 as identifier
import systemathics.apis.services.daily.v1.daily_bars_pb2 as daily_bars
import systemathics.apis.services.static_data.v1.static_data_pb2 as static_data
import systemathics.apis.services.daily.v1.daily_bars_pb2_grpc as daily_bars_service
import systemathics.apis.services.static_data.v1.static_data_pb2_grpc as static_data_service


class Selection:
    """The Selection class contains lots of data about equities that belongs to a specific index and exchange as well as functions enabling us to do many computation on these data."""
    
    def __init__(self, index='NASDAQ', exchange='XNGS', market_based_classification='Nasdaq', start_date="2019-01-01", adjustment=False, use_corr=False, use_statio=True, mincorr_level=0.7, statio_level=0.05, use_adfuller=True, use_kpss=False, use_zivotandrews=False):
        '''
        Selection class constructor.
        :param index: The index from which we want to get its equities.
        :type index: str
        :param exchange: The exchange from which we want to get its equities.
        :type exchange: str
        :param market_based_classification: The market based classification used to define sectors ('ICB', 'Nasdaq'...)
        :type market_based_classification: str
        :param start_date: Collect the prices starting from that date (until now or today).
        :type start_date: str format YYYY-MM-DD
        :param adjustment: Use the adjusted price or not.
        :type adjustment: bool
        :param use_corr: Calculate the correlation between two equities or not.
        :type use_corr: bool
        :param use_statio: Calculate the stationarity of a pair series or not.
        :type use_statio: bool
        :param mincorr_level: Minimum level to consider two equities as correlated.
        :type mincorr_level: float
        :param statio_level: p-value used to invalidate the null hypothesis of a stationarity test.
        :type statio_level: float
        :param use_adfuller: Use adfuller stationarity test or not.
        :type use_adfuller: bool
        :param use_kpss: Use kpss stationarity test or not.
        :type use_kpss: bool
        :param use_zivotandrews: Use zivot and andrews stationarity test or not.
        :type use_zivotandrews: bool      
        '''
        self.index = index
        self.exchange = exchange
        self.market_based_classification = market_based_classification
        self.start_date = start_date
        self.from_period = self.businessday_number(start_date) # Get the number of business days past from the selected starting date until today
        self.adjustment = adjustment
        self.use_corr = use_corr
        self.use_statio = use_statio
        self.mincorr_level = mincorr_level
        self.statio_level = statio_level
        self.use_adfuller = use_adfuller
        self.use_kpss = use_kpss
        self.use_zivotandrews = use_zivotandrews
        self.token = f"Bearer {os.environ['AUTH0_TOKEN']}"
        self.data = self.getData() # Get a dataframe of equities with its related data
        self.df_all_prices = self.getAllPrices() # Get a dataframe of equities with their prices from the starting day until today, day by day.
    
    
    def businessday_number(self, date, end=None):
        """Return the number of business day from a starting date until a specific date, otherwise until today."""
        start = pd.to_datetime(date, format='%Y-%m-%d')
        if end != None:
            return len(pd.bdate_range(start, pd.to_datetime(end, format='%Y-%m-%d')))
        return len(pd.bdate_range(start, pd.to_datetime("now")))


    # ---------- FETCH EQUITIES ----------

    def get_equities_dataframe(self, sectors, response):
        """Define a method to handle the equities reponse using a Pandas dataframe -> return the dataframe."""
        exchange = [equity.identifier.exchange for equity in response.equities]
        ticker = [equity.identifier.ticker for equity in response.equities]
        name = [equity.name for equity in response.equities]
        primary = [equity.primary for equity in response.equities]
        index = [equity.index for equity in response.equities]
        isin = [equity.isin for equity in response.equities]
        cusip = [equity.cusip for equity in response.equities]
        sedol = [equity.sedol for equity in response.equities]
        sector = [sectors[i][self.market_based_classification] for i in range(len(sectors))]   
        
        # Create pandas dataframe
        d = {'Index': index, 'Name': name, 'Ticker': ticker, 'Exchange': exchange, 'Primary':primary, 'Isin': isin, 'Cusip': cusip, 'Sedol': sedol, 'Sector': sector}
        df = pd.DataFrame(data=d)
        return df
    
    
    # ---------- GET PRICES AND data ----------

    
    def getData(self):
        """Create a dataframe with all equities and related data according the instance variables filters set."""
        # FETCH DATA
        # Generate static data request
        request = static_data.StaticDataRequest( 
            asset_type = static_data.AssetType.ASSET_TYPE_EQUITY
        )

        request.index.value = self.index # add index as per filter value
        # request.exchange.value = exchange # add exchange as per filter value
        request.count.value = 1000 # by default the count is set to 100

        # Open a gRPC channel
        with open(os.environ['SSL_CERT_FILE'], 'rb') as f:
            credentials = grpc.ssl_channel_credentials(f.read())
        with grpc.secure_channel(os.environ['GRPC_APIS'], credentials) as channel:
            # instantiate the static data service
            service = static_data_service.StaticDataServiceStub(channel)
            
            # Process the request
            response = service.StaticData(
                request = request, 
                metadata = [('authorization', self.token)]
            )

        # Get a list of all the sectors names according their market-based classification : 'ICB', 'SIC', 'GICS'...
        sectors = [equity.sectors for equity in response.equities]

        # FETCH EQUITIES
        data = self.get_equities_dataframe(sectors, response)
        data = data[data.Exchange == self.exchange] # filter by exchange
        
        return data
    

    def getPrice(self, ticker):
        """Get list of closing prices and dates of an equity from a specific exchange and ticker."""
        daily_request = daily_bars.DailyBarsRequest(identifier = identifier.Identifier(exchange = self.exchange, ticker = ticker), adjustment = self.adjustment)
        
        with open(os.environ['SSL_CERT_FILE'], 'rb') as f:
            credentials = grpc.ssl_channel_credentials(f.read())
        with grpc.secure_channel(os.environ['GRPC_APIS'], credentials) as channel:
            daily_service = daily_bars_service.DailyBarsServiceStub(channel)
            response = daily_service.DailyBars(request = daily_request, metadata = [('authorization', self.token)])
    
        # Create lists to store close prices and dates for the pair instruments
        dates = [datetime(ts.date.year, ts.date.month, ts.date.day) for ts in response.data[-self.from_period:]]
        prices = [ts.close for ts in response.data[-self.from_period:]]
            
        return prices, dates
    
    
    def getAllPrices(self):
        """Create a dataframe with all tickers and their prices according the time."""
        all_tickers = self.data.Ticker.tolist()

        columns_names = ['Dates']
        all_prices = []

        for ticker in all_tickers:
            prices, dates = self.getPrice(ticker)
            if len(prices) == self.from_period: # check if there are no missing values from the starting date until the ending date
                if len(all_prices) == 0: # we only want to append the dates once since it will be the same for all
                    columns_names.append(ticker)
                    for i in range(len(prices)):
                        all_prices.append([dates[i], prices[i]])
                else:
                    columns_names.append(ticker)
                    for i in range(len(prices)):
                        all_prices[i].append(prices[i])
                        
        df_all_prices = pd.DataFrame(all_prices, columns=columns_names)

        # Since the market can also close during public holiday we will be fetching more data than wanted because we have only rejected the business day.
        # Therefore we need to filter again and remove the few extra lines before our wanted starting date.  
        df_all_prices = df_all_prices[~(df_all_prices['Dates'] < self.start_date)]

        return df_all_prices
    
    
    # ---------- COMPUTATION FUNCTIONS ----------

    
    def logAndRatio(self, ticker1, ticker2, start_date='', end_date=''):
        """
        Return between two dates a new dataframe with the prices of each equity via its ticker, its daily percentage change and the ratio of both.
        :param ticker1: Ticker of one of the two equity.
        :param ticker2: Ticker of one of the two equity.
        :param start_date: Perform the computation with the values starting from that date (format YYYY-MM-DD).
        :param end_date: Perform the computation with the values from the starting date until this ending date (format YYYY-MM-DD).
        :return: Dataframe with the prices of the two equities, their evolution price and their ratio data by date.
        """
        if not start_date:
            start_date = self.start_date
        if not end_date:
            end_date = date.today().strftime("%Y-%m-%d")        
        
        df_prices = self.df_all_prices
        # Retrieve only the prices between the two specified dates
        mask = (df_prices['Dates'] >= start_date) & (df_prices['Dates'] <= end_date)
        df_prices = df_prices.loc[mask]
        
        dates = df_prices.Dates.tolist()
        prices1 = df_prices[ticker1].tolist()
        prices2 = df_prices[ticker2].tolist()
        
        if len(prices1) != len(prices2):
            return False # cannot compute the values in list one by one
        
        data = {'Date': dates, 'Price_1': prices1, 'Price_2': prices2}
        df = pd.DataFrame(data=data)
        
        # Calculate the daily percentage change and stationarity of the ratio
        if self.use_corr:
            df['EvolPrice_1'] = df['Price_1']/df['Price_1'].shift(1)
            df['EvolPrice_2'] = df['Price_2']/df['Price_2'].shift(1)
        if self.use_statio:
            df['Ratio'] = np.log10(df['Price_1']/df['Price_2'])
        
        return df

    
    def pairCorr(self, ticker1, ticker2, start_date='', end_date=''):
        """
        Return a dictionary with the correlation value of a pair and its stationarity.
        :param ticker1: Ticker of one of the two equity.
        :param ticker2: Ticker of one of the two equity.
        :param start_date: Perform the computation with the values starting from that date (format YYYY-MM-DD).
        :param end_date: Perform the computation with the values from the starting date until this ending date (format YYYY-MM-DD).
        :return: Dictionary containing the correlation and stationarity value.
        """
        if not start_date:
            start_date = self.start_date
        if not end_date:
            end_date = date.today().strftime("%Y-%m-%d") 
        
        result = {}
        
        df = self.logAndRatio(ticker1, ticker2, start_date, end_date)
        
        if isinstance(df, bool): # check if we received a full dataframe or a negative response
            if df == False:
                return {'corr': None, 'statio': None}
        
        # Because of the division in logAndRatio, some values can be so big that they are consider as infinite.
        # Therefore we remove them so that they don't affect our correlation and stationarity computation.
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)
        
        # Get the correlation of the evolution between two equities only if we've set the instance variable to True .
        result['corr'] = df['EvolPrice_1'].corr(df['EvolPrice_2']) if self.use_corr else None
        # For the stationarity return we need the pvalue that we can get at index 1,
        # We also need to do one computation according adfuller method, kpss method or zivot-andrews's one, for that we check what instance variable was set to True.
        result['statio'] = (adfuller(df['Ratio'])[1] if self.use_adfuller else (kpss(df['Ratio'])[1] if self.use_kpss else zivot_andrews(df['Ratio'])[1])) if self.use_statio else None
        
        return result
    

    # ---------- GET BEST PAIRS ----------

    def get_best_pairs(self, start_date='', end_date=''):
        """
        Saves the pairs with a satisfying correlation value and/or stationarity following the instance variable criteria set.
        :param start_date: Perform the computation with the values starting from that date (format YYYY-MM-DD).
        :param end_date: Perform the computation with the values from the starting date until this ending date (format YYYY-MM-DD).
        :return: Dataframe of the tickers making up a pair, the correlation value and/or their ratio stationarity.
        """
        if not start_date:
            start_date = self.start_date
        if not end_date:
            end_date = date.today().strftime("%Y-%m-%d") 
            
        # ----- FILTER BY SECTOR -----
        # Get all the sectors in our dataframe with duplicate (needed later to count)
        all_sectors = self.data['Sector'].tolist()
        all_sectors = list(filter(None, all_sectors))

        # Get all the sectors without duplicate
        unique_sectors = set(all_sectors)

        # Create a df with the sectors and their total appearance
        unique_sectors = list(unique_sectors)
        tot = [all_sectors.count(sect) for sect in unique_sectors]
        cols = {'Sector': unique_sectors, 'Total': tot}
        df = pd.DataFrame(data=cols)
        ranked_total_sectors = df.sort_values(by=['Total'], ascending=False)
        ranked_total_sectors.reset_index(drop=True, inplace=True)

        # ----- COREELATION LOOP COMPUTATION -----
        selected_tickers = self.df_all_prices.columns.tolist()
        corr_and_statio_list = []

        # Loop through all sectors
        for sect in unique_sectors:
            if ranked_total_sectors[ranked_total_sectors.Sector == sect].Total.tolist()[0] >= 2: # check if the sector contain at least two equity
                tickers_in_sector = self.data[self.data.Sector == sect].Ticker.tolist() # get all the tickers that belongs to that sector
                tickers_in_sector = list(set(selected_tickers).intersection(tickers_in_sector)) # remove unselected tickers
                for ticker1, ticker2 in itertools.combinations(tickers_in_sector, 2): # compare all data in list in twos
                    r = self.pairCorr(ticker1, ticker2, start_date, end_date)
                    corr, statio = r['corr'], r['statio']
                    if corr == None and statio == None: # an error migh have occured so ignore and next
                        continue
                    corr_and_statio_list.append([ticker1, ticker2, corr, statio])

        if self.use_statio:
            corr_and_statio_list.sort(key=lambda x: abs(x[3])) # sort according the stationnarity (at index 3)
        else:
            corr_and_statio_list.sort(key=lambda x: abs(x[2])) # sort according the correlation (at index 2)
            
        df_correlation = pd.DataFrame(corr_and_statio_list, columns=['Ticker 1', 'Ticker 2', 'Correlation', 'Stationnarity'])

        df_topcorrelation = df_correlation

        if self.use_corr:
            # Keep the pair constitution which has a correlation higher than the one set in the instance variable
            df_topcorrelation = df_topcorrelation[df_topcorrelation.Correlation > self.mincorr_level].reset_index(drop=True)
        if self.use_statio:
            # Keep the pair constitution which has a stationarity higher than the one set in the instance variable and according the computation method
            df_topcorrelation = df_topcorrelation[df_topcorrelation.Stationnarity < self.statio_level].reset_index(drop=True) if (self.use_adfuller or self.use_zivotandrews) else df_topcorrelation[df_topcorrelation.Stationnarity > self.statio_level].reset_index(drop=True)

        return df_topcorrelation
    

    def add_months(self, start_date, interval):
        """From a starting date in string format 'YYYY-MM-DD', return the same format date after an interval of X month(s) later."""
        date_format = '%Y-%m-%d'
        dtObj = datetime.strptime(start_date, date_format)
        # Add months to a given datetime object
        future_date = dtObj + relativedelta(months=interval)
        # Convert datetime object to string in required format
        future_date_str = future_date.strftime(date_format)
        return future_date_str
    
    
    def get_alltime_best_pairs(self, interval=6, repetition=1, filename="best_pairs"):
        """
        From the starting date until last date and progressing in a range of a specific interval in months, it saves in a json file the pairs with a satisfying correlation value and/or stationarity following the instance variable criteria set and this between two increasing months of a specific interval.
        We presume that start_date is 2015-03-01 and end_date is 2021-06-18, interval is 6 and repetition is 2.
        We will then start the computations on price data between 2015-03-01 and 2015-09-01 (+6 months),
        then do it again after 2 months: therefore between 2015-05-01 and 2015-11-01 etc until end_date is 2021-06-01.
        :param interval: Number of months between an increasing start date and end date on which to get the prices and compute the correlation and stationarity.
        :param repetition: Repeat the corr and statio computation every X months.
        :param filename: Name of the generated json file.
        """
        start_date = self.start_date
        end_date = self.add_months(self.start_date, interval)

        # To know when to stop the loop: the month and year of the last saved price
        last_date = self.df_all_prices.iloc[-1]['Dates'] 
        last_year = last_date.strftime('%Y')
        last_month = last_date.strftime('%m')

        best_pairs_dict = {}
        while True:
            # Get the best pairs of a specific period
            top = self.get_best_pairs(start_date, end_date)
            best_pairs_dict[end_date] = [[top.iloc[i]['Ticker 1'], top.iloc[i]['Ticker 2']] for i in range(len(top))]
            # increment start and end for the get_best_pairs() computation
            start_date = self.add_months(start_date, repetition)
            end_date = self.add_months(end_date, repetition)
            # check if we've reached the month and year of the last saved price
            splt = end_date.split('-')
            if splt[0] == last_year and splt[1] == last_month:
                break
        
        # Save the results in a json for backtesting purpose
        with open(filename + ".json", "w") as f:
            json.dump(best_pairs_dict, f)
        
