import pandas as pd

# Carregar os dados
df = pd.read_csv('novatabela.csv')

# Excluir a coluna 'Month' se existir
df = df.drop(columns=['Month'], errors='ignore')

# Calcular o total de infecções para cada país
total_infections_per_country = df.sum()

# Selecionar os 10 países com o maior número de infecções
top_10_countries = total_infections_per_country.nlargest(10).reset_index()
top_10_countries.columns = ['Country/Region', 'Total Infections']

# Salvar a nova tabela em um arquivo CSV
top_10_countries.to_csv('top_10_countries.csv', index=False)

# Visualizar a nova tabela
print(top_10_countries)
