import xarray as xr
import pandas as pd
import numpy as np

IND_LAT_LESS = 37.6
IND_LAT_GRTR = 8.4
IND_LON_LESS = 97.25
IND_LON_GRTR = 68.7

class INFO:
	def __init__(self):
		pass

	def save_to_csv(self, ds, attr, destination):
		ds[attr].to_dataframe().to_csv(destination)

	def to_dataframe(self, ds, attr):
		return ds[attr].to_dataframe()

	def read_csv(self, filename):
		return pd.read_csv(filename)

	def remove_nan_csv(self, df, attr):
		return df[np.isfinite(df[attr])]

	def remove_non_lat_lon_data(self, df, lat_less_than, lat_greater_than, lon_less_than, lon_greater_than):
		return df[(df["latitude"] >= lat_greater_than) 
		            & (df["latitude"] <= lat_less_than) 
		            & (df["longitude"] >= lon_greater_than) 
		            & (df["longitude"] <= lon_less_than)]

	def convert_and_save_nc(self, filename, group, csv_name, attr):
		ds = xr.open_dataset(filename, group=group)
		self.save_to_csv(ds, attr, csv_name)

		df = self.read_csv(csv_name)
		df = self.remove_nan_csv(df, attr)
		df = self.remove_non_lat_lon_data(df, IND_LAT_LESS, IND_LAT_GRTR, IND_LON_LESS, IND_LON_GRTR)

		return df

if __name__ == '__main__':
	obj = INFO()
	obj.convert_and_save_nc("./no2/S5P_OFFL_L2__NO2____20191203T064154_20191203T082324_11079_01_010302_20191209T092015.nc", "PRODUCT", "data.csv", "nitrogendioxide_tropospheric_column_precision")
