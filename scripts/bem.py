bem_data_atualizada = csv_data.copy()
bem_data_atualizada['Sequencia'] = bem_data_atualizada['166381']
bem_data_atualizada['Tipo'] = bem_data_atualizada['F']
bem_data_atualizada['Responsabilidade'] = bem_data_atualizada['COORDENACAO DE GESTAO TECNOL. INFORMACAO']
bem_data_atualizada['Categoria_ID'] = bem_data_atualizada['12.311.02.01']  # Exemplo de referência ao grupo
bem_data_atualizada['Situacao'] = bem_data_atualizada['EM PROCESSO DE LOCALIZAÇÃO           ']

bem_data_atualizada = bem_data_atualizada[['Sequencia', 'EQUIPAMENTOS DE PROCESSAMENTO DE DADOS       ', '12.311.02.01', '9583,97', 'Tipo', 'Responsabilidade', 'Categoria_ID', 'Situacao']]
bem_data_atualizada.columns = ['Sequencia', 'Nome', 'Descricao', 'Valor', 'Tipo', 'Responsabilidade', 'Categoria_ID', 'Situacao']

bem_data_atualizada = bem_data_atualizada.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

bem_csv_atualizado_path = '/mnt/data/dados_bem_atualizado.csv'
bem_data_atualizada.to_csv(bem_csv_atualizado_path, index=False)

bem_csv_atualizado_path
