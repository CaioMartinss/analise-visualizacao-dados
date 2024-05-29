import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer

# Carregar os dados
data = pd.read_csv('media_alunos_agrupada.csv')

# Ajustar o formato da média final
data['media_final'] = data['media_final'].str.replace(',', '.').astype(float)

# Remover o turno "diurno" dos dados
data = data[data['turno'] != 'DIURNO']

# Filtrar os anos de 2022 a 2026
data = data[data['ano'].between(2022, 2026)]

# Preencher valores nulos na coluna de média final com a média ou a moda dos períodos existentes
imputer = SimpleImputer(strategy='mean')
data['media_final'] = imputer.fit_transform(data[['media_final']])

# Agrupar as médias por turno e ano
grouped_data = data.groupby(['turno', 'ano'])['media_final'].mean().reset_index()

# Plotar o gráfico de dispersão
plt.figure(figsize=(10, 6))

# Ajustar a regressão polinomial para cada turno
for turno in grouped_data['turno'].unique():
    subset = grouped_data[grouped_data['turno'] == turno]
    if len(subset) == 0:
        continue
    X = subset['ano'].values.reshape(-1, 1)
    y = subset['media_final'].values
    poly_features = PolynomialFeatures(degree=2)
    X_poly = poly_features.fit_transform(X)
    poly_model = LinearRegression()
    poly_model.fit(X_poly, y)
    y_pred_poly = poly_model.predict(X_poly)
    plt.scatter(subset['ano'], subset['media_final'], label=f'{turno}', marker='o')
    plt.plot(subset['ano'], y_pred_poly, linestyle='-', color='gray')
    
    # Calcular previsibilidade para o ano de 2025 para cada turno
    X_pred = np.array([[2025]])
    X_pred_poly = poly_features.transform(X_pred)
    y_pred = poly_model.predict(X_pred_poly)
    
    # Adicionar o valor previsto no gráfico
    plt.scatter(2025, y_pred, marker='o', color='red')
    plt.text(2025, y_pred, f'{y_pred[0]:.2f}', verticalalignment='bottom', horizontalalignment='right')

# Configurações do gráfico
plt.xlabel('Ano')
plt.ylabel('Média Final (0-10)')
plt.title('Relação entre Notas e Turnos de 2022 a 2026 com Projeção Polinomial para 2025')
plt.legend()
plt.grid(True)
plt.xticks([2023, 2024, 2025])
plt.yticks(np.arange(0, 11, 1))
plt.show()
