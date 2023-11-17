grupo_siafi_data = csv_data[['12.311.02.01', 'EQUIPAMENTOS DE PROCESSAMENTO DE DADOS       ']]
grupo_siafi_data.columns = ['Grupo', 'Descricao']

grupo_siafi_data = grupo_siafi_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

grupo_siafi_data = grupo_siafi_data.drop_duplicates()

grupo_siafi_csv_path = '/mnt/data/grupo_siafi.csv'
grupo_siafi_data.to_csv(grupo_siafi_csv_path, index=False)

grupo_siafi_csv_path
