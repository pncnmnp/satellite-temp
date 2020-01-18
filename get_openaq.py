import openaq
import json
import pandas as pd

class Fetch_OpenAQ:
	def __init__(self):
		self.FETCH_DIR = "./ground_data/"

	def get_filename(self, start_date, end_date, directory):
		return directory + "data_" + str(start_date) + "to" + str(end_date) + ".csv"

	def get_param_dict(self, country, limit, start_date, end_date, pollutants, df):
		return {
			'country': country,
			'limit': limit,
			'date_from': start_date,
			'date_to': end_date,
			'parameter': pollutants,
			'page': 1
		}

	def fetch(self, country, limit, start_date, end_date, pollutants, df=True):
		api = openaq.OpenAQ()
		data = self.get_param_dict(country, limit, start_date, end_date, pollutants, df)

		status, resp = api.measurements(**data)
		no_pages = resp['meta']['found']//10000 + 1

		if df == True:
			data['df'] = True

		pollutants_df = pd.DataFrame()
		for index in range(0, no_pages):
			df = api.measurements(**data)
			pollutants_df = pd.concat([pollutants_df, df])
			print("Fetched: page " + str(data['page']))
			data['page'] += 1

		pollutants_df.to_csv(self.get_filename(start_date, end_date, directory=self.FETCH_DIR), encoding="utf-8", index=False)

		return pollutants_df

if __name__ == '__main__':
	ground = Fetch_OpenAQ()
	ground.fetch("IN", 10000, "2019-12-01", "2019-12-05", ["co", "pm25", "so2", "no2"])