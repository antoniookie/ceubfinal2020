import mysql.connector

class SQL:
    def __init__(self, usuario, senha):
        self.cnx = mysql.connector.connect(user=usuario, password=senha, database='ceub', host='localhost')
    def executar(self, comando, parametros):
        cs = self.cnx.cursor()
        cs.execute(comando, parametros)
        self.cnx.commit()
        cs.close()
        return True
    def consultar(self, comando, parametros):
        cs = self.cnx.cursor()
        cs.execute(comando, parametros)
        return cs
    def __del__(self):
        self.cnx.cursor()
