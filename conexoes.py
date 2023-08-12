import sqlite3
import mysql.connector



from settings import HOST_DB,BASE_DB,PASS_DB,USER_DB


class Mysql():
    def __init__(self) -> None:
        try:
            self.conn_mysql = mysql.connector.connect(
                host=HOST_DB,
                user=USER_DB,
                password=PASS_DB,
                database=BASE_DB
            )
        except mysql.connector.Error as err:
            print("Erro ao conectar ao MySQL:", err)
            self.conn_mysql = None



import sqlite3

class SQLite3Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def criar_tabelas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS apps (
                id INTEGER PRIMARY KEY,
                id_usuario INTEGER,
                nome TEXT,
                login TEXT,
                senha TEXT,
                extra TEXT,
                observacao TEXT,
                FOREIGN KEY (id_usuario) REFERENCES usuarios (id)
            );                
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                usuario VARCHAR(80) NOT NULL UNIQUE,
                senha_hash VARCHAR(300),
                nome_completo VARCHAR(250) NOT NULL,
                email VARCHAR(250) NOT NULL,
                hash VARCHAR(300) 
            );
        ''')
        self.conn.commit()

    def executar_sql(self, sql, data=None):
        if data:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        else:
            self.cursor.execute(sql)
            self.conn.commit()




    def fechar_conexao(self):
        self.conn.close()

