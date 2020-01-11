import xarray as xr
import pandas as pd
import numpy as np

IND_LAT_LESS = 37.6
IND_LAT_GRTR = 8.4
IND_LON_LESS = 97.25
IND_LON_GRTR = 68.7

class INFO:
	def __init__(filename):
		self.filename = filename

	def filename(self):
		return self.filename

	def save_to_csv(self, ds, attr, destination):
		ds[attr].to_dataframe().to_csv(destination)

	def to_dataframe(self, ds, attr):
		return ds[attr].to_dataframe()

	def read_csv(self, filename):
		return pd.read_csv()

	def remove_nan_csv(self, df, attr):
		return df[np.isfinite(df[attr])]

	def remove_non_lat_lon_data(df, lat_less_than, lat_greater_than, lon_less_than, lon_greater_than):
		return df[(df["latitude"] >= lat_greater_than) 
		            & (df["latitude"] <= lat_less_than) 
		            & (df["longitude"] >= lon_greater_than) 
		            & (df["longitude"] <= lon_less_than)]