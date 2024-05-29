import pandas as pd
import mysql.connector

# Conectar ao servidor MySQL
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="escola"
)

# Consulta para ler dados da tabela dados_matricula
query_dados_matricula = """
    SELECT registro_geral, nome, situacao_matricula, data_matricula, turno
    FROM dados_matricula
    WHERE situacao_matricula = 'MATRICULADO'
"""

# Consulta para ler dados da tabela media_alunos
query_media_alunos = """
    SELECT registro_geral, media_final, turma
    FROM media_alunos
"""

# Ler dados das tabelas
dados_matricula = pd.read_sql(query_dados_matricula, conn)
media_alunos = pd.read_sql(query_media_alunos, conn)

# Fechar a conexão
conn.close()

# Extrair o ano da data de matrícula
dados_matricula['ano'] = pd.to_datetime(dados_matricula['data_matricula'], format='%d/%m/%Y').dt.year

# Agrupar as médias por aluno
media_agrupada = media_alunos.groupby('registro_geral')['media_final'].mean().reset_index()
media_agrupada.columns = ['registro_geral', 'media_final']

# Mesclar dados de matrícula com médias agrupadas
result = pd.merge(dados_matricula, media_agrupada, on='registro_geral')

# Selecionar os campos desejados
result = result[['registro_geral', 'media_final', 'ano', 'turno']]

# Salvar os dados em um arquivo Excel
with pd.ExcelWriter('media_alunos_agrupada.xlsx', engine='xlsxwriter') as writer:
    result.to_excel(writer, sheet_name='Media_Alunos', index=False)

print("Arquivo Excel criado com sucesso!")
