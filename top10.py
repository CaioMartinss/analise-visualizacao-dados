import pandas as pd

# Carregar os dados
df = pd.read_csv('covid_global.csv')

# Excluir a coluna 'Province/State' se existir
df = df.drop(columns=['Province/State'], errors='ignore')

# Agrupar por país e calcular a soma de todas as datas
total_cases_per_country = df.groupby('Country/Region').sum()

# Calcular o total de infecções para cada país
total_infections = total_cases_per_country.sum(axis=1)

# Selecionar os 10 países com o maior número de infecções
top_10_countries = total_infections.nlargest(10).reset_index()
top_10_countries.columns = ['Country/Region', 'Total Infections']

# Salvar a nova tabela em um arquivo CSV
top_10_countries.to_csv('top_10_countries.csv', index=False)

# Visualizar a nova tabela
print(top_10_countries)
