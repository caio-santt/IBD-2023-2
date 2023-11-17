compra_data = csv_data[['166381', '2018-09-06', '9583,97']]
compra_data.columns = ['Bem_ID', 'Data', 'Valor']

compra_data = compra_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

compra_data = compra_data.drop_duplicates()

compra_csv_path = '/mnt/data/compra.csv'
compra_data.to_csv(compra_csv_path, index=False)

compra_csv_path
