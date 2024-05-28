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
            nome VARCHAR(100),
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
            INSERT INTO media_alunos (registro_geral, disciplina, nome, media_final, turma)
            VALUES (%s, %s, %s, %s, %s)
        """, (row['registro_geral'], row['disciplina'], row['nome'], row['media_final'], row['turma']))

# Conectar ao servidor MySQL
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="root",
    database="escola"
)

cursor = conn.cursor()

# Criar as tabelas
criar_tabelas(cursor)

# Ler arquivos CSV
dados_matricula = pd.read_csv('dados_matricula.csv')
media_alunos = pd.read_csv('media_alunos.csv')

# Inserir dados nas tabelas
inserir_dados_matricula(cursor, dados_matricula)
inserir_media_alunos(cursor, media_alunos)

# Confirmar as alterações no banco de dados
conn.commit()

# Fechar a conexão
cursor.close()
conn.close()

print("Tabelas criadas e dados importados com sucesso!")
