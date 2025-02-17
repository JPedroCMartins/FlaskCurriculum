import sqlite3

class DatabaseSqlite:
    def __init__(self):
        self.db_name = 'dados.db'
        pass

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        pass

    def close(self):
        self.conn.close()
        pass
    
    def create_database(self):
        self.connect()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS curriculo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT,
            telefone TEXT,
            email TEXT,
            objetivo TEXT,
            perfil TEXT
        );
        """)
        self.conn.commit()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS curso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instituicao TEXT,
            curso_nome TEXT,
            ano_conclusao TEXT,
            status TEXT,
            curriculo_id INTEGER,
            FOREIGN KEY (curriculo_id) REFERENCES curriculo(id)
        )
        """)
        self.conn.commit()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiencia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tempo_inicio TEXT,
            tempo_fim TEXT,
            empresa TEXT,
            cargo TEXT,
            curriculo_id INTEGER,
            FOREIGN KEY (curriculo_id) REFERENCES curriculo(id)
        )
        """)
        self.conn.commit()

        self.close()
        pass

    def insert_curriculo(self, nome, endereco, telefone, email, objetivo, perfil):
        self.connect()
        self.cursor.execute("INSERT INTO curriculo (nome, endereco, telefone, email, objetivo, perfil) VALUES (?, ?, ?, ?, ?,?)", (nome, endereco, telefone, email, objetivo, perfil))
        self.conn.commit()
        last_id = self.cursor.lastrowid
        self.close()
        return last_id 

    def insert_curso(self, instituicao, curso_nome, ano_conclusao, status, curriculo_id):
        self.connect()
        self.cursor.execute("INSERT INTO curso (instituicao, curso_nome, ano_conclusao, status, curriculo_id) VALUES (?, ?, ?, ?, ?)", (instituicao, curso_nome, ano_conclusao, status, curriculo_id))
        self.conn.commit()
        self.close()
        pass
    
    def insert_experiencia(self, tempo_inicio, tempo_fim, empresa, cargo, curriculo_id):
        self.connect()
        self.cursor.execute("INSERT INTO experiencia (tempo_inicio, tempo_fim, empresa, cargo, curriculo_id) VALUES (?, ?, ?, ?, ?)", (tempo_inicio, tempo_fim, empresa, cargo, curriculo_id))
        self.conn.commit()
        self.close()
        pass

    def get_curriculos(self):
        self.connect()
        self.cursor.execute("SELECT * FROM curriculo")
        curriculos = self.cursor.fetchall()  
        self.close()
        return curriculos
    def get_curriculo_by_id(self, id):
        self.connect()
        self.cursor.execute("SELECT * FROM curriculo WHERE id = ?", (id,))
        curriculo = self.cursor.fetchone()
        self.close()
        return curriculo
    def get_cursos_by_curriculo_id(self, id):
        self.connect()
        self.cursor.execute("SELECT * FROM curso WHERE curriculo_id = ?", (id,))
        cursos = self.cursor.fetchall()
        self.close()
        return cursos
    def get_experiencias_by_curriculo_id(self, id):
        self.connect()
        self.cursor.execute("SELECT * FROM experiencia WHERE curriculo_id = ?", (id,))
        experiencias = self.cursor.fetchall()
        self.close()
        return experiencias
