import pandas as pd

AQI_FILE = "./AQI_INDIA.csv"

class Aqi:
	def __init__(self):
		pass

	def read_aqi(self):
		return pd.read_csv(AQI_FILE)

	def find_aqi(self, pollutants, aqi_file=None, range_attr_name="aqi_range"):
		"""
		The format followed is specific to India
		The formula is from: http://www.indiaenvironmentportal.org.in/files/file/Air%20Quality%20Index.pdf
		"""
		if aqi_file == None:
			aqi_file = self.read_aqi()

		sub_indices = dict()
		for pollutant in pollutants:
			conc = pollutants[pollutant]
			''' b_hi -> breakpoint high
				b_lo -> breakpoint low
				i_hi -> AQI corresponding to b_hi
				i_lo -> AQI corresponding to b_lo
			'''
			conc_name = [name for name in aqi_file.keys().tolist() if pollutant in name][0]

			for aqi_conc_level in aqi_file[conc_name].tolist():
				low, high = int(aqi_conc_level.split("_")[0]), int(aqi_conc_level.split("_")[1])
				if conc >= low and conc <= high:
					b_hi = high
					b_lo = low

					index_aqi_file = aqi_file[conc_name].tolist().index(aqi_conc_level)
					aqi_range = aqi_file[range_attr_name][index_aqi_file]

					low_aqi, high_aqi = int(aqi_range.split("_")[0]), int(aqi_range.split("_")[1])

					i_lo = low_aqi
					i_hi = high_aqi

					aqi_val = (((i_hi - i_lo)/(b_hi - b_lo))*(conc - b_lo)) + i_lo

			sub_indices[pollutant] = aqi_val

		total_aqi_val = max(sub_indices.values())

		return total_aqi_val, sub_indices

if __name__ == '__main__':
	obj = Aqi()
	print(obj.find_aqi({"pm_10": 101, "pm_2.5": 82, "so2": 79, "nh3": 220}))