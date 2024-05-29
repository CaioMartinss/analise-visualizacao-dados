import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Carregar os dados
data = pd.read_csv('media_alunos_agrupada.csv')

# Ajustar o formato da média final
data['media_final'] = data['media_final'].str.replace(',', '.').astype(float)

# Remover o turno "diurno" dos dados
data = data[data['turno'] != 'DIURNO']

# Agrupar as médias por ano e turno
grouped_data = data.groupby(['ano', 'turno'])['media_final'].mean().reset_index()

# Plotar o gráfico de dispersão
plt.figure(figsize=(10, 6))

# Adicionar os pontos para cada turno e traçar a reta de regressão
for turno in ['MATUTINO', 'VESPERTINO']:
    subset = grouped_data[grouped_data['turno'] == turno]
    plt.scatter(subset['ano'], subset['media_final'], label=turno)

# Adicionar uma linha de tendência para todos os dados
X = grouped_data['ano'].values.reshape(-1, 1)
y = grouped_data['media_final'].values
linear_model = LinearRegression()
linear_model.fit(X, y)
X_pred = np.arange(2022, 2027).reshape(-1, 1)
y_pred = linear_model.predict(X_pred)
plt.plot(X_pred, y_pred, color='black', linestyle='--', label='Linha de Tendência')

# Adicionar as projeções lineares para 2025 para cada turno
X_2025 = np.array([[2025]])
for turno in ['MATUTINO', 'VESPERTINO']:
    subset = grouped_data[grouped_data['turno'] == turno]
    X_turno = subset['ano'].values.reshape(-1, 1)
    y_turno = subset['media_final'].values
    linear_model_turno = LinearRegression()
    linear_model_turno.fit(X_turno, y_turno)
    y_2025_pred_turno = linear_model_turno.predict(X_2025)
    plt.scatter(2025, y_2025_pred_turno, marker='o', color='red', label=f'Projeção Linear 2025 - {turno}')

# Configurações do gráfico
plt.xlabel('Ano')
plt.ylabel('Média Final (0-10)')
plt.title('Média Final dos Alunos por Ano e Turno com Projeção Linear para 2025')
plt.legend()
plt.grid(True)
plt.xticks(np.arange(2022, 2027, 1))
plt.yticks(np.arange(0, 11, 1))
plt.show()
