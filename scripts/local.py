local_data = csv_data[['166381', 'CGTI-PROCC/PRESIDÊNCIA                                 ']]
local_data['Sala'] = '' 
local_data.columns = ['ID', 'Endereco', 'Sala']

local_data = local_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

local_data = local_data.drop_duplicates()

local_csv_path = '/mnt/data/local.csv'
local_data.to_csv(local_csv_path, index=False)

local_csv_path
