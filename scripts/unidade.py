unidade_data = csv_data[['COGEAD         ', 'COORDENACAO DE GESTAO TECNOL. INFORMACAO', '001011017']]
unidade_data.columns = ['Sigla', 'Setor_Descricao', 'Setor_Codigo']

unidade_data = unidade_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

unidade_data = unidade_data.drop_duplicates()

unidade_csv_path = '/mnt/data/unidade.csv'
unidade_data.to_csv(unidade_csv_path, index=False)

unidade_csv_path
