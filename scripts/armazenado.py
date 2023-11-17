armazenado_data = csv_data[['166381']]
armazenado_data['Local_ID'] = armazenado_data['166381'] 
armazenado_data['Inventario'] = '' 
armazenado_data.columns = ['Bem_ID', 'Local_ID', 'Inventario']

armazenado_data = armazenado_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

armazenado_csv_path = '/mnt/data/armazenado.csv'
armazenado_data.to_csv(armazenado_csv_path, index=False)

armazenado_csv_path
