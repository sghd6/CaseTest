import json, requests, datetime, time, json
#import matplotlib.pyplot as plt
#import mplfinance as mpf
#import pandas as pd
import pygal
import numpy as np


def main():
    #variables
    apiKey = "WZYK9TQ3C96A9WXT"
    #Ask the user to enter the stock symbol for the company they want data for.
    def stockSymbolGetter():
    
     while True:
        symbol = input("\nPlease enter the stock symbol for the company you want data for: ").upper()
        if (symbol == ""):
            print("Please enter a valid stock symbol.")
            continue
        else:
            break
     return symbol

    stockSymbol = stockSymbolGetter()
    def getChartType():
    #Ask the user for the chart type they would like.
        validChartTypes = ["LINE", "BAR"]
    #validChartTypes = ["LINE", "BAR", "CANDLESTICK"]
        chartInput = input("\nPlease enter the chart type you would like (1. LINE, 2. BAR): ").upper()
    #chartType = input("\nPlease enter the chart type you would like (LINE, BAR, CANDLESTICK): ").upper()
        if (chartInput== 1):
            chartType = "LINE"
        if (chartInput == 2):
            chartType = "BAR"

        while chartType not in validChartTypes:
            print("Invalid chart type. Please enter a valid option.")
            chartType = input("\nPlease enter the chart type you would like (LINE, BAR): ").upper()
        #chartType = input("\nPlease enter the chart type you would like (LINE, BAR, CANDLESTICK): ").upper()
        return chartType
    
    chartType= getChartType()

    def getTimeSeries():
    #Ask the user for the time series function they want the api to use.
        validTimeSeries = ["INTRADAY", "DAILY", "DAILY_ADJUSTED", "WEEKLY", "WEEKLY_ADJUSTED", "MONTHLY", "MONTHLY_ADJUSTED"]
        timeSeries = input("\nPlease enter the time series function you would like the api to use (INTRADAY, DAILY, DAILY_ADJUSTED, WEEKLY, WEEKLY_ADJUSTED, MONTHLY, MONTHLY_ADJUSTED): ").upper()

        while timeSeries not in validTimeSeries:
            print("Invalid time series function. Please enter a valid option.")
            timeSeries = input("\nPlease enter the time series function you would like the api to use (INTRADAY, DAILY, DAILY_ADJUSTED, WEEKLY, WEEKLY_ADJUSTED, MONTHLY, MONTHLY_ADJUSTED): ").upper()    
    timeSeries=getTimeSeries()


    convertedBeginDate, convertedEndDate = ChoosingDates()

    #generating chart
    GetData(stockSymbol, apiKey, timeSeries, convertedBeginDate, convertedEndDate, chartType)


#getting the api data
def GetData(stockSymbol, apiKey, timeSeries, convertedBeginningDate, convertedEndDate, chartType):
    
    #getting the data from the API
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_{timeSeries}&symbol={stockSymbol}&outputsize=compact&apikey={apiKey}&datatype=json"
    
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} from the API")
        return
    
    time_series_key = None
    for key in data.keys():
        if 'Time Series' in key:
            time_series_key = key
            break
    
    if not time_series_key:
        print("Error: Could not find time series data in the API response")
        print("Available keys:", data.keys())
        return
    
    filtered_data = {}
    for date, values in data[time_series_key].items():
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        if convertedBeginningDate <= date_obj <= convertedEndDate:
            filtered_data[date] = values

    limited_data = dict(list(filtered_data.items()))

    dates = list(limited_data.keys())[::-1]

    if not dates:
        print("There is no data for the selected dates")
        return
    
    
    print("")
    time.sleep(2)
    for i in range(3, 0, -1):
        time.sleep(1)
        print("Generating chart" + "." * i) #to look cool
    
    time.sleep(2)
    print("\n", json.dumps(limited_data, indent=4))
    with open("data.json", "w") as file:
        json.dump(data, file)

    
    #print("Data received from API:", limited_data)
    GenerateChart(chartType, limited_data, convertedBeginningDate, convertedEndDate, stockSymbol)
    
    return

#generate the chart
def GenerateChart(chartType, data, startDate, EndDate, stockSymbol):
    dates = list(data.keys())[::-1]
    opens, highs, lows, closes = [], [], [], []


    for date in dates:
        values = data[date]  
    
        if all(key in values for key in ['1. open', '2. high', '3. low', '4. close']):
            opens.append(float(values['1. open']))
            highs.append(float(values['2. high']))
            lows.append(float(values['3. low']))
            closes.append(float(values['4. close'])) 

    if chartType == "LINE":
        line_chart = pygal.Line()
        line_chart.title = '%s %s Chart from %s to %s' % (stockSymbol, chartType, startDate, EndDate)
        line_chart.x_labels = dates
        line_chart.add('Open', opens)
        line_chart.add('High', highs)
        line_chart.add('Low',  lows)
        line_chart.add('Close', closes)
        line_chart.render_in_browser()
    elif chartType == "BAR":
        bar_chart = pygal.Bar()
        bar_chart.title = '%s %s Chart from %s to %s' % (stockSymbol, chartType, startDate, EndDate)
        bar_chart.x_labels = dates
        bar_chart.add('Open', opens)
        bar_chart.add('High', highs)
        bar_chart.add('Low',  lows)
        bar_chart.add('Close', closes)
        bar_chart.render_in_browser()

    #elif chartType == "CANDLESTICK":
        

        #ohlc_data = [(datetime.datetime.strptime(date, "%Y-%m-%d"), float(values['1. open']), float(values['2. high']), float(values['3. low']), float(values['4. close'])) for date, values in data.items()]
        #mpf.plot(pd.DataFrame(ohlc_data, columns=['Date', 'Open', 'High', 'Low', 'Close']).set_index('Date'), type='candle', style='charles')
    return
    
    
#getting user dates
def ChoosingDates():

    try:
        beginningDate = input("\nPlease enter the beginning date in M-D-YY or MM-DD-YY format: ")
        convertedBeginDate = datetime.datetime.strptime(beginningDate, "%m-%d-%y")

        #beginning date cant be past the present
        if (convertedBeginDate > datetime.datetime.now()):
            print("The beginning date should not be in the future.")
            return ChoosingDates()
    except ValueError:
        print("Please enter the date in the correct format.")
        return ChoosingDates()
    except Exception as e:
        print("An error occurred: ", e)
        return ChoosingDates()

    #end date should not be before the begin date
    while True:
        try:
            endDate = input("\nPlease enter the end date in M-D-YY or MM-DD-YY format: ")
            convertedEndDate = datetime.datetime.strptime(endDate, "%m-%d-%y")
        except ValueError:
            print("Please enter the date in the correct format.")
            continue
        except Exception as e:
            print("An error occurred: ", e)
            continue

        if (convertedEndDate < convertedBeginDate):
            print("The end date should not be before the begin date.")
            
            changeDates = input("Would you like to restart the dates portion? (y/n): ").lower()
            if (changeDates == 'y'):
                return ChoosingDates()
            else:
                continue
        else:
            return convertedBeginDate, convertedEndDate

if __name__ == "__main__":
    main()