import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            port=3307,
            user='root',
            password='root',
            database='matheuseduardodb_sa'
        )
        
        # Verificar e criar tabelas se não existirem
        verificar_tabelas(conn)
        
        print("✅ Conexão estabelecida com sucesso!")
        return conn
    except Error as err:
        print(f"❌ Erro de conexão: {err}")
        return None

def verificar_tabelas(conn):
    tabelas_necessarias = {
        'usuario': """
            CREATE TABLE IF NOT EXISTS usuario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                senha VARCHAR(50) NOT NULL,
                tipo ENUM('administrador', 'comum') NOT NULL DEFAULT 'comum'
            )
        """,
        'funcionario': """
            CREATE TABLE IF NOT EXISTS funcionario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                cargo VARCHAR(50) NOT NULL,
                cpf VARCHAR(11) UNIQUE NOT NULL,
                salario DECIMAL(10,2) NOT NULL
            )
        """,
        # Adicione as outras tabelas conforme o SQL acima
    }
    
    cursor = conn.cursor()
    try:
        for tabela, sql in tabelas_necessarias.items():
            cursor.execute(f"SHOW TABLES LIKE '{tabela}'")
            resultado = cursor.fetchone()
            if not resultado:
                cursor.execute(sql)
                print(f"Tabela {tabela} criada com sucesso!")
        
        # Criar usuário admin padrão se não existir
        cursor.execute("SELECT * FROM usuario WHERE nome = 'admin'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO usuario (nome, senha, tipo) VALUES (%s, %s, %s)",
                ('admin', 'admin123', 'administrador')
            )
            conn.commit()
            print("Usuário admin criado com sucesso!")
            
    except Error as e:
        print(f"Erro ao verificar tabelas: {e}")
    finally:
        cursor.close()