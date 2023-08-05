"""
Import functions for all datasets.  Datasets for 'iris' and 'boston_house_price'
are from scikit-learn.
"""

from os.path import dirname
import pandas as pd

def list_data():
    """
    Lists the datasets which are available, and where they are located.
    """
    
    print("All datasets for the starlib package are in the ./data directory.")
    print("  ")
    print("Available datasets:")
    print("iris.csv")
    print("boston_house_prices.csv")
    print("weather.csv")
    print("  ")
    print("Each dataset has its own load utility.  For example, to load iris:")
    print("starlib.load_iris()")
    print("  ")
    print("Datasets are read using Pandas, i.e. pd.read_csv.")    
    
# Load Boston housing prices dataset as pandas dataframe. 
def boston_house_prices():
        
    module_path = dirname(__file__)
    data_file_name = 'boston_house_prices.csv'
    csv_file = module_path + '/data/' + data_file_name
    
    boston_house_prices = pd.read_csv(csv_file)
    return boston_house_prices
    
 # Load iris dataset as pandas dataframe.
def load_iris():
        
    module_path = dirname(__file__)
    data_file_name = 'iris.csv'
    csv_file = module_path + '/data/' + data_file_name
    
    iris = pd.read_csv(csv_file)
    return iris

 # Load iris dataset as pandas dataframe.
def load_weather():
        
    module_path = dirname(__file__)
    data_file_name = 'weather.csv'
    csv_file = module_path + '/data/' + data_file_name
    
    weather = pd.read_csv(csv_file)
    return weather
