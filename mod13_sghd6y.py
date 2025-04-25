import StockDataVisualizer
from unittest.mock import patch
import unittest

class TestData(unittest.TestCase):
#Stock Symbol Test
    @patch('builtins.input', side_effect=['googl'])
    def test_GetSymbol(self, mock_input):

        validSymbol = ''
        validSymbol = StockDataVisualizer.stockSymbolGetter()
        self.assertEqual('GOOGL', validSymbol)
        self.assertGreater(len(validSymbol),0)
        self.assertLess(len(validSymbol),8)

#Chart Type Test
    @patch('builtins.input', side_effect=['3', '1'])
    def test_GetChartType(self, mock_input):

        chartype = StockDataVisualizer.getChartType()
        self.assertEqual(chartype, 'LINE')
        self.assertNotEqual(chartype, 'line')
        self.assertNotEqual(chartype, '1')

#Time Series Test
    @patch('builtins.input', side_effect=['DAILY', 'Other'])
    def test_GetTimeSeries(self, mock_input):

        timeSeries = StockDataVisualizer.getTimeSeries()
        self.assertEqual(timeSeries, 'DAILY')
        self.assertNotEqual(timeSeries, 'daily')



#Date Test
    @patch('builtins.input', side_effect=['02-02-24', '03-02-24'])
    def test_getTimeseries(self, mock_input):

        dateBegin, dateEnd = StockDataVisualizer.ChoosingDates()
        self.assertGreater(dateEnd,dateBegin)
        self.assertNotEqual(dateBegin, dateEnd)

    





    
        
if __name__ == '__main__':
   unittest.main()



    