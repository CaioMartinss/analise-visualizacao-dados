import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Carregar os dados
data = pd.read_csv('./media_alunos_agrupada.csv')

# Verificar valores ausentes
print(data.isnull().sum())

# Remover linhas com valores ausentes
data = data.dropna()

# Mapear os turnos para números
turno_map = {'MATUTINO': 0, 'VESPERTINO': 1, 'NOTURNO': 2}
data['turno_num'] = data['turno'].map(turno_map)

# Verificar valores ausentes novamente
print(data[['turno_num', 'media_todas_materias']].isnull().sum())

# Remover qualquer linha que tenha NaN em 'turno_num' ou 'media_todas_materias'
data = data.dropna(subset=['turno_num', 'media_todas_materias'])

# Configurar o gráfico de dispersão
plt.figure(figsize=(10, 6))
sns.scatterplot(x='turno_num', y='media_todas_materias', hue='turno', data=data)

# Configurar o modelo de regressão linear
X = data[['turno_num']]
y = data['media_todas_materias']

# Ajustar a regressão linear
linear_model = LinearRegression()
linear_model.fit(X, y)
y_pred_linear = linear_model.predict(X)

# Adicionar a linha de regressão linear ao gráfico
plt.plot(data['turno_num'], y_pred_linear, color='red', label='Regressão Linear')

# Configurar o modelo de regressão polinomial (grau 2)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
poly_model = LinearRegression()
poly_model.fit(X_poly, y)
y_pred_poly = poly_model.predict(X_poly)

# Adicionar a linha de regressão polinomial ao gráfico
plt.plot(data['turno_num'], y_pred_poly, color='blue', label='Regressão Polinomial (grau 2)')

# Configurações finais do gráfico
plt.xlabel('Turno')
plt.ylabel('Média de Todas as Matérias')
plt.title('Relação entre Notas e Turnos com Projeção Linear e Polinomial')
plt.legend()
plt.xticks(ticks=[0, 1, 2], labels=['MATUTINO', 'VESPERTINO', 'NOTURNO'])
plt.grid(True)
plt.show()
