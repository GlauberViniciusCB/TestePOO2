import mysql.connector
from mysql.connector import Error

def conexaoComBanco():
    try:
        print("Tentando conectar ao banco de dados...")
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="trabalho_de_poo2"
        )
        
        if conexao.is_connected():
            print("Conexão Bem Sucedida!")
        else:
            print("Conexão falhou!")
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None



