import pandas as pd
import mysql.connector
from datetime import datetime

# Função para criar as tabelas
def criar_tabelas(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados_matricula (
            registro_geral INT PRIMARY KEY,
            nome VARCHAR(100),
            situacao_matricula VARCHAR(50),
            data_matricula DATE,
            turno VARCHAR(20)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media_alunos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            registro_geral INT,
            disciplina VARCHAR(100),
            media_final FLOAT,
            turma VARCHAR(20),
            FOREIGN KEY (registro_geral) REFERENCES dados_matricula(registro_geral)
        )
    """)

# Função para converter data do formato DD/MM/YYYY para YYYY-MM-DD
def converter_data(data_str):
    return datetime.strptime(data_str, '%d/%m/%Y').strftime('%Y-%m-%d')

# Função para inserir dados na tabela dados_matricula
def inserir_dados_matricula(cursor, data):
    for index, row in data.iterrows():
        data_matricula_convertida = converter_data(row['data_matricula'])
        cursor.execute("""
            INSERT INTO dados_matricula (registro_geral, nome, situacao_matricula, data_matricula, turno)
            VALUES (%s, %s, %s, %s, %s)
        """, (row['registro_geral'], row['nome'], row['situacao_matricula'], data_matricula_convertida, row['turno']))

# Função para inserir dados na tabela media_alunos
def inserir_media_alunos(cursor, data):
    for index, row in data.iterrows():
        cursor.execute("""
            INSERT INTO media_alunos (registro_geral, disciplina, media_final, turma)
            VALUES (%s, %s, %s, %s)
        """, (row['registro_geral'], row['disciplina'], row['media_final'], row['turma']))

# Conectar ao servidor MySQL
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="escola"
)

cursor = conn.cursor()

# Criar as tabelas
criar_tabelas(cursor)

# Ler arquivos CSV
dados_matricula = pd.read_csv('dados_matricula.csv')
media_alunos = pd.read_csv('media_alunos.csv')

# Remover duplicatas no dados_matricula
dados_matricula = dados_matricula.drop_duplicates(subset=['registro_geral'])

# Inserir dados nas tabelas
inserir_dados_matricula(cursor, dados_matricula)

# Filtrar valores nulos em media_final
media_alunos = media_alunos.dropna(subset=['media_final'])

# Converter valores de media_final para float, substituindo vírgulas por pontos
media_alunos['media_final'] = media_alunos['media_final'].str.replace(',', '.').astype(float)

# Agrupar os dados por registro_geral e calcular a média das notas
media_agrupada = media_alunos.groupby(['registro_geral', 'disciplina', 'turma'])['media_final'].mean().reset_index()

# Inserir dados na tabela media_alunos
inserir_media_alunos(cursor, media_agrupada)

# Confirmar as alterações no banco de dados
conn.commit()

# Fechar a conexão
cursor.close()
conn.close()

print("Tabelas criadas e dados importados com sucesso!")
