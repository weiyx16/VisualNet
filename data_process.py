# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import os
from utils import utils

csv_path = r'./data/raw/WDI/WDIData.csv'

assert os.path.isfile(csv_path), " No such csv file! "
data = pd.read_csv(csv_path)
row_num, column_num = data.shape
print(" >> Succeed to load csv file from: {}\n >> With row: {}, column: {}" .format(csv_path, row_num, column_num))
# Filter out rows if including "" data
empty_row = []
for index, row in data.iterrows():
    if row.isnull()[:-1].values.any():
        # it seems the last column must be "" in WDIData.csv
        empty_row.append(index)
data = data.drop(data.index[empty_row])
row_num, column_num = data.shape
print(" >> Remove rows with empty values. \n >> For now, with row: {}, column: {}" .format(row_num, column_num))

save_dir = os.path.join('./data/postprocess', csv_path.split('/')[-2])
save_csv_path = os.path.join(save_dir, csv_path.split('/')[-1])
utils.mkdir_safe(save_dir)
data.to_csv(save_csv_path)

# Group according to the country
save_dir_country = os.path.join(save_dir, 'Country')
utils.mkdir_safe(save_dir_country)
Country_list = pd.unique(data.loc[:, 'Country Code']).tolist()
for country in Country_list:
    ext = os.path.splitext(csv_path)[-1]
    save_csv_path = os.path.join(save_dir_country, country + ext)
    data[data['Country Code'] == country].to_csv(save_csv_path)
print(" >> Split Data according to the country, number: {}" .format(len(Country_list)))

# Group according to the Indicator
save_dir_indicator = os.path.join(save_dir, 'Indicator')
utils.mkdir_safe(save_dir_indicator)
Indicator_list = pd.unique(data.loc[:, 'Indicator Code']).tolist()
for indicator in Indicator_list:
    ext = os.path.splitext(csv_path)[-1]
    save_csv_path = os.path.join(save_dir_indicator, indicator + ext)
    data[data['Indicator Code'] == indicator].to_csv(save_csv_path)
print(" >> Split Data according to the indicator, number: {}" .format(len(Indicator_list)))
