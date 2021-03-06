import xarray as xr
import pandas as pd
import pickle
import numpy as np
import os.path
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

IND_LAT_LESS = 37.6
IND_LAT_GRTR = 8.4
IND_LON_LESS = 97.25
IND_LON_GRTR = 68.7

class Hotspot:
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

	def save_listX(self,X,filename):
		filename=filename
		file = open(filename, "w")

		file.write(str(X))

	def remove_non_lat_lon_data(self, df, lat_less_than, lat_greater_than, lon_less_than, lon_greater_than):
		'''
		Removes all the not required latitudes and longitudes
		'''
		return df[(df["latitude"] >= lat_greater_than) 
		            & (df["latitude"] <= lat_less_than) 
		            & (df["longitude"] >= lon_greater_than) 
		            & (df["longitude"] <= lon_less_than)]

	def convert_and_save_nc(self, filename, group, csv_name, attr):
		ds = xr.open_dataset(filename, group=group)

		if os.path.exists(csv_name) == False:
			self.save_to_csv(ds, attr, csv_name)

		df = self.read_csv(csv_name)
		df = self.remove_nan_csv(df, attr)
		df = self.remove_non_lat_lon_data(df, IND_LAT_LESS, IND_LAT_GRTR, IND_LON_LESS, IND_LON_GRTR)

		return df

	def filter_percentile(self, df, percentile_attr, percentile=0.99):
		return df[df[percentile_attr] >= df[percentile_attr].quantile(percentile)]

	def clustering_dbscan(self, df, conc_attr, eps=10, min_samples=2):
		"""
        Please make sure that `df` has been filtered percentile wise
        To do that, use filter_percentile method
		"""
		X = df[["latitude", "longitude"]].values
		wt = df[conc_attr].values

		metric = "haversine"
		algorithm = "ball_tree"
		min_samples = 2
		eps = eps/6371

		# without weight DBSCAN
		clustering = DBSCAN(eps=10/6371, min_samples=2, algorithm=algorithm, metric=metric).fit(np.radians(X))
		# with weight
		# clustering = DBSCAN(eps=10/6371, min_samples=2, algorithm=algorithm, metric=metric).fit(np.radians(X), sample_weight=wt)

		labels = clustering.labels_

		return X, wt, clustering, labels

	def plot_clustering_dbscan(self, X, weight, clustering, labels):
		temp_lats = [x[0] for x in X]
		temp_lons = [x[1] for x in X]

		lats, lons, modified_labels = list(), list(), list()
		for index in range(0, len(labels)):
			if labels[index] == -1:
				continue
			lats.append(temp_lats[index])
			lons.append(temp_lons[index])
			modified_labels.append(labels[index])

		color_codes = np.unique(clustering.labels_, return_counts=True)[0][1:]
		colors = [list(np.random.random(size=3)) for i in range(len(color_codes))]

		m = Basemap(projection='lcc', 
			         resolution='h', 
			         llcrnrlat=IND_LAT_GRTR, 
			         urcrnrlat=IND_LAT_LESS, 
			         llcrnrlon=IND_LON_GRTR, 
			         urcrnrlon=IND_LON_LESS, 
			         lon_0=np.mean(lons), 
			         lat_0=np.mean(lats))

		m.drawcoastlines(color='gray')
		m.drawcountries(color='gray')
		m.drawstates(color='gray')
		xi, yi = m(lons, lats)

		for index in range(len(xi)):
			color_val = modified_labels[index]
			if color_val != -1:
				m.scatter(xi[index], yi[index], color=colors[color_val], s=2)
		plt.legend()
		plt.savefig("foo.png")

	def X_to_json(self, X, wt, labels):
		'''
		Converting X and labels to a file
		'''
		# Excluding -1 values
		# total_labels = len(np.unique(labels)) - 1
		lat_lon_mapping = dict()
		for index in range(len(X)):
			if labels[index] != -1:
				try:
					lat_lon_mapping[labels[index]]["total_wt"] += wt[index]
					lat_lon_mapping[labels[index]]["positions"] += [str(X[index][0]) + ", " + str(X[index][1])]
				except:
					lat_lon_mapping[labels[index]] = dict()
					lat_lon_mapping[labels[index]]["total_wt"] = wt[index]
					lat_lon_mapping[labels[index]]["positions"] = [str(X[index][0]) + ", " + str(X[index][1])]
		return [pos["positions"] for pos in sorted(lat_lon_mapping.values(), key=lambda x: x["total_wt"], reverse=True)]

	def heatmap_json(self, X, wt):
		x_wt = list()
		for index in range(len(X)):
			x_arr = [X[index][0], X[index][1], wt[index]]
			x_wt.append(x_arr)

		return x_wt

if __name__ == '__main__':
	obj = Hotspot()
	path_to_NCfile = "./no2/S5P_OFFL_L2__NO2____20191206T072611_20191206T090741_11122_01_010302_20191212T054053.nc" 
	df = obj.convert_and_save_nc(path_to_NCfile, "PRODUCT", "data_no2_6_dec.csv", "nitrogendioxide_tropospheric_column")
	df = obj.filter_percentile(df, "nitrogendioxide_tropospheric_column")
	X, wt, clustering, labels = obj.clustering_dbscan(df, "nitrogendioxide_tropospheric_column")
	obj.plot_clustering_dbscan(X, wt, clustering, labels)

	listOfPoints = obj.X_to_json(X, wt, labels)
	obj.save_listX(listOfPoints ,'./list1.txt')
