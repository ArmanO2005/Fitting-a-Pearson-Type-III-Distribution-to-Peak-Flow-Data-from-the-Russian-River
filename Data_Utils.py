import pandas as pd
import numpy as np

class Data_Utils:
    def __init__(self):
        self.data = None

    def load_data(self):
        Calpella_data = pd.read_csv('russian_river_data/Calpella_daily.csv')
        Guerneville_data = pd.read_csv('russian_river_data/Guerneville_daily.csv')
        Hopland_data = pd.read_csv('russian_river_data/Hopland_daily.csv')
        WarmSprings_data = pd.read_csv('russian_river_data/WarmSprings_Inflow_daily.csv')

        self.data = {
            'Calpella Gage FLOW': Calpella_data,
            'Guerneville Gage FLOW': Guerneville_data,
            'Hopland Gage FLOW': Hopland_data,
            'Warm Springs Dam Inflow FLOW': WarmSprings_data
        }


    def Get_Peak_Flows(self):
        """Returns a dict of peak flow dataframes for all basins, indexed by basin name."""
        for basin in self.data.keys():
            basin_df = self.data[basin][['Date', basin]]
            basin_df['Date'] = pd.to_datetime(basin_df['Date'])
            basin_df['water_year'] = np.where(basin_df['Date'].dt.month >= 10, basin_df['Date'].dt.year + 1, basin_df['Date'].dt.year)
            
            peak_flows = basin_df.groupby('water_year')[basin].max().reset_index()
            peak_flows.to_csv(f'russian_river_peak_flows/{basin.split()[0]}.csv')

    def Get_N_Day_Avg_Minimums(self, N):
        """Returns a dict of N-day min flow dataframes for all basins, indexed by basin name and climatic year (April 1st to March 31st)."""
        for basin in self.data.keys():
            basin_df = self.data[basin][['Date', basin]]
            basin_df['Date'] = pd.to_datetime(basin_df['Date'])
            basin_df['climatic_year'] = np.where(basin_df['Date'].dt.month >= 4, basin_df['Date'].dt.year + 1, basin_df['Date'].dt.year)
            basin_df['mav'] = basin_df[basin].rolling(window=7, min_periods=N).mean()

            min_flows = basin_df.groupby('climatic_year')["mav"].min().reset_index()
            min_flows.to_csv(f'russian_river_low_flows(7d-avg)/{basin.split()[0]}.csv')

    def Get_N_Day_Avg_Maximums(self, N):
        """Returns a dict of N-day max flow dataframes for all basins, indexed by basin name and water year (October 1st to September 30th)."""
        for basin in self.data.keys():
            basin_df = self.data[basin][['Date', basin]]
            basin_df['Date'] = pd.to_datetime(basin_df['Date'])
            basin_df['water_year'] = np.where(basin_df['Date'].dt.month >= 10, basin_df['Date'].dt.year + 1, basin_df['Date'].dt.year)
            basin_df['mav'] = basin_df[basin].rolling(window=7, min_periods=7).mean()

            max_flows = basin_df.groupby('water_year')["mav"].max().reset_index()
            max_flows.to_csv(f'russian_river_peak_flows(7d-avg)/{basin.split()[0]}.csv')
        
    

x = Data_Utils()
x.load_data()
x.Get_Peak_Flows()
x.Get_N_Day_Avg_Minimums(7)
x.Get_N_Day_Avg_Maximums(7)