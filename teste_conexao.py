from conexao import conectar

try:
    conexao = conectar()
    print("Conectado ao PostgreSQL!")
    conexao.close()

except Exception as erro:
    print("Erro na conexão:", erro)