pertence_data = csv_data[['166381', '001011017']]
pertence_data.columns = ['Bem_ID', 'Unidade_ID']

pertence_data = pertence_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

pertence_csv_path = '/mnt/data/pertence.csv'
pertence_data.to_csv(pertence_csv_path, index=False)

pertence_csv_path
